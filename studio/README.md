# Liquid Glass Studio

Liquid Glass Studio is the ChatGPT-side execution twin of the `$liquid-glass` Codex Skill.

It is designed for requests such as: “@Liquid Glass Studio, inspect this repository and implement a real Liquid Glass interface.” Studio must perform the repository work through the connected GitHub app; a written strategy is not a substitute for an authorized implementation.

## Product boundary

- **Shared core:** the same material specification, L0–L3 fidelity tiers, platform discovery, Android compatibility policy, rendering strategy, motion, accessibility, performance, and validation rules used by the Codex Skill.
- **Studio execution adapter:** the connected GitHub app reads the user's project, applies changes, commits them, and reads the resulting workflow checks.
- **Codex execution adapter:** the local Skill can inspect and edit files in the user's local workspace and run local build tools.
- **Different access, same engineering standard:** the adapters differ; neither twin may lower the visual target or invent capabilities.

Studio is a private, app-backed Agent Plugin containing a portable Skill and a verified binding to the existing GitHub connector. It does not ship a second GitHub server, fake an MCP endpoint, or modify ChatGPT's own interface.

## Package source

- [Architecture](architecture.md)
- [Studio workflow contracts](tool-contracts.md)
- [Plugin manifest](package-source/plugin.json)
- [GitHub app binding](package-source/.app.json)
- [Studio Skill source](package-source/skills/liquid-glass-studio/SKILL.md)
- [Package builder](scripts/build_plugin_package.py)
- [Package tests](tests/test_studio_package.py)

The builder copies canonical Skill references and platform documentation into the plugin archive. Rebuild it after changing shared knowledge so the two twins do not drift.

## Build the private plugin archive

Run from the repository root:

```bash
python studio/scripts/build_plugin_package.py --output /tmp/liquid-glass-studio.zip
```

The archive is a single plugin at its root, including the hidden `.app.json` binding. It is for private account creation, not public-directory submission. Public upload rules differ and exclude app bindings.

## Runtime setup

The plugin requires the user's existing GitHub connector to be available and authorized for the target repository. Its permissions remain governed by ChatGPT's GitHub connection and permission settings. Studio must not assume access to local files, private repositories not granted to GitHub, Actions logs without permission, or a local emulator/device.

The package uses a Skill plus a connected app. Its named Studio operations are workflow contracts executed by the agent using GitHub's supported actions; they are not advertised as a custom remote MCP server. A hosted Site/MCP endpoint is intentionally not fabricated.
