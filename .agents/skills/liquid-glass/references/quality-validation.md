# Quality, Accessibility, and Performance Validation

A finished effect is a working UI feature plus optical evidence—not merely code that compiles.

## Build and behavior checks

Run the actual project commands, not guessed replacements:
- formatter/linter and static analysis;
- unit tests for geometry, state transitions, and parameter bounds;
- integration/UI tests for input, lifecycle, clipping, and fallback branches;
- build/package tasks for the supported target;
- runtime smoke test on the minimum or representative device/browser;
- visual capture at comparable viewport, scale, backdrop, and state.

Record exact commands and results. If a test cannot run, state why and what substitute evidence exists. Never call a dry-run a build test.

## Visual review

Use [the review template](../assets/visual-review.template.md). Compare at least a detailed/high-frequency backdrop, a soft/low-frequency backdrop, a bright backdrop, a dark backdrop, high-contrast edges crossing behind the surface, and moving/scrolling content where supported.

Review silhouette, transmission, actual displacement, clipping, curvature, thickness, edge response, reflections, restrained spectral behavior, and crisp foreground content. Use side-by-side captures when available. Record Pass, Partial, Fail, or Not Applicable for each criterion.

## State and accessibility review

Check applicable states: idle, hover, keyboard focus, pressed, dragged, release/cancel, disabled, settled, and reduced motion.

Also verify readable contrast over changing backdrops; semantic role, accessible name, and screen-reader order; keyboard/controller navigation and visible focus; predictable hit regions during shape deformation; touch/pointer target sizing; reduced-motion behavior and static usability; and high-contrast/transparency-reduction settings exposed by the platform.

Do not communicate selection, focus, or enabled state by color, blur, or motion alone.

## Performance review

Measure on representative target hardware when possible: frame pacing and input latency; CPU/GPU time and shader complexity; render-target and texture memory; full-screen passes, overdraw, and blur/capture frequency; lifecycle/resource release; thermal/power under sustained use; and scaling with multiple surfaces.

Avoid unbounded shader loops, repeated full-resolution backdrop capture, unnecessary offscreen passes, and per-frame allocations. Define lower quality tiers before the device reaches an unstable state.

## Fidelity and final report

Use L0/L1/L2/L3 as defined in the technique-selection reference. State which individual properties are genuine, approximated, or absent. A blur-only implementation is at most L1.

Separate source/build/test verification, runtime behavior actually exercised, visual evidence reviewed, hardware/platforms not tested, and known gaps/fallback. Never claim pixel-perfect match or universal support without reproducible evidence.
