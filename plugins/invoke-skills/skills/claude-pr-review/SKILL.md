---
name: claude-pr-review
description: Use Claude to review a new or updated GitHub pull request and post actionable inline findings. Use when the user explicitly asks for a Claude PR review or asks to test this reviewer on a PR.
---

# Claude PR Review

Identify the open GitHub PR from the user's URL or number. If they refer to
the current branch, match the branch to its open PR using GitHub tools or
`gh pr view --json number,url,headRefOid`. Ask for the PR only if the target
remains ambiguous.

Run the packaged `scripts/review_pr.py` relative to this skill directory:

```sh
python3 /path/to/claude-pr-review/scripts/review_pr.py OWNER/REPO PR_NUMBER
```

The runner uses `ANTHROPIC_API_KEY` and `GH_TOKEN` or `GITHUB_TOKEN` from
the environment. GitHub authentication must allow pull request writes.
If credentials are available only in GitHub Actions, check the **Claude PR
review** run for the PR's current head. Use its result if it completed, wait
if it is running, or rerun it when the user asks to run the review and a
retry is appropriate. This repository's workflow starts on PR open, new
commits, reopening, and transition out of draft.

The runner uses Claude's [review prompt](references/review-prompt.md) and
posts one GitHub review with inline comments when it has actionable
findings. Report the PR and review links, or state that Claude found no
actionable findings when the runner confirms that result. Report failures and
skips explicitly, including missing credentials or unavailable diff coverage.
