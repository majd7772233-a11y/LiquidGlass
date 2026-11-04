# Implementation and Integration Workflow

## Before editing

- Establish the real project root and read its local agent instructions.
- Trace the target component through its caller, composition parent, and backdrop owner.
- Record baseline build/test status.
- Create a brief naming visual criteria, primary strategy, alternative, affected files, API boundary, capability gates, fallback, and validation plan.
- Identify what must remain unchanged: behavior, navigation, input, semantic labels, persistence, layout, minimum targets, and localization.

## Architecture boundaries

Prefer the smallest useful integration. Where practical, keep separate modules/components for shape geometry and mask generation; backdrop access/capture and distortion; material parameters (tint, thickness, edge, reflection, optional spectral response); interaction state and motion; and semantic content, hit regions, focus, and accessibility.

These may live together when the target framework naturally combines them. Do not split code merely to satisfy an abstract architecture, and do not introduce a universal rendering engine.

## Implementation sequence

1. Build the static silhouette and semantic control first; verify layout and hit targets.
2. Add backdrop transmission and masking. Confirm the exact backdrop being sampled.
3. Add true displacement only when the chosen pipeline can provide reliable backdrop pixels.
4. Add depth, thickness, edge response, and reflections as coherent contributions.
5. Add restrained spectral behavior only if supported by the reference and useful at the target scale.
6. Add interaction states and continuous shape transitions. Keep layout and semantic identity stable.
7. Add quality gates, fallback behavior, and accessible reduced-motion behavior.
8. Integrate with existing theme, lifecycle, navigation, and state management.
9. Run checks and update documentation/evidence.

Do not implement every optical contribution in a single opaque component if that makes it difficult to test or downgrade.

## Changes and dependencies

- Prefer existing project dependencies and platform facilities.
- Justify any new dependency or minimum-target change with measured or demonstrated value.
- Gate optional features by runtime capability and test each branch.
- Keep shader code bounded and deterministic; avoid unbounded loops and per-frame allocations.
- Release resources with the owning component/window/scene lifecycle.
- Prevent stale backdrop snapshots, feedback loops, and recursive captures.
- Preserve keyboard, touch, pointer, controller, and screen-reader behavior.
- Do not refract semantic text/icons by default; compose them above the optical layer.
- Do not overwrite unrelated work, delete assets, or reformat broad areas without need.

## Failure handling

| Symptom | Investigate | Corrective direction |
|---|---|---|
| Surface looks like a painted card | Transmission, opacity, backdrop ownership | Restore visible backdrop detail; lower tint; validate over varied scenes |
| Blur is presented as refraction | Backdrop sampling and displacement path | Add real displacement if supported or relabel L1/L0 |
| Distortion leaks beyond contour | Mask coordinates, alpha, render order | Unify mask and optical coordinate spaces |
| Highlights drift during morph | Separate geometry/light state | Derive optical response from the same animated shape |
| Icons move or blur unexpectedly | Semantic layer and transforms | Keep semantic layout independent and crisp |
| Jitter or slow settling | Time step, retargeting, damping, geometry bounds | Preserve velocity where suitable; clamp and test variable frame rates |
| Performance collapses with many surfaces | Capture frequency, pass count, resolution, overdraw | Cache/reuse safe frames, reduce quality, batch or downgrade |
| Older target breaks | Ungated API/shader feature | Add capability check and tested fallback path |

## Change hygiene

Keep diffs narrow. Follow host-project formatting and naming. Add comments for non-obvious rendering math and platform-specific limitations. Never hide a failing test or alter unrelated code to make a demo pass.
