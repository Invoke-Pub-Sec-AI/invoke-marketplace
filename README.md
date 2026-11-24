# Invoke Marketplace

Local Codex project skills for Agentic Auditor (AA).

| Start with | Use it for |
| --- | --- |
| [AA project](plugins/invoke-skills/skills/aa-project/SKILL.md) | Find the right checkout for PBC evidence, Lab questions, research-worker operations, or an SME review package. The skill also identifies which worker versions support the six specialist AA workflows. |
| [Summarize a pull request](plugins/invoke-skills/skills/summarize-pull-request/SKILL.md) | Explain a PR or a local branch diff, including what changed and what was verified. |
| [Marketplace maintenance](plugins/invoke-skills/skills/invoke-marketplace/SKILL.md) | Add or update a skill or plugin in this catalog. |

## Install from this checkout

Open the repository in the desktop app. Restart the app to discover the marketplace, then choose **Plugins → Invoke Marketplace → Invoke Skills**. Start a new chat and ask, for example, “Use `aa-project` to trace a returned SME review package.”

To use this checkout across projects, register it locally and install the desired package.

```sh
codex plugin marketplace add .
codex plugin add invoke-skills@invoke-marketplace
```

## Add a skill or plugin

To extend **Invoke Skills**, add a folder under `plugins/invoke-skills/skills/`
with a `SKILL.md` whose `name` matches the folder. Bump the plugin version when updating released skills.

For a separate plugin, place the package under `plugins/<name>/` and add an entry to
[the marketplace catalog](.agents/plugins/marketplace.json). Set `source.path`
to the package path relative to the repository root, starting with `./`.
See [OpenAI's plugin packaging guide](https://developers.openai.com/plugins/build/plugins)
for the manifest and marketplace formats.
