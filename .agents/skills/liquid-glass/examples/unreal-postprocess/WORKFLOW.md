# Worked workflow: Unreal Engine Post Process Material

**Purpose:** verify scene-color access and post-process placement without assuming UMG is part of the sampled scene texture.

## Project profile to record

- Exact Unreal Engine minor version, renderer, platform RHI, and forward/deferred path.
- Post Process Volume settings and blendable location/priority.
- Camera and scene capture/render-target use.
- UMG/Slate widget composition and whether it renders before or after the selected pass.

## Strategy decision

Use a Post Process Material with Post Process material domain when the effect needs scene color. Epic documents sampling through SceneTexture and PostProcessInput0, plus optional user scene textures for intermediate data. The post-process graph is ordered; verify the actual input at the selected location.

For an L2 lens, sample neighboring positions in the scene color using a bounded displacement field and shape mask. If the semantic UI is rendered outside that scene-color input, keep the optical effect in the scene and place UMG/Slate semantic controls above or in a separately controlled UI pass.

## Minimal implementation plan

- Create a post-process material and choose an appropriate Blendable Location.
- Sample PostProcessInput0, not an assumed generic framebuffer.
- Add a lens mask and clamp all neighbor UV samples to the valid texture region.
- If required, use a User Scene Texture as an explicit intermediate.
- Keep focus, input, and labels in UMG/Slate.

## Reproducible validation

1. Build/package or launch the project using its exact engine version and renderer settings.
2. Confirm which scene color is supplied at the selected post-process location.
3. Verify a high-contrast scene feature visibly moves through the mask.
4. Confirm whether UMG is included; if not, record the separate widget composition strategy.
5. Test temporal anti-aliasing, resolution scale, multiple cameras, mobile/desktop RHI, and performance.
6. Test keyboard/gamepad focus and accessible state.

**Expected tier:** L2 only when scene-color displacement is proven; L3 additionally requires coherent dynamic contour and optical response.

## Official reference

- Unreal Engine Post Process Materials: https://dev.epicgames.com/documentation/unreal-engine/post-process-materials-in-unreal-engine
