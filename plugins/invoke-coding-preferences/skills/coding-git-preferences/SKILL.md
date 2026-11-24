---
name: coding-git-preferences
description: Apply Git and GitHub CLI preferences when working on feature branches, commits, pull requests, or repository reviews.
---

# Git and GitHub preferences

- Use `git` to create a feature branch, stage the files or hunks for one change, and inspect the staged diff before committing.
- Keep each commit focused on one outcome. Review the branch against its intended base with `git diff <base>...HEAD` before proposing a small pull request.
- Use `gh` for GitHub pull requests, issues, checks, and releases. Use `gh api` when there is no dedicated subcommand.

Follow the user's repository conventions and requested scope for commits, pushes, and pull requests.
