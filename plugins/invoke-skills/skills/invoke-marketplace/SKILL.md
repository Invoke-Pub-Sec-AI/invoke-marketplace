---
name: invoke-marketplace
description: Add, update, or remove skill packages in the Invoke Marketplace repository. Use when editing its plugin catalog or adding a workflow to a plugin.
---

# Invoke Marketplace

Find the marketplace repository and read `.agents/plugins/marketplace.json`.
It should have the name `invoke-marketplace`. Use the repository root to
resolve each catalog entry's relative source path.

- For a new workflow, use `invoke-git-workflows` for Git and PR tasks or
  `invoke-skills` for marketplace maintenance. Create
  `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`. Give it YAML frontmatter
  with a `name` that matches the directory and a `description` that says when to
  use the workflow. Keep related skills and references in the same package.
  Each package has its own catalog entry and appears as a separate Codex option.
- For a separate plugin, put its package in `plugins/<plugin-name>/`. Use a
  portable root `plugin.json` with the Agent Plugins schema for new packages.
  Add one catalog entry with the manifest's name, a local source path beginning
  with `./plugins/`, a category, and install and authentication policies. Follow
  the [plugin packaging guide](https://developers.openai.com/plugins/build/plugins#marketplace-metadata).
- To unlist a plugin, remove its catalog entry. Check whether the request also
  calls for removing its source files or uninstalling a cached copy.

Parse the edited JSON and skill frontmatter. Check that each affected catalog
entry resolves to its intended plugin and that its skills are discoverable in
Codex when you have access to the host. Report which plugin and skills changed
and whether the installed copy needs a refresh.
