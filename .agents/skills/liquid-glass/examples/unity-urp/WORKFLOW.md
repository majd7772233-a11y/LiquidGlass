# Worked workflow: Unity 6 URP

**Purpose:** use an explicit camera-color input and renderer injection point, not an assumed global screen grab.

## Project profile to record

- Unity Editor and Universal RP package versions.
- Renderer asset, Render Graph setting, camera stack, injection order, and post-processing settings.
- Graphics API, target device/GPU, render scale, dynamic resolution, and Canvas render mode.

## Strategy decision

Use the URP Full Screen Pass Renderer Feature when the effect belongs in the camera render pipeline. Select the Color requirement when the pass needs the camera color texture; Unity documents the shader input as _BlitTexture. Add Depth/Normal/Motion requirements only if the design needs them because extra passes can cost performance.

Use a mask and bounded texture-coordinate displacement to create an L2 scene-color lens. Keep UI controls in a layer whose render order is deliberate; a Canvas rendered later is not automatically in the sampled camera texture.

## Minimal implementation plan

- Add one Full Screen Pass at the chosen injection point.
- Provide a material or Shader Graph fullscreen shader.
- Bind a shape mask and lens parameters; clamp sample offsets and edge reads.
- Keep text/icons and EventSystem hit targets in the UI layer.
- Add a non-shader fallback for unsupported devices.

## Reproducible validation

1. Open the project in its actual Unity/URP versions and build for the target platform.
2. Verify the selected pass sees the intended camera color at the chosen injection point.
3. Move a high-contrast grid behind the lens and verify geometric displacement inside the mask.
4. Test camera stacks, multiple cameras, UI render mode, render scale, MSAA/TAA/upscaling, and resize.
5. Profile full-screen cost, overdraw, and multiple surfaces.
6. Test keyboard/controller navigation and any project accessibility layer.

**Expected tier:** L2 only if the camera-color texture is displaced; L3 only when the moving shape/mask/light state stays coherent. A simple screen tint or blur is not L2.

## Official reference

- Unity 6 URP Full Screen Pass Renderer Feature: https://docs.unity.com/en-us/engine/6000.6/manual/post-processing-and-full-screen-effects/urp/custom-post-processing/renderer-feature-full-screen-pass
