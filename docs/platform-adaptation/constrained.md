# Constrained or Backdrop-Inaccessible Environments

Use this guide when the target lacks a safe backdrop source, has no shader API, cannot afford capture/render passes, uses a software renderer, includes protected surfaces, or must support devices with substantially different GPU capability.

## Decision

Do not promise L2/L3 without accessible backdrop pixels and a stable render path. A shader that draws a colored surface does not prove refraction.

Use the strongest available honest tier:

- **L0:** translucent/tinted surface with a clear contour and readable semantic content.
- **L1:** add a supported, affordable blur and restrained highlights. Confirm blur is actually visible at runtime.
- **L2:** only when the app can supply an owned background texture and displace it within a bounded mask.
- **L3:** only when L2 is already verified and the platform can keep geometry, mask, distortion, and highlight response coherent during shape changes.

## Low-cost fallback design

- Prefer native rounded shapes and compositing rather than introducing a second rendering engine.
- Keep the fill subtle and preserve backdrop legibility.
- Use a narrow edge treatment and restrained static highlight instead of multiple full-screen effects.
- Avoid simulated RGB splitting if it harms text/icon readability.
- Keep geometry stable; use short, interruptible transitions or no animation.
- Provide an opaque/high-contrast alternate surface when transparency reduces legibility.
- Expose the same semantic action, focus, enabled/disabled state, and hit target as a higher fidelity implementation.

## Downgrade conditions

Downgrade at startup or when runtime quality becomes unstable if:
- texture allocation or shader creation fails;
- the required composition surface is unavailable or becomes protected;
- frame pacing drops below the product target;
- the device is thermally constrained or loses the GPU context;
- the user enables reduce motion/transparency/high contrast;
- the window is backgrounded or the component is not visible.

A downgrade must not change the control's meaning, hit target, or accessibility identity.

## Validation

Test the fallback itself, not just the high-end path:
- older API/device or software backend;
- low-memory and graphics-resource failure where reproducible;
- high-contrast and bright/dark background;
- reduced-motion and transparency-reduction behavior;
- readable text/icons and unchanged keyboard/touch actions;
- CPU/GPU cost, frame pacing, and no per-frame allocations.

Report the tier and the exact missing capability. Do not describe the fallback as a broken L2 implementation when the platform intentionally cannot provide backdrop access.
