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

The emulator/CI workflow builds the APK, launches it, waits for the GL renderer diagnostic, captures a screenshot, and uploads both as workflow artifacts.

## Demonstrated behavior

- **L2 — refractive glass:** a procedural high-contrast scene is rendered into an application-owned RGBA framebuffer texture. A fragment shader samples offset texels based on the rounded surface's signed-distance gradient.
- **L3 — dynamic liquid glass:** the “Connect lens” button expands a secondary lobe using a smooth-union distance function. The same shape field drives the refraction mask and edge lighting.
- **Native semantics:** the title, buttons, and strength SeekBar are ordinary Android Views with accessible descriptions and system focus/touch behavior.
- **Fallback:** if the scene framebuffer is incomplete, the renderer reports L0 and draws a tinted/highlighted lens without claiming refraction. GLES2 itself is a declared required device feature.

## Renderer boundaries

The shader samples only the generated scene texture owned by this app. It does not sample arbitrary Android View hierarchies, another window, protected content, SurfaceView video, or device screenshots. The TextView/Button/SeekBar controls are intentionally composited above the material and are not distorted.

The sample is an analytical reference, not a physical-optics simulation. It uses SDF-gradient normals, bounded sample displacement, a procedural backdrop, and approximate Fresnel/specular terms. No production visual-parity or measured-device-performance claim is made.

## Validation checklist

- Build the debug APK with the documented JDK/Gradle/SDK combination.
- On emulator, confirm the log contains `GL_READY tier=L3 renderer=GLES2_APP_OWNED_FBO`.
- Inspect the captured screenshot for visible grid displacement under the glass and a connected lobe when enabled.
- Toggle the morph control; adjust the refractive strength; verify buttons/SeekBar remain native and responsive.
- Test API 23+ device/runtime branches, portrait rotation, TalkBack, touch targets, contrast, and release of GL resources on pause/destroy on real hardware.
- If FBO setup fails, verify the truthful L0 fallback log and appearance rather than claiming L2.
