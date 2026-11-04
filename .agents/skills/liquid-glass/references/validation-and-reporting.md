# Validation and truthful reporting

## Validation sequence

1. Run the host project's formatter, lint/static analysis, unit tests, and build relevant to the changed code.
2. Run the app/component on the minimum supported target when available, not only a developer machine or latest simulator.
3. Capture a comparable viewport, scale, content, and backdrop against the chosen reference.
4. Inspect bright, dark, detailed, low-detail, and high-contrast backgrounds.
5. Inspect idle/rest, focus, hover where relevant, pressed, drag, release/settle, disabled, resize/scroll, and reduced-motion states.
6. Confirm clipping during motion, foreground readability, hit testing, accessibility semantics, and lifecycle behavior.
7. Measure performance on representative hardware; note when performance has not been measured.
8. Compare against the visual contract; fix failures or document platform limits and the chosen fallback.

## Review rubric

For each applicable property, mark **Pass**, **Partial**, **Fail**, or **Not tested**:

- intended silhouette and connected geometry;
- backdrop transmission;
- actual background displacement when claiming refraction;
- shape/thickness-aware distortion and stable clipping;
- depth/curvature on bright and dark backdrops;
- coherent edge response and specular highlights;
- restrained spectral effects;
- crisp readable foreground content;
- stable interaction, hit regions, and semantics;
- reduced-motion and fallback behavior;
- frame pacing/resource use on target hardware.

## Report format

Include:

- **Target:** platform, framework/runtime, minimum version, and device/browser if tested.
- **Approach:** chosen renderer and evidence that justified it; alternatives rejected and why.
- **Changes:** concrete files/components and public configuration/API changes.
- **Fidelity:** highest demonstrated tier (L0–L3), plus a per-feature statement of real/approximated/missing behavior.
- **Validation:** exact commands/tests/builds run and their actual outcomes; screenshots/videos or steps to reproduce visual review.
- **Performance/accessibility:** measurements or checks performed; explicitly say when not measured.
- **Limitations:** platform restrictions, untested paths, and next steps.

Never say “pixel-perfect,” “physically accurate,” “true refraction,” “works on all devices,” or “tested” unless the relevant evidence exists. A successful compile does not prove a correct visual result.
