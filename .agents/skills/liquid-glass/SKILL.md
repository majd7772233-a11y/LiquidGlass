---
name: liquid-glass
description: Implement, adapt, review, or debug Liquid Glass and refractive glass UI in an existing software project. Use for translucent optical surfaces, real backdrop refraction/distortion, liquid or connected shapes, fluid controls, glass navigation, or for evaluating a glass implementation across any programming language, UI framework, operating system, game engine, or rendering stack. Inspect the actual project before choosing APIs; do not trigger for unrelated generic styling unless Liquid Glass behavior is requested.
---

# Liquid Glass Skill

This is the Codex/local-workspace execution twin of [Liquid Glass Studio](../../../studio/README.md). Both use the same canonical visual specifications, platform rules, fidelity tiers, and validation standards. Studio executes through the connected GitHub app; this Skill executes in the local workspace. When shared knowledge changes, rebuild and test the Studio package using `studio/scripts/build_plugin_package.py`.

Deliver a convincing, usable Liquid Glass implementation that fits the **actual host project**. The visual target is an optical surface with background transmission, shape-aware refraction/distortion where supported, readable depth and edge response, coherent highlights, and fluid interaction when required. It is not synonymous with a blurred translucent card.

## Mandatory workflow

1. **Understand the request.** Identify whether the task is implementation, adaptation, review, debugging, or explanation. Preserve the user's requested scope and existing behavior.
2. **Inspect before deciding.** Read repository instructions (`AGENTS.md`, nested instructions, project docs), inspect the source tree and relevant components, and identify the real language, framework, runtime, build system, minimum OS/device/browser, graphics APIs, and existing dependencies. Never infer a platform from the wording of the request alone.
   - For native Android, resolve the effective variant-specific `minSdk` and inspect the device runtime API separately. Follow `docs/platform-adaptation/android.md` and `docs/platform-adaptation/android-library-catalog.md`. Preserve an existing project's minSdk; for a new project with no user-specified minimum, explain the trade-off and ask before writing one.
   - Use `scripts/inspect_project.py <project-root>` as a quick inventory when useful. It reports evidence; it does not choose a renderer.
   - Read [Project discovery](references/project-discovery.md).
3. **Translate the reference into criteria.** Identify the applicable surface shape, backdrop behavior, optical cues, interaction states, and target fidelity. When assets or screenshots are supplied, inspect the actual assets. When working from the LiquidGlass repository, read `docs/visual-specification.md`, `docs/interaction-and-motion.md`, `docs/reference-matrix.md`, and the matching guide under `docs/platform-adaptation/`. Start from [the platform adaptation index](../../../docs/platform-adaptation/README.md) and [the capability matrix](../../../docs/platform-adaptation/capability-matrix.md). When installed in another project, use the bundled platform-specific worked workflows as decision/verification fixtures; do not assume those guides describe the target's exact version. The packaged references remain the portable baseline.
4. **Choose a renderer from evidence.** Compare existing native material/compositor facilities, GPU/shader rendering, custom drawing/scene rendering, canvas/DOM composition, and layered fallbacks. Read [Rendering strategy](references/rendering-strategy.md). Select the strongest reliable option compatible with the target; do not force one language, API, or shared abstraction.
5. **Plan the smallest complete integration.** Identify the exact files and components to change, data/backdrop flow, shape/mask ownership, animation/input ownership, accessibility behavior, fallbacks, and tests. Reuse existing architecture and dependencies unless there is a demonstrated reason to change them.
6. **Implement the material and semantics together.** Keep the semantic control, hit target, focus behavior, and readable foreground content independent from decorative contour changes. Make refraction, masks, shape geometry, lighting, and motion follow one coherent surface state.
7. **Validate the real result.** Run the project's formatter, static checks, tests, and build that are available. Review captures over varied backdrops and relevant interaction states. Read [Validation and reporting](references/validation-and-reporting.md).
8. **Report truthfully.** Distinguish observed behavior from assumptions. State the achieved tier (L0–L3), which optical features are real versus approximated, tests actually run, target environment, and remaining gaps. Never claim physical accuracy, true refraction, runtime success, or visual parity without evidence.

## Non-negotiable rules

- Blur is not refraction: a blur, tint, translucent fill, border, and shadow alone are not refraction. Label a blur-only result **L1** at most; label tint/translucency without blur **L0**.
- Never choose CSS, WebGL, WebGPU, GLSL, Metal, Vulkan, Skia, Android, iOS, Unity, Unreal, or any other stack until project evidence and target constraints justify it. These are options, not requirements.
- Do not replace an existing rendering architecture or add a heavy dependency just to create a glass effect when a smaller native approach is sufficient.
- Do not fake unavailable capabilities. When backdrop access or shaders are unavailable, implement the best stable fallback and disclose the limitation.
- Keep text and icons crisp unless the user explicitly asks to refract foreground content. Preserve control semantics, hit targets, keyboard/controller access, screen-reader labels, and reduced-motion behavior.
- Avoid unbounded shader work, full-screen recapture on every input event, per-frame allocations, layout thrashing, and uncontrolled animation overshoot.
- Do not delete or overwrite user assets or project configuration without first verifying their role and necessity.
- Make a complete, tested change within the requested scope. Do not stop at a generic plan or a decorative mock-up when implementation was requested.

## Quick decision gates

- Can the platform expose or reconstruct the content behind the surface? If not, do not promise dynamic refraction.
- Can the selected path distort that content inside a stable shape mask? If not, it is not L2.
- Does the target need connected/morphing surfaces? Add a continuous geometry/motion model only when required; do not add metaballs or a physics system as decoration.
- Does the implementation work across bright, dark, detailed, and low-detail backdrops without losing content or clipping?
- Does it remain usable with reduced motion, high contrast/transparency reduction, keyboard/touch input, and lower-end hardware?

## Capability labels

Use the project's tiers consistently:

- **L0 — Translucent fallback:** stable translucent/tinted surface; no meaningful blur/refraction implied.
- **L1 — Blurred glass fallback:** backdrop blur/translucency with coherent contour/highlights; no optical displacement.
- **L2 — Refractive glass:** visible backdrop displacement through a shape-aware surface mask.
- **L3 — Dynamic liquid glass:** L2 plus coherent interactive deformation, connection/merge/split, or equivalent dynamic surface behavior.

Report feature-level facts as well as the highest demonstrated tier; partial L2 features do not automatically establish L2 as a whole.

## Reference map

Load only the references needed for the current task:

- [Project discovery](references/project-discovery.md) — evidence gathering and platform detection.
- [Rendering strategy](references/rendering-strategy.md) — renderer selection and integration boundaries.
- [Visual contract](references/visual-contract.md) — material anatomy, shape families, and fidelity tiers.
- [Motion, accessibility, and performance](references/motion-accessibility-performance.md) — behavior and resilience.
- [Validation and reporting](references/validation-and-reporting.md) — verification and final report format.
- [Platform adaptation index](../../../docs/platform-adaptation/README.md) and [capability matrix](../../../docs/platform-adaptation/capability-matrix.md) — use when this repository is available to select a verified platform-family route.
- [Liquid Glass Studio twin and package](../../../studio/README.md) — the ChatGPT execution adapter and canonical shared-knowledge packaging workflow.
- [Android dependency and renderer catalog](../../../docs/platform-adaptation/android-library-catalog.md) — third-party options, versions, and compatibility limits.
- [Platform worked workflows](examples/README.md) — Apple, Windows, Qt, Flutter, Unity, Unreal, and constrained target decision/validation fixtures.
- [Implementation workflow](references/implementation-workflow.md) — integration sequence, failure handling, and change hygiene.
- [Implementation brief template](assets/implementation-brief.template.md) and [visual review template](assets/visual-review.template.md) — reusable planning and evidence records.
- [Web DOM worked workflow](examples/web-dom/WORKFLOW.md) and [Android Java/XML worked workflow](examples/android-java/WORKFLOW.md) — examples of platform-aware reasoning, not universal prescriptions.

For the full project specification when this skill is being used from the LiquidGlass repository, see `../../../docs/` relative to this skill directory.
