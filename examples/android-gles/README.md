# Android Java / OpenGL ES 2.0 Liquid Glass demo

A standalone Android Views/Java reference app. It owns and renders the backdrop in an OpenGL ES framebuffer, then samples/displaces that texture inside a rounded lens mask. Native Android TextViews, Buttons and SeekBar controls stay above the shader and preserve platform semantics.

## Requirements

- Android Studio or Android SDK command-line tools.
- JDK 17.
- Gradle 8.7 (Android Gradle Plugin 8.6.1).
- An Android device/emulator with OpenGL ES 2.0.
- Standalone example baseline: minSdk 23, compileSdk 35, targetSdk 35.

The minSdk 23 choice applies only to this new sample application. It does not prescribe a new minimum for any existing app. The sample deliberately uses GLES2 rather than API-33 RuntimeShader so its custom scene-texture path can run on a broader Android range. It still requires a working GLES2 framebuffer implementation.

## Build and install

Open `examples/android-gles/` as an Android Studio project, or run:

```bash
gradle :app:assembleDebug
adb install -r app/build/outputs/apk/debug/app-debug.apk
adb shell am start -n org.liquidglass.reference.debug/org.liquidglass.reference.MainActivity
```

The emulator/CI workflow builds the APK, validates native accessibility node names and target dimensions through UIAutomator, captures the primary L3 state, changes logical size/density and rotates to landscape, then launches a four-surface SDF workload. Before capture it verifies that the Liquid Glass Activity is resumed, focused, laid out, and present in UIAutomator's accessibility hierarchy; it rejects splash/launcher screenshots. A separate profile window preserves frame timing, memory, display, battery, thermal, and SurfaceFlinger diagnostics.

## Demonstrated behavior

- **L2 — refractive glass:** a procedural high-contrast scene is rendered into an application-owned RGBA framebuffer texture. A fragment shader samples offset texels based on the rounded surface's signed-distance gradient.
- **L3 — dynamic liquid glass:** the “Connect lens” button expands a secondary lobe using a smooth-union distance function. The same shape field drives the refraction mask and edge lighting.
- **Native semantics:** the title, buttons, and strength SeekBar are ordinary Android Views with accessible descriptions and system focus/touch behavior. Action buttons are 48 dp high and the SeekBar layout is 48 dp high.
- **Accessibility settings:** high-text-contrast is read from the `Settings.Secure` `high_text_contrast_enabled` flag, preserving the sample's API 23 compatibility. Reduced animation follows the system animator scale / ValueAnimator setting. The Activity follows the device orientation rather than forcing portrait.
- **Demand-driven rendering:** GLSurfaceView uses RENDERMODE_WHEN_DIRTY; an activity-owned 16 ms frame pump is active only during playback or a settling morph and is removed while paused.
- **Multiple surfaces:** the optional `extra_surfaces` launch extra adds up to three independent refractive circular SDF regions to the main lens. They share the app-owned scene texture and one glass draw pass; they are a shader stress mode, not three additional Android View controls.
- **Fallback:** if the scene framebuffer is incomplete, the renderer reports L0 and draws a tinted/highlighted lens without claiming refraction. GLES2 itself is a declared required device feature.

## Renderer boundaries

The shader samples only the generated scene texture owned by this app. It does not sample arbitrary Android View hierarchies, another window, protected content, SurfaceView video, or device screenshots. The TextView/Button/SeekBar controls are intentionally composited above the material and are not distorted.

The sample is an analytical reference, not a physical-optics simulation. It uses SDF-gradient normals, bounded sample displacement, a procedural backdrop, and approximate Fresnel/specular terms. No production visual-parity or measured-device-performance claim is made.

## Validation checklist

- Build the debug APK with the documented JDK/Gradle/SDK combination.
- On the API 35 emulator, confirm `GL_READY tier=L3 renderer=GLES2_APP_OWNED_FBO` and the GL vendor/renderer diagnostic.
- Verify TalkBack-facing content descriptions and 48 dp action hit regions using the uploaded accessibility report.
- Inspect default, 720 × 1280 / 320 dpi, and 1280 × 720 landscape captures; verify the UI remains usable after resizing and orientation changes.
- Run the `extra_surfaces=3` benchmark and confirm `SURFACE_COUNT main=1 additional=3 total=4` before profiling.
- Review frame callback intervals, CPU command submission, FBO texture estimate, meminfo, gfxinfo, battery/thermal snapshots, and surface list. GPU execution time is not inferred from CPU timing.
- Test TalkBack speech, API 23+ hardware, real GPU/driver behavior, overdraw, battery delta, and sustained thermal behavior on physical devices before a production claim.
- If FBO setup fails, verify the truthful L0 fallback log and appearance rather than claiming L2.

See the [Phase 6 validation and physical-device profiling guide](../validation/README.md).
