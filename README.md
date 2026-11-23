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
