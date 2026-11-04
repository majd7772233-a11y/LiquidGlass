# Worked workflow: browser DOM project

**Purpose:** exercise project discovery and an honest web-specific fallback decision. This is an L1 example, not a claim that CSS backdrop blur recreates the supplied refractive video.

## 1. Discovery evidence

The automated package test creates a temporary browser fixture containing:

- `package.json` with a Vite development dependency;
- `index.html` and `src/main.ts` browser entry points;
- `src/style.css` with DOM layout and CSS material styling;
- no native mobile manifest or custom GPU/render pipeline.

The correct family is **web DOM/browser**. Confirm the real browser support matrix and app build commands before changing a real project; do not infer WebGPU/WebGL availability merely because it is a browser app.

## 2. Strategy decision

For this intentionally small fixture, preserve DOM semantics and use a CSS layered surface with `backdrop-filter` when supported. This demonstrates a stable **L1 blur fallback**. It does not displace background geometry, so it is not L2. Do not add a WebGL/WebGPU dependency until the task explicitly requires L2/L3 and the project can own the backdrop texture, masks, shader lifecycle, and performance budget.

## 3. Minimal implementation shape

A browser implementation may use a semantic button as the control and a pseudo-element or inner visual layer for the material. For example:

```html
<button class="glass-control" type="button" aria-label="Play">
  <span aria-hidden="true">▶</span>
</button>
```

```css
.glass-control {
  position: relative;
  isolation: isolate;
  border: 1px solid rgb(255 255 255 / 0.42);
  border-radius: 999px;
  color: white;
  background: rgb(255 255 255 / 0.12);
  box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.34),
              0 8px 24px rgb(0 0 0 / 0.16);
}

@supports (backdrop-filter: blur(12px)) {
  .glass-control {
    background: rgb(255 255 255 / 0.16);
    backdrop-filter: blur(12px) saturate(1.15);
    -webkit-backdrop-filter: blur(12px) saturate(1.15);
  }
}

@media (prefers-reduced-motion: reduce) {
  .glass-control { transition: none; }
}
```

This snippet is intentionally a fallback baseline. It does not contain a refraction shader or liquid morph system. Production work must add visible focus/pressed styles and confirm text/icon contrast over real backgrounds.

## 4. Validation and report

- Serve/build using the fixture's actual scripts (do not install dependencies just to validate static package metadata).
- Inspect in each supported target browser over a detailed image and a flat bright/dark background.
- Confirm the blur stays clipped and foreground icon remains crisp.
- Test keyboard focus, activation, disabled state, and reduced motion.
- Report **L1** only if backdrop blur is visibly working; otherwise report L0. State clearly that geometric backdrop displacement and fluid morphing were not implemented.

## 5. End-to-end workflow test

The package test runner creates a temporary web project, runs the read-only inventory helper against it, checks that web entry/build evidence is discovered, and verifies this trace covers discovery → strategy → implementation → validation → report without labeling blur as refraction.
