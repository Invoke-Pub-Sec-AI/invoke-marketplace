# Invoke Marketplace

A repo-scoped Codex marketplace for our own skills. **Invoke Skills** includes
[the Invoke Marketplace skill](plugins/invoke-skills/skills/invoke-marketplace/SKILL.md),
a skill for adding and updating packages in this catalog.

## Install and use Invoke Skills

Open this repository in the ChatGPT desktop app. Restart the app to discover
the marketplace, then open **Plugins**, select **Invoke Marketplace**, and
install **Invoke Skills**. Start a new chat in this project, select
`@Invoke Skills`, and ask it to use `invoke-marketplace`.

To make the marketplace available outside this repository, run this command
from the repository root:

```sh
codex plugin marketplace add .
```

## Add a skill or plugin

To extend **Invoke Skills**, add a folder under `plugins/invoke-skills/skills/`
with a `SKILL.md` whose `name` matches the folder.

For a separate plugin, place the package under `plugins/<name>/` and add an entry to
[the marketplace catalog](.agents/plugins/marketplace.json). Set `source.path`
to the package path relative to the repository root, starting with `./`.
See [OpenAI's plugin packaging guide](https://developers.openai.com/plugins/build/plugins)
for the manifest and marketplace formats.

## Review a PR with Claude

In Codex, ask `@Invoke Skills` to use `claude-pr-review` on a GitHub PR URL.
The local skill needs `ANTHROPIC_API_KEY` and an authenticated `GH_TOKEN`
or `GITHUB_TOKEN` with pull request write access.

The [GitHub Actions hook](.github/workflows/claude-pr-review.yml) runs the same
reviewer on new and updated non-draft PRs from branches in this repository.
Add `ANTHROPIC_API_KEY` to the repository's Actions secrets to enable Claude.
For existing PRs, use the skill locally or rerun the review job in GitHub
Actions. Each run sends the PR title, description, and complete textual
patches to Anthropic. GitHub receives inline comments only for findings that
resolve to changed lines. The workflow log reports skipped patches and
whether the reviewer found anything.

The [review prompt](plugins/invoke-skills/skills/claude-pr-review/references/review-prompt.md)
adapts Anthropic's guidance on checking evidence, filtering false positives,
and anchoring actionable feedback to the diff. The runner uses Claude's
structured output to validate those anchors before posting.
[Anthropic's code-review workflow](https://github.com/anthropics/claude-plugins-official/blob/main/plugins/code-review/commands/code-review.md)
· [Claude prompting guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview)
· [Claude structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
