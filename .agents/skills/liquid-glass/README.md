# Liquid Glass Skill

A portable Codex Skill for implementing and reviewing Liquid Glass interfaces
across languages, UI frameworks, operating systems, game engines, and
rendering stacks.

- Entry point: [SKILL.md](SKILL.md)
- Installation, update, and safe uninstall: [INSTALL.md](INSTALL.md)
- Package version: [VERSION](VERSION)
- Project inspection helper: [scripts/inspect_project.py](scripts/inspect_project.py)
- Safe installation scripts: [scripts/install.ps1](scripts/install.ps1) and [scripts/uninstall.ps1](scripts/uninstall.ps1)
- Worked workflows: [examples/README.md](examples/README.md)
- Platform guidance is bundled in release ZIPs under references/project-docs/platform-adaptation/.
- Package tests: [tests/](tests/)
- Planning and review templates: [assets/](assets/)

The package is deliberately platform-neutral. It does not bundle a rendering
engine or claim that a blur-only fallback reproduces refraction.
