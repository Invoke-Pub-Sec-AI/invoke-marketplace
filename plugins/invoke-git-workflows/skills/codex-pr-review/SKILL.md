---
name: codex-pr-review
description: Use Codex to review a new or updated GitHub pull request and post actionable inline findings. Use when the user explicitly asks for a Codex PR review or asks to test this reviewer on a PR.
---

# Codex PR Review

Identify the open GitHub PR from the user's URL or number. If they refer to
the current branch, match the branch to its open PR using GitHub tools or
`gh pr view --json number,url,headRefOid`. Ask for the PR only if the target
remains ambiguous.

Run the packaged `scripts/review_pr.py` relative to this skill directory:

```sh
python3 /path/to/codex-pr-review/scripts/review_pr.py OWNER/REPO PR_NUMBER
```

The runner uses the installed Codex CLI and its saved sign-in. To publish
directly, provide `GH_TOKEN` or `GITHUB_TOKEN` with pull request write access.
For a GitHub App installation token, also pass `--reviewer-login` with the
app's bot login.
If a connected GitHub tool can write reviews but the shell lacks a token, run
with `--preview`. For private PRs, the preview still needs GitHub read access.
When the preview returns findings, verify they are actionable and the PR head
still matches the returned commit. Submit its comments as a single GitHub
`COMMENT` review at that commit. Before posting, check whether the connected
reviewer already posted the returned marker.

If credentials are available only in GitHub Actions, check the **Codex PR
review** run for the PR's current head. Use its result if it completed, wait
if it is running, or rerun it when the user asks to run the review and a
retry is appropriate. Once the hook is on the default branch, it starts on PR
open, new commits, reopening, and transition out of draft.

The runner uses Codex's [review prompt](references/review-prompt.md) and
posts one GitHub review with inline comments when it has actionable
findings. Report the PR and review links, or state that Codex found no
actionable findings when the runner confirms that result. Report failures and
skips explicitly, including missing credentials or unavailable diff coverage.
