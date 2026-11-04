# Project discovery and evidence collection

Do this before selecting a graphics technique. The goal is to establish what is actually present, not to infer a stack from a user saying “make it glassy.”

## 1. Read project instructions first

Inspect root and nested `AGENTS.md`, `README`, build files, architecture notes, platform manifests, and existing UI/material components. Respect the repository's contribution, dependency, naming, formatting, and test conventions. Identify files the user asked you not to change.

## 2. Build an evidence profile

Record facts and their source. Prefer actual build configuration and source imports over filenames or assumptions.

| Dimension | Evidence to inspect |
|---|---|
| Languages | Source extensions, compiler configuration, module declarations |
| UI framework | Imports, project files, plugin configuration, component tree |
| Runtime | Browser/runtime version, OS, JVM, CLR, native runtime, game engine version |
| Build system | Gradle, Maven, Xcode, SwiftPM, MSBuild, CMake, Cargo, npm/pnpm/yarn, custom scripts |
| Target baseline | minSdk/deployment target/browser support/OS version/device class |
| Graphics path | Compositor/material APIs, shader languages, GPU backend, canvas/DOM, Skia-like renderer, game render pipeline |
| Backdrop access | Live backdrop sampling, snapshots, render targets, readback restrictions, cross-window limitations |
| Geometry and masks | Clip paths, stencil, alpha masks, SDF support, vector paths, custom drawing |
| Animation/input | Existing animation engine, gesture/pointer model, frame callbacks, reduced-motion hooks |
| Quality constraints | GPU/CPU budget, memory, battery/thermal, accessibility, offline, licensing, privacy |

Use `scripts/inspect_project.py` for a quick, read-only file inventory. Inspect its evidence in context; it is heuristic and must not be treated as an architectural diagnosis.

## 3. Identify the project family without excluding other signals

Typical signals include:

- **Web DOM/browser:** HTML, CSS, JS/TS, `package.json`, browser entry points, bundler/framework configuration.
- **Native Android:** `AndroidManifest.xml`, Gradle Android plugin, Java/Kotlin source, resources, Compose configuration.
- **Native Apple:** Xcode project/workspace, Swift/Objective-C, deployment target, SwiftPM/CocoaPods configuration.
- **Desktop:** `.csproj`, `.sln`, Qt/CMake, AppKit/WinUI/WPF/Avalonia/JavaFX project files, native window/compositor APIs.
- **Game/real-time 2D/3D:** Unity/Unreal/Godot project files, scene/material/shader pipelines, render-pipeline assets.
- **Cross-platform/custom:** Flutter, React Native, MAUI, Qt, Skia, SDL, custom canvas/GPU layers, or multiple targets in one repository.

A monorepo may contain multiple independent targets. Map each relevant UI surface to its own build target instead of flattening the repository into a single platform label.

## 4. Establish the backdrop/rendering capability

Answer these questions with direct evidence:

1. Can the surface access the actual background pixels, a compositor-provided backdrop, or a reusable rendered texture?
2. Can it displace background samples with a spatially varying field and clip the result to a changing shape?
3. Can it produce a stable mask/normal/shape representation at the required resolution and frame rate?
4. Are custom shaders permitted on the minimum supported target, not only on the developer's machine?
5. Can the chosen path keep semantic text/icons outside the distortion pass?
6. What is the fallback when capture, shaders, memory, or GPU features are unavailable?

Distinguish GPU sampling from CPU readback. The latter can be prohibitively expensive or restricted; do not assume it is needed.

## 5. Report uncertainty explicitly

Use `confirmed`, `strong inference`, or `unknown` per important fact. If a platform feature is version-gated, find the project's minimum supported version and inspect the existing implementation. Do not silently raise minimum OS/API levels.

## Discovery output

Before implementing, write a short internal checklist or plan containing:

- project family and exact target;
- language/framework/runtime/build system;
- minimum supported environment;
- existing rendering/backdrop facilities and source evidence;
- important constraints and unknowns;
- likely rendering options to compare;
- files/components likely to change and tests to run.
