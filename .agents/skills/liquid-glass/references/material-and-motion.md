# Material, Geometry, and Motion Contract

This reference summarizes the target qualities. In the LiquidGlass repository, the normative detailed documents are [the visual specification](../../../../docs/visual-specification.md), [interaction and motion](../../../../docs/interaction-and-motion.md), and [the reference matrix](../../../../docs/reference-matrix.md).

## Optical behavior

### Transmission
The backdrop remains recognizable through the surface. Transmission may vary with tint, thickness, curvature, and edges; it must not collapse into a uniformly opaque card.

### Refraction and distortion
Background features bend, shift, magnify, compress, or warp within the surface. Distortion must follow the apparent shape/thickness, remain clipped, and stay stable during scrolling and animation. Blur and color gradients are not refraction.

### Depth and thickness
Curvature, body shading, edge bands, and separation from foreground content make the material read as a volume rather than a flat overlay.

### Reflections and edge response
Broad highlights and tighter specular cues reinforce a coherent light environment. A Fresnel-like rim or bright/dark edge transition follows curvature and backdrop brightness. Avoid a detached outline or a constant halo.

### Spectral response
Chromatic dispersion and iridescence are optional accents. Keep them spatially restrained, coherent with the surface, and subordinate to readability and real optical behavior.

## Shape families

Select the silhouette needed by the component; do not force everything into a capsule:
- pill/capsule lens;
- circular or oval bubble;
- connected control group;
- attached lobe or protrusion;
- organic continuous or joined-lobe form;
- slider track with a raised thumb.

## Layering model

A conceptual composition may include the actual backdrop; shape coverage and mask; transmitted/refracted backdrop clipped to the shape; body tint/absorption; depth, edge, and specular contributions; and crisp semantic content/focus indicators.

This is not a mandatory render graph. Native effects may combine layers differently. Keep the hit region and semantic identity independent of a deforming decorative contour.

## Interaction and motion

Treat the surface as an interactive material, not a static sticker. Relevant states include idle, hover/focus, press, drag, release, merge, split, disabled, reduced motion, and settled.

Use a continuous and interruptible model. A damped spring or suitable interpolation may be used, but exact timing must be tuned for the target; do not treat approximate reference-video timings as normative constants.

During a morph, the silhouette, mask, backdrop displacement, edge thickness, and highlights must follow one coherent shape state. Keep labels/icons legible and stable. Bound movement, provide a settling threshold, and avoid jitter, runaway overshoot, ghost fragments, and abrupt contour pops.

When reduced motion is enabled, suppress large morphs, parallax, and nonessential floating while preserving the same actions and clearly perceivable states.
