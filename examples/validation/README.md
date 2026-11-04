# Phase 6 — Validation, accessibility, and performance

This directory defines repeatable validation for the runnable WebGL2 and Android GLES2 references. It separates automated evidence from checks that still require a physical device and a human visual/accessibility review.

## Run the automated checks

From the repository root:

```bash
python -m unittest discover -s examples/tests -v
```

WebGL2 browser matrix:

```bash
cd examples/webgl2
npm install
npx playwright install chromium
npm test
```

Android API 35 emulator validation (JDK 17, Gradle 8.7, Android SDK 35):

```bash
cd examples/android-gles
gradle --no-daemon :app:assembleDebug
cd ../..
bash -n examples/android-gles/scripts/verify-emulator.sh
bash -n examples/android-gles/scripts/profile-emulator.sh
```

The `reference-demos` GitHub Actions workflow runs the browser tests, assembles and launches the Android app, exercises accessibility hit regions, changes display density/size and orientation, captures a four-surface workload, and collects emulator profiling diagnostics. Its artifacts are retained for 14 days.

## Visual comparison procedure

1. Select the relevant supplied reference and record its criterion IDs from [the reference matrix](../../docs/reference-matrix.md). Do not compare unrelated crops or infer animation from a still.
2. Use the same viewport, orientation, density/device-pixel ratio, content, and interaction state for the reference and capture. Record those values in [the review record](visual-review-template.md).
3. Compare silhouette, transmission, actual sample displacement, mask leakage, thickness, curvature, edge response, reflections, foreground legibility, state continuity, and settling. A blur-only result is L1, never L2.
4. Review at least a dark backdrop, a bright backdrop, and a high-frequency/detail backdrop. The browser CI run captures all three, plus a portrait/landscape and high-DPR combination.
5. Review idle, connected/morphed, keyboard-focused, playing/paused, and reduced-motion states. For platforms exposing hover or dragging, add those states to the record.
6. Mark every applicable criterion Pass, Partial, Fail, or N/A. Attach the original reference and the exact capture; explain any Partial/Fail result and the platform limitation.

Automated WebGL2 capture cases:

| Capture | Viewport | DPR | Backdrop |
|---|---:|---:|---|
| desktop-midnight | 1440 × 960 | 1 | Dark, regular high-contrast geometry |
| tablet-bright | 768 × 1024 | 1 | Bright, low-frequency palette |
| mobile-detailed | 390 × 844 | 2 (renderer capped at 1.65) | Dense fine-line/high-frequency pattern |
| landscape-bright | 844 × 390 | 2 (renderer capped at 1.65) | Bright, wide layout |

Android CI exercises the native app at its default emulator configuration, a 720 × 1280 / 320 dpi portrait display, an emulator-console-rotated 1280 × 720 landscape display, and a separate mode with one primary plus three additional refractive SDF surfaces (four independent refractive SDF surfaces in total). The medium-density and landscape cases restart the Activity and validate its UI hierarchy, Android `Configuration.orientation`, dp viewport dimensions, UIAutomator rotation, WindowManager size override, screenshot orientation, and minimum capture size; a blank or portrait-in-landscape screenshot fails CI. The landscape case uses Android Emulator's `adb emu rotate` command rather than relying only on a WindowManager rotation lock. These are emulator scenarios, not device-family coverage.

## Accessibility quality gates

### Web

The Playwright check verifies accessible names/roles, the range label, pressed state, keyboard tab order, a visible focus outline, 44 CSS-pixel action targets, a 40-pixel slider hit region, reduced-motion state continuity, increased-contrast styling, reduced-transparency styling, forced-colors behavior, and the computed CSS filter state for L0 (no blur) versus L1 (backdrop blur).

The demo responds to:

- `prefers-reduced-motion`: removes nonessential animation and keeps the selected morph state usable.
- `prefers-contrast: more`: increases opacity, border emphasis, and text contrast.
- `prefers-reduced-transparency: reduce`: replaces translucent surfaces with opaque surfaces when the browser/OS exposes this preference.
- `forced-colors: active`: uses system colors and explicit focus outlines.

### Android

Native controls expose content descriptions and use 48 dp action-button targets; the SeekBar has a 48 dp layout height. High-text-contrast mode is read from the system's `Settings.Secure` `high_text_contrast_enabled` flag (the public `AccessibilityManager` query is only available starting with API 36), and reduced animation is read from the system animator setting / `ValueAnimator` when available. The activity no longer locks the app to portrait. GL rendering uses `RENDERMODE_WHEN_DIRTY`; a frame pump is active only while playback or a morph needs animation and is removed while the activity is paused.

The emulator script validates the TalkBack-facing accessibility node names and verifies hit-region dimensions from UIAutomator bounds. It does **not** certify TalkBack speech quality, switch access, magnification, or a real device's accessibility configuration. Those remain human checks on physical hardware.

## Performance evidence and interpretation

### Browser

The browser report contains a reset, isolated 3-second single-page frame-pacing window with average/P95/max interval, intervals above 16.7 ms, CPU-side WebGL command-submission time, draw calls per frame, canvas pixel ratio, and the estimated RGBA8 scene-texture allocation. The other viewport capture pages are opened only after the isolated timing window, so their screenshot load does not contaminate the desktop sample.

- CPU submission time measures JavaScript/driver command submission only.
- Estimated scene-texture memory is `width × height × 4` bytes for one RGBA8 off-screen texture; it excludes browser compositor surfaces, driver allocations, and other process memory.
- The extension flag only reports whether `EXT_disjoint_timer_query_webgl2` is exposed. GPU execution time is not reported by this test.

### Android

The renderer logs GL vendor/renderer/version, frame callback interval statistics, P95 frame interval, approximate FPS, intervals above 16.7/33.3 ms, CPU-side GL command-submission P95, and the app-owned RGBA FBO texture byte estimate. The profiling script preserves:

- `dumpsys gfxinfo` and frame stats;
- `dumpsys meminfo` and a one-shot process CPU snapshot;
- display size/density and SurfaceFlinger layer listing;
- battery and thermal service snapshots;
- GL renderer diagnostics and the renderer's PERF records.

The additional-surface workload keeps one FBO and two full-screen passes (scene render plus glass composition) while evaluating up to four SDF surfaces in the glass shader. Its screenshot is accepted only after activity focus and native UI hierarchy are verified, so a splash screen or launcher cannot be mistaken for a multi-surface capture. It records `full_screen_passes=2` and the number of SDF surfaces. The memory estimate therefore remains the single RGBA8 scene texture; the extra shader work is not represented as extra FBO allocations. This is a draw-pass accounting aid, not a hardware overdraw counter. On physical devices, inspect color/depth overdraw using Android Developer Options' GPU overdraw visualization and correlate it with GPU Inspector/Perfetto traces; save the overlay and counters with the review record.

**Important measurement boundary:** CI uses an API 35 x86_64 emulator with SwiftShader. The frame callback intervals, CPU command-submission time, memory snapshots, and battery/thermal dumps are useful regression diagnostics for that emulator only. They do not measure physical GPU execution time, real-device power drain, or sustained thermal behavior. Do not compare the emulator's values with a physical handset or use them as a product performance claim.

### Physical-device profiling protocol

Before a production/release claim, repeat on at least one low/mid-range and one higher-tier physical Android device supported by the intended audience:

1. Record model, SoC/GPU, Android API, GLES version, display resolution/density/refresh rate, battery state, ambient conditions, and app build SHA.
2. Keep brightness, refresh rate, power mode, network state, and background process conditions fixed. Let the device reach a stable thermal state.
3. Run 60 seconds idle, 60 seconds animated playback, 30 repeated morph cycles, and 60 seconds each at 1, 2, and 4 simultaneous surfaces. Repeat each scenario three times.
4. Use Android Studio Profiler / Perfetto for CPU scheduling and frame timelines, and Android GPU Inspector or vendor GPU tools for GPU duration/counters where supported. Use system battery/thermal telemetry over a longer, repeatable run; short emulator snapshots are not battery-life evidence.
5. Report median and worst-run frame pacing, GPU duration, peak/steady memory, CPU cost, overdraw evidence, surface count, thermal throttling, and battery delta. Save traces and device details with the visual captures.
6. Compare the measured result against the application's own frame budget (for example, 16.7 ms at 60 Hz or 11.1 ms at 90 Hz). Do not assume 60 Hz on every device.

No physical-device profiling or TalkBack certification is claimed by the current CI run.

## Fallback tiers

- WebGL2 L2/L3 is available only when the app-owned WebGL2 framebuffer initializes. WebGL/context loss drops to CSS L1 when backdrop blur is supported, otherwise L0.
- Android L2/L3 requires the GLES2 app-owned framebuffer. Shader failure or incomplete FBO yields L0. The sample does not capture arbitrary Android View trees or external surfaces.
- Reduced-motion and high-contrast settings do not upgrade a renderer tier; they preserve usable semantic controls while lowering visual effects.
- Always record the actual tier observed at runtime. Do not infer capability from a dependency, API level, or successful build alone.
