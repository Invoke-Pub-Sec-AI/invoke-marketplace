#!/usr/bin/env python3
"""Ask Codex to review a GitHub PR and publish validated inline findings."""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MAX_FINDINGS = 5
MAX_INPUT_BYTES = 300_000
PROMPT = Path(__file__).resolve().parents[1] / "references" / "review-prompt.md"
HUNK = re.compile(r"^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@")
FINDING_FIELDS = {
    "path": {"type": "string"},
    "line": {"type": "integer"},
    "side": {"type": "string", "enum": ["LEFT", "RIGHT"]},
    "body": {"type": "string"},
}


def request_json(url, headers, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, headers={"Content-Type": "application/json", **headers})
    try:
        with urlopen(request, timeout=120) as response:
            return json.load(response)
    except HTTPError as error:
        request_id = error.headers.get("request-id") or error.headers.get("x-github-request-id")
        raise RuntimeError(f"{request.host} returned HTTP {error.code} (request ID {request_id or 'unavailable'})") from None
    except URLError as error:
        raise RuntimeError(f"Could not reach {request.host}: {error.reason}") from None


def github_pages(url, headers):
    page = 1
    while True:
        items = request_json(f"{url}?per_page=100&page={page}", headers)
        yield from items
        if len(items) < 100:
            return
        page += 1


def has_review(endpoint, headers, marker, login):
    return any(
        (review.get("user") or {}).get("login", "").casefold() == login.casefold()
        and marker in (review.get("body") or "")
        for review in github_pages(f"{endpoint}/reviews", headers)
    )


def changed_lines(patch):
    anchors = set()
    old_line = new_line = None
    for line in patch.split("\n"):
        match = HUNK.match(line)
        if match:
            old_line, new_line = map(int, match.groups())
        elif old_line is not None:
            if line.startswith("+"):
                anchors.add(("RIGHT", new_line))
                new_line += 1
            elif line.startswith("-"):
                anchors.add(("LEFT", old_line))
                old_line += 1
            elif line.startswith(" "):
                old_line += 1
                new_line += 1
    return anchors


def diff_context(files):
    patches = []
    anchors = {}
    omitted = []
    for file in files:
        path = file["filename"]
        patch = file.get("patch")
        changed = changed_lines(patch) if patch else set()
        if not changed or len(changed) != file["additions"] + file["deletions"]:
            if file["changes"]:
                omitted.append(path)
            continue
        anchors[path] = changed
        patches.append({"path": path, "patch": patch})
    return patches, anchors, omitted


def ask_codex(context):
    schema = {
        "type": "object",
        "properties": {
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": FINDING_FIELDS,
                    "required": list(FINDING_FIELDS),
                    "additionalProperties": False,
                },
            }
        },
        "required": ["findings"],
        "additionalProperties": False,
    }
    with tempfile.TemporaryDirectory(prefix="codex-pr-review-") as workspace:
        schema_file = Path(workspace) / "schema.json"
        schema_file.write_text(json.dumps(schema), encoding="utf-8")
        output_file = Path(workspace) / "findings.json"
        prompt = f"{PROMPT.read_text(encoding='utf-8')}\n\nPull request evidence (JSON):\n{context}"
        env = {key: value for key, value in os.environ.items() if key not in {
            "GH_TOKEN", "GITHUB_TOKEN", "GH_ENTERPRISE_TOKEN", "GITHUB_ENTERPRISE_TOKEN",
        }}
        try:
            result = subprocess.run(
                [
                    "codex", "exec", "--ephemeral", "--ignore-user-config",
                    "--skip-git-repo-check", "--sandbox", "read-only",
                    "--disable", "shell_tool", "--disable", "hooks",
                    "-c", 'web_search="disabled"', "--color", "never",
                    "--output-schema", str(schema_file),
                    "--output-last-message", str(output_file), "-",
                ],
                input=prompt, text=True, cwd=workspace, env=env,
                capture_output=True, timeout=300, check=False,
            )
        except FileNotFoundError:
            raise RuntimeError("Install and authenticate the Codex CLI to review this PR") from None
        except subprocess.TimeoutExpired:
            raise RuntimeError("Codex exceeded the five-minute review timeout") from None
        if result.returncode != 0 or not output_file.is_file():
            raise RuntimeError(f"Codex did not complete the review (exit {result.returncode}); check Codex CLI authentication and availability")
        findings = json.loads(output_file.read_text(encoding="utf-8"))["findings"]
    if not isinstance(findings, list):
        raise RuntimeError("Codex returned an invalid findings list")
    return findings


def inline_comments(findings, anchors):
    comments = []
    seen = set()
    for finding in findings:
        path, side, line, body = (finding[key] for key in ("path", "side", "line", "body"))
        anchor = (path, side, line)
        body = body.strip()
        if type(line) is not int or (side, line) not in anchors.get(path, ()) or not 0 < len(body) <= 1200:
            continue
        if anchor in seen:
            continue
        seen.add(anchor)
        # Model output is untrusted. Prevent user and team mentions.
        body = re.sub(r"@(?=[A-Za-z0-9])", "@\u200b", body)
        comments.append({"path": path, "side": side, "line": line, "body": body})
        if len(comments) == MAX_FINDINGS:
            break
    return comments


def review_pr(repo, number, *, expected_head=None, expected_base_ref=None, preview=False, reviewer_login=None):
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    pr_url = f"https://github.com/{repo}/pull/{number}"
    if not token and not preview:
        raise RuntimeError(f"{pr_url}: set GH_TOKEN or GITHUB_TOKEN, or use --preview")

    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    endpoint = f"https://api.github.com/repos/{repo}/pulls/{number}"
    pr = request_json(endpoint, headers)
    if pr["state"] != "open" or pr["draft"]:
        print(f"Skipped closed or draft PR: {pr_url}")
        return
    head = pr["head"]["sha"]
    base = pr["base"]["sha"]
    base_ref = pr["base"]["ref"]
    if ((expected_head and head != expected_head) or
            (expected_base_ref and base_ref != expected_base_ref)):
        print(f"Skipped outdated workflow run: {pr_url}")
        return
    marker = f"<!-- invoke-codex-pr-review:{base}:{head} -->"
    if not preview:
        if not reviewer_login:
            try:
                reviewer_login = request_json("https://api.github.com/user", headers)["login"]
            except (RuntimeError, KeyError) as error:
                raise RuntimeError(f"Could not identify the GitHub reviewer. For an installation token, pass --reviewer-login: {error}") from None
        if has_review(endpoint, headers, marker, reviewer_login):
            print(f"An inline review by {reviewer_login} already exists for this PR revision: {pr_url}")
            return

    files = list(github_pages(f"{endpoint}/files", headers))
    if len(files) != pr["changed_files"]:
        raise RuntimeError(f"GitHub returned an incomplete changed-file list: {pr_url}")
    patches, anchors, omitted = diff_context(files)
    if omitted:
        print(f"Omitted {len(omitted)} file(s) with missing or incomplete patches.")
    if not patches:
        print(f"Skipped PR with no complete textual patches: {pr_url}")
        return
    context = json.dumps({"title": pr["title"], "description": pr["body"], "patches": patches})
    if len(context.encode("utf-8")) > MAX_INPUT_BYTES:
        raise RuntimeError(f"PR exceeds the {MAX_INPUT_BYTES:,}-byte review input limit: {pr_url}")
    findings = ask_codex(context)
    comments = inline_comments(findings, anchors)

    if comments and not preview and has_review(endpoint, headers, marker, reviewer_login):
        print(f"An inline review by {reviewer_login} already exists for this PR revision: {pr_url}")
        return
    current = request_json(endpoint, headers)
    if (current["state"] != "open" or current["draft"] or
            current["head"]["sha"] != head or current["base"]["sha"] != base or
            current["base"]["ref"] != base_ref):
        raise RuntimeError(f"PR changed during review. Run again on its current revision: {pr_url}")
    if not findings:
        print(f"Codex found no actionable findings in the reviewed patches: {pr_url}")
        return
    if not comments:
        raise RuntimeError(f"Codex returned findings, but none passed inline comment validation: {pr_url}")

    review = {"commit_id": head, "event": "COMMENT", "body": f"Codex PR review\n\n{marker}", "comments": comments}
    if preview:
        print(json.dumps(review))
        return
    result = request_json(f"{endpoint}/reviews", headers, review)
    print(f"Posted {len(comments)} Codex inline comment(s): {result['html_url']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", help="GitHub repository as OWNER/REPO")
    parser.add_argument("number", type=int, help="Pull request number")
    parser.add_argument("--expected-head", help="Skip if the PR has advanced from this commit")
    parser.add_argument("--expected-base-ref", help="Skip if the PR no longer targets this branch")
    parser.add_argument("--preview", action="store_true", help="Print validated findings without posting them")
    parser.add_argument("--reviewer-login", help="Posting identity for a GitHub App installation token")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo) or args.number < 1:
        parser.error("Expected OWNER/REPO and a positive pull request number")
    if any(part in {".", ".."} for part in args.repo.split("/")):
        parser.error("Repository segments must be names")
    try:
        review_pr(
            args.repo, args.number, expected_head=args.expected_head,
            expected_base_ref=args.expected_base_ref, preview=args.preview,
            reviewer_login=args.reviewer_login,
        )
    except (RuntimeError, KeyError, TypeError, ValueError, TimeoutError) as error:
        print(f"Review failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
