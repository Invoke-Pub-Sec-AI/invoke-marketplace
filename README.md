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

## Review a PR with Codex

In Codex, ask `@Invoke Skills` to use `codex-pr-review` on a GitHub PR URL.
The skill uses your signed-in Codex CLI. It can post inline findings through a
connected GitHub tool or directly with `GH_TOKEN` or `GITHUB_TOKEN` that has
pull request write access. Use `--preview` for a review without posting.

The [GitHub Actions hook](.github/workflows/codex-pr-review.yml) runs the same
reviewer on new and updated non-draft PRs from branches in this repository.
Add `OPENAI_API_KEY` to the repository's Actions secrets to enable CI reviews.
For an existing PR, use the skill locally or rerun its review job. Each run
sends the PR title, description, and complete textual patches to Codex. GitHub
receives inline comments only for findings that resolve to changed lines.

The [review prompt](plugins/invoke-skills/skills/codex-pr-review/references/review-prompt.md)
asks Codex to verify a concrete regression and its impact before reporting it.
The runner uses structured output and validates diff anchors before posting.
[Codex review guidance](https://developers.openai.com/blog/custom-code-review-rules-for-codex)
· [Structured reviews with Codex](https://developers.openai.com/cookbook/examples/codex/build_iterative_repair_loops_with_codex)
