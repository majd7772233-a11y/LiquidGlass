# LiquidGlass — AI Agent Instructions

> This file is the project-level instruction contract for AI coding agents (including Codex). Read it before planning, editing, reviewing, or documenting work in this repository.

## 1. Mission

Build a reusable, technically credible way to design and implement the **Liquid Glass** visual material and interaction language across programming languages, UI frameworks, operating systems, and rendering environments.

The goal is to reproduce the visual behavior shown by the project's reference assets as closely as the target platform reasonably allows. The goal is **not** to apply a generic glassmorphism theme.

The repository is intended to deliver:
1. A platform-aware, language-agnostic coding Skill that can inspect a project and choose a suitable implementation strategy.
2. A dedicated **Liquid Glass Studio** assistant/plugin workflow for analyzing references, planning implementations, generating or adapting code, and reviewing results.
3. A set of validated implementation examples, platform notes, and visual/performance tests.

Do not claim that the Skill, plugin, or complete cross-platform support already exists until the corresponding roadmap phases have actually been delivered.

## 2. Phase execution and completion contract

When the user asks to start or complete a roadmap phase, treat the phase as a complete delivery unit—not as permission to do only its first task.

1. Read the entire relevant phase, its deliverables, acceptance criteria, and any dependent repository instructions before editing.
2. Complete every in-scope task and deliverable in the same execution cycle. Do not stop after creating a partial draft, a skeleton, or only the first requested file.
3. Resolve problems independently when they are within the granted scope. Diagnose failed approaches, use another supported tool or workflow, verify the result, and continue. Do not merely report a solvable error or ask the user to perform routine repair work.
4. Do not skip a requirement silently. If a requirement is genuinely impossible after reasonable alternatives are exhausted, complete every other in-scope item, record the exact remaining blocker and its impact, and do not mark the phase complete.
5. Update the roadmap and related documentation to reflect actual work. Check off work only after its acceptance criteria have been verified.
6. Verify the published repository state—not merely the local draft or a successful write response.
7. Send one final phase report only after the phase is complete and verified. Do not send a premature completion report while deliverables or acceptance checks remain.

A phase is complete only when its required deliverables exist, agree with one another, satisfy the acceptance criteria, and have been checked in the target repository. A polished explanation is not a substitute for finished work.

## 3. Source of truth and working order

Before every substantial task:

1. Read this file and the relevant sections of ROADMAP.md.
2. Inspect the repository tree and the latest commit. Do not assume a previously remembered file layout is still current.
3. Read the relevant example catalog in examples/README.md and inspect the actual reference images when available.
4. Read the specification documents under docs/ before implementing or reviewing material and motion behavior.
5. Inspect the target project's source, framework, language, build system, deployment target, rendering APIs, and existing design conventions before proposing an implementation.
6. Identify constraints and state the intended approach before making broad or destructive changes.

Treat the visual reference assets as the target for appearance, not as implementation instructions. Treat the target project's existing architecture as the source of truth for integration. Avoid asking the user to repeat information already present in repository files or conversation context.

## 4. Visual target: what Liquid Glass means here

A convincing result may combine the following, as appropriate to the reference and platform:

- **Transmission and translucency:** the background remains perceptible through the material; opacity is spatially varied rather than a uniform translucent fill.
- **Refraction and distortion:** background content bends, shifts, magnifies, or warps through the surface. A simple blur is not a substitute.
- **Depth and thickness:** surface curvature, edge thickness, layered contours, and internal shading create the impression of a three-dimensional optical object.
- **Specular response:** broad soft highlights and tighter reflections respond coherently to lighting and shape.
- **Edge behavior:** Fresnel-like rims, bright/dark edge transitions, controlled glow, and subtle color separation can help communicate curvature.
- **Spectral effects:** restrained chromatic dispersion or iridescent color is used where supported by the reference; avoid arbitrary rainbow decoration.
- **Fluid form:** blobs, pills, controls, and connected surfaces can deform, merge, split, and settle with continuous, natural transitions.
- **Interaction:** controls should feel like physical surfaces responding to touch, pointer movement, focus, drag, press, and release—not static stickers placed over a blurred background.

The detailed platform-neutral contract is in:
- docs/visual-specification.md
- docs/interaction-and-motion.md
- docs/reference-matrix.md

A solution that uses only backdrop blur, transparency, border, and shadow is a **basic fallback**, not full Liquid Glass parity. Label it honestly using the capability tiers in the visual specification.

## 5. Reference asset interpretation

The curated still images live under examples/references/. The catalog at examples/README.md explains each inspected image and lists unclassified assets that must not be used as evidence until reviewed.

The supplied motion reference was inspected during Phase 1. Its observable motion behaviors and approximate sequence are documented in docs/reference-matrix.md. Do not assume the original video is included in the repository.

Treat all references as evidence of visible behavior, not proof of the original rendering implementation or physical parameters. Do not invent implementation details from a screenshot.

## 6. Platform- and language-neutral engineering

Never assume that the target is a web page, CSS, Android, iOS, or a particular language.

First detect:
- language(s), framework(s), runtime, build tool, and project structure;
- minimum OS/device/API level and supported hardware;
- available GPU and rendering APIs, shader support, compositing model, and access to the backdrop;
- whether the UI is native, web-based, game-engine-driven, canvas-based, or custom-rendered;
- performance, accessibility, power, licensing, and distribution constraints.

Then select the best fit. Possible implementation families include native compositor/material APIs, GPU shaders, custom drawing, scene/render pipelines, canvas or DOM effects, and carefully layered native components. Technologies such as WebGL/GLSL, WebGPU, platform shaders, Skia-like renderers, game-engine materials, or native visual-effect APIs are examples—not mandatory dependencies.

Use the most capable reliable option that fits the target environment. Keep platform-specific code behind clear adapters or modules when a shared design specification can be reused. Do not build a lowest-common-denominator abstraction that prevents high-quality platform-native rendering.

When the platform cannot provide true backdrop sampling, refraction, or dynamic lighting, explain the limitation and implement the strongest honest fallback. Never silently describe a blur-only approximation as physically refractive glass.

## 7. Rendering and motion guidance

Choose techniques based on measured needs and platform capability. Potential building blocks include:

- screen-space backdrop sampling and distortion;
- normal fields, signed-distance functions, or other shape representations;
- environment/reflection approximations where live reflections are unavailable;
- Fresnel-style edge response and specular lighting;
- carefully bounded chromatic dispersion;
- metaballs or equivalent implicit surfaces for organic merging;
- spring/damped motion for settling, dragging, and morphing;
- input-driven parallax and deformation with stable limits.

These are candidate techniques, not a fixed stack. Avoid expensive multi-pass rendering when a simpler native solution achieves the target. Avoid fake motion that jitters, jumps, leaks outside masks, or changes layout unexpectedly.

Motion should have coherent timing, damping, and continuity. Support reduced-motion preferences and provide a stable non-animated state. Interactive movement must not block input or make controls difficult to use.

## 8. Integration rules

- Preserve the host project's architecture, language, conventions, and existing visual system unless a justified change is necessary.
- Prefer small, composable material primitives and reusable behavior over duplicated one-off effects.
- Keep rendering, shape geometry, animation, input handling, and semantic/accessibility behavior separable where practical.
- Do not introduce a new framework, runtime, native dependency, or rendering engine without explaining why it is required.
- Keep public APIs explicit and document platform-specific limitations.
- Do not overwrite user work or remove existing assets without verifying their role.
- Keep example assets organized and referenced from the example catalog.

## 9. Accessibility and resilience

A visually rich surface is still a user interface. Every delivered implementation must consider:

- readable text and sufficient contrast over changing backgrounds;
- visible keyboard focus and predictable focus order where applicable;
- touch/pointer target sizes and clear pressed/selected/disabled states;
- screen-reader semantics and accessible names;
- reduced motion and non-animated alternatives;
- high-contrast or transparency-reduction system settings where the platform exposes them;
- safe fallbacks when shaders, GPU features, backdrop access, or animation are unavailable.

Do not rely on color, refraction, blur, or motion alone to communicate state.

## 10. Performance and quality

Measure before optimizing and test on the actual target class of device when possible. Consider frame pacing, GPU/CPU cost, memory and render-target use, overdraw, battery/thermal impact, startup cost, and behavior under scrolling or multiple simultaneous surfaces.

Use graceful quality tiers when hardware varies. Avoid unbounded shader loops, unnecessary full-screen passes, excessive blur radii, repeated offscreen captures, and per-frame allocations.

A change is not complete merely because it compiles. Run the relevant formatter, static checks, tests, build, and runtime/visual review available in the target project. Record unavailable tests and environmental blockers honestly.

## 11. Visual validation protocol

For any substantial visual implementation:

1. Capture the result using the same or a deliberately comparable viewport, scale, content, and background as the reference.
2. Compare silhouette, edge behavior, transmission, distortion, depth, highlights, color response, and animation—not just overall color.
3. Check multiple backgrounds, including detailed/high-frequency imagery and low-contrast surfaces.
4. Check component states: idle, hover/focus, pressed, dragged, disabled, and settled, as applicable.
5. Check resizing, scrolling, orientation, density/DPI, and accessibility settings supported by the target.
6. Record gaps against the reference and either fix them or document the platform limitation.

Do not claim pixel-perfect or reference-matched output without evidence. Prefer side-by-side captures and reproducible test instructions.

## 12. Documentation and delivery

For each feature or platform adapter, document:
- target platform and minimum requirements;
- implementation approach and why it was selected;
- limitations and fallback behavior;
- configuration/public API;
- build and run instructions;
- validation performed, device/runtime used, and known visual gaps.

Keep ROADMAP.md accurate. Mark a phase or task complete only when its acceptance criteria are met. Split large work into reviewable changes, preserve a clean history, and report changed paths, tests, results, and remaining gaps.

## 13. Definition of done

A task is done only when all applicable conditions are met:

- it follows this instruction file and the current roadmap;
- it integrates with the actual target architecture;
- its material behavior is described honestly (full, partial, or fallback);
- it builds and passes relevant automated checks;
- its visible states and accessibility behavior have been reviewed;
- performance and fallback behavior have been considered;
- documentation and examples are updated;
- the final report lists concrete changes and any unverified items.

When instructions conflict, prioritize user intent, repository facts, platform correctness, accessibility, and measured quality over assumptions or cosmetic shortcuts.
