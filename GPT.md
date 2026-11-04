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

## 2. Source of truth and working order

Before every substantial task:

1. Read this file and the relevant sections of ROADMAP.md.
2. Inspect the repository tree and the latest commit. Do not assume a previously remembered file layout is still current.
3. Read the relevant example catalog in examples/README.md and inspect the actual reference images when available.
4. Inspect the target project's source, framework, language, build system, deployment target, rendering APIs, and existing design conventions before proposing an implementation.
5. Identify constraints and state the intended approach before making broad or destructive changes.

Treat the visual reference assets as the target for appearance, not as implementation instructions. Treat the target project's existing architecture as the source of truth for integration. Avoid asking the user to repeat information already present in repository files or conversation context.

## 3. Visual target: what Liquid Glass means here

A convincing result may combine the following, as appropriate to the reference and platform:

- **Transmission and translucency:** the background remains perceptible through the material; opacity is spatially varied rather than a uniform translucent fill.
- **Refraction and distortion:** background content bends, shifts, magnifies, or warps through the surface. A simple blur is not a substitute.
- **Depth and thickness:** surface curvature, edge thickness, layered contours, and internal shading create the impression of a three-dimensional optical object.
- **Specular response:** broad soft highlights and tighter reflections respond coherently to lighting and shape.
- **Edge behavior:** Fresnel-like rims, bright/dark edge transitions, controlled glow, and subtle color separation can help communicate curvature.
- **Spectral effects:** restrained chromatic dispersion or iridescent color is used where supported by the reference; avoid arbitrary rainbow decoration.
- **Fluid form:** blobs, pills, controls, and connected surfaces can deform, merge, split, and settle with continuous, natural transitions.
- **Interaction:** controls should feel like physical surfaces responding to touch, pointer movement, focus, drag, press, and release—not static stickers placed over a blurred background.

A solution that uses only backdrop blur, transparency, border, and shadow is a **basic fallback**, not full Liquid Glass parity. Label it honestly.

## 4. Reference asset interpretation

The curated images live under examples/references/. Their purpose is to establish visual characteristics and use cases:

- **controls/translucent-controls-and-sliders.png:** floating glass controls, pill-shaped surfaces, sliders, and simple action affordances.
- **storyboards/liquid-glass-interface-storyboard.png:** a sequence/contact sheet showing glass navigation and search-like controls over changing photographic backgrounds.
- **media/refractive-media-playback-controls.png:** translucent circular media controls with visible background transmission and colored edge/reflection behavior.
- **material/organic-iridescent-liquid-glass-form.png:** a large continuous organic surface with soft depth, luminous edges, and pearlescent color transitions.
- **unclassified/additional-concept-reference-01.png** through **04.png:** retained source images that still need visual inspection and classification. Do not infer their contents from their former numeric filenames.

These images are examples, not exhaustive specifications. Do not force every component to look identical. Extract reusable material properties and interaction rules, then adapt their expression to the component's role and platform conventions.

## 5. Platform- and language-neutral engineering

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

## 6. Rendering and motion guidance

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

## 7. Integration rules

- Preserve the host project's architecture, language, conventions, and existing visual system unless a justified change is necessary.
- Prefer small, composable material primitives and reusable behavior over duplicated one-off effects.
- Keep rendering, shape geometry, animation, input handling, and semantic/accessibility behavior separable where practical.
- Do not introduce a new framework, runtime, native dependency, or rendering engine without explaining why it is required.
- Keep public APIs explicit and document platform-specific limitations.
- Do not overwrite user work or remove existing assets without verifying their role.
- Keep example assets organized and referenced from the example catalog.

## 8. Accessibility and resilience

A visually rich surface is still a user interface. Every delivered implementation must consider:

- readable text and sufficient contrast over changing backgrounds;
- visible keyboard focus and predictable focus order where applicable;
- touch/pointer target sizes and clear pressed/selected/disabled states;
- screen-reader semantics and accessible names;
- reduced motion and non-animated alternatives;
- high-contrast or transparency-reduction system settings where the platform exposes them;
- safe fallbacks when shaders, GPU features, backdrop access, or animation are unavailable.

Do not rely on color, refraction, blur, or motion alone to communicate state.

## 9. Performance and quality

Measure before optimizing and test on the actual target class of device when possible. Consider frame pacing, GPU/CPU cost, memory and render-target use, overdraw, battery/thermal impact, startup cost, and behavior under scrolling or multiple simultaneous surfaces.

Use graceful quality tiers when hardware varies. Avoid unbounded shader loops, unnecessary full-screen passes, excessive blur radii, repeated offscreen captures, and per-frame allocations.

A change is not complete merely because it compiles. Run the relevant formatter, static checks, tests, build, and runtime/visual review available in the target project. Record unavailable tests and environmental blockers honestly.

## 10. Visual validation protocol

For any substantial visual implementation:

1. Capture the result using the same or a deliberately comparable viewport, scale, content, and background as the reference.
2. Compare silhouette, edge behavior, transmission, distortion, depth, highlights, color response, and animation—not just overall color.
3. Check multiple backgrounds, including detailed/high-frequency imagery and low-contrast surfaces.
4. Check component states: idle, hover/focus, pressed, dragged, disabled, and settled, as applicable.
5. Check resizing, scrolling, orientation, density/DPI, and accessibility settings supported by the target.
6. Record gaps against the reference and either fix them or document the platform limitation.

Do not claim pixel-perfect or reference-matched output without evidence. Prefer side-by-side captures and reproducible test instructions.

## 11. Documentation and delivery

For each feature or platform adapter, document:
- target platform and minimum requirements;
- implementation approach and why it was selected;
- limitations and fallback behavior;
- configuration/public API;
- build and run instructions;
- validation performed, device/runtime used, and known visual gaps.

Keep ROADMAP.md accurate. Mark a phase or task complete only when its acceptance criteria are met. Split large work into reviewable changes, preserve a clean history, and report changed paths, tests, results, and remaining gaps.

## 12. Definition of done

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
