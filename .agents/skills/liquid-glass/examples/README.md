# Platform Adaptation Workflow Catalog

These are compact, reproducible decision and validation workflows. They are designed to make platform constraints explicit and to protect the Skill from choosing APIs by habit. They are **not** runnable demo applications.

Runnable visual implementations and CI capture routes now live in the root [examples catalog](../../../../examples/README.md): the WebGL2 app-owned-backdrop demo and Android Java/OpenGL ES 2.0 app. Keep these implementation demos separate from the decision/validation fixtures below.

| Family / sample | Strategy being evaluated | Honest expected tier before target-specific testing |
|---|---|---|
| [Web DOM](web-dom/WORKFLOW.md) | CSS backdrop filter and the boundary between DOM and app-owned WebGL/WebGPU | L1 at most for CSS blur |
| [Android Java/XML](android-java/WORKFLOW.md) | Native View baseline, minSdk gates, API 31/33 routes, and explicit backdrop ownership | L0 baseline |
| [Apple SwiftUI](apple-swiftui/WORKFLOW.md) | Native material, SwiftUI view-layer shaders, app-owned Metal texture | L1 baseline |
| [Windows WinUI](windows-winui/WORKFLOW.md) | Composition effect graphs and supplied texture boundaries | No L2 without an owned scene texture |
| [Qt 6 Quick](qt6-quick/WORKFLOW.md) | QSB ShaderEffect, RHI backend, QRhi/QSGRenderNode integration | No L2 from ShaderEffect alone |
| [Flutter](flutter/WORKFLOW.md) | Clipped BackdropFilter, BackdropKey, Impeller-gated ImageFilter.shader | L1 baseline; L2 conditional |
| [Unity 6 URP](unity-urp/WORKFLOW.md) | Full Screen Pass, camera color input, injection point and UI pass | L2 candidate after scene-color displacement |
| [Unreal Engine](unreal-postprocess/WORKFLOW.md) | Post Process material and PostProcessInput0 | L2 candidate after scene-color displacement |
| [Constrained fallback](constrained-fallback/WORKFLOW.md) | Capability downgrade with stable semantic controls | L0 default; L1 if blur is verified |

## How to use a workflow

1. Match its project profile to the actual target; do not copy its assumed versions blindly.
2. Inspect the project's manifest/build settings, render graph, and minimum hardware/OS.
3. Follow the strategy decision and verify the documented source texture/backdrop boundary.
4. Run the workflow's validation checklist against the target project.
5. Record the demonstrated tier, tested environment, and any unsupported branches.

The Skill package tests assert that each workflow exists and contains validation/tier guidance. They are documentation/decision regression tests; they do not compile Swift, QML, Unity, Unreal, or a Flutter app. Target application builds and visual captures remain explicit work in Phase 5.


## Runnable implementation demos

- [WebGL2 L2/L3 reference implementation](../../../../examples/webgl2/README.md) — app-owned scene texture, true sample displacement, semantic HTML controls, desktop/mobile browser capture.
- [Android Java/GLES2 L2/L3 reference app](../../../../examples/android-gles/README.md) — app-owned framebuffer, native Android controls, emulator build and capture.
