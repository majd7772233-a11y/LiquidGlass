# Native Android UI

This guide covers Java/Kotlin, Android Views/XML, Jetpack Compose, Canvas, RenderNode, and app-owned GPU rendering. Preserve the project's existing UI framework; do not prescribe Compose for a Views app.

## Mandatory compatibility workflow

### 1. Inspect the actual Android project

Resolve the effective \`minSdk\` for the exact app module and build variant, including Gradle convention plugins, version catalogs, product flavors, and manifest placeholders. Also inspect \`compileSdk\`, \`targetSdk\`, Android Gradle Plugin, Gradle wrapper, JDK, Java/Kotlin bytecode targets, existing dependency versions/repositories, and whether the UI uses Views/XML or Compose.

Inspect the actual device's runtime API (\`Build.VERSION.SDK_INT\`) separately from the app's minSdk. These values are not interchangeable: minSdk is the install floor; runtime API decides which branch this device can execute; compileSdk controls the APIs available at compile time; targetSdk controls compatibility behavior. An app with minSdk 23 can use a guarded API-33 branch on a device running Android 13+, while older supported devices continue on a compatible route.

Identify whether the backdrop is normal app-owned View/Compose content, a bitmap/texture, TextureView, SurfaceView, video, or another separately composed surface. Inspect the current dependency graph, library minSdk, transitive dependencies, licenses, Kotlin/Compose/AGP/JDK requirements, and repository availability before adding a dependency.

### 2. Preserve the user-selected minimum

- **Existing project:** preserve its current effective minSdk. Never raise it to 31 or 33 solely to use RenderEffect or RuntimeShader. Implement runtime-gated higher-quality paths with tested fallbacks for every older API still supported by the app.
- **New project with an explicit minSdk:** follow the user's value exactly. Find compatible alternatives rather than overriding their choice.
- **New project without a specified minSdk:** before writing a minSdk into Gradle, explain the API-33 RuntimeShader/AGSL capability and the compatibility/performance trade-off of older Android support. Ask which minimum Android version/device range the user wants. Do not silently choose 33, or silently choose a lower value.

### 3. Runtime decision matrix

| Device API at runtime | Available native path | Guidance |
|---|---|---|
| 33+ (Android 13+) | RuntimeShader / AGSL | Use AGSL when it fits the project's renderer and has a valid shader input. A shader does not automatically capture unrelated Views, another window, or protected video. |
| 31–32 (Android 12/12L) | RenderEffect | Use for blur/effects on available rendered content. RuntimeShader is not available. Blur is L1, not refraction. Use an owned texture/custom renderer for real displacement or downgrade honestly. |
| 29–30 (Android 10/11) | No RenderEffect or RuntimeShader | View/XML BlurView can take its OpenGL blur route. Custom OpenGL ES can provide shader math when the app owns the source texture. |
| 23–28 | No RenderEffect or RuntimeShader | View/XML BlurView uses its legacy RenderScript blur path. Compose Haze supports API 23+, but its legacy blur path below API 31 is experimental/RenderScript-backed and can be slow or lag during motion. Prefer L0 when that cost is unacceptable. |
| 18–22 | No RenderEffect or RuntimeShader | BlurView's RenderScript route may be considered for View/XML after profiling; otherwise use a stable L0 drawable/Canvas fallback. |
| Below API 18 | No verified BlurView 4.0.0 support | Use a native L0 fallback or separately verify a legacy dependency. |

Use explicit runtime checks before referencing newer APIs, e.g. \`Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU\`. Isolate newer API references where needed so old devices do not load/call unavailable classes. Build success against a new compileSdk is not proof that the app is safe on old devices.

## Native capabilities and their limits

### RenderEffect — API 31+

RenderEffect can apply effects such as blur to rendered content. It is not the programmable AGSL RuntimeShader API, and it does not grant automatic access to arbitrary pixels behind an unrelated View.

### RuntimeShader / AGSL — API 33+

RuntimeShader was added in API 33 and accepts AGSL source. It can customize drawing/filtering only using inputs bound to its shader pipeline. It does not create a backdrop source. For L2 refraction, first provide the correct app-owned or explicitly captured texture, then displace its samples inside a stable shape mask.

### OpenGL ES — an alternative below API 33

OpenGL ES is independent of AGSL and can run GLSL shaders on older Android devices that support the required GLES version. Use an existing app renderer or a deliberate GLSurfaceView/GLSurfaceView.Renderer or TextureView route. It can implement custom distortion below API 33 **only if the app can supply the source texture**. It does not automatically sample arbitrary View hierarchies, windows, SurfaceView/video, or secure content. Capturing a normal View tree into a synchronized texture while retaining z-order, clipping, lifecycle, and crisp semantic foreground controls requires additional engineering. Check real device GLES support/driver behavior.

### Backdrop capture

Prefer a texture or scene the app already owns. PixelCopy is asynchronous; it is not permission to recapture the entire screen every frame. A throttled snapshot or View.draw() bitmap can be a constrained route for app-owned content but has synchronization, memory, and performance costs. Respect secure/protected content and Surface composition boundaries. A shader cannot sample pixels that were never supplied to it.

## Third-party choices by UI framework

### Views / Java / Kotlin / XML — BlurView

For L1 backdrop blur in a View hierarchy below API 33, evaluate **Dimezis BlurView** before writing a custom capture pipeline. The verified JitPack tag \`version-4.0.0\` declares minSdk 18 and selects RenderEffect for API 31+, OpenGL for API 29–30, and RenderScript below API 29. It uses a BlurTarget/BlurView relationship in the view hierarchy. It provides blur, not refraction.

Limits to check:
- SurfaceView-based sources such as VideoView, MapFragment, and GLSurfaceView cannot be blurred by BlurView. TextureView blur is documented only on API 31+.
- RenderScript is deprecated; measure its legacy route on the actual low-end device.
- BlurView 4.0.0 is built with Java 11 and minSdk 18. Check the host project's AGP/D8/JDK compatibility, especially older Java 8 or legacy Gradle projects.

If unsuitable, use L0 layered drawables/Canvas or a bounded app-owned bitmap/GLES path only when its source and cost are justified.

### Jetpack Compose — Haze

Evaluate **Haze 2.1.0** when the project already uses Compose. Use the \`haze\` plus \`haze-glass\` modules for Glass, or \`haze-blur\` for blur-only work; keep module versions aligned. Haze documents Android API 23+ support.

Haze Glass can provide refraction, depth blur, tint, edge response, specular lighting, chromatic effects, interaction response, and connected Glass containers when its full renderer is available. Its fallback renderer deliberately drops refraction and blur, preserving tint/shape and approximating edges/highlights. Verify the actual renderer and report the actual tier rather than the dependency's advertised feature list.

Haze Blur is enabled by default on API 31+. API 31/32 have progressive-effect/redraw performance caveats. On API 30 and below, blur is disabled by default; the optional RenderScript path is experimental, slower, and can lag during moving content. Haze's optional native window-backdrop integration is a separate experimental Android 37.2 / API 37 QPR2 path; do not confuse it with API-33 RuntimeShader or assume it exists on Android 13. It is window-scoped and has documented restrictions/fallbacks.

Haze 2.1.0 was published 2026-11-02. Check its current Kotlin, Compose, Gradle, and AndroidX requirements before introducing it or upgrading a project's toolchain. Do not migrate Java/XML to Compose solely to get Haze without user approval.

### Other candidates

See [Android dependency and renderer catalog](android-library-catalog.md) for versions, coordinates, and limitations:
- **miuix-blur**: Compose shader blur/blend/noise/highlight effects requiring API 33+; not an old-device fallback.
- **Rive Android**: authored interactive vector motion for animated blobs/highlights (minSdk 21 in its runtime documentation); not a blur or refraction engine.
- **RealtimeBlurView**: legacy comparison only; old release history and per-draw blur costs make it unsuitable as the default for new work.

Do not add several blur libraries together by default. Select a single solution that fits the actual project, behavior, baseline, and build stack.

## Integration, failure handling, and validation

1. Preserve the current UI framework and semantic controls. Keep text/icons crisp and outside the distortion layer.
2. Isolate shader/capture resources from Activity/Composable lifecycle; release on detach and cancel asynchronous work.
3. Use one coordinate space and consistent masks for backdrop sampling/composition; bound displacement and prevent edge leaks.
4. Avoid full-screen capture every frame, unbounded shader work, per-frame allocations, and excessive simultaneous blur surfaces.
5. Test dependency licensing, resolution, minSdk, transitive requirements, and toolchain compatibility before adoption.
6. Test every runtime branch in the app's supported range: API 29–30, 31–32, 33+, and lower API 18/23 where relevant to the chosen dependency.
7. Record effective minSdk, compileSdk, targetSdk, AGP/JDK/Kotlin/Compose/GLES versions, runtime API, dependency version, and active renderer.
8. Use a high-contrast line/grid behind the lens to prove sample displacement before claiming L2. Blur alone is L1.
9. Verify SurfaceView/TextureView behavior, touch/focus, TalkBack, reduced motion/transparency, density/orientation, resource release, scrolling performance, and lower-end hardware.
10. For Haze Glass, inspect both the full renderer and old-API fallback. Library install compatibility is not proof that all visual effects run on that API.

## References

- [Android RenderEffect](https://developer.android.com/reference/android/graphics/RenderEffect)
- [Android RuntimeShader](https://developer.android.com/reference/android/graphics/RuntimeShader)
- [Android AGSL](https://developer.android.com/develop/ui/views/graphics/agsl)
- [Android OpenGL ES overview](https://developer.android.com/develop/ui/views/graphics/opengl/about-opengl)
- [Android OpenGL ES environment](https://developer.android.com/develop/ui/views/graphics/opengl/environment)
- [Android PixelCopy](https://developer.android.com/reference/android/view/PixelCopy)
- [Dimezis BlurView](https://github.com/Dimezis/BlurView)
- [Haze documentation](https://chrisbanes.github.io/haze/latest/)
- [Haze Android platform behavior](https://chrisbanes.github.io/haze/latest/blur/platforms/)
- [Haze Glass effect](https://chrisbanes.github.io/haze/latest/effects/glass/)
- [miuix-blur](https://github.com/compose-miuix-ui/miuix/blob/main/docs/guide/blur.md)
- [Rive Android runtime](https://github.com/rive-app/rive-android)
- [RealtimeBlurView](https://github.com/mmin18/RealtimeBlurView)
