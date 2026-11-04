# LiquidGlass

A cross-platform engineering project for recreating a rich, physically convincing **Liquid Glass** material and interaction language.

This is not a synonym for ordinary glassmorphism. The target combines background refraction and distortion, depth, edge lighting, specular reflections, subtle spectral dispersion, and fluid shape transitions where the platform permits them.

## Project guides

- [GPT.md](GPT.md) — instructions for AI coding agents working in this repository.
- [ROADMAP.md](ROADMAP.md) — phased delivery plan, dependencies, and completion criteria.
- [Visual specification](docs/visual-specification.md) — platform-neutral material requirements.
- [Interaction and motion](docs/interaction-and-motion.md) — shape transitions and interaction behavior.
- [Reference matrix](docs/reference-matrix.md) — maps reference assets to review criteria.
- [Examples catalog](examples/README.md) — visual reference image catalog.
- [Platform adaptation guide](docs/platform-adaptation/README.md) — capability matrix and verified family-specific approaches.
- [Codex Skill](.agents/skills/liquid-glass/SKILL.md) — platform-neutral coding Skill for implementation and review.
- [Skill installation](.agents/skills/liquid-glass/INSTALL.md) — repository-local and personal installation/update instructions.
- [Liquid Glass Studio](studio/README.md) — ChatGPT-side execution twin, architecture, GitHub binding, and private plugin package.

## Working principle

Study the references, inspect the target project's actual platform and rendering capabilities, then choose the strongest technically sound implementation for that environment. Do not force one framework or rendering engine onto every platform, and do not claim visual parity without a buildable implementation and visual validation.

The reusable, platform-aware Codex Skill is available at `.agents/skills/liquid-glass/`. Liquid Glass Studio is maintained alongside it as the ChatGPT-side execution twin; see `studio/README.md` for its private plugin package and connected-GitHub execution model.
