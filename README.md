# Invoke Marketplace

A repo-scoped Codex marketplace with separate options for related workflows.

| Codex option | Included skills |
| --- | --- |
| **Git Workflows** (`invoke-git-workflows`) | [Review a PR with Codex](plugins/invoke-git-workflows/skills/codex-pr-review/SKILL.md) and [Summarize a pull request](plugins/invoke-git-workflows/skills/summarize-pull-request/SKILL.md). |
| **Marketplace Maintenance** (`invoke-skills`) | [Invoke Marketplace](plugins/invoke-skills/skills/invoke-marketplace/SKILL.md), for adding and updating packages in this catalog. |

## Install and use the skill groups

Open this repository in the ChatGPT desktop app. Restart the app to discover
the marketplace, then open **Plugins**, select **Invoke Marketplace**, and
install **Git Workflows** or **Marketplace Maintenance** as needed. Start a new
chat in this project and select the group for your task.

To make the marketplace available outside this repository, run this command
from the repository root:

```sh
codex plugin marketplace add .
codex plugin add invoke-git-workflows@invoke-marketplace
# Optional marketplace maintenance
codex plugin add invoke-skills@invoke-marketplace
```

## Pick up new skills

Each plugin discovers workflows from its own `skills/` directory. Related
skills in that directory share the plugin's marketplace entry.

If you installed from a local checkout, pull the latest changes and restart
the ChatGPT desktop app. If the skill still doesn't appear, reinstall
the affected plugin from **Invoke Marketplace** and start a new chat.

If you registered the Git repository as a marketplace source, run
`codex plugin marketplace upgrade invoke-marketplace` to refresh its snapshot.
Reinstall the affected plugin from the refreshed marketplace, then start a new
Codex chat.

Existing **Invoke Skills** installs now appear as **Marketplace Maintenance**,
retaining the `invoke-skills` plugin ID. Refresh that plugin to replace its old
bundled copy, and install **Git Workflows** separately to continue using PR
review and summaries. Refreshing the old plugin alone does not install the new
group.

## Add a skill or plugin

Add a folder under `plugins/<plugin-name>/skills/` in the appropriate group,
with a `SKILL.md` whose `name` matches the folder. Put Git and PR workflows in
`invoke-git-workflows` and marketplace maintenance in `invoke-skills`. Keep
related references with each skill and bump the affected plugin's version.

For a separate plugin, place the package under `plugins/<name>/` and add an entry to
[the marketplace catalog](.agents/plugins/marketplace.json). Set `source.path`
to the package path relative to the repository root, starting with `./`.
See [OpenAI's plugin packaging guide](https://developers.openai.com/plugins/build/plugins)
for the manifest and marketplace formats.

## Review a PR with Codex

In Codex, ask `@Git Workflows` to use `codex-pr-review` on a GitHub PR URL.
The skill uses your signed-in Codex CLI. It can post inline findings through a
connected GitHub tool or directly with `GH_TOKEN` or `GITHUB_TOKEN` that has
pull request write access. For GitHub App installation tokens, pass the
app's bot login with `--reviewer-login`. Use `--preview` for a review without
posting.

The [GitHub Actions hook](.github/workflows/codex-pr-review.yml) runs the same
reviewer on new and updated non-draft PRs targeting the default branch from
branches in this repository. It runs the reviewer from the trusted base
revision. The hook must be on the default branch and the repository must have
an `OPENAI_API_KEY` Actions secret.
For an existing PR, use the skill locally or rerun its review job. Each run
sends the PR title, description, and complete textual patches to Codex. GitHub
receives inline comments only for findings that resolve to changed lines.

The [review prompt](plugins/invoke-git-workflows/skills/codex-pr-review/references/review-prompt.md)
asks Codex to verify a concrete regression and its impact before reporting it.
The runner uses structured output and validates diff anchors before posting.
[Codex review guidance](https://developers.openai.com/blog/custom-code-review-rules-for-codex)
· [Structured reviews with Codex](https://developers.openai.com/cookbook/examples/codex/build_iterative_repair_loops_with_codex)
