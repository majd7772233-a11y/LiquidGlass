# Liquid Glass — Reference-to-Criterion Matrix

**Status:** Phase 1 deliverable  
**Purpose:** identify what each asset can legitimately demonstrate and how it should be used during design review.

## 1. Still-image references

| Reference | Observed content | Primary criteria | Secondary criteria | Evidence limits |
|---|---|---|---|---|
| [Translucent controls and sliders](../examples/references/controls/translucent-controls-and-sliders.png) | Several floating capsule and rounded controls over a light grid, including slider-like tracks and colored fills | Shape families, translucency, edge contour, component scale | Raised thumb vs track, neutral glass over a clean backdrop | Static image cannot establish motion or prove real-time refraction |
| [Liquid Glass interface storyboard](../examples/references/storyboards/liquid-glass-interface-storyboard.png) | Contact sheet of interface states over floral and soft natural backgrounds | Background sensitivity, control placement, navigation/search variations, state continuity | Repeated states across a changing background | Contact sheet is compressed and small; use source image, not tiny cell crops, for detailed optical inspection |
| [Refractive media playback controls](../examples/references/media/refractive-media-playback-controls.png) | Circular previous/play/next controls over flowers and blue sky, with visible background color through the controls | Circular lens silhouette, backdrop transmission, edge response, optical color cues | Relative depth and control hierarchy | A still image suggests refraction visually but cannot prove how it was rendered |
| [Organic iridescent liquid-glass form](../examples/references/material/organic-iridescent-liquid-glass-form.png) | Large continuous asymmetrical joined-lobe form with pearlescent color and luminous perimeter | Organic silhouette, connected contour, edge lighting, surface color transitions | Thickness impression and highlight placement | Abstract backdrop provides limited evidence about detailed background distortion |

## 2. Motion reference

**Source:** the user-provided clip named Liquid.mp4, inspected during Phase 1. The clip was available in the working session but is not stored in this repository. It is not redistributed here because its publication/provenance and permission for public re-hosting have not been established.

The inspected clip is approximately 50.6 seconds at 30 frames per second and 582 × 576 pixels. It contains a visible social-platform watermark; this document records only visual observations needed for engineering and does not claim ownership of the clip.

### 2.1 Observed sequences

| Approximate time | Observed behavior | Criteria to extract |
|---|---|---|
| 0–10 s | A wide transparent navigation/control bar over a detailed flower image; a separate rounded search-like surface appears connected near the bar; icons remain readable while the backdrop is strongly visible through the material | L2-style backdrop displacement cues, pill lens, attached/detached lobe, clear foreground content |
| 10–23 s | The bar and smaller rounded surface change relative shape and position; the search affordance appears to grow into a larger bubble while the navigation surface changes contour and content alignment | Continuous contour deformation, stable icon semantics, interruptible movement, optical mask following shape |
| 24–33 s | Scene changes to a soft green/golden natural background; a long upper surface and lower navigation-like surface coexist, with a curved connector/protrusion between regions | Multiple surfaces, backdrop-dependent tint/refraction, smooth attached shapes |
| 33–46 s | A circular search-like region rises from or reconnects with the lower horizontal bar; the lobe moves between configurations while the lower bar remains a connected material body | Merging/splitting, connected-lobe morph, stable action placement, smooth settling |

Time ranges are approximate visual reading points, not measured keyframe timings. They are not normative animation durations.

### 2.2 Cross-cutting observations

- The background remains visible through large parts of the surfaces; the material is not a solid card.
- High-contrast flowers and foliage show prominent optical displacement and colored edge behavior.
- The colored effects are strongest around curved or high-contrast regions and should not be interpreted as a requirement for a constant rainbow outline.
- Horizontal bars can become irregular connected contours with circular/rounded protrusions.
- Search and navigation symbols remain comparatively crisp, visually separated from the refracted backdrop.
- The shape changes are continuous rather than simple opacity swaps between unrelated components.
- The second background changes the perceived material color, demonstrating why a single static tint is not enough to validate the effect.

## 3. Criterion index

Use this index when reviewing a feature.

| Criterion ID | What to inspect | Best reference |
|---|---|---|
| REF-01 | Transmission through the surface | Storyboard; motion clip |
| REF-02 | Actual background displacement/refraction, not blur alone | Motion clip; media controls image as a still cue |
| REF-03 | Capsule/pill and slider silhouette | Translucent controls image |
| REF-04 | Circular lens and compact action surface | Media controls image; motion clip |
| REF-05 | Continuous organic/connected silhouette | Organic form image; motion clip |
| REF-06 | Edge thickness, rim, and curvature response | Media controls image; organic form image |
| REF-07 | Controlled spectral dispersion/iridescence | Media controls image; organic form image; motion clip |
| REF-08 | Multiple backdrops and changing background response | Storyboard; motion clip |
| REF-09 | Crisp icons/labels over optical material | Storyboard; motion clip |
| REF-10 | Connected-lobe growth, merge, split, and settle | Motion clip |
| REF-11 | Component grouping and navigation layout | Translucent controls image; storyboard; motion clip |
| REF-12 | Stable material response while geometry changes | Motion clip |

## 4. Evidence confidence and prohibited inferences

- A still can demonstrate visible color, silhouette, layering, and apparent optical cues. It cannot establish animation quality, interaction semantics, frame rate, or the exact rendering method.
- A contact sheet can indicate a sequence of states but may not preserve enough detail for pixel-level optical measurements.
- The motion clip supports qualitative observations about contour movement and background interaction. The listed timestamps are approximate and must not be converted into exact timing constants.
- The four assets still located in examples/references/unclassified/ have not been inspected in this phase. They MUST NOT be cited as evidence for any specific property until reviewed.
- The references do not prove physical correctness, actual refractive index, shader architecture, or exact optical parameters.
- Never claim pixel-perfect reproduction from visual inspection alone. Use captured implementations and side-by-side review during the validation phase.

## 5. How to use the matrix

1. Select the reference most relevant to the component and behavior being implemented.
2. Record the criterion IDs that apply before implementation.
3. Capture the result over comparable backgrounds and in comparable states.
4. Mark each criterion Pass, Partial, Fail, or Not Applicable.
5. Record whether the implementation is L0, L1, L2, or L3 as defined in the visual specification.
6. Explain any platform limitation and verify that the chosen fallback is stable and usable.
