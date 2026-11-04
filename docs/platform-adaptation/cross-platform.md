# Cross-Platform UI Frameworks

Cross-platform does not mean one rendering capability on every backend. Compare the concrete engine/backend used on each target before choosing a strategy.

## Flutter

Flutter BackdropFilter applies an ImageFilter to previously painted content within its parent/ancestor clip. It can be expensive, especially for non-local filters such as blur. Flutter documents BackdropGroup/BackdropKey as a way to combine compatible filters, with care around overlapping filters.

Flutter also supports custom fragment shaders through FragmentProgram. Flutter's fragment-shader guide states that shader-backed ImageFilter usage is supported by the Impeller backend; do not assume it works identically on every renderer. Verify the actual Skia/Impeller backend and platform-view composition in the app.

Recommended route:
- Use ClipRRect/ClipPath + BackdropFilter for an L1 surface.
- Consider ImageFilter.shader for a shader-based effect only after confirming Impeller and testing the actual rendered backdrop input.
- For L2, prove that the shader displaces existing painted backdrop content, not merely the child widget.
- Share BackdropKey only for filters that truly share the same source and do not overlap in a way that changes appearance.
- Keep buttons and labels as normal semantic Flutter widgets above the optical layer.

## Qt Quick

Qt Quick is also cross-platform, and its RHI translates rendering to the selected graphics API. ShaderEffect uses packaged .qsb shader files. The software backend does not render ShaderEffect, and custom scene-graph rendering has thread/lifecycle rules.

Use Qt's ShaderEffect for material drawing where the shader inputs are explicitly supplied. For true scene-color displacement, inspect QRhi/QSGRenderNode or an app-owned texture pipeline. Do not assume the shader can sample arbitrary siblings by magic.

## Other cross-platform frameworks

For Compose Multiplatform, React Native, MAUI, Avalonia, or similar frameworks:
1. Inspect the concrete renderer for each OS.
2. Identify whether a visual effect is native, rasterized, or emulated.
3. Confirm backdrop source and clipping behavior on each backend separately.
4. Keep semantic controls in the framework's accessibility layer.
5. Define per-platform quality tiers; do not force the highest common implementation across all devices if it degrades platform-native quality.

## Validation workflow

- Record framework version and backend/renderer for each OS.
- Test the blur/shader on every supported backend, including software or low-GPU fallback if supported.
- Confirm clip/mask, scrolling, overlap, and render order.
- Test platform views, native embedding, focus, semantics, text scaling, and reduced motion.
- Report a capability table per backend; a Flutter or Qt API available on one backend is not proof that it is available on every backend.

## Official references

- [Flutter BackdropFilter](https://api.flutter.dev/flutter/widgets/BackdropFilter-class.html)
- [Flutter fragment shaders](https://docs.flutter.dev/ui/design/graphics/fragment-shaders)
- [Qt Quick ShaderEffect](https://doc.qt.io/qt-6/qml-qtquick-shadereffect.html)
- [Qt Quick Scene Graph](https://doc.qt.io/qt-6/qtquick-visualcanvas-scenegraph.html)
