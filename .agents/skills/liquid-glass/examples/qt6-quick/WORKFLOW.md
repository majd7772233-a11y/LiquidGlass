# Worked workflow: Qt 6 Quick / QML

**Purpose:** check the selected Qt RHI backend, ShaderEffect asset pipeline, and render-thread integration boundary.

## Project profile to record

- Exact Qt 6 minor/patch version and Qt Quick modules.
- QPA platform, selected RHI backend, and whether a software adaptation is permitted.
- Existing QML scene graph, custom QQuickItem, and supplied textures.
- Threading and render-resource ownership.

## Strategy decision

- QML ShaderEffect applies a vertex/fragment shader to a rectangle. Qt 6 shaders are packaged as .qsb assets through the shader tools pipeline.
- The software scene graph does not render ShaderEffect. Check the actual renderer/backend before enabling it.
- For true backdrop displacement, explicitly supply a texture from the app-owned scene or use a justified QRhi/QSGRenderNode integration. The scene graph does not expose a general public property that automatically gives a ShaderEffect all pixels behind its item.
- QSGRenderNode/native graphics work must obey Qt's render-thread and external-command rules. Do not manipulate render resources from arbitrary GUI-thread callbacks.

## Example material boundary

Use ShaderEffect only when its texture/uniform inputs are explicit and the selected backend supports it. Treat a shader applied to an isolated rectangle with no sampled backdrop as a material/highlight example, not refraction.

## Reproducible validation

1. Build the QML module and .qsb shader with the project's configured Qt Shader Tools.
2. Run with qt.scenegraph.general and qt.rhi logging enabled; record the selected backend.
3. Confirm the software backend fallback if it is in the support range.
4. For L2, demonstrate a scene-owned background texture being displaced through the mask.
5. Test resize, DPR, render-thread synchronization, resource teardown, keyboard focus, accessibility, and reduced motion.

**Expected baseline:** a ShaderEffect alone does not establish L2. The actual backdrop texture and the selected backend must be validated.

## Official references

- Qt Quick ShaderEffect: https://doc.qt.io/qt-6/qml-qtquick-shadereffect.html
- Qt Quick Scene Graph: https://doc.qt.io/qt-6/qtquick-visualcanvas-scenegraph.html
- Qt Scene Graph Adaptations: https://doc.qt.io/qt-6/qtquick-visualcanvas-adaptations.html
