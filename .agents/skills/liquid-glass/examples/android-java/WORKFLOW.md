# Worked workflow: native Android Java/XML project

**Purpose:** exercise platform detection and native fallback reasoning without assuming that every Android version exposes the same compositor/shader facilities. This is an L0 example, not a finished refractive implementation.

## 1. Discovery evidence

The automated package test creates a temporary Android fixture containing:

- Gradle Android project files;
- `app/src/main/AndroidManifest.xml`;
- a Java `MainActivity`;
- an XML layout and drawable resource;
- a declared minimum SDK of 23.

The family is **native Android UI, Java + XML**. The minimum SDK is part of the implementation constraint. Do not select an API introduced after API 23 without a checked compatibility branch or an explicitly approved minimum-version change.

## 2. Strategy decision

For the baseline fixture, use a native drawable/layered surface that requires no backdrop capture or shader support. It is an **L0 translucent fallback**. Do not call it blurred or refractive. If a real project requires L1, inspect its minimum platform and available blur/compositor APIs. If it requires L2/L3, verify backdrop access, shader/runtime support, clipping, and fallback behavior on the actual minimum target before selecting a renderer. The skill must not silently prescribe a newer API.

## 3. Minimal implementation shape

A simple `layer-list`/`shape` drawable can provide a restrained tint and contour without claiming refraction:

```xml
<shape xmlns:android="http://schemas.android.com/apk/res/android"
    android:shape="rectangle">
    <corners android:radius="28dp" />
    <solid android:color="#332A3445" />
    <stroke android:width="1dp" android:color="#66FFFFFF" />
    <padding android:left="16dp" android:top="12dp"
        android:right="16dp" android:bottom="12dp" />
</shape>
```

Attach it to a semantic clickable/focusable view in the existing XML layout; keep click handling in the existing Java activity/view model. Add accessible text, focus/pressed state resources, and contrast checks for the real screen. Do not add a custom rendering engine for this L0 sample.

## 4. Validation and report

- Parse the XML resources and confirm all referenced resource names resolve.
- Run the project's Gradle resource/build tasks with its configured Android SDK when available.
- Run on the minimum supported API and a current target, checking layout, density, focus, touch, TalkBack semantics, and light/dark backdrops.
- Report **L0**. State that this example does not sample, blur, or geometrically displace the backdrop and does not implement fluid merging.

## 5. End-to-end workflow test

The package test runner creates a temporary Android Java/XML project, runs the inventory helper against it, checks manifest/Gradle/minimum-SDK evidence and parses its XML resources, then verifies this trace covers discovery → strategy → implementation → validation → report without claiming unsupported APIs or refraction.
