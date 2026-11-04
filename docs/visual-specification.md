# Liquid Glass — Visual Specification

**Status:** Phase 1 deliverable  
**Scope:** platform-neutral visual/material specification  
**Normative language:** MUST = required for a conforming implementation; SHOULD = strong default; MAY = optional and platform-dependent.

## 1. Purpose and interpretation

This specification defines the observable visual qualities that the LiquidGlass project is trying to reproduce. It is deliberately independent of programming language, operating system, UI framework, and rendering engine.

The target is an optical, translucent, depth-bearing surface that interacts with the content behind it. It may also deform and connect to nearby glass surfaces as the interface moves. It is **not** satisfied by adding a translucent fill, a blur, a thin white border, and a shadow.

The specification distinguishes three things:

1. **Observed reference behavior:** what is visibly supported by the still images and the supplied motion clip.
2. **Visual requirement:** what a result should look like and how it can be reviewed.
3. **Implementation choice:** the platform-specific technique used to produce that result.

Do not confuse an implementation technique with the visual requirement. A shader is not itself a quality target; a convincing, stable refractive surface is.

## 2. Visual priorities

When trade-offs are necessary, prioritize in this order:

1. Preserve interface meaning, legibility, and interaction.
2. Preserve the component's intended silhouette and spatial relationship to neighboring surfaces.
3. Make the backdrop visibly transmit through the material and, where supported, refract/distort through it.
4. Establish convincing thickness, curvature, edge response, and depth.
5. Add coherent specular/environment reflections.
6. Add restrained spectral dispersion or iridescence when the reference supports it.
7. Add secondary glows, decorative color, and other embellishments.

A lower-priority effect MUST NOT undermine a higher-priority one. Strong rainbow fringes, glow, or blur cannot compensate for a surface that does not transmit or distort its background.

## 3. Anatomy of the material

A Liquid Glass surface can be understood as a set of visual contributions. They need not be implemented as separate render passes.

### 3.1 Backdrop transmission

The content behind the surface remains recognizable through it. Transmission SHOULD vary spatially with the surface's thickness, curvature, tint, and edge region.

Review criteria:
- recognizable background features remain visible inside the surface;
- the material does not become a uniformly opaque white or colored card;
- any tint preserves enough local detail and contrast for the component's purpose;
- the appearance responds to the backdrop rather than looking identical over every image.

### 3.2 Refraction and distortion

The background is displaced as it passes through the curved surface. This may appear as bending, local magnification, compression, shifting, or warping of background features.

Review criteria:
- straight or high-contrast background features visibly change direction or position through the lens region;
- displacement follows the apparent shape/thickness rather than an arbitrary global offset;
- the distortion is clipped to the surface and does not leak outside its silhouette;
- changes remain stable during scrolling, resizing, and animation.

A blur alone is not refraction. A static color gradient alone is not refraction. When the platform cannot sample or approximate the backdrop, the result MUST be labeled as a fallback tier in Section 8.

### 3.3 Thickness, curvature, and depth

The surface should appear to have a curved boundary and finite thickness rather than a flat overlay.

Visual cues may include:
- a bright or dark contour that changes around the silhouette;
- a narrow edge band and a softer inner transition;
- shading that suggests a convex lens, rounded volume, or varying thickness;
- slight magnification or displacement near the perimeter;
- separation between the glass surface and the content it contains.

Review criteria:
- the viewer can read the surface boundary against both dark and bright backgrounds;
- edge thickness is coherent around rounded corners and changing contours;
- the body and edge do not look like unrelated stacked strokes;
- the surface does not appear uniformly flat.

### 3.4 Reflection and specular response

Highlights should reinforce surface curvature and a plausible light environment. A result may use environment reflections, screen-space approximations, analytic highlights, or platform-native material lighting.

Review criteria:
- broad soft reflections and tighter highlights have a coherent relationship to the shape;
- highlights do not obscure important text or icons;
- the highlight direction and intensity remain coherent as the surface moves;
- the same static highlight is not blindly stamped onto every shape if the result makes the material look painted.

### 3.5 Edge response

The edge is a key optical cue. It may combine a Fresnel-like rim, a bright/dark transition, subtle inner shading, and limited colored separation.

Review criteria:
- the rim is strongest where the apparent view angle/curvature calls for it, not equally bright around every pixel;
- it remains visible but not cartoonishly outlined;
- it adapts to the brightness and color of the backdrop;
- it does not create a hard halo detached from the surface.

### 3.6 Spectral dispersion and iridescence

Chromatic separation and pearlescent color are optional accents, not the base material.

Use them:
- near high-curvature or high-contrast optical regions;
- with restrained offsets and limited spatial extent;
- when consistent with the supplied reference or intended lighting.

Avoid:
- continuous rainbow outlines on every edge;
- exaggerated RGB splitting that damages icon/text readability;
- arbitrary animated hue cycling unrelated to surface motion or lighting.

### 3.7 Surface body and tint

The surface may have a subtle neutral, cool, warm, or context-derived tint. Tint SHOULD preserve backdrop detail and SHOULD vary gently with thickness or lighting.

Avoid a uniform opaque fill. Avoid using color as a substitute for optical depth.

## 4. Geometry and shape families

The material should be reusable across different silhouettes. Do not force all components into one capsule.

### 4.1 Capsule and pill lens

A long rounded surface used for navigation, sliders, search, and compact control groups. It should retain a coherent optical profile through the straight-ish center and curved ends.

### 4.2 Circular lens or bubble

A compact circular/oval surface used for a single action, search affordance, or floating control. The lens should have a readable center and a continuous edge.

### 4.3 Connected control group

Several actions sharing one continuous material body. Internal icons remain distinct and aligned while the outer contour can flow around them. Gaps between actions are not automatically physical gaps in the glass.

### 4.4 Attached lobe or protrusion

A circular or rounded region that grows out of a bar or larger surface. The connection should be smooth and intentional, not a circle placed over a rectangle.

### 4.5 Organic continuous form

A blob, joined-lobe, wave, or asymmetric surface whose silhouette changes over time. Curvature and surface lighting should remain coherent across the entire connected form.

### 4.6 Slider and track

A track can remain a glass body while its thumb is a raised lens. Filled/unfilled regions must be legible without losing the material response. The thumb should feel attached to or moving within the track.

## 5. Component composition and content

A common conceptual composition is:

1. the actual backdrop;
2. a shape/coverage representation for the material;
3. a transmitted/refracted view of the backdrop, clipped to the shape;
4. a subtle body tint or absorption contribution;
5. depth, edge, and specular contributions;
6. semantic UI content such as icons, labels, and focus indicators.

This is a conceptual order, not a mandated render graph. Native materials may combine these contributions in another order.

Foreground text and icons SHOULD remain crisp and geometrically stable. Do not refract a label merely because the glass behind it refracts the background. Keep semantic content above the optical layer unless a deliberate effect is being demonstrated. Maintain hit targets and focus regions independently of decorative contour changes.

## 6. Background sensitivity

The material must be reviewed against more than one kind of backdrop:

- detailed, high-frequency imagery such as foliage, flowers, fabric, or fine text;
- low-frequency gradients and soft photographic blur;
- bright backgrounds;
- dark backgrounds;
- high-contrast edges crossing behind the surface;
- moving or scrolling content, where supported.

The material SHOULD visibly adapt to these backdrops. A static overlay that looks identical regardless of underlying content is insufficient evidence of refraction.

## 7. Visual states

At minimum, review the applicable component in:
- idle/rest;
- pointer hover where available;
- keyboard focus;
- pressed/active;
- dragged or continuously manipulated;
- disabled;
- settled after a transition;
- reduced-motion/static presentation.

Different states MAY alter contour, depth, highlight, tint, or scale. State changes MUST not make the material flicker, lose its clipping, or obscure the component's semantic state.

## 8. Capability and fidelity tiers

Use these labels in documentation and reviews. They describe observed capability, not marketing quality.

| Tier | Name | Minimum behavior | What it does not prove |
|---|---|---|---|
| L0 | Translucent fallback | A stable tinted/translucent surface with readable content | No meaningful blur, refraction, or optical depth is implied |
| L1 | Blurred glass fallback | Backdrop blur/translucency plus coherent contour and restrained highlights | Blur is not refraction; background geometry is not optically displaced |
| L2 | Refractive glass | Backdrop sampling or an equivalent technique visibly displaces background content through a curved/thickness-aware surface | Does not by itself prove fluid morphing or fully dynamic lighting |
| L3 | Dynamic liquid glass | L2 behavior plus coherent shape deformation/connection/merging and interaction-responsive surface behavior | Does not imply physically exact simulation or identical capability on every device |

A platform may support some L2/L3 features but not others. Report the achieved behaviors individually as well as the highest tier. A blur-only implementation MUST NOT be called L2 or L3.

## 9. Platform-neutral implementation constraints

The visual result is the invariant; the rendering mechanism is selected after inspecting the target project.

Potential implementation families include native compositor/material effects, GPU shaders, screen-space backdrop capture, custom drawing, vector/implicit geometry, canvas/DOM effects, scene renderers, or layered native components. None is mandatory.

The implementation MUST:
- inspect actual target capabilities before choosing a path;
- preserve the host project's language, architecture, and minimum OS/device targets;
- use a stable clipping/masking strategy;
- keep interactive and semantic content functional;
- define a lower-cost fallback when required facilities are unavailable;
- document which optical properties are genuine, approximated, or absent.

## 10. Visual review checklist

A reviewer should answer each item with Pass, Partial, Fail, or Not Applicable, and attach a screenshot/video where possible.

- [ ] The silhouette matches the intended control/shape family.
- [ ] The backdrop is visible through the material.
- [ ] Backdrop geometry is actually distorted when claiming refraction.
- [ ] Distortion follows shape/thickness and stays inside the mask.
- [ ] Curvature and depth are readable on bright and dark backdrops.
- [ ] Edge response is coherent and not a detached outline.
- [ ] Reflections reinforce form without obscuring content.
- [ ] Spectral color is restrained and reference-appropriate.
- [ ] Foreground text/icons remain crisp and legible.
- [ ] The surface remains stable during state changes and movement.
- [ ] The result is honestly labeled L0, L1, L2, or L3.
- [ ] Platform limits and fallback behavior are documented.

A visual review is not complete merely because the surface looks attractive on one background.
