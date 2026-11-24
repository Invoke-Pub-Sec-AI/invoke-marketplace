import contextlib
import importlib.util
import io
import json
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plugins/invoke-skills/skills/codex-pr-review/scripts/review_pr.py"
)
SPEC = importlib.util.spec_from_file_location("review_pr", SCRIPT)
reviewer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reviewer)


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.pr = {
            "state": "open", "draft": False, "title": "Replace line", "body": "",
            "head": {"sha": "b" * 40}, "base": {"sha": "a" * 40, "ref": "main"},
            "changed_files": 1,
        }
        self.file = {
            "filename": "example.txt",
            "patch": "@@ -9,2 +9,2 @@\n unchanged\n-old\n+new",
            "additions": 1, "deletions": 1, "changes": 2,
        }
        self.files = [self.file]
        lock_dir = tempfile.TemporaryDirectory()
        self.addCleanup(lock_dir.cleanup)
        tempdir_patch = patch.object(reviewer.tempfile, "gettempdir", return_value=lock_dir.name)
        tempdir_patch.start()
        self.addCleanup(tempdir_patch.stop)
        self.published = []
        self.findings = []
        self.updated_head = None
        self.existing_reviews = []
        self.retarget_on_final_review_lookup = False
        self.review_lookups = 0

    def request(self, url, headers, payload=None):
        if url == "https://api.github.com/user":
            return {"login": "reviewer"}
        if url.endswith("/files?per_page=100&page=1"):
            return self.files
        if url.endswith("/reviews?per_page=100&page=1"):
            self.review_lookups += 1
            if self.review_lookups > 1 and self.retarget_on_final_review_lookup:
                self.pr["base"]["ref"] = "other"
            return self.existing_reviews
        if url.endswith("/reviews"):
            self.published.append(payload)
            return {"html_url": "https://github.com/owner/repo/pull/1#pullrequestreview-1"}
        pr = self.pr.copy()
        if self.updated_head and self.pr_seen:
            pr["head"] = {"sha": self.updated_head}
        self.pr_seen = True
        return pr

    def run_review(self, preview=False, **options):
        self.pr_seen = False
        self.review_lookups = 0
        env = {} if preview else {"GH_TOKEN": "github-test-token"}
        with (
            patch.dict("os.environ", env, clear=True),
            patch.object(reviewer, "request_json", self.request),
            patch.object(reviewer, "ask_codex", return_value=self.findings),
            contextlib.redirect_stdout(io.StringIO()) as output,
        ):
            reviewer.review_pr("owner/repo", 1, preview=preview, **options)
            return output.getvalue()

    def test_preview_maps_inline_findings_without_auth_or_posting(self):
        self.findings = [{"path": "example.txt", "line": 10, "side": "RIGHT", "body": "Fix the addition."}]
        review = json.loads(self.run_review(preview=True))
        self.assertEqual(review["commit_id"], self.pr["head"]["sha"])
        self.assertEqual(review["comments"], self.findings)
        self.assertEqual(self.published, [])

    def test_preview_reports_a_pure_rename_without_polluting_json(self):
        self.findings = [{"path": "example.txt", "line": 10, "side": "RIGHT", "body": "Fix the addition."}]
        self.pr["changed_files"] = 2
        self.files.append({
            "filename": "renamed.py", "previous_filename": "original.py", "status": "renamed",
            "additions": 0, "deletions": 0, "changes": 0,
        })
        with contextlib.redirect_stderr(io.StringIO()) as warnings:
            preview = json.loads(self.run_review(preview=True))
        self.assertEqual(preview["comments"], self.findings)
        self.assertIn("renamed.py", warnings.getvalue())

    def test_posts_valid_inline_findings_once_with_pinned_head(self):
        valid = {"path": "example.txt", "line": 10, "side": "LEFT", "body": "Fix the removal."}
        self.findings = [valid, valid.copy(), {**valid, "line": 9}]
        self.assertIn("Posted 1 Codex inline comment", self.run_review())
        [review] = self.published
        self.assertEqual(review["commit_id"], self.pr["head"]["sha"])
        self.assertEqual(review["event"], "COMMENT")
        self.assertEqual(review["comments"], [valid])

    def test_duplicate_marker_counts_only_for_the_authenticated_reviewer(self):
        marker = f'<!-- invoke-codex-pr-review:{self.pr["base"]["sha"]}:{self.pr["head"]["sha"]} -->'
        self.findings = [{"path": "example.txt", "line": 10, "side": "RIGHT", "body": "Fix the addition."}]
        self.existing_reviews = [{"user": {"login": "different-user"}, "body": marker}]
        self.assertIn("Posted 1 Codex inline comment", self.run_review())
        self.existing_reviews.append({"user": {"login": "REVIEWER"}, "body": marker})
        self.assertIn("An inline review by reviewer already exists", self.run_review())
        self.assertEqual(len(self.published), 1)

    def test_does_not_post_for_clean_review(self):
        self.assertIn("no actionable findings", self.run_review())
        self.assertEqual(self.published, [])

    def test_does_not_post_on_stale_head(self):
        self.updated_head = "c" * 40
        self.findings = [{"path": "example.txt", "line": 10, "side": "RIGHT", "body": "Fix the addition."}]
        with self.assertRaisesRegex(RuntimeError, "PR changed during review"):
            self.run_review()
        self.assertEqual(self.published, [])

    def test_outdated_event_skips_a_retargeted_pr(self):
        self.pr["base"]["ref"] = "other"
        self.assertIn("Skipped outdated workflow run", self.run_review(expected_base_ref="main"))
        self.assertEqual(self.review_lookups, 0)

    def test_retarget_after_duplicate_lookup_prevents_posting(self):
        self.retarget_on_final_review_lookup = True
        self.findings = [{"path": "example.txt", "line": 10, "side": "RIGHT", "body": "Fix the addition."}]
        with self.assertRaisesRegex(RuntimeError, "PR changed during review"):
            self.run_review(expected_base_ref="main")
        self.assertEqual(self.published, [])

    def test_incomplete_patch_is_not_reviewed(self):
        self.file["additions"] = 2
        self.file["changes"] = 3
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertIn("no complete textual patches", self.run_review())
        self.assertEqual(self.published, [])

    def test_publish_lock_serializes_same_repo_pr_and_reviewer(self):
        started = threading.Event()
        acquired = threading.Event()

        def wait_for_lock():
            started.set()
            with reviewer.publish_lock("owner/Repo", 1, "REVIEWER"):
                acquired.set()

        with ThreadPoolExecutor(max_workers=1) as executor:
            with reviewer.publish_lock("Owner/repo", 1, "reviewer"):
                future = executor.submit(wait_for_lock)
                self.assertTrue(started.wait(2))
                self.assertFalse(acquired.wait(0.1))
            future.result(timeout=2)
        self.assertTrue(acquired.is_set())

    def test_parses_multiple_hunks_without_counting_diff_markers(self):
        diff = "@@ -1 +1 @@\n-old\n+new\n\\ No newline at end of file\n@@ -8,0 +9 @@\n+tail"
        self.assertEqual(reviewer.changed_lines(diff), {("LEFT", 1), ("RIGHT", 1), ("RIGHT", 9)})


if __name__ == "__main__":
    unittest.main()
