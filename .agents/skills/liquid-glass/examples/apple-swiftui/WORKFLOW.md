# Worked workflow: Apple UIKit / SwiftUI / Metal

**Purpose:** distinguish native material blur from shader distortion and a true app-owned refractive backdrop.

## Project profile to record

- Xcode/Swift toolchain and exact deployment target.
- SwiftUI/UIKit view hierarchy and any UIViewRepresentable/AppKit-backed views.
- Whether the background is a SwiftUI-rendered layer, UIKit view, video/platform view, or Metal texture.
- Available Metal device and the render target/lifecycle owner.

## Strategy decision

- Start with SwiftUI Material or UIKit UIVisualEffectView when native system blur is sufficient. This is L1, not L2.
- SwiftUI Shader modifiers (colorEffect, distortionEffect, layerEffect) operate on the view/layer they filter. Do not assume they can sample unrelated content behind the view.
- For L2, supply a texture from a renderer the app owns and implement the refractive composite in Metal or a supported shader path. Preserve native semantic controls above it.

## Minimal native baseline

~~~swift
Capsule()
    .fill(.ultraThinMaterial)
    .overlay {
        Capsule().stroke(.white.opacity(0.35), lineWidth: 1)
    }
~~~

This is a native translucent material baseline, not a custom refractive shader. Report L1 only if the actual platform material visibly blurs the backdrop; otherwise report L0.

## Reproducible validation

1. Build with the project's actual Xcode version and deployment target.
2. Verify native material appearance over detailed, bright, and dark scenes.
3. If using distortionEffect, prove which view's pixels are being distorted.
4. For L2, display a high-contrast grid behind the app-owned texture and confirm displacement is inside the lens mask.
5. Test UIKit/AppKit representable boundaries, VoiceOver, Reduce Motion, Dynamic Type, Increase Contrast, memory, and repeated transitions.

**Expected baseline:** L1 at most. The workflow is not a compiled app or evidence of parity; the project build and visual capture are required for that claim.

## Official references

- UIVisualEffectView: https://developer.apple.com/documentation/uikit/uivisualeffectview/
- SwiftUI Shader: https://developer.apple.com/documentation/swiftui/shader
- SwiftUI distortionEffect: https://developer.apple.com/documentation/swiftui/view/distortioneffect(_:maxsampleoffset:isenabled:)
- Metal: https://developer.apple.com/documentation/metal
