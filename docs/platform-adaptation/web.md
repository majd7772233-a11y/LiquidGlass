# Web DOM and Browser Graphics

## Choose the path by backdrop ownership

### DOM-only UI: L1 fallback

Use a semantic DOM control with CSS backdrop-filter when the requirement is blur/translucency, not geometric refraction. Keep a transparent background so the filtered backdrop remains visible. Check stacking contexts and the nearest backdrop root: an ancestor with effects such as opacity, filter, mask, or another backdrop-filter can change which pixels are available to the child filter.

Example baseline:

~~~css
.glass-control {
  color: white;
  background: rgb(255 255 255 / 0.14);
  border: 1px solid rgb(255 255 255 / 0.38);
  border-radius: 999px;
  backdrop-filter: blur(14px) saturate(1.2);
  -webkit-backdrop-filter: blur(14px) saturate(1.2);
}
~~~

This is L1 only when blur visibly works. It is not a refraction shader.

### App-owned canvas: L2 candidate

For real backdrop displacement, render the backdrop into a texture owned by the application. A WebGL2 or WebGPU pipeline can then sample neighboring positions through a mask/normal field and composite crisp semantic DOM controls above it.

Before coding, verify:
- the background is actually rendered by the app-owned canvas/render pipeline;
- cross-origin image/video sources remain origin-clean or use a permitted texture path;
- device-pixel ratio, resize, scrolling, clipping, and coordinate transforms agree between DOM and canvas;
- WebGPU exists and can request an adapter/device on the target browser, and the site is in a secure context when required;
- a WebGL2 path or L1 fallback exists where WebGPU is unavailable.

Do not attempt to turn arbitrary DOM pixels into a shader texture by assumption. CSS backdrop-filter filters the painted backdrop; it does not expose a general-purpose sampled texture to application shader code.

## Version and support notes

MDN marks backdrop-filter as Baseline 2024, while noting that older browsers/devices may not support it. MDN marks WebGPU as Limited availability and secure-context-only in supporting browsers. Therefore feature-detect rather than keying decisions to "modern browser" labels.

Useful checks:
- CSS.supports("backdrop-filter", "blur(1px)")
- navigator.gpu presence, then requestAdapter() and requestDevice() with rejection handling
- actual draw/compile of the required shader and successful composition with the app scene

A successful API-presence check is not proof that the required effect can run at the target's performance budget.

## Shape and motion

Use CSS/SVG geometry for straightforward pill/circle masks. For organic connected lobes and coherent moving refraction, drive the mask and distortion from one GPU shape state (for example an SDF/metaball field) while DOM owns the semantic buttons. Keep animation bounded and reduce/suppress it under prefers-reduced-motion.

## Validation workflow

1. Test the DOM-only L1 path over detailed and plain bright/dark backdrops.
2. Confirm blur is clipped at the intended rounded contour and is not cut off by an unexpected backdrop root.
3. If L2 is required, validate the texture source and show visibly displaced high-contrast lines through the lens.
4. Test with WebGPU disabled/unavailable and verify the fallback.
5. Test keyboard focus, keyboard activation, reduced motion, resize, device-pixel-ratio changes, scrolling, and browser zoom.

## Official references

- [MDN: backdrop-filter](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/backdrop-filter)
- [MDN: WebGPU API](https://developer.mozilla.org/en-US/docs/Web/API/WebGPU_API)
