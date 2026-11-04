# Platform Adaptation Guide

**Research snapshot:** 2026-11-04  
**Scope:** platform-aware implementation guidance for the LiquidGlass material contract. This is a capability-selection guide, not a promise that every platform can render identical optics.

## Read this first

1. Read the [capability matrix](capability-matrix.md).
2. Open the family guide matching the actual project.
3. Inspect the project's minimum OS/API/browser, graphics backend, composition tree, and backdrop owner.
4. Choose a primary route and a tested fallback; document which features are genuine, approximated, or unavailable.
5. Use the [worked adaptation workflows](../../.agents/skills/liquid-glass/examples/) as reproducible decision/verification fixtures. They do not replace Phase 5 runnable visual demos.

## Platform-family guides

- [Web DOM and browser graphics](web.md)
- [Native Android](android.md) — mandatory minSdk/runtime policy and [third-party dependency catalog](android-library-catalog.md)
- [Apple platforms](apple.md)
- [Desktop UI and compositors](desktop.md)
- [Game engines](game-engines.md)
- [Cross-platform UI frameworks](cross-platform.md)
- [Constrained or backdrop-inaccessible environments](constrained.md)

## Core rule

**Backdrop access is the decisive capability.** A shader can distort only pixels it can sample. A blur API may read previously rendered content but still provide no shape-aware displacement. Never infer access to arbitrary views, other windows, protected video, another process, or all UI layers from the existence of a shader or compositor API.

Use project fidelity labels consistently:

- **L0:** translucent/tinted surface only.
- **L1:** blur/translucency; backdrop geometry is not displaced.
- **L2:** visible shape-aware backdrop displacement/refraction.
- **L3:** L2 plus coherent dynamic/interactive shape deformation and connection/merge/split.

## Version and evidence policy

The examples name concrete APIs and version gates where official documentation states them. Browser support, OS availability, engine packages, graphics backends, and device driver support change. At implementation time, re-check the exact version in the target project's lockfiles/manifests and the official documentation linked in each guide. Runtime-check optional capabilities; do not raise the project's minimum target without approval.

## Sources and checked assumptions

The family guides link official documentation for browser effects and WebGPU, Android RenderEffect/AGSL, Apple visual effects/SwiftUI shaders/Metal, WinUI Composition, Qt Quick, Flutter, Unity URP, and Unreal post-processing. Their limits are recorded separately from visual recommendations. A cited API demonstrates only the capability described by its source; it does not prove that the complete Liquid Glass target is available automatically.
