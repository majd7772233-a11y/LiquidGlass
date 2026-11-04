# Worked workflow: Windows App SDK / WinUI Composition

**Purpose:** validate composition-source boundaries before choosing a desktop glass renderer.

## Project profile to record

- Windows App SDK/Windows SDK and target OS/package versions.
- XAML visual tree, SpriteVisuals, composition surfaces, and window lifecycle.
- Existing image/texture sources and which UI layers are composed separately.
- DPI/monitor scaling, GPU, and graphics-resource ownership.

## Strategy decision

Microsoft.UI.Composition effect brushes operate on supplied images/surfaces and are used with SpriteVisuals or XAML composition brushes. The documented effect graph can reference existing surfaces/textures, but not the output of another composition tree.

Therefore:
- use supported effect-graph operations on app-owned textures when they meet the requirement;
- do not assume arbitrary sibling XAML elements or other windows are available as a shader input;
- use a custom Direct3D/Win2D render target if actual scene-color displacement is required and the app can own that rendering boundary;
- keep XAML controls as the semantic/input layer.

Do not assume a Gaussian blur operation is part of every supported Composition effect set. Inspect the API/package version and supported effects list for the target framework.

## Minimal integration plan

Create a bounded SpriteVisual for the material, feed it a known CompositionSurfaceBrush/texture, and animate its supported effect properties. Keep text, glyphs, focus, and control actions in XAML above the material. Add a separate app-owned texture path only when L2 is explicitly required.

## Reproducible validation

1. Build the project for its actual Windows App SDK target.
2. Test that the expected source image/texture is used; verify no sibling composition tree is assumed.
3. If L2 is implemented, displace a high-contrast scene feature through a mask.
4. Test per-monitor DPI, resize, minimize/restore, occlusion, device loss, keyboard focus, UI Automation, high contrast, and reduced motion.
5. Record L0/L1/L2/L3 only from observed output.

**Expected baseline:** source-texture effect only; L2 is not established until displacement of app-owned backdrop pixels is demonstrated.

## Official reference

- Microsoft WinUI Composition effects: https://learn.microsoft.com/en-us/windows/apps/develop/composition/composition-effects
