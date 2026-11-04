# Worked workflow: native Android Java/XML project

**Purpose:** exercise platform detection and runtime-compatible renderer selection without assuming every Android release exposes the same compositor or shader facilities. The fixture is Java + XML with minSdk 23. Its baseline output is L0; dependencies below are conditional candidates, not preselected requirements.

## 1. Discovery

The automated fixture contains Gradle Android project files, AndroidManifest.xml, a Java MainActivity, an XML layout/drawable, and minSdk 23. Resolve the effective minSdk for the actual app variant. Inspect compileSdk, targetSdk, AGP, Gradle, JDK, Java/Kotlin target, current dependencies, and device runtime via \`Build.VERSION.SDK_INT\` separately. Do not infer minSdk from compileSdk or targetSdk.

## 2. Strategy decision: preserve the user's baseline

For an **existing app**, do not change minSdk to unlock API 31/33 effects. Use runtime checks so API 33+ devices can take an AGSL path while older supported devices take a compatible route. For a **new app**, obey an explicit minSdk. If the user did not supply one, explain the API-33 RuntimeShader advantage and ask for the intended Android baseline/device range before changing Gradle.

| Runtime API | View/XML candidate | Compose candidate |
|---|---|---|
| 33+ | AGSL RuntimeShader with explicit source input; BlurView if only L1 blur is needed | Haze Glass full renderer; miuix-blur for API-33 shader effects |
| 31–32 | RenderEffect or BlurView L1; custom GLES if an owned texture and real displacement are required | Haze Blur; do not assume fallback Glass has refraction |
| 29–30 | BlurView's OpenGL blur route; custom GLES for an owned source | Inspect Haze's disabled/experimental fallback; do not silently promise blur |
| 23–28 | BlurView's RenderScript route only if acceptable and measured; otherwise L0 | Haze supports API 23+, but legacy blur is experimental RenderScript and disabled by default |
| 18–22 | BlurView's legacy route after performance checks; otherwise L0 | No Haze API 23+ assumption |
| Below API 18 | L0 drawable/Canvas or a separately verified legacy solution | No Haze/BlurView support assumption |

BlurView 4.0.0 declares minSdk 18 and uses RenderEffect on API 31+, OpenGL on API 29–30, and RenderScript below API 29. It provides blur, not refraction. Haze 2.1.0 supports Android API 23+ in Compose, but Glass fallback drops refraction/blur and Haze's legacy blur route is experimental. Read the Android dependency catalog before choosing a library. Do not combine blur libraries by default.

For custom L2 below API 33, OpenGL ES may be used only if the app can supply a valid app-owned backdrop texture. It does not automatically read arbitrary View trees or protected Surface content. Without a safe source, select L0/L1 and disclose the limit.

## 3. Minimal baseline implementation

For this fixture, use a native drawable/layered surface requiring no backdrop capture or shader support. It is an **L0 translucent fallback**, not blur or refraction.

\`\`\`xml
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="28dp" />
    <solid android:color="#332A3445" />
    <stroke android:width="1dp" android:color="#66FFFFFF" />
    <padding android:left="16dp" android:top="12dp"
        android:right="16dp" android:bottom="12dp" />
</shape>
\`\`\`

Attach it to a semantic clickable/focusable view in the existing XML layout; keep click handling in the existing Java activity/view model. Add accessible text, focus/pressed states, and contrast checks. Do not add a custom renderer for this L0 sample.

## 4. Validation

- Parse XML resources and confirm referenced resources resolve.
- Run the project's Gradle resource/build tasks with its configured SDK when available.
- Test every runtime API branch within the supported range; distinguish API 29–30, 31–32, and 33+ when applicable.
- Record effective minSdk, runtime API, dependency/version, and active renderer.
- Use a high-contrast grid/line behind the lens to prove displacement before claiming L2; blur alone remains L1.
- Check SurfaceView/TextureView, density, focus, touch, TalkBack, reduced motion/transparency, and light/dark backdrops.
- Profile scrolling/multiple surfaces on a lower-end physical device where possible.

## 5. Report

Report the demonstrated L0–L3 tier and explain exactly what the old-device branch renders. State unsupported APIs, fallback approximations, build versions, and tests not run. The fixture itself remains L0: it does not sample, blur, or geometrically displace the backdrop and does not implement fluid merging.

## 6. End-to-end workflow test

The package test runner creates a temporary Android Java/XML project, runs the inventory helper against it, checks manifest/Gradle/minimum-SDK evidence and parses XML resources, then verifies the trace covers discovery → minSdk/runtime strategy → implementation → validation → report without claiming unsupported APIs/refraction.
