---
name: git-workflow
description: Use when choosing a Git feature branch, splitting work into small commits or pull requests, or reviewing what a branch would submit.
---

# Feature branches, commits, and pull requests

## Start from the intended base

Read the repository's contribution guidance and inspect `git status --short --branch`. Use the requested base or the repository's integration branch. If an existing task branch already targets that base, continue there. Otherwise create a short, descriptive feature branch with `git switch -c <feature> <base>`. Use the repository or user's branch naming convention.

Inspect existing changes with `git diff` and `git diff --cached`. If unrelated changes are already staged or the working edits would overlap, use `git worktree add -b <feature> <new-directory> <base>` to start in a separate checkout. The new worktree has its own index, so committing there preserves the user's staged changes and working files.

## Choose a reviewable unit

Aim for one behavior change per PR. Keep its implementation, regression test, and any documentation needed to use it together. A small PR is one a reviewer can understand, verify, and merge independently. Split an unrelated cleanup onto its own branch. If a change must build on an unmerged prerequisite, branch from that prerequisite, target it as the PR base, and identify the dependency in the description.

Within the branch, make each commit one coherent step. For example, a behavior-preserving refactor and a feature that uses it can be two commits in one PR. Keep a fix and its regression test together when they explain each other. Avoid slicing a change by file count or leaving intermediate commits broken.

## Stage, verify, and review

- Stage the intended files or use `git add -p` for mixed changes. Inspect `git diff --cached` and `git diff --cached --check` before committing. Leave unrelated staged work for its owner.
- Run the checks that exercise the changed behavior. When committing is in scope, use a message that states the outcome. Confirm the result with `git show --stat HEAD` and `git status --short`.
- Before proposing a PR, inspect `git log --oneline <base>..HEAD` and `git diff <base>...HEAD`. The three-dot diff compares the branch with its merge base. Check staged, unstaged, and untracked work separately because the branch diff only shows commits.
- Describe the purpose, observable change, checks actually run, and any prerequisite PR. For local-only work, prepare the description from local refs. When asked to publish, use `git` for the push and `gh pr create --base <base> --head <feature> --body-file <file>` for the PR.
