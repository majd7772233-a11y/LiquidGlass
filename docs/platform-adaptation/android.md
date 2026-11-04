# Native Android UI

This guide covers Java/Kotlin, Android Views/XML, Canvas, RenderNode, and app-owned GPU rendering. It does not prescribe Compose when the project is using Views.

## Capability routes

### Native blur path: L1

Android's RenderEffect API was added in API 31 and can apply effects such as blur to a rendered content node. Treat it as a blur/effect facility, not a guarantee that arbitrary content behind an unrelated View can be sampled and geometrically displaced.

Use the simplest supported native path when L1 is acceptable. Gate APIs unavailable below the project's minSdk and provide a fallback.

### Programmable drawing path: API 33+

Android's RuntimeShader is available from API 33 and evaluates an AGSL function as part of the Canvas/RenderNode drawing pipeline. AGSL can customize painting and filter View content. It does not automatically hand the shader every pixel behind the current View.

For L2, establish the source texture explicitly:
- use a scene/content representation owned by the app;
- integrate backdrop capture/rendering at a valid View/RenderNode/compositor boundary;
- verify View/Surface ordering, clipping, lifecycle, color space, and whether video/SurfaceView content is capturable;
- then use AGSL or another renderer to displace the source under a stable shape mask.

If the app does not own a safe backdrop source, do not promise L2. Use L0/L1 according to the demonstrated behavior.

## Java/XML integration guidance

1. Read Gradle minSdk, targetSdk, Java compatibility, and Android Gradle Plugin versions.
2. Locate the actual View hierarchy and the view that owns the background pixels.
3. Keep semantic controls as native Views with content descriptions, focus/pressed state, and stable touch bounds.
4. Isolate shader/capture code from the Activity lifecycle; allocate and release render resources with the owning view/window.
5. Feature-gate API 31 and API 33 paths. Do not raise minSdk solely to use one visual effect without explicit approval.
6. Test the oldest supported API/device plus a current GPU/device.

For a Java project supporting devices below API 31 or 33, the fallback must remain usable and must not depend on the missing API.

## Common failure modes

- A shader changes only the current View pixels instead of the backdrop: fix the texture/source ownership or report the feature as unavailable.
- A SurfaceView/video surface appears above/below the glass unexpectedly: verify composition order and capture limitations; do not try to fix it by increasing blur.
- API works on emulator but not on minimum hardware: add runtime capability checks and test the lowest supported device tier.
- Refraction leaks at rounded edges: use the same coordinate space and shape mask for backdrop sampling and final composite.

## Validation workflow

- Run the actual Gradle build and tests.
- Record minSdk and the runtime API level used.
- Test API <31, 31–32, and 33+ branches when they are within the product support range.
- Confirm actual displacement with a high-contrast line/grid behind the lens; blur alone is L1.
- Check touch bounds, TalkBack, keyboard/focus, reduced motion, orientation, density, and resource release.

## Official references

- [Android RenderEffect](https://developer.android.com/reference/android/graphics/RenderEffect)
- [Android RuntimeShader](https://developer.android.com/reference/android/graphics/RuntimeShader)
- [Android Graphics Shading Language (AGSL)](https://developer.android.com/develop/ui/views/graphics/agsl)
