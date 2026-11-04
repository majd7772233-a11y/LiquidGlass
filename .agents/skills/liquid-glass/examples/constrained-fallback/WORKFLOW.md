# Worked workflow: constrained / no-backdrop target

**Purpose:** show a deliberate capability downgrade rather than a fake refractive implementation.

## Project profile to record

- Minimum OS/API, CPU/GPU, graphics backend, memory/thermal budget.
- Whether the application owns the background texture.
- Whether shader compilation, render targets, blur, or capture are unavailable or too expensive.
- Required semantic controls, readability, and input paths.

## Strategy decision

If no safe backdrop source exists, choose L0. If the system exposes an affordable blur of the correct content, choose L1. Do not claim L2/L3. Keep a higher tier as an optional capability-gated path only when an application-owned texture becomes available and can be tested.

## Minimal fallback

- Native rounded shape with subtle translucent/tinted fill.
- Readable text/icons and a stable contrasting edge.
- Static or very short pressed/focus feedback.
- Opaque/high-contrast presentation when transparency is reduced or contrast requires it.

Do not add a shader or repeated full-screen capture merely for decoration.

## Reproducible validation

1. Disable or remove optional graphics features and run the fallback branch.
2. Confirm no shader or backdrop allocation is required to display or activate the control.
3. Test bright/dark backgrounds, low-memory conditions, and the oldest supported API.
4. Test focus, touch/keyboard, screen reader, high contrast/transparency reduction, and reduced motion.
5. Record L0 or L1 from observed behavior and explicitly list unavailable optical properties.

**Expected tier:** L0 by default; L1 only after runtime blur is observed. A stable fallback is a valid outcome, not a failed attempt at L2.
