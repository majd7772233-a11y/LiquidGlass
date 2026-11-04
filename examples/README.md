# Visual Reference Catalog

These files are visual references for the LiquidGlass material and interaction language. They are not implementation samples and do not prescribe a particular framework.

## Inspected still-image references

| File | What it visibly demonstrates | Useful review dimensions |
|---|---|---|
| [translucent-controls-and-sliders.png](references/controls/translucent-controls-and-sliders.png) | Floating transparent controls and pill/slider-like elements on a light grid background | Translucency, contour, subtle edge highlights, control silhouettes |
| [liquid-glass-interface-storyboard.png](references/storyboards/liquid-glass-interface-storyboard.png) | A contact sheet of interface states over photographic backgrounds | Background transmission, changing content behind glass, placement and state variation |
| [refractive-media-playback-controls.png](references/media/refractive-media-playback-controls.png) | Circular media buttons over a bright floral/sky background, with visible colored optical edges | Backdrop visibility, refraction cues, edge color, control depth |
| [organic-iridescent-liquid-glass-form.png](references/material/organic-iridescent-liquid-glass-form.png) | A large continuous organic form with soft pearlescent color and luminous edges | Organic silhouette, continuity, depth, iridescence, highlight gradients |

## Motion reference analyzed for Phase 1

The user-provided clip Liquid.mp4 was inspected locally to identify connected navigation surfaces, a growing/reconnecting search-like lobe, background-dependent optical response, and continuous shape changes. The video is not copied into this repository because its publication/provenance and permission for public re-hosting have not been established. The observations and approximate sequence are documented in [the reference matrix](../docs/reference-matrix.md).

## Additional references awaiting classification

The following original images are retained without descriptive claims because they could not be previewed during cataloging:

- [additional-concept-reference-01.png](references/unclassified/additional-concept-reference-01.png) — original Screenshot_64.png
- [additional-concept-reference-02.png](references/unclassified/additional-concept-reference-02.png) — original Screenshot_65.png
- [additional-concept-reference-03.png](references/unclassified/additional-concept-reference-03.png) — original Screenshot_66.png
- [additional-concept-reference-04.png](references/unclassified/additional-concept-reference-04.png) — original Screenshot_67.png

Inspect and reclassify these files before relying on them as evidence for a specific material behavior.

## Usage rules

- Compare implementations against the actual images and the written specification.
- Use the image most relevant to the feature under review; do not expect every example to show every property.
- Preserve source assets unless provenance, relevance, and licensing have been checked.
- Do not describe an effect as true refraction when the implementation only blurs or tints the background.


## Runnable reference implementations

These standalone examples are implementation evidence, distinct from the visual reference images above. Both own the background pixels they refract; neither assumes that a shader can read arbitrary DOM or native View content.

| Platform | Demo | Implemented tier | Main proof |
|---|---|---|---|
| Browser / WebGL2 | [WebGL2 reference lab](webgl2/README.md) | L2 + L3, with CSS L1/L0 fallback | An app-owned RGBA8 framebuffer is sampled/displaced by an SDF-shaped lens; a connected lobe morphs interactively. |
| Android Views / Java / OpenGL ES 2.0 | [Android GLES2 reference app](android-gles/README.md) | L2 + L3, with L0 framebuffer fallback | An app-owned GLES2 FBO feeds a refractive shader; native Android buttons and a SeekBar control the liquid shape and strength. |

### Reproducible build and capture

The [reference-demo workflow](../.github/workflows/reference-demos.yml) runs a headless Chromium/WebGL2 test and captures desktop/mobile screenshots. It also builds the Android debug APK, launches it on an API 35 emulator, verifies the app-owned FBO path through the renderer diagnostic, activates the connected-lens control through Android's accessibility tree, and uploads an emulator capture.

Artifacts are retained for 14 days per GitHub Actions run. These are reproducible CI/emulator captures, not proof of performance on every physical GPU. Real-device profiling, TalkBack review, and thermal/battery measurements remain in Phase 6.
