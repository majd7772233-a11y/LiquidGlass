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
| 2. Core coding Skill | Complete | Portable Codex Skill with project inspection, renderer selection, install guide, web and Android workflows, and package tests |
| 3. Platform adaptation guidance | Complete | Backdrop/capability matrix, seven platform-family guides, nine worked workflow fixtures, and CI validation |
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

<badge>Complete</badge>

**Goal:** create a portable, installable Skill that makes coding agents follow the project's discovery, planning, implementation, and validation process.

Tasks:
- [x] Define Skill metadata and repository/personal installation layout using the current Codex Skill format.
- [x] Write a concise entry-point instruction file that delegates detailed material, rendering, platform, accessibility, and validation guidance to focused references.
- [x] Add a project-detection workflow for languages, frameworks, runtimes, build tools, graphics signals, minimum Android SDK evidence, and project constraints.
- [x] Add a decision process for native material/compositor, GPU/shader, custom rendering, canvas/DOM, hybrid, and layered fallback approaches.
- [x] Define repository inspection, minimal integration, semantics, architecture preservation, failure modes, and truthful reporting rules.
- [x] Add worked web DOM and native Android Java/XML workflows with explicitly different fallback tiers.
- [x] Add package tests for Skill metadata, local reference links, web discovery, Android Java/XML discovery, minimum SDK extraction, XML parsing, and fidelity-tier honesty.

Deliverables:
- [x] [.agents/skills/liquid-glass/SKILL.md](.agents/skills/liquid-glass/SKILL.md) — portable Skill entry point.
- [x] [.agents/skills/liquid-glass/references/](.agents/skills/liquid-glass/references/) — five focused technical references.
- [x] [.agents/skills/liquid-glass/examples/](.agents/skills/liquid-glass/examples/) — web DOM and Android Java/XML worked workflows.
- [x] [.agents/skills/liquid-glass/scripts/inspect_project.py](.agents/skills/liquid-glass/scripts/inspect_project.py) — read-only project inventory helper.
- [x] [.agents/skills/liquid-glass/tests/test_skill_package.py](.agents/skills/liquid-glass/tests/test_skill_package.py) — automated package and workflow-fixture tests.
- [x] [.agents/skills/liquid-glass/INSTALL.md](.agents/skills/liquid-glass/INSTALL.md) and [README.md](.agents/skills/liquid-glass/README.md) — installation, update, and package overview.
- [x] [.agents/skills/liquid-glass/agents/openai.yaml](.agents/skills/liquid-glass/agents/openai.yaml) — optional user-facing metadata.
- [x] [.agents/skills/liquid-glass/references/implementation-workflow.md](.agents/skills/liquid-glass/references/implementation-workflow.md) — practical integration and failure-handling checklist.
- [x] [.agents/skills/liquid-glass/assets/](.agents/skills/liquid-glass/assets/) — implementation brief and visual-review templates.
- [x] [docs/skill-installation.md](docs/skill-installation.md) — repository-level install/update/validation index.

Acceptance:
- [x] The Skill has a valid `SKILL.md` name/description manifest and lives in the Codex repository skill discovery directory.
- [x] The description covers Liquid Glass implementation/review across languages and platforms without matching unrelated generic styling.
- [x] The workflow requires inspecting the actual target environment before choosing APIs or rendering techniques.
- [x] The workflow gives concrete implementation, accessibility, performance, validation, and reporting steps.
- [x] Web DOM and native Android Java/XML fixtures exercise different discovery and fallback decisions without forcing one platform's APIs on the other.
- [x] All five package tests pass; Python syntax checks pass; internal Skill reference links resolve.
- [x] Installation and update instructions are provided for Windows PowerShell and macOS/Linux.

**Verification boundary:** package tests validate the Skill structure, references, read-only project detection, Android minimum-SDK evidence/XML parsing, and the documented workflows for two different platform families. They do not launch a Codex client to measure implicit skill routing, build/deploy either fixture as a real app, or prove visual refraction on physical hardware. Use explicit `$liquid-glass` invocation when deterministic selection is needed. Runtime demonstrations and visual/performance evidence remain in later roadmap phases.

## Phase 3 — Platform adaptation guidance

<badge>Complete</badge>

**Goal:** make the Skill useful across materially different rendering environments without pretending every platform has identical capabilities.

**Research snapshot:** 2026-11-04. API versions and support notes are based on the linked official vendor documentation checked for this phase. Re-check the target project's exact versions at implementation time.

Candidate families covered:
- Web DOM/CSS and browser graphics pipelines.
- Native Android UI and custom drawing/rendering.
- Native iOS/iPadOS UI and graphics pipelines.
- Desktop UI frameworks and native compositors.
- Game engines and real-time 2D/3D rendering.
- Cross-platform UI frameworks and custom GPU/canvas renderers.
- Constrained devices or environments with limited backdrop/shader access.

Tasks:
- [x] Build a capability matrix for backdrop access, refraction route, shaders/custom drawing, masks/motion, accessibility integration, and version/hardware gates.
- [x] Document a preferred approach and fallback for each family using official vendor API documentation.
- [x] Distinguish system blur/material APIs from a texture-backed path that can genuinely displace the backdrop.
- [x] Record composition boundaries and limits: backdrop roots, View/Surface ordering, SwiftUI filtered layers, WinUI composition-tree sources, Qt RHI/software backend, Flutter renderer/backend, and game-engine render-pass/UI ordering.
- [x] Keep examples small and independent; do not build a universal renderer or a lowest-common-denominator abstraction.
- [x] Record concrete API/version assumptions and instruct agents to re-check versions against the target project's manifest and official documentation.
- [x] Add worked adaptation workflows for each covered family and a catalog of expected tiers/validation steps.
- [x] Add automated regression tests for the guide files, workflow fixtures, official-source coverage, fidelity labels, local Markdown links, and the ChatGPT Desktop installation path.
- [x] Add GitHub Actions CI to compile the Python helper/tests, run the package suite, and smoke-test the read-only project inventory.

Deliverables:
- [x] [docs/platform-adaptation/README.md](docs/platform-adaptation/README.md) — family index and evidence/version policy.
- [x] [docs/platform-adaptation/capability-matrix.md](docs/platform-adaptation/capability-matrix.md) — comparison of backdrop access, refraction route, shader/mask/motion facilities, accessibility, and hardware/API gates.
- [x] [Web guide](docs/platform-adaptation/web.md) — DOM/backdrop-filter versus app-owned WebGL/WebGPU scene.
- [x] [Android guide](docs/platform-adaptation/android.md) — API 31 RenderEffect, API 33 RuntimeShader/AGSL, and explicit backdrop-source ownership.
- [x] [Apple guide](docs/platform-adaptation/apple.md) — UIKit visual effects, SwiftUI Shader modifiers, and app-owned Metal textures.
- [x] [Desktop guide](docs/platform-adaptation/desktop.md) — WinUI Composition and Qt Quick/RHI, plus framework-specific discovery rules.
- [x] [Game-engine guide](docs/platform-adaptation/game-engines.md) — Unity 6 URP Full Screen Pass and Unreal Post Process Materials.
- [x] [Cross-platform guide](docs/platform-adaptation/cross-platform.md) — Flutter BackdropFilter/Impeller and Qt Quick backend distinctions.
- [x] [Constrained-target guide](docs/platform-adaptation/constrained.md) — stable L0/L1 fallbacks and downgrade rules.
- [x] [Platform workflow catalog](.agents/skills/liquid-glass/examples/README.md) and seven new family workflows under [.agents/skills/liquid-glass/examples/](.agents/skills/liquid-glass/examples/).
- [x] [Updated Liquid Glass Skill entry point](.agents/skills/liquid-glass/SKILL.md), linking the platform matrix and worked workflows.
- [x] [GitHub Actions validation workflow](.github/workflows/skill-validation.yml) and expanded [package tests](.agents/skills/liquid-glass/tests/test_skill_package.py).

Acceptance:
- [x] Every candidate family has a preferred strategy, explicit limits, a fallback, and official documentation references.
- [x] The matrix identifies backdrop access/refraction separately from shader, mask, and animation availability.
- [x] Version/hardware gates are explicit where vendor docs publish them; otherwise the guide requires runtime/availability checks rather than inventing a universal minimum.
- [x] Each family has a reproducible decision/validation workflow fixture; automated tests verify that all covered families, tiers, and validation steps remain present.
- [x] Language/framework choices remain discoverable and extensible without forcing one renderer across platforms.
- [x] GitHub Actions on the published repository passes Python compilation, all 8 package/workflow tests, and the read-only project inventory smoke test.

**Validation boundary:** the workflows are reproducible decision/validation fixtures, not finished visual applications. The passing tests check their structure, source coverage, platform constraints, install guidance, and validation criteria. They do not compile Swift/QML/Unity/Unreal/Flutter applications or prove runtime refraction on physical devices. Runnable visual demonstrations, captures, and device-level performance evidence remain in Phases 5 and 6.

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
