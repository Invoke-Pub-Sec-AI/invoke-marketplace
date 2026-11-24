#!/usr/bin/env python3
"""Ask Claude to review a GitHub PR and publish validated inline findings."""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

MODEL = "claude-sonnet-4-6"
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


def ask_claude(context, api_key, model):
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
    result = request_json(
        "https://api.anthropic.com/v1/messages",
        {"x-api-key": api_key, "anthropic-version": "2023-06-01"},
        {
            "model": model,
            "max_tokens": 4096,
            "system": PROMPT.read_text(encoding="utf-8"),
            "messages": [{"role": "user", "content": context}],
            "output_config": {"format": {"type": "json_schema", "schema": schema}},
        },
    )
    if result.get("stop_reason") != "end_turn":
        raise RuntimeError(f"Claude review did not complete ({result.get('stop_reason')})")
    text = "".join(block["text"] for block in result["content"] if block["type"] == "text")
    findings = json.loads(text)["findings"]
    if not isinstance(findings, list):
        raise RuntimeError("Claude returned an invalid findings list")
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


def review_pr(repo, number, expected_head=None):
    token = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN")
    api_key = os.getenv("ANTHROPIC_API_KEY")
    pr_url = f"https://github.com/{repo}/pull/{number}"
    missing = []
    if not api_key:
        missing.append("ANTHROPIC_API_KEY")
    if not token:
        missing.append("GH_TOKEN or GITHUB_TOKEN")
    if missing:
        raise RuntimeError(f"{pr_url}: missing {' and '.join(missing)}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2026-03-10",
    }
    endpoint = f"https://api.github.com/repos/{repo}/pulls/{number}"
    pr = request_json(endpoint, headers)
    if pr["state"] != "open" or pr["draft"]:
        print(f"Skipped closed or draft PR: {pr_url}")
        return
    head = pr["head"]["sha"]
    base = pr["base"]["sha"]
    if expected_head and head != expected_head:
        print(f"Skipped outdated workflow run: {pr_url}")
        return
    marker = f"<!-- invoke-claude-pr-review:{base}:{head} -->"
    if any(marker in (review["body"] or "") for review in github_pages(f"{endpoint}/reviews", headers)):
        print(f"An inline review already exists for this PR revision: {pr_url}")
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
    findings = ask_claude(context, api_key, os.getenv("CLAUDE_REVIEW_MODEL") or MODEL)
    comments = inline_comments(findings, anchors)

    current = request_json(endpoint, headers)
    if (current["state"] != "open" or current["draft"] or
            current["head"]["sha"] != head or current["base"]["sha"] != base):
        raise RuntimeError(f"PR changed during review. Run again on its current revision: {pr_url}")
    if not findings:
        print(f"Claude found no actionable findings in the reviewed patches: {pr_url}")
        return
    if not comments:
        raise RuntimeError(f"Claude returned findings, but none passed inline comment validation: {pr_url}")

    if any(marker in (review["body"] or "") for review in github_pages(f"{endpoint}/reviews", headers)):
        print(f"An inline review already exists for this PR revision: {pr_url}")
        return
    result = request_json(
        f"{endpoint}/reviews", headers,
        {"commit_id": head, "event": "COMMENT", "body": f"Claude PR review\n\n{marker}", "comments": comments},
    )
    print(f"Posted {len(comments)} Claude inline comment(s): {result['html_url']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", help="GitHub repository as OWNER/REPO")
    parser.add_argument("number", type=int, help="Pull request number")
    parser.add_argument("--expected-head", help="Skip if the PR has advanced from this commit")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo) or args.number < 1:
        parser.error("Expected OWNER/REPO and a positive pull request number")
    if any(part in {".", ".."} for part in args.repo.split("/")):
        parser.error("Repository segments must be names")
    try:
        review_pr(args.repo, args.number, args.expected_head)
    except (RuntimeError, KeyError, TypeError, ValueError, TimeoutError) as error:
        print(f"Review failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
