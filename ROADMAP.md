# LiquidGlass — Roadmap

This roadmap sequences the work from a visual reference collection into a reusable cross-platform Skill and a dedicated assistant workflow. A phase is complete only when its acceptance criteria are demonstrably satisfied.

## Product direction

**Primary outcome:** enable an AI coding agent to inspect an arbitrary software project and implement a convincing Liquid Glass material using the best rendering approach available for that project's language, framework, platform, and hardware.

**Secondary outcome:** provide Liquid Glass Studio as a focused assistant workflow for reference analysis, implementation planning, code generation/adaptation, review, and optimization.

**Non-goal:** ship one universal rendering engine or force every target to use the same language, framework, shader system, or visual fallback.

## Phase execution rule

A requested roadmap phase is one complete delivery unit. The agent must finish every in-scope task and deliverable, resolve solvable problems using supported alternatives, update the roadmap only after acceptance checks pass, verify the published repository state, and then send one final report. It must not stop after partial progress or send a premature completion report. Genuine external blockers must be stated precisely; they must never be used to label unfinished work complete.

## Status overview

| Phase | Status | Outcome |
|---|---|---|
| 0. Repository and reference baseline | In progress | Project instructions, roadmap, and organized visual references |
| 1. Visual specification | Complete | Testable, platform-neutral material, interaction, motion, and reference criteria |
| 2. Core coding Skill | Not started | Installable Skill with reliable discovery and implementation workflow |
| 3. Platform adaptation guidance | Not started | Technique selection and adapter guidance for major platform families |
| 4. Liquid Glass Studio workflow | Not started | Dedicated assistant/plugin capabilities and tool contracts |
| 5. Reference implementations | Not started | Small, runnable examples demonstrating distinct material capabilities |
| 6. Validation, accessibility, and performance | Not started | Reproducible visual and runtime quality gates |
| 7. Packaging and release | Not started | Versioned, documented, installable deliverables |

## Phase 0 — Repository and reference baseline

**Goal:** establish reliable project instructions and a traceable reference catalog.

Tasks:
- [x] Create the root project instruction file (GPT.md).
- [x] Create this phased roadmap.
- [x] Organize the available images into a predictable example/reference structure.
- [x] Give visually inspected images descriptive names and document their purpose.
- [ ] Inspect and classify the four retained additional images that could not be previewed during initial cataloging.
- [ ] Add the original motion-video reference or a stable, documented location for it when available to this repository.
- [ ] Confirm licensing/provenance and permitted reuse for every reference asset before redistribution in a public release.

Acceptance:
- Every asset has a stable path and catalog entry.
- No asset is described beyond what has actually been inspected.
- The repository's goals, working rules, and delivery phases are clear.

## Phase 1 — Visual and interaction specification

<badge>Complete</badge>

**Goal:** turn the reference material into a framework-independent specification that can guide implementation and review.

Tasks:
- [x] Define the material model: transmission, refraction, distortion, depth, edge response, specular highlights, and restrained spectral effects.
- [x] Define shape families: pills, rounded controls, circular surfaces, connected/organic forms, and merged liquid surfaces.
- [x] Define interaction states and transitions: idle, hover/focus, press, drag, release, merge, split, and settle.
- [x] Separate essential visual properties from optional embellishments.
- [x] Define a visual vocabulary and a reference-to-criterion matrix so reviewers can identify which image demonstrates each property.
- [x] Specify fallback levels, clearly distinguishing true backdrop refraction from blur/tint-only approximations.

Deliverables:
- [x] [docs/visual-specification.md](docs/visual-specification.md)
- [x] [docs/interaction-and-motion.md](docs/interaction-and-motion.md)
- [x] [docs/reference-matrix.md](docs/reference-matrix.md)
- [x] [docs/README.md](docs/README.md) — specification index

Acceptance:
- [x] Each core visual property has a written description and review criterion.
- [x] The spec can be applied without choosing a programming language or framework.
- [x] The basic-glass fallback is explicitly distinguished from the target material.
- [x] Still-image and motion references are mapped to the behaviors they can legitimately support.
- [x] The specification distinguishes observed evidence from design recommendations and unverified assumptions.

## Phase 2 — Core coding Skill

**Goal:** create a portable, installable Skill that makes coding agents follow the project's discovery, planning, implementation, and validation process.

Tasks:
- Define the Skill metadata and installation layout according to the current official Codex Skill format; verify the format at implementation time.
- Write a concise entry-point instruction file that delegates detailed material, rendering, platform, accessibility, and validation guidance to focused references.
- Add a project-detection workflow that identifies language, framework, runtime, build tooling, graphics APIs, minimum device/OS, and constraints.
- Add a decision process for selecting platform-native, GPU/shader, custom-rendering, canvas/DOM, or layered fallback approaches.
- Define when to inspect existing code, when to add a reusable primitive, and how to avoid unnecessary architecture changes.
- Add implementation checklists, failure modes, and truthful reporting requirements.
- Test activation and usefulness in more than one unrelated language/platform family.

Deliverables:
- A documented Skill package (proposed name: liquid-glass).
- Focused reference documents and minimal examples.
- Installation and update instructions.

Acceptance:
- The Skill activates for Liquid Glass implementation/review tasks without requiring a specific language.
- It inspects the target environment before selecting techniques.
- It gives actionable implementation steps rather than generic design advice.
- It does not force one platform's APIs on another.
- At least two distinct platform families complete a tested end-to-end workflow.

## Phase 3 — Platform adaptation guidance

**Goal:** make the Skill useful across materially different rendering environments without pretending every platform has identical capabilities.

Candidate families to research and cover:
- Web DOM/CSS and browser graphics pipelines.
- Native Android UI and custom drawing/rendering.
- Native iOS/iPadOS UI and graphics pipelines.
- Desktop UI frameworks and native compositors.
- Game engines and real-time 2D/3D rendering.
- Cross-platform UI frameworks and custom GPU/canvas renderers.
- Constrained devices or environments with limited backdrop/shader access.

Tasks:
- Build a capability matrix (backdrop capture, refraction, custom shaders, masks, animation, accessibility hooks, minimum hardware/API).
- Document the preferred approach and fallback for each family only after technical validation.
- Keep examples small and independent; do not build a giant shared abstraction prematurely.
- Record framework/version assumptions and re-check them when updating guidance.

Acceptance:
- Each covered family has a verified approach, explicit capability limits, and a runnable or otherwise reproducibly validated example.
- Language/framework choices remain discoverable and extensible.

## Phase 4 — Liquid Glass Studio assistant/plugin workflow

**Goal:** create a focused assistant product that helps users move from a visual reference to an integrated, reviewed implementation.

Planned capabilities:
1. **Reference inspection:** analyze supplied screenshots or video frames and extract material, geometry, lighting, motion, and interaction characteristics.
2. **Visual specification:** turn observations into a structured, editable implementation brief with explicit confidence and unknowns.
3. **Project diagnosis:** identify platform, framework, rendering facilities, and constraints from supplied project context.
4. **Strategy selection:** compare viable implementation paths and explain trade-offs.
5. **Code generation/adaptation:** produce platform-appropriate code that fits the host project rather than an isolated generic snippet.
6. **Implementation review:** compare code and captures against the specification, identify missing optical/interaction features, and recommend fixes.
7. **Performance/accessibility review:** identify expensive rendering patterns, quality-tier options, and accessibility gaps.

Tasks:
- Verify the current supported private-plugin creation and packaging workflow before choosing architecture.
- Define tool names, inputs, outputs, validation, error handling, and boundaries before implementation.
- Make reference analysis return evidence-based observations, not unsupported claims.
- Keep code-writing operations explicit and scoped to user-provided projects.
- Avoid duplicating capabilities already better handled by the Skill or the host coding agent.

Acceptance:
- Plugin installation/availability is verified in the intended environment.
- Each implemented tool has a clear contract and meaningful tested behavior.
- The workflow can guide a user from reference to a platform-aware implementation review.
- The plugin does not claim to render or change the ChatGPT application interface itself.

## Phase 5 — Reference implementations

**Goal:** prove that the specification and Skill can produce working interfaces, not just documents.

Tasks:
- Choose representative platform families based on available environments and test devices.
- Build a minimal demo for each selected family, with a real background visible through the material.
- Demonstrate at least: a static refractive surface, an interactive control, and one organic/liquid transition where the platform permits it.
- Keep each demo runnable, documented, and independent from unrelated sample projects.
- Capture reference-aligned screenshots or video and record deviations.

Acceptance:
- Every demo builds/runs using documented steps in its target environment.
- Each demo clearly states whether it demonstrates full refraction, a partial approximation, or fallback rendering.
- The examples exercise different capabilities instead of repeating the same blur card.

## Phase 6 — Validation, accessibility, and performance

**Goal:** establish repeatable quality gates for both generated code and maintained examples.

Tasks:
- Create a visual review checklist and side-by-side capture procedure.
- Add automated checks where meaningful (formatting, static analysis, builds, unit/integration tests).
- Review multiple backgrounds, densities/viewports, orientations, and component states.
- Review text contrast, keyboard/focus behavior, touch targets, semantics, reduced motion, and transparency/high-contrast settings.
- Measure frame pacing, GPU/CPU cost, memory, overdraw, thermal/battery impact, and behavior with multiple surfaces.
- Define fallback and quality tiers for hardware or APIs that cannot support the full effect.

Acceptance:
- Test procedures are reproducible and results are recorded.
- Known gaps and hardware/platform limitations are explicit.
- No release claims visual parity without comparative evidence.

## Phase 7 — Packaging and release

**Goal:** publish maintainable, versioned deliverables.

Tasks:
- Finalize the Skill package layout and install/update/uninstall documentation.
- Finalize plugin packaging and user-facing setup instructions.
- Add versioning, changelog, license/provenance notes, and contribution guidance.
- Verify public links and installation instructions from a clean environment.
- Tag a release only after all required acceptance criteria pass.

Acceptance:
- The Skill can be installed from a clean supported environment.
- The plugin can be installed or enabled using the verified supported workflow.
- Documentation matches the shipped files and verified behavior.
- Release notes identify supported platform families and known limitations.

## Global definition of done

A deliverable is complete only when it is integrated with its target environment, validated to the extent claimed, documented, accessible, and honest about visual fidelity and platform limitations. A successful text response or code snippet alone does not satisfy this roadmap.
