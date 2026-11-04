# Apple Platforms: UIKit, SwiftUI, and Metal

Use the native material stack when it meets the requirement. Move to a custom GPU pipeline only when the required behavior exceeds what the native effect actually exposes.

## UIKit material route

UIKit UIVisualEffectView can apply a UIBlurEffect or vibrancy effect to content layered behind the effect view. This is a reliable native path for system-style blur/translucency, but do not describe it as a custom shape-aware refraction renderer.

Place semantic controls in the effect view's contentView as documented by Apple. Follow Apple's guidance about not arbitrarily lowering alpha on the effect view, since compositing the entire view hierarchy offscreen can change performance and appearance.

## SwiftUI shader route

SwiftUI Shader functions can be used with colorEffect, distortionEffect, and layerEffect. Apple describes distortionEffect as a geometric distortion of the pixels of the view to which the modifier is applied, and layerEffect as a filter on a raster layer created from that view.

Important boundary: these modifiers do not mean that any view can automatically sample every unrelated view behind it. They operate on the filtered view/layer. Verify how the target hierarchy is rasterized, especially where UIKit/AppKit-backed content is involved.

For native blur, SwiftUI Material styles or UIKit visual effects are the lower-risk route. For L2, supply the backdrop from an app-owned renderer or Metal texture, then render the optical layer and semantic controls with explicit coordination.

## Metal route

Metal provides direct GPU access for rendering and compute. It is appropriate when the app owns a render graph or can safely provide a background texture. It is not a general-purpose API for capturing arbitrary pixels from another app/window or protected content.

Keep the shader input/output format, color space, texture lifetime, render-pass ordering, and display scale explicit. Do not introduce Metal just to reproduce a blur that a native material already provides adequately.

## SwiftUI / UIKit integration checklist

- Read the Xcode project deployment target and SDK versions.
- Check availability for every SwiftUI/UIKit API used; compile against the actual deployment target.
- Identify whether the backdrop belongs to SwiftUI, UIKit, a platform view, video, or a Metal surface.
- Keep accessibility labels, traits, VoiceOver, focus, Dynamic Type, Reduce Motion, and Increase Contrast in the semantic UI tree.
- Test SwiftUI representable boundaries and UIKit-backed views within shader-filtered layers; some views may not render as expected into a filtered layer.
- Keep the shape and optical state synchronized during morphs; do not distort labels unless explicitly required.

## Validation workflow

1. Compare UIVisualEffectView or SwiftUI material alone against the required baseline. Label blur-only output L1.
2. If using SwiftUI distortionEffect/layerEffect, verify which view pixels are actually being filtered.
3. For L2, demonstrate that high-contrast features of the app-owned backdrop move through the lens, not just that the glass shape itself warps.
4. Check the oldest supported iOS/iPadOS/macOS deployment target, light/dark appearance, VoiceOver, Reduce Motion, text scaling, and memory/performance.
5. Record which native material behaviors differ by OS version.

## Official references

- [UIKit UIVisualEffectView](https://developer.apple.com/documentation/uikit/uivisualeffectview/)
- [SwiftUI Shader](https://developer.apple.com/documentation/swiftui/shader)
- [SwiftUI distortionEffect](https://developer.apple.com/documentation/swiftui/view/distortioneffect(_:maxsampleoffset:isenabled:))
- [SwiftUI graphics and rendering modifiers](https://developer.apple.com/documentation/swiftui/view-graphics-and-rendering)
- [Metal](https://developer.apple.com/documentation/metal)
