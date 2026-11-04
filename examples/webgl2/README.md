# WebGL2 refractive Liquid Glass demo

A dependency-light, runnable browser reference implementation. It renders its own animated high-contrast scene into an off-screen WebGL2 texture, then samples and displaces those scene pixels through a rounded lens mask. Semantic HTML controls are composited above the optical surface and remain sharp.

## Run

Requires Node.js 20+ and npm.

```bash
cd examples/webgl2
npm install
npm run serve
```

Open [http://127.0.0.1:4173](http://127.0.0.1:4173). No remote image, API key, or external runtime service is required.

## Demonstrated behavior

- **L2 — refractive glass:** the background is an application-owned framebuffer texture. The glass shader samples displaced neighboring pixels through a rounded-rectangle/connected-lobe signed-distance mask. The background grid/rings make displacement observable. It is not CSS backdrop blur.
- **L3 — dynamic liquid glass:** the “Connect the lens” control animates a smooth-union lobe into/out of the primary lens. One SDF drives mask, refraction normal, and edge response.
- **Interactive semantics:** native buttons, range input, accessible names, keyboard focus, pressed states, and reduced-motion support remain in HTML above the shader.
- **Fallback:** when WebGL2 or the framebuffer path cannot initialize, the page switches to a CSS backdrop-blur L1 treatment and clearly reports the fallback. It does not call this L2.

## Rendering pipeline

1. Render a moving procedural scene to an RGBA8 off-screen texture.
2. Draw a full-screen material pass that computes a rounded-box/connected-lobe distance field.
3. Estimate its normal from bounded central differences and displace actual scene-texture samples.
4. Add restrained spectral separation, edge response, and specular highlights.
5. Draw HTML controls above the canvas in their own semantic/accessibility layer.

The render target is capped at 1.65 device-pixel ratio to bound fragment and memory cost. Shader loops are fixed/bounded and the scene is app-owned; arbitrary DOM or cross-origin pixels are not captured.

## Validation

```bash
npm install
npx playwright install chromium
npm test
```

The browser smoke test requires WebGL2 (SwiftShader is used in headless CI). It verifies renderer initialization, the morph state, playback state, range input, and creates desktop/mobile screenshots under `artifacts/`.

## Known visual limits

This is a compact analytical reference, not a full physical-optics simulator. It uses a procedural scene rather than the original reference video, estimates normals from an SDF, and approximates reflection/dispersion. It demonstrates actual backdrop displacement (L2) and a connected animated shape (L3), but makes no pixel-parity or physical-accuracy claim. Test on target GPUs and browsers before shipping it in a production app.
