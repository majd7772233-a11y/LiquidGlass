# Worked workflow: Flutter

**Purpose:** distinguish BackdropFilter's painted-content input from an isolated widget filter, and record the actual renderer backend.

## Project profile to record

- Flutter SDK version and target OS list.
- Renderer backend for each target (Impeller/Skia where applicable).
- Widget tree and clip ancestry around the glass.
- PlatformViews, opacity/saveLayer ancestors, and backdrop grouping.
- Whether ImageFilter.shader is used and whether the target renderer supports it.

## Strategy decision

- ClipRRect + BackdropFilter with ImageFilter.blur is a practical L1 route. The filter applies to previously painted content within the parent/ancestor clip.
- BackdropFilter can be expensive. Use a shared BackdropKey only for surfaces that truly share compatible input; overlapping regions with one key can produce unexpected results.
- Flutter's custom fragment shaders are loaded through FragmentProgram. The documentation limits shader-backed ImageFilter usage to the Impeller backend. Check and test the backend on each platform.
- Consider ImageFilter.shader as an L2 candidate only after confirming the shader actually displaces the painted backdrop on the target backend. Keep semantic Flutter widgets above the optical layer.

## Minimal L1 baseline

~~~dart
ClipRRect(
  borderRadius: BorderRadius.circular(28),
  child: BackdropFilter(
    filter: ImageFilter.blur(sigmaX: 12, sigmaY: 12),
    child: const SizedBox(width: 240, height: 64),
  ),
)
~~~

This is blur, not refraction. Report L1 only if the blur is visible; otherwise report L0.

## Reproducible validation

1. Run flutter analyze and the target build.
2. Record Flutter version and renderer backend for each target platform.
3. Verify the filter is clipped to the intended shape; inspect saveLayer/Opacity ancestors.
4. Test platform views and overlapping BackdropFilters.
5. If using ImageFilter.shader, run on the exact Impeller backend and prove visible displacement of a grid behind the material.
6. Test Semantics, Focus, text scaling, VoiceOver/TalkBack, reduced motion, scrolling, and frame cost.

**Expected baseline:** L1. L2 is conditional on shader-backed backdrop displacement being demonstrated on that specific backend.

## Official references

- Flutter BackdropFilter: https://api.flutter.dev/flutter/widgets/BackdropFilter-class.html
- Flutter fragment shaders: https://docs.flutter.dev/ui/design/graphics/fragment-shaders
