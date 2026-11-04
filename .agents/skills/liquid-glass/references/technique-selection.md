# Rendering Technique Selection

Choose an implementation by matching required visual behavior to verified project capabilities. A particular API or shader is never the goal by itself.

## Capability gates

Before comparing techniques, answer:

1. Can the target access the real backdrop or a faithful app-owned representation?
2. Can it displace that backdrop within a stable shape mask?
3. Can the chosen path render on every supported minimum device/OS, or can it be gated?
4. Can the optical layer be composited with semantic controls without breaking input, clipping, z-order, or accessibility?
5. Can the result meet the performance budget under scrolling, resizing, and multiple surfaces?

If the first two answers are no, do not call the result refractive. Consider changing the composition boundary, using an app-owned render surface, or providing an honest fallback.

## Strategy comparison

| Strategy | Prefer when | Verify before choosing | Common risks |
|---|---|---|---|
| Native material/compositor | The platform provides a mature effect that matches required backdrop, blur, tint, and depth behavior | API availability on minimum target, actual optical capabilities, contrast behavior, compositor restrictions | Native effect may be blur-only or vary across OS versions |
| GPU/shader path | The app owns or can safely provide backdrop pixels and needs controlled displacement, masks, or coherent optical response | Shader language/version, texture access, precision, color space, compositing, driver support, memory and pass cost | Capture cost, render-target memory, driver variance, clipping and alpha errors |
| Custom drawing/vector geometry | Shape, edge, and interaction behavior matter more than complex live backdrop sampling, or the framework exposes an efficient custom path | Path/mask quality, anti-aliasing, coordinate scaling, clipping, animation cost | Can imitate depth but cannot create true displacement without backdrop access |
| Canvas/DOM composition | The browser/framework owns the relevant scene and can render the background and glass in a controlled pipeline | Origin cleanliness, canvas tainting, CSS stacking contexts, backdrop restrictions, browser support | Arbitrary DOM is not automatically available as a shader texture |
| Game/scene render pipeline | A camera/scene render target and materials already exist | Pipeline variant, render order, UI composition, platform shader variants | Additional passes, camera stacking, pipeline maintenance |
| Layered fallback | Backdrop access or advanced APIs are unavailable, too expensive, or outside supported targets | Contrast, stable tint, reduced blur/decoration, clear labeling | Easy to overstate fidelity or produce an opaque card |
| Hybrid | Native controls need to remain semantic while a GPU/custom layer supplies optical pixels | Coordinate mapping, clipping, hit regions, lifecycle, accessibility and input synchronization | Layer drift, duplicate input, z-order or lifecycle defects |

## Decision procedure

1. List requirements: transmission, actual refraction, depth, reflection/edge response, spectral accents, geometry, and motion.
2. Classify each as required, optional, or unavailable/not requested.
3. Eliminate techniques that cannot satisfy a required behavior on the minimum target.
4. Compare remaining options for backdrop ownership, integration size, lifecycle, accessibility, testability, and measured cost.
5. Select one primary strategy and one fallback. Explain why a plausible alternative was not chosen.
6. Define capability gates and runtime downgrade behavior before coding.
7. Revisit the decision if a probe or benchmark contradicts an assumption.

| Dimension | Decision question |
|---|---|
| Fidelity | Does it provide the required optical and shape behavior? |
| Compatibility | Does it work across the actual support range? |
| Integration | Does it fit the existing architecture with limited disruption? |
| Performance | Does measured/projected cost fit the device budget? |
| Resilience | Is there a stable downgrade path? |
| Accessibility | Can semantics, focus, contrast, and reduced motion remain intact? |
| Maintainability | Can the team test, document, and update it safely? |

Do not let a high fidelity score hide a failure on a required compatibility, accessibility, or stability gate.

## Fidelity labels

- **L0 — Translucent fallback:** stable translucent/tinted surface; no implied blur or refraction.
- **L1 — Blurred glass fallback:** blur/translucency with coherent contour; no displaced backdrop geometry.
- **L2 — Refractive glass:** backdrop features are visibly displaced through the masked surface.
- **L3 — Dynamic liquid glass:** L2 plus coherent shape deformation, connection/merge/split, and interaction response.

A strategy can combine genuine and approximated properties. List them separately. Never upgrade the tier based on a polished screenshot, shader complexity, or marketing language.
