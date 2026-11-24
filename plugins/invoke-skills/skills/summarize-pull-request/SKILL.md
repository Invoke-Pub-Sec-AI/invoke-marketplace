---
name: summarize-pull-request
description: Summarize a pull request when given its URL, number, or diff, or when asked for a PR recap from a local branch.
---

# Summarize a Pull Request

Identify the PR or branch the user means. For a GitHub PR, use `gh pr view`
for its description and base, and `gh pr diff` for the changes. Use supplied
PR materials or local Git refs for a local-only review. Check linked context
when it explains why the change exists.
For a local branch, determine the intended base and compare it to the branch
head from their merge base, for example with `git diff <base>...HEAD`.
If the target or base is still ambiguous after checking available context,
ask which one to summarize.

Open with the purpose and the most important behavior change. Group related
changes by what they do, with file or symbol names where those help readers
locate the implementation. Call out confirmed effects on users, APIs, data,
configuration, or deployment when relevant.

Summarize tests added or updated and any test or CI results you can verify.
Attribute validation claims from the PR description to the author. If the
diff or results are unavailable, say what evidence the summary relies on.

Keep the summary proportional to the change and adapt it to the user's
audience and format. When details warrant headings, use **Overview**,
**Key changes**, and **Validation**. Return the summary in the chat.
