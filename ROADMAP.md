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
| 4. Liquid Glass Studio workflow | Complete | Private ChatGPT execution twin, seven workflow contracts, shared knowledge, verified GitHub binding, and user-confirmed host invocation |
| 5. Reference implementations | Complete | Runnable WebGL2 and Android Java/GLES2 L2/L3 demos with automated browser/emulator builds and captured evidence |
| 6. Validation, accessibility, and performance | In progress | Browser/emulator quality gates, accessibility coverage, reproducible profiling protocol; physical-device evidence remains outstanding |
| 7. Packaging and release | In progress | Versioned self-contained Skill package, private Studio setup, Windows install CI; stable tag awaits maintainer-owned Phase 6 device evidence |

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

<badge>Complete</badge>

**Goal:** create Liquid Glass Studio as the ChatGPT-side execution twin of `$liquid-glass`, using the same visual/platform knowledge and actual GitHub repository actions. The plugin is a portable Skill package bound to the existing GitHub connector; it does not create a duplicate GitHub server or claim local-machine access.

**Delivered capabilities:**
1. **Reference inspection:** evidence-based analysis of supplied screenshots/frames, with confidence and unknowns.
2. **Visual specification:** structured material, geometry, motion, semantics, fidelity, and validation brief.
3. **Project diagnosis:** connected-repository inspection of source tree, framework, build, dependencies, renderer, and constraints.
4. **Strategy selection:** comparison of native, existing libraries, custom GPU/drawing, and fallbacks.
5. **Code implementation:** scoped GitHub repository edits and commits after an explicit change request.
6. **Implementation review:** source/diff/capture review against the visual contract.
7. **Performance/accessibility audit:** code-risk review plus measured evidence only when real profiling/tests are available.

**Tasks:**
- [x] Verify the supported private-plugin creation and account-package workflow; use the existing GitHub app binding because the Sites MCP server reference is unavailable in this environment.
- [x] Define seven Studio workflow contracts with inputs, outputs, evidence, validation, and error boundaries.
- [x] Make reference analysis evidence-based and confidence-labelled.
- [x] Keep code-writing operations explicit and scoped to user-authorized projects.
- [x] Establish shared knowledge synchronization from canonical Skill/specification files into the portable Studio package.
- [x] Add a reproducible plugin package builder and automated manifest, binding, reference, and archive tests.
- [x] Create the private plugin in the user's personal account; verify its private metadata, current release, 28-file package inventory, and `.app.json` GitHub connector ID.
- [x] Verify the actual `@Liquid Glass Studio` invocation in ChatGPT. The user tested it and confirmed the behavior matches the intended workflow.

**Acceptance:**
- [x] The private plugin is saved in the personal account; its release metadata, packaged Skill, and GitHub app binding are verified.
- [x] The user confirmed the actual host invocation works in ChatGPT.
- [x] Each Studio workflow has a clear contract and meaningful automated regression coverage.
- [x] The workflow can take a request from reference to platform-aware repository implementation and review through the GitHub connector.
- [x] Studio and `$liquid-glass` use the same packaged specifications and L0–L3 definitions.
- [x] The plugin does not claim to render or change the ChatGPT application interface itself.

**Release:** private plugin version `0.1.0`, current release `pluginrel_6aeb56991a6c8191acff6f509dc51779`. See [Studio setup and release details](studio/README.md).

## Phase 5 — Reference implementations

<badge>Complete</badge>

**Goal:** prove that the specification and Skill can produce working interfaces, not just documents.

**Selected targets and rationale:**
- **Browser / WebGL2:** a controlled app-owned scene texture demonstrates true sample displacement, a portable browser rendering path, semantic HTML controls, and responsive desktop/mobile layouts.
- **Android Views / Java / OpenGL ES 2.0:** a native Java app with an app-owned GLES framebuffer demonstrates the equivalent material path while keeping text, buttons, and the strength control as native Android Views. The standalone sample uses minSdk 23; this is not a prescribed minimum for existing Android projects.

**Tasks:**
- [x] Select two representative platform families with runnable browser and Android emulator environments.
- [x] Build a self-contained WebGL2 demo with an animated background, rounded refractive surface, interactive timeline/playback controls, and a connected organic lobe.
- [x] Build a standalone Android Java/GLES2 app with an owned framebuffer, refractive SDF lens, native buttons/SeekBar, and connected-shape interaction.
- [x] Demonstrate real backdrop sampling/displacement for L2 and an animated connected/morphing surface for L3 in both implementations.
- [x] Provide honest L1/L0 fallback paths and label them separately from refraction.
- [x] Document standalone build/run steps, supported baseline, renderer boundaries, fidelity, and visual/physical-optics limitations.
- [x] Add automated contract tests plus a browser smoke test and Android API 35 emulator launch/interaction test.
- [x] Capture desktop/mobile WebGL2 screenshots and an Android L3 emulator screenshot after activating the connected-lens control.
- [x] Record deviations and emulator/browser coverage limits; upload APK, GL log, UI hierarchy, and captures as CI artifacts.

**Acceptance:**
- [x] Both demos build and run using documented steps in their actual target environments.
- [x] WebGL2 headless Chromium verifies the owned-texture renderer, morph control, playback state, range input, and desktop/mobile captures.
- [x] Android API 35 emulator verifies app launch, the GLES2 app-owned framebuffer, the L3 renderer diagnostic, the native accessibility node, and a tap that activates the connected lens before capture.
- [x] Each demo clearly states its actual L2/L3 path and its L0/L1 fallback, without claiming that blur alone is refraction.
- [x] The examples demonstrate distinct platform implementations rather than repeating a blur-only card.

**Verified CI evidence (2026-11-04):**
- [x] [Runnable reference demos — GitHub Actions run 41872058940](https://github.com/majd7772233-a11y/LiquidGlass/actions/runs/41872058940) — both WebGL2 and Android Java/GLES2 jobs completed with `success` on commit `ec2ddd9ec23c46dc1329b28b939e25ac94f56364`.
- [x] [Skill, Studio, and reference-demo contract validation — run 41872058961](https://github.com/majd7772233-a11y/LiquidGlass/actions/runs/41872058961) — all 8 Skill tests, 4 Studio package tests, and 5 reference-demo tests passed; package builder and read-only project inventory checks passed.
- [x] WebGL2 artifacts contain desktop and mobile Chromium screenshots.
- [x] Android artifacts contain the debug APK, GL diagnostic log, accessibility-window XML, and post-interaction L3 screenshot. The diagnostic log records `GL_CONTEXT_READY`, `SCENE_FBO_READY`, and `GL_READY tier=L3 renderer=GLES2_APP_OWNED_FBO`.

**Validation boundary and deviations:**
- The WebGL2 capture uses headless Chromium with SwiftShader; the Android capture uses an API 35 x86_64 Google APIs emulator. Neither proves identical performance or behavior on every physical GPU/device.
- The scene is procedural, the surface normal is estimated from an SDF, and reflection/dispersion terms are approximations. The samples demonstrate real displacement of an app-owned texture and a connected-shape transition; they do not claim physical-optics accuracy or pixel parity with the supplied still/video references.
- No physical-device frame pacing, GPU utilization, battery, thermal, TalkBack certification, or cross-device visual study is claimed. These remain Phase 6 work.

**Deliverables:**
- [x] [Runnable implementation catalog](examples/README.md).
- [x] [WebGL2 implementation and validation guide](examples/webgl2/README.md).
- [x] [Android Java/GLES2 implementation and validation guide](examples/android-gles/README.md).
- [x] [Android emulator verification script](examples/android-gles/scripts/verify-emulator.sh).
- [x] [Reference-demo GitHub Actions workflow](.github/workflows/reference-demos.yml).
- [x] [Reference implementation contract tests](examples/tests/test_reference_demos.py).

## Phase 6 — Validation, accessibility, and performance

<badge>In progress</badge>

**Goal:** establish repeatable quality gates for both generated code and maintained examples, and preserve evidence that distinguishes automated/emulator measurements from physical-device results.

**Delivered automation and guidance:**
- [x] Create a visual review checklist, review-record template, and side-by-side capture procedure with evidence labels.
- [x] Add WebGL2 diagnostics for rolling frame intervals, average/P95/max frame time, slow-frame counts, CPU-side GL command submission, draw calls, DPR, and estimated RGBA8 scene-texture memory.
- [x] Add Android GLES2 diagnostics for GL vendor/renderer/version, frame callback intervals, P95 frame pacing, approximate FPS, slow-frame counts, CPU-side GL submission, estimated FBO texture memory, and pass/surface counts.
- [x] Add multiple background cases: dark, bright, and high-frequency/detail scenes; adapt bright-scene foreground and glass-surface tones to maintain contrast and enforce WCAG AA checks in the browser matrix.
- [x] Add responsive browser captures for desktop, tablet, mobile/high-DPR, and landscape; test semantic names, state, keyboard order, focus indicator, and action hit targets.
- [x] Add browser reduced-motion, increased-contrast, reduced-transparency, forced-colors, and L0/L1 fallback tests.
- [x] Improve Android touch targets, high-text-contrast handling, reduced-animation handling, orientation behavior, and demand-driven rendering while paused/idle.
- [x] Add UIAutomator checks for native accessibility names and dp-sized hit regions.
- [x] Add Android emulator scenarios for alternate density/size, a deterministic test-only landscape Activity request, and one primary plus three additional SDF glass surfaces.
- [x] Add reproducible Android profiling collection for gfxinfo/frame stats, process memory, CPU snapshot, display/density, SurfaceFlinger layers, battery, and thermal service diagnostics.
- [x] Add CI contract tests and retain browser/device evidence as workflow artifacts.
- [x] Document GPU/overdraw/thermal/battery physical-device profiling protocol and the exact limits of emulator/headless evidence.

**Acceptance evidence:**
- [x] Test procedures and review record are reproducible and checked in.
- [x] Browser and Android automation cover backgrounds, viewport/density/orientation, accessibility states, fallback tiers, and multiple surfaces. The browser's bright-scene text and button checks require at least 4.5:1 against all tested palette anchors.
- [x] Emulator/headless diagnostic results and raw evidence are captured by CI; no visual-parity claim is made without comparative evidence.
- [x] Known platform and hardware limitations are explicit in docs and generated reports.

**Remaining external validation before release:**
- [ ] **Maintainer-owned (delegated to the user):** run the Android profiler on physical low/mid-range and higher-tier GPUs; collect real GPU duration/counters, total memory/overdraw, sustained thermal and battery-delta measurements.
- [ ] **Maintainer-owned (delegated to the user):** perform human TalkBack/screen-reader speech, switch-access, magnification, and visual reference review on representative physical devices.
- [ ] **Maintainer-owned (delegated to the user):** validate WebGL2 behavior and GPU timing on a physical browser/GPU (the current headless CI uses SwiftShader).

**Verified CI evidence (2026-11-04):**
- [x] [WebGL2 browser validation job 126817477347](https://github.com/majd7772233-a11y/LiquidGlass/actions/runs/41899401878/job/126817477347) passed on the unchanged WebGL2 bright-scene/accessibility implementation. It emitted the responsive capture matrix, L0/L1 fallback captures, and JSON diagnostics.
- [x] [Android API 35 emulator validation job 126818622052](https://github.com/majd7772233-a11y/LiquidGlass/actions/runs/41899729725/job/126818622052) passed on commit `f3d7c1ed71ca0359e095068279489c3ace50d57b`: L3 framebuffer initialization, accessibility target report, 720×1280 portrait, a test-only landscape Activity layout at 1280×720, four SDF surfaces, and Android profiler artifacts.

**Observed software-renderer warning:** the captured headless Chromium/SwiftShader desktop sample averaged 152.77 ms/frame (P95 266.80 ms); the Android SwiftShader four-surface sample averaged 281.31 ms/frame (P95 775.20 ms, about 3.6 FPS). These are poor software-emulation results, not evidence of physical-device performance and not a production performance pass. They are recorded to prevent an optimistic performance claim and to motivate the remaining physical-GPU profiling.

**Measurement boundary:** the GitHub Actions Android job uses an API 35 x86_64 emulator with SwiftShader; its landscape scenario requests `SCREEN_ORIENTATION_LANDSCAPE` through a test-only launch extra to verify layout and configuration, not physical accelerometer rotation; browser CI uses headless Chromium/SwiftShader. Frame callback and CPU command-submission numbers are diagnostics, not GPU execution timings. Texture-byte values describe only the app-owned RGBA8 texture, not total process/driver memory. Battery and thermal snapshots from an emulator are not device-endurance evidence. See [Phase 6 validation and profiling protocol](examples/validation/README.md).

**Deliverables:**
- [x] [Phase 6 validation guide](examples/validation/README.md).
- [x] [Visual review template](examples/validation/visual-review-template.md).
- [x] [WebGL2 multi-scenario/accessibility/performance test](examples/webgl2/tests/smoke.mjs).
- [x] [Android demand-driven renderer and performance diagnostics](examples/android-gles/app/src/main/java/org/liquidglass/reference/GlassRenderer.java).
- [x] [Android emulator verification script](examples/android-gles/scripts/verify-emulator.sh).
- [x] [Android emulator profiling script](examples/android-gles/scripts/profile-emulator.sh).
- [x] [Phase 6 contract tests](examples/tests/test_phase6_validation.py).
- [x] [Extended reference-demo CI workflow](.github/workflows/reference-demos.yml).

## Phase 7 — Packaging and release

<badge>In progress</badge>

**Goal:** publish maintainable, versioned, installable deliverables without redistributing uncleared reference assets or private account bindings.

**Delivered packaging work:**
- [x] Add strict SemVer version metadata for the standalone Skill and keep it aligned with the existing private Studio plugin manifest.
- [x] Build a self-contained Skill ZIP with bundled canonical project documentation, rewritten repository-relative links, and SHA-256 inventory manifest.
- [x] Add PowerShell install/update/uninstall scripts. Updates stage and verify the new folder, preserve the previous version in a timestamped backup, and never remove sibling Skills.
- [x] Add package tests for archive inventory, documentation-link closure, version alignment, asset/private-binding exclusion, and deterministic ZIP output.
- [x] Add a Windows clean-runner CI job for checkout installation, update/backup behavior, scoped uninstall, and installation from the built ZIP.
- [x] Add changelog, contribution guidance, license boundary, asset provenance notes, and end-user release/setup documentation.
- [x] Finalize the private Studio setup/update guide. The existing personal Studio plugin (0.1.0) and its GitHub binding remain verified; its package is explicitly not a public plugin artifact.

**Acceptance evidence:**
- [x] The Skill archive is a single top-level liquid-glass/ folder with a valid SKILL.md, strict version, bundled platform references, installation scripts, license/provenance notices, and SHA-256 manifest.
- [x] The package builder checks all local Markdown links and produces a reproducible archive.
- [x] Windows CI installs from both the repository and the ZIP, tests update backup preservation, and removes only the Skill folder while preserving an unrelated Skill.
- [x] Studio setup instructions match the verified existing private account installation and explicitly describe the GitHub connector and privacy boundary.
- [x] Release notes list the supported Skill host target and known platform/performance limitations.


**Verified packaging CI evidence (2026-11-05):**
- [x] [Windows/Linux packaging workflow run 42036825924](https://github.com/majd7772233-a11y/LiquidGlass/actions/runs/42036825924) completed successfully on commit `4c04a7784a265d8433ab9f91618c2155ea8ddfda`; both validation jobs passed.
- [x] Linux: 8 Skill tests, 4 Studio package tests, 10 reference/Phase 6 contract tests, and 5 release-package tests passed; Python compilation, package builders, project inventory smoke test, and standalone Skill artifact upload passed.
- [x] Windows: standalone ZIP build, checkout install, update/backup preservation, scoped uninstall, and ZIP-based install/uninstall all passed.
- [x] [Standalone Skill build artifact](https://github.com/majd7772233-a11y/LiquidGlass/actions/runs/42036825924) — `liquid-glass-skill-0.1.0`, artifact ID `13418124335`, 102,172 bytes; 14-day retention.
- [x] Downloaded package inspection: inner ZIP 107,142 bytes, SHA-256 `4442788ba6cbe108b39cbc71acba5d7618a95eded506fc77195071b5a201cb48`; 49 entries with 48 SHA-256 manifest entries, zero mismatches, and no bundled reference media, APKs, or private `.app.json` binding.
- [x] Privacy hardening: CI builds and validates the private Studio package in an ephemeral runner but uploads only the standalone Skill artifact. No Studio plugin archive is emitted as a downloadable artifact by the current workflow.

**Release boundary:**
- The standalone Skill package version is 0.1.0; Studio's private package remains 0.1.0. No public GitHub Release or stable tag exists yet.
- A stable tag is deliberately withheld until the maintainer supplies the physical-device evidence listed in Phase 6. CI packaging does not certify real Android GPU timing, phone battery/thermal behavior, human accessibility, or physical-browser GPU timing.
- The repository has not selected a general open-source or redistribution license; LICENSE is a rights-status notice, not a standard-form license. Supplied visual references are excluded from generated packages because their redistribution permissions are not established.
- The private Studio archive contains the account-bound .app.json GitHub connector binding and must never be attached to a public release.

**Deliverables:**
- [x] Skill package builder (scripts/build_skill_package.py) and package tests (scripts/tests/test_release_package.py).
- [x] Skill install/update/uninstall scripts (.agents/skills/liquid-glass/scripts/).
- [x] Windows clean-install workflow (.github/workflows/skill-validation.yml).
- [x] Standalone Skill installation guide (.agents/skills/liquid-glass/INSTALL.md).
- [x] Studio setup and private update guide (studio/INSTALL.md).
- [x] Packaging and release guide (docs/release/README.md).
- [x] CHANGELOG.md, CONTRIBUTING.md, LICENSE, and PROVENANCE.md.
- [ ] Publish a stable tag and GitHub Release after all Phase 6 maintainer-owned physical-device acceptance evidence has been recorded.

## Global definition of done

A deliverable is complete only when it is integrated with its target environment, validated to the extent claimed, documented, accessible, and honest about visual fidelity and platform limitations. A successful text response or code snippet alone does not satisfy this roadmap.
