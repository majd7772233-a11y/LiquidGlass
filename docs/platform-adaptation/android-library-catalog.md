# Android dependency and renderer catalog

**Research snapshot: 2026-11-04.** Versions and release tags below were checked against upstream project documentation/repositories on this date. Recheck them during implementation. A dependency can simplify a visual treatment, but it does not automatically provide arbitrary backdrop access or real refraction.

## Shortlist

| Candidate | Best fit | Verified baseline / version | What it contributes | Important limit |
|---|---|---|---|---|
| [Dimezis BlurView](https://github.com/Dimezis/BlurView) | Native Views / Java / Kotlin / XML | JitPack tag \`version-4.0.0\`; module minSdk 18 | Live blur of a configured View target; API-specific blur route | L1 blur only; SurfaceView sources unsupported; TextureView only API 31+; Java 11 compatibility check |
| [Haze](https://chrisbanes.github.io/haze/latest/) | Existing Jetpack Compose project | 2.1.0, published 2026-11-02; Android API 23+ | Separate blur/Glass modules; optical Glass, edge lighting, chromatic effects, interactions, connected surfaces | Fallback renderer omits refraction/blur; API 30 and below blur is experimental RenderScript and off by default |
| [miuix-blur](https://github.com/compose-miuix-ui/miuix/blob/main/docs/guide/blur.md) | Compose shader blur/blend/noise/highlight | Android API 33+ | Third-party RuntimeShader-backed visual effects | Not a fallback below API 33; still needs correct source inputs |
| [Rive Android](https://github.com/rive-app/rive-android) | Authored vector motion for controls, blobs, highlights | Runtime documents minSdk 21 | Designer-authored stateful vector animations and interaction | Motion only: no live backdrop blur/capture/refraction |
| [RealtimeBlurView](https://github.com/mmin18/RealtimeBlurView) | Existing legacy View app only | 1.2.1; sample minSdk 15 | Old real-time blur overlay | Old release history (2019); per-draw blur can hurt scrolling; not recommended for new work |
| [OpenGL ES](https://developer.android.com/develop/ui/views/graphics/opengl/about-opengl) | Custom renderer / app-owned scene needing custom shader math below API 33 | Device/runtime GLES support | GLSL route for distortion, lighting, masks, geometry | Requires explicit source texture; does not sample unrelated Views or protected surfaces automatically |

## Dependency coordinates and constraints

### Dimezis BlurView — Views/XML

The verified JitPack tag is \`version-4.0.0\`:

\`\`\`kotlin
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
        maven(url = "https://jitpack.io")
    }
}
\`\`\`

\`\`\`kotlin
dependencies {
    implementation("com.github.Dimezis:BlurView:version-4.0.0")
}
\`\`\`

The tagged library Gradle file declares minSdk 18, Java source/target compatibility 11, and compileSdk 36. Its documented blur routes are API 31+ RenderEffect, API 29–30 OpenGL, and RenderScript below API 29. Its README uses BlurTarget around source content; children in BlurView remain sharp above the blur.

Do not use it for SurfaceView-based video/maps/GL sources. Upstream states TextureView blur is supported only on API 31+. BlurView is L1 blur, not refraction. Check Java 11 bytecode and the project's AGP/D8/JDK compatibility, especially in old Java 8 / legacy Gradle projects.

### Haze — Jetpack Compose

Haze 2.1.0 was published on 2026-11-02. The modular artifacts are:

\`\`\`kotlin
dependencies {
    implementation("dev.chrisbanes.haze:haze:2.1.0")
    implementation("dev.chrisbanes.haze:haze-glass:2.1.0")
    // Or blur-only:
    // implementation("dev.chrisbanes.haze:haze-blur:2.1.0")
}
\`\`\`

Use \`haze-glass-material3\` only if Material 3 theme integration is needed. Keep all Haze modules on the same version. Haze documents Android API 23+ support.

- Glass can provide refraction, depth blur, tint, Fresnel/ambient edge response, specular highlights, optional dispersion, interaction response, and connected Glass containers.
- Glass fallback rendering preserves tint/shape and approximates edge/highlight appearance but omits refraction, blur, and other advanced optical adjustments. Check the active renderer and classify the demonstrated tier.
- Haze Blur is enabled by default on API 31+. API 31/32 have progressive-effect/redraw caveats. On API 30 and below blur is disabled by default; optional RenderScript is experimental, slower, and can lag while content moves.
- Haze's native window-backdrop integration is a separate experimental Android 37.2 / API 37 QPR2 path. Do not confuse this with API-33 RuntimeShader or assume it exists on Android 13. It is window-scoped and has restrictions/fallbacks.

Resolve Maven metadata and compare Kotlin, Compose, Gradle, AGP, AndroidX, and transitive dependencies before bringing Haze into an existing application. Do not migrate Views/XML to Compose without user approval.

### miuix-blur — Compose, API 33+

Upstream coordinate pattern:

\`\`\`kotlin
dependencies {
    implementation("top.yukonga.miuix.kmp:miuix-blur-android:<version>")
}
\`\`\`

Its Android blur/blend/noise/highlight effects rely on RuntimeShader and require API 33+. Its guide documents capability helpers such as \`isRenderEffectSupported()\` and \`isRuntimeShaderSupported()\` for guarded calls when the app has a lower minSdk. Verify current setup instructions and runtime checks. It is not an old-device replacement.

### Rive — motion layer, not glass

Rive's Android runtime documents minSdk 21. It is useful for authored, interactive vector states such as animated blobs, moving highlights, and expressive buttons. Keep a real semantic control for input/accessibility. Rive does not provide backdrop pixels, blur, or refraction; check current artifact and license before adding it.

### RealtimeBlurView — legacy comparison only

The upstream README documents version 1.2.1 and sample minSdk 15, but its last listed release is from 2019. Its performance notes describe blur work on window draws and warn about multiple instances in lists. It does not support SurfaceView/TextureView sources. Prefer a maintained framework-appropriate option; consider it only for an old application after profiling.

## Custom OpenGL ES path below API 33

For L2 displacement on API 18–32, OpenGL ES is a legitimate alternative to AGSL when the app owns and supplies the rendered source as a texture. Use an existing engine/renderer or a deliberate GLSurfaceView.Renderer / TextureView path. Validate GLES version/driver, source freshness, composition order, texture format/color space, masks, clipping, lifecycle, and GPU budget.

Do not replace a complete View hierarchy just to refract one card. Capturing Views into bitmaps or using PixelCopy is asynchronous/expensive and introduces synchronization, memory, and protected-content constraints. If the app cannot provide a valid source texture, select L0/L1 rather than claiming L2.

## Selection rules for Codex

1. Detect Views/XML versus Compose. Do not add Compose to a View project just to gain a library.
2. Read effective minSdk/toolchain and inspect dependency versions, transitive requirements, and licenses. A dependency must not force minSdk upward without explicit user approval.
3. Prefer BlurView for View/XML L1 when API 18+ and toolchain requirements are met. Prefer Haze for an existing Compose app when its toolchain is compatible and its full/fallback behavior fits the request.
4. Use miuix-blur only for API-33 shader paths, Rive only for authored animation, and custom GLES only when the source texture is owned and refraction justifies the renderer cost.
5. Do not combine blur libraries by default. Do not add a dependency for tint/border/gradient/highlight that a small drawable/Canvas primitive can provide.
6. Recheck current documentation and dependency metadata at implementation time. This is a maintained shortlist, not a command to use stale versions.

## Upstream references

- [BlurView README and releases](https://github.com/Dimezis/BlurView)
- [BlurView 4.0.0 Gradle configuration](https://github.com/Dimezis/BlurView/blob/version-4.0.0/library/build.gradle)
- [Haze 2.1.0 changelog](https://github.com/chrisbanes/haze/blob/main/CHANGELOG.md)
- [Haze documentation](https://chrisbanes.github.io/haze/latest/)
- [Haze Android behavior](https://chrisbanes.github.io/haze/latest/blur/platforms/)
- [Haze Glass behavior/fallback](https://chrisbanes.github.io/haze/latest/effects/glass/)
- [miuix-blur compatibility](https://github.com/compose-miuix-ui/miuix/blob/main/docs/guide/blur.md)
- [Rive Android runtime](https://github.com/rive-app/rive-android)
- [RealtimeBlurView README](https://github.com/mmin18/RealtimeBlurView)
- [Android OpenGL ES](https://developer.android.com/develop/ui/views/graphics/opengl/about-opengl)
- [Android PixelCopy](https://developer.android.com/reference/android/view/PixelCopy)
