# Motion, accessibility, and performance

## Separate control from appearance

- The semantic control owns action/value/focus/accessibility identity.
- The hit region owns predictable input behavior.
- The shape owns its evolving contour and connected regions.
- The material owns transmission, refraction, thickness, and reflection.
- The motion system coordinates geometry and optical response.

A decorative contour change must not unexpectedly move a hit target, change an action, or intercept input intended for a neighboring control.

## State vocabulary

Use applicable states: rest, hover, focus, pressed, dragging, settling, merging, splitting, disabled, and reduced-motion. These are design states, not mandatory class names. New input must be able to interrupt/retarget ongoing motion safely.

## Continuity requirements

- Morph boundaries continuously; avoid jumps, seams, visible pops, or isolated overlapping circles.
- When surfaces merge/split, the neck and contour transition coherently.
- The mask, transmitted backdrop, distortion field, rim, thickness, and highlights must follow the same evolving geometry.
- Motion should follow input with bounded lag/displacement and settle without jitter or indefinite oscillation.
- Use damped springs or another stable interpolation appropriate to the platform. Preserve velocity/position continuity when retargeting where practical.
- Suggested starting durations are not measured facts: small press/focus 100–220 ms, short state change 140–260 ms, connected-lobe morph 220–480 ms, larger reconfiguration 350–650 ms. Tune to context and measured frame behavior.

## Accessibility

- Maintain readable contrast over changing backdrops.
- Preserve keyboard/controller focus order, accessible names, and screen-reader semantics.
- Keep touch/pointer targets predictable and usable.
- Make focus, pressed, selected, and disabled states perceivable without relying only on color, blur, or motion.
- Respect reduced-motion settings: suppress large morphs, parallax, and overshoot while preserving state feedback.
- Respect high-contrast/transparency-reduction settings when exposed by the platform; offer a stable opaque/translucent fallback as appropriate.

## Performance

Measure on the target class of device. Inspect frame pacing, GPU/CPU time, render-target bandwidth, overdraw, memory, allocation rate, thermal/battery behavior, startup, scrolling, and multiple simultaneous surfaces.

Avoid:

- full-screen backdrop recapture on every pointer event when reuse is possible;
- unnecessary multi-pass blur/refraction;
- unbounded shader loops and dynamic work;
- per-frame object/texture allocation;
- oversized offscreen targets when a lower-resolution sample is visually adequate;
- animation that continues at full cost off-screen or while inactive;
- effects that block scrolling, input, navigation, or assistive technology.

Offer quality tiers or a stable fallback when device capabilities vary. Do not raise the minimum OS/API silently to gain one visual feature.
