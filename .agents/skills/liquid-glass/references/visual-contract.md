# Visual contract

This is a portable summary of the LiquidGlass project's Phase 1 specification. The full source documents, when available, are `docs/visual-specification.md`, `docs/interaction-and-motion.md`, and `docs/reference-matrix.md` in the main repository.

## What the material must communicate

- **Transmission:** recognizable backdrop detail remains visible through the surface; opacity/tint varies intentionally rather than forming an opaque card.
- **Refraction/distortion:** background features bend, shift, magnify, compress, or warp through the curved surface. Distortion follows shape/thickness and remains clipped. Blur, static gradients, and color tint are not refraction.
- **Depth/thickness:** coherent contour, inner transition, edge shading, curvature, or magnification creates a finite optical body rather than a flat overlay.
- **Specular response:** broad and tight highlights reinforce curvature and a plausible light environment without covering important content.
- **Edge response:** controlled bright/dark/Fresnel-like rim and inner shading adapt to shape and backdrop; avoid detached halos or uniform cartoon outlines.
- **Spectral effects:** restrained chromatic dispersion/iridescence may accent high-curvature regions when the reference supports it. It is optional, never a constant rainbow border.
- **Surface tint:** neutral/cool/warm/contextual tint preserves enough local background detail and content contrast.

## Shape families

Support the shapes the interface actually needs: capsule/pill lens, circular or oval lens, connected control group, attached lobe, continuous organic form, and slider/track with a raised thumb. Do not force all controls into pills, or create connected shapes by simply overlapping opaque circles.

## Composition and content

Conceptually place the backdrop first, then shape/mask, transmitted/refracted content, restrained body tint, edge/depth/highlights, and semantic content. The exact order may differ in native renderers. Keep icons, labels, focus indicators, hit targets, and accessibility identity crisp and stable unless foreground distortion is explicitly requested.

## Backdrop matrix

Review at least:

- detailed/high-frequency imagery;
- soft gradients or low-frequency photography;
- bright and dark backgrounds;
- high-contrast lines crossing behind the material;
- scrolling/moving content when supported.

A material that looks identical over every backdrop has not demonstrated meaningful background response.

## Fidelity tiers

| Tier | Definition | Do not claim |
|---|---|---|
| L0 | Translucent/tinted stable fallback | Blur, refraction, optical depth |
| L1 | Backdrop blur/translucency plus coherent contour and restrained highlights | Optical displacement; blur is not refraction |
| L2 | Visible backdrop displacement through a shape-aware surface mask | Fluid merging or dynamic liquid behavior unless separately demonstrated |
| L3 | L2 plus coherent interactive deformation/connection/merge/split behavior | Physically exact simulation or identical capability on all devices |

A feature may be partial. Report exactly which behaviors are demonstrated and which are approximated or absent.

## Reference evidence rules

A still image can support observations about silhouette, apparent layering, color, highlights, and apparent optical cues; it cannot prove the rendering method or motion quality. A video can support qualitative observations of continuity and interaction; approximate timestamps are not normative timing constants. Never infer a shader architecture or exact optical parameter from a screenshot.
