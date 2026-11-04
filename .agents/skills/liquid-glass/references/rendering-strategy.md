# Rendering strategy selection

Choose an implementation route only after completing [project discovery](project-discovery.md). There is no universal Liquid Glass rendering stack.

## Strategy comparison

| Strategy | Prefer when | Verify before use | Common limit/failure |
|---|---|---|---|
| Native material/compositor | The platform already provides a high-quality live material integrated with its compositor | Availability on minimum OS, tint/transmission controls, backdrop behavior, masking, accessibility settings | Native blur/translucency may not provide shape-aware displacement or fluid geometry |
| GPU shader pipeline | The project can safely sample a backdrop/render target and supports a suitable shader stage | Backdrop capture path, texture formats, shader language/version, precision, mask, render scale, synchronization, device support | Extra passes, bandwidth, overdraw, shader incompatibility, unstable clipping |
| Custom drawing/scene renderer | Existing app already owns a canvas, scene graph, vector renderer, or custom compositor | Whether background content can be sampled/re-rendered, mask and geometry facilities, batching | Drawing the rim without transmitting/displacing the real backdrop looks painted or flat |
| DOM/CSS composition | Browser UI and DOM semantics should remain primary | Browser support, stacking contexts, clipping, `backdrop-filter`, filter costs, scroll behavior | CSS blur is L1, not refraction; filters can clip, repaint, or create stacking issues |
| Layered fallback | Backdrop sampling/shaders are unavailable, not allowed, or too costly | Minimum capability, stable color/alpha, contrast, edge, focus and pressed states | Must be labeled L0/L1; cannot claim L2/L3 |
| Hybrid/native + custom | Native composition handles standard controls while a focused custom layer supplies missing optical/shape behavior | Synchronization, accessibility tree, hit testing, memory, z-order, lifecycle | Duplicate rendering/state systems and seams between surface and content |

## Decision process

1. **Keep a capable existing renderer.** Do not replace a project-wide render stack for one control. Prefer extending an existing material, effect, scene, or component abstraction.
2. **Use a native material when it meets the visual contract.** Confirm the actual behavior. A native blur can be excellent L1 without being refractive.
3. **Use a GPU path for real displacement when backdrop data and shader support are available.** Prefer bounded, low-pass-count rendering, texture reuse, and a shape-aware distortion field. Consider reduced-resolution intermediate targets only after checking visual quality and edge stability.
4. **Use custom geometry only as required.** Rounded rectangles, vector paths, signed-distance fields, metaballs/implicit surfaces, and mesh geometry are alternatives. Choose the simplest geometry that yields the intended silhouette and transition.
5. **Use DOM/canvas for web only when it fits the app.** DOM provides semantics and layout; Canvas/WebGL/WebGPU/SVG filters may provide visual effects when supported. Keep foreground controls accessible and separate from the optical background.
6. **Fall back honestly.** If no stable backdrop sample exists, use a translucent surface, optional blur, coherent rim, and controlled highlights. Document exactly what is missing.
7. **Keep the strategy adaptable.** Encapsulate platform-specific material logic behind a small local component/adapter only where the host architecture benefits. Do not introduce a universal API that erases meaningful platform capabilities.

## Shape and material pipeline

A practical conceptual pipeline may contain:

1. backdrop/content source;
2. evolving surface geometry and mask;
3. transmitted backdrop with shape/thickness-aware displacement, when supported;
4. body tint/absorption;
5. depth and edge response;
6. coherent specular/environment contribution;
7. crisp semantic foreground content.

Native compositors may combine these stages. Do not force this render graph when a native feature provides the same result more safely.

## Distortion and lighting guidance

- Distortion should depend on the curved surface and thickness, not a constant global offset.
- Clamp displacement and keep the entire effect inside the mask, including during resize and animation.
- Use a plausible normal/shape field when available; do not add arbitrary refraction vectors.
- Keep chromatic dispersion subtle, localized, and optional.
- Tie highlights and rim response to one coherent geometry/light state.
- Do not blur icons or labels unless requested; put foreground semantics above the refractive layer.

## Architecture boundaries

Keep these concerns separable when useful:

- semantic control/state and accessibility;
- hit testing/gesture handling;
- contour/geometry and morph state;
- backdrop sampling/distortion;
- lighting/material parameters;
- quality-tier selection and fallbacks.

This is a separation of responsibilities, not a requirement to create six classes or modules. Follow the host project's scale and conventions.
