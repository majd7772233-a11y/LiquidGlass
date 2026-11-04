# Installing and Updating the Liquid Glass Skill

The Skill package lives at [`.agents/skills/liquid-glass/`](../.agents/skills/liquid-glass/SKILL.md). It follows the current Codex/Agent Skills folder format: one `SKILL.md` with `name` and `description`, optional focused references/assets/scripts, and optional `agents/openai.yaml` metadata.

## Install into a project

1. Clone or open this repository as part of the project workspace.
2. Keep `.agents/skills/liquid-glass/` in the repository.
3. Launch Codex from the repository root (or a descendant directory). Codex discovers repository skills from `.agents/skills`.
4. Select `$liquid-glass` explicitly, or describe a task that matches the Skill description to allow implicit discovery.

This is the preferred team setup because the Skill is versioned with the project and shared through Git.

## Install for your user account

In Codex CLI or the Codex IDE extension, use the built-in installer with this repository directory:

~~~text
$skill-installer install https://github.com/majd7772233-a11y/LiquidGlass/tree/main/.agents/skills/liquid-glass
~~~

The personal skills directory is `~/.agents/skills/liquid-glass`. On Windows, this normally resolves beneath `%USERPROFILE%\.agents\skills\liquid-glass`.

A manual copy also works: copy the complete `liquid-glass` folder—not only `SKILL.md`—into the personal skills directory. Preserve the internal `references`, `assets`, and `agents` folders.

## Update

- For a repository installation, pull the latest changes to this repository.
- For a personal installation, back up local edits, then replace the contents of only the `liquid-glass` folder with the latest folder from this repository.
- Do not delete or overwrite neighboring skills.
- If Codex does not show the new or updated Skill, restart Codex and check that the folder contains exactly one `SKILL.md` with valid `name` and `description` front matter.

## Validate the package

From the repository root, run:

~~~bash
python tests/skill-validation/validate_skill.py
~~~

The validator uses only the Python standard library. It checks Skill metadata, support files, local links, and the Web and native Android workflow fixtures. It validates package structure and scenario coverage; it does not substitute for building or visually testing a target application.

## Current scope

This is a standalone coding Skill. It does not install or create the Liquid Glass Studio plugin, and it does not add a rendering engine to Codex or ChatGPT. Plugin packaging is a separate roadmap phase.
