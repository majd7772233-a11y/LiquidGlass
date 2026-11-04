# Liquid Glass visual and interaction review

Copy this file for each implementation/release candidate. Attach both the supplied reference and the corresponding capture set.

## Build and environment

- Repository / commit:
- Platform / OS / API:
- Device / GPU / driver:
- App or browser build:
- Viewport / physical resolution:
- Density / device-pixel ratio:
- Orientation / refresh rate:
- Renderer tier observed at runtime:
- Background/content source:
- Date and tester:

## Capture matrix

| Scenario | State | Capture path/name | Result (Pass / Partial / Fail / N/A) | Notes |
|---|---|---|---|---|
| Dark backdrop | Idle | | | |
| Bright backdrop | Idle | | | |
| High-frequency backdrop | Idle | | | |
| Connected / morphed | Settled | | | |
| Keyboard focus / touch focus | Focus | | | |
| Pressed / active | Pressed | | | |
| Dragged / manipulated | Dragging | | | |
| Reduced motion | Static/settled | | | |
| Reduced transparency / high contrast | Fallback | | | |
| Multiple simultaneous surfaces | 1 / 2 / 4 | | | |
| Alternate density and orientation | Resized | | | |

## Visual criteria

| Criterion | Result | Evidence / gap |
|---|---|---|
| Silhouette and spatial relationship | | |
| Backdrop transmission | | |
| Actual background displacement (required for L2+) | | |
| Distortion follows the shape and stays clipped | | |
| Thickness, curvature, and depth | | |
| Edge response and reflection coherence | | |
| Restrained spectral response | | |
| Crisp foreground text/icons | | |
| Background sensitivity | | |
| Continuous morph / settling | | |
| Stable interaction and hit regions | | |
| Honest L0/L1/L2/L3 label and fallback | | |

## Accessibility review

- Keyboard/controller order and visible focus:
- TalkBack/screen-reader names, roles, and state announcements:
- Touch/pointer target dimensions:
- Contrast on every tested backdrop:
- Reduced-motion behavior:
- Reduced-transparency / high-contrast / forced-colors behavior:
- Text scaling / display scaling:
- Disabled and pressed states:
- Accessibility defects and remediation:

## Performance record

| Scenario | Surface count | Refresh budget | Median frame time | P95 / worst frame | GPU time | CPU cost | Peak memory | Thermal / battery notes |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Idle | 1 | | | | | | | |
| Animated | 1 | | | | | | | |
| Morph cycles | 1 | | | | | | | |
| Animated | 2 | | | | | | | |
| Animated | 4 | | | | | | | |

Record the measurement tool and whether the values are physical-device or emulator-only. CPU command-submission time is not GPU execution time. Texture-byte estimates are not total process memory.

## Decision

- Confirmed renderer tier:
- Highest-priority visual/accessibility/performance gaps:
- Known platform/device limitations:
- Release blockers:
- Reviewer and review date:
