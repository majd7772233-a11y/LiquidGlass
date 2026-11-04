# Game Engines: Unity and Unreal Engine

Game engines usually provide more direct access to scene color than native application UI frameworks because they own a camera/render pipeline. That access is still bounded by render-pass ordering, camera stacks, UI layers, and selected renderer.

## Unity 6 URP

The URP Full Screen Pass Renderer Feature injects a full-screen pass at a selected point. Selecting Color provides a camera color texture to the shader (documented as _BlitTexture in the renderer feature workflow). Depth/normal/motion requirements can introduce extra work and should be enabled only when needed.

Recommended route:
1. Check the actual Unity Editor version, URP package, renderer asset, Render Graph configuration, graphics API, camera stack, and target hardware.
2. Add a Full Screen Pass at the correct injection point and request Color only when the shader needs scene color.
3. Sample the supplied scene texture with a shape mask and bounded screen-space displacement.
4. Keep the final control geometry and semantic UI as a separate, correctly ordered UI layer if that layer is not present in the sampled camera color.
5. Profile pass cost and verify the effect with multiple cameras and resolutions.

A full-screen scene effect does not automatically imply that a Canvas rendered in a later UI pass is included. Choose the injection point deliberately. For local lens effects, restrict the pass with a mask/region where the pipeline permits; avoid running unnecessary full-resolution work over the whole screen.

## Unreal Engine 5.x

Unreal Post Process Materials use the Post Process material domain and can sample SceneTexture inputs such as PostProcessInput0. Epic documents post-process materials as part of the post-processing graph and recommends using built-in Post Process Volume controls where possible for common optimized effects.

Recommended route:
1. Verify the exact UE minor version, forward/deferred renderer, platform RHI, post-process graph location, and UI composition order.
2. Implement a Post Process Material only when the scene-color sampling is required.
3. Use bounded neighboring samples around the lens UV, a shape mask, and a controlled displacement field. Use a User Scene Texture if an intermediate target is genuinely needed.
4. Confirm whether UMG/Slate is rendered before or after the chosen pass; do not assume a post-process material samples widget pixels.
5. Keep controls in UMG/Slate with focus/navigation/accessibility independent of the material.

## Shared game-engine rules

- Keep screen-space coordinates consistent across viewport resize, dynamic resolution, camera stacking, and render scale.
- Test MSAA/TAA/upscaling and temporal stability at lens edges.
- Prefer one pass and a reusable mask over multiple full-screen passes.
- Clamp displacement and guard edge samples to avoid texture wrap/bleed.
- Use lower-resolution intermediate targets only after confirming edge quality.
- Profile on the slowest target hardware and report the exact pipeline and render scale.

## Validation workflow

- A scene-color sample must demonstrably move a high-contrast feature beneath the lens.
- Test whether the UI layer is included in the sampled pass; record the actual render order.
- Test multiple cameras, resolutions, dynamic resolution, render scale, and UI composition.
- Check gamepad/keyboard navigation and accessible nonvisual state through the game's UI layer.
- Report L2 only when real scene pixels are displaced inside the surface mask. Report L3 only when shape deformation and optical response remain coherent through morphing.

## Official references

- [Unity 6 URP Full Screen Pass Renderer Feature](https://docs.unity.com/en-us/engine/6000.6/manual/post-processing-and-full-screen-effects/urp/custom-post-processing/renderer-feature-full-screen-pass)
- [Unreal Engine Post Process Materials](https://dev.epicgames.com/documentation/unreal-engine/post-process-materials-in-unreal-engine)
