# Desktop UI and Native Compositors

Desktop is not one renderer. Detect the concrete UI framework and compositor, then inspect the boundary between application visuals, window composition, and GPU resources.

## Windows App SDK / WinUI Composition

Microsoft.UI.Composition supports real-time effects with animatable properties. The documented effect-brush workflow paints SpriteVisuals from existing images/surfaces. Composition effects can reference existing surfaces or textures, but the documentation explicitly says they cannot use the output of other composition trees as an effect source.

Recommended routing:
- Use native Composition effect brushes for supported image effects and animatable properties.
- Keep XAML controls semantic and use XamlCompositionBrushBase where a Composition brush must appear on a XAML element.
- For custom L2 refraction, provide an app-owned surface/texture or a Direct3D/Win2D render target. Do not assume Composition can sample every sibling visual or another window.
- Respect visual bounds, z-order, clipping, and input/focus ownership.

## Qt Quick on desktop or embedded Linux

Qt 6 uses the scene graph and Qt Rendering Hardware Interface (RHI) to target APIs such as OpenGL, Vulkan, Metal, and Direct3D. ShaderEffect applies a custom shader to a rectangle and expects packaged shader assets. The software scene graph backend does not render ShaderEffect.

For a simple material surface, use QML shapes and a ShaderEffect with a supplied input texture. For more complex integration, inspect QRhi and QSGRenderNode; custom render-node work is render-thread-sensitive and must obey Qt's synchronization/rendering rules.

Do not use QQuickPaintedItem as an assumed high-performance substitute for scene graph rendering. Qt documents that it uses an indirect 2D surface and a two-step operation.

## Other desktop frameworks

For WPF, WinForms, Avalonia, GTK, Electron, or another stack, do not copy WinUI or Qt assumptions. Find the framework's actual backdrop/compositor API and determine whether it exposes pixels, only a blur/material, or no backdrop at all. If the application already owns a Direct3D/Vulkan/Metal/Skia scene, integrating there may be better than trying to capture the native window tree.

## Validation workflow

- Record framework/version, deployment/OS floor, GPU backend, DPI scale, and monitor count.
- Inspect visual-tree/window composition and whether the required background is in the same render tree.
- Test resize, multi-monitor DPI, window transparency, z-order, occlusion, minimize/restore, and device loss.
- Check keyboard navigation, UI Automation or framework semantics, high contrast, and reduced motion.
- Use a high-contrast line/grid backdrop to prove displacement. A blur effect is L1; a ShaderEffect or Composition effect graph is not automatically L2.

## Official references

- [Microsoft WinUI Composition effects](https://learn.microsoft.com/en-us/windows/apps/develop/composition/composition-effects)
- [Qt Quick ShaderEffect](https://doc.qt.io/qt-6/qml-qtquick-shadereffect.html)
- [Qt Quick Scene Graph](https://doc.qt.io/qt-6/qtquick-visualcanvas-scenegraph.html)
- [Qt Scene Graph Adaptations](https://doc.qt.io/qt-6/qtquick-visualcanvas-adaptations.html)
