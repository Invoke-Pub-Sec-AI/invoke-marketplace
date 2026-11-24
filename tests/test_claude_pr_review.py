import contextlib
import importlib.util
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "plugins/invoke-skills/skills/claude-pr-review/scripts/review_pr.py"
)
SPEC = importlib.util.spec_from_file_location("review_pr", SCRIPT)
reviewer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(reviewer)


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.pr = {
            "state": "open", "draft": False, "title": "Replace line", "body": "",
            "head": {"sha": "b" * 40}, "base": {"sha": "a" * 40}, "changed_files": 1,
        }
        self.file = {
            "filename": "example.txt",
            "patch": "@@ -9,2 +9,2 @@\n unchanged\n-old\n+new",
            "additions": 1, "deletions": 1, "changes": 2,
        }
        self.published = []
        self.findings = []
        self.updated_head = None

    def request(self, url, headers, payload=None):
        if url == "https://api.anthropic.com/v1/messages":
            self.assertNotIn("Authorization", headers)
            self.assertIn("example.txt", payload["messages"][0]["content"])
            self.assertEqual(payload["output_config"]["format"]["type"], "json_schema")
            return {
                "stop_reason": "end_turn",
                "content": [{"type": "text", "text": json.dumps({"findings": self.findings})}],
            }
        self.assertNotIn("x-api-key", headers)
        if url.endswith("/files?per_page=100&page=1"):
            return [self.file]
        if url.endswith("/reviews?per_page=100&page=1"):
            return []
        if url.endswith("/reviews"):
            self.published.append(payload)
            return {"html_url": "https://github.com/owner/repo/pull/1#pullrequestreview-1"}
        pr = self.pr.copy()
        if self.updated_head and self.pr_seen:
            pr["head"] = {"sha": self.updated_head}
        self.pr_seen = True
        return pr

    def run_review(self):
        self.pr_seen = False
        env = {"GH_TOKEN": "github-test-token", "ANTHROPIC_API_KEY": "anthropic-test-key"}
        with patch.dict("os.environ", env, clear=True), patch.object(reviewer, "request_json", self.request):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                reviewer.review_pr("owner/repo", 1)
            return output.getvalue()

    def test_posts_valid_inline_findings_once_with_pinned_head(self):
        valid = {"path": "example.txt", "line": 10, "side": "LEFT", "body": "Fix the removal."}
        self.findings = [valid, valid.copy(), {**valid, "line": 9}]
        self.assertIn("Posted 1 Claude inline comment", self.run_review())
        [review] = self.published
        self.assertEqual(review["commit_id"], self.pr["head"]["sha"])
        self.assertEqual(review["event"], "COMMENT")
        self.assertEqual(review["comments"], [valid])

    def test_does_not_post_for_clean_review(self):
        self.assertIn("no actionable findings", self.run_review())
        self.assertEqual(self.published, [])

    def test_does_not_post_on_stale_head(self):
        self.updated_head = "c" * 40
        self.findings = [{"path": "example.txt", "line": 10, "side": "RIGHT", "body": "Fix the addition."}]
        with self.assertRaisesRegex(RuntimeError, "PR changed during review"):
            self.run_review()
        self.assertEqual(self.published, [])

    def test_incomplete_patch_is_not_reviewed(self):
        self.file["additions"] = 2
        self.file["changes"] = 3
        self.assertIn("no complete textual patches", self.run_review())
        self.assertEqual(self.published, [])

    def test_parses_multiple_hunks_without_counting_diff_markers(self):
        diff = "@@ -1 +1 @@\n-old\n+new\n\\ No newline at end of file\n@@ -8,0 +9 @@\n+tail"
        self.assertEqual(reviewer.changed_lines(diff), {("LEFT", 1), ("RIGHT", 1), ("RIGHT", 9)})


if __name__ == "__main__":
    unittest.main()
