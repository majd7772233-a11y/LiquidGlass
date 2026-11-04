# Liquid Glass — Interaction and Motion Specification

**Status:** Phase 1 deliverable  
**Scope:** platform-neutral input, state, shape-transition, and motion behavior.

## 1. Intent

Liquid Glass should behave like a responsive physical surface while remaining a reliable interface. Shape movement, optical response, and control semantics are related but separate concerns:

- the **control** owns its action, value, focus, and accessibility semantics;
- the **shape** owns the visible contour and connected regions;
- the **material** owns transmission, refraction, depth, and reflection;
- the **motion system** coordinates how shape and material change over time.

A visual deformation MUST NOT move the actual hit target unexpectedly or change the action represented by a control.

## 2. Interaction state model

Use only states relevant to the target platform and component. The following model is a reference state vocabulary.

| State | Entry condition | Visual response | Exit condition |
|---|---|---|---|
| Rest | No active input | Stable contour, baseline depth and lighting | Hover, focus, press, drag, disable |
| Hover | Pointer enters an interactive region | Optional subtle lift, highlight/parallax response | Pointer leaves or press begins |
| Focus | Keyboard/controller focus enters | Clear focus indication; may gently alter rim or lift | Focus moves or control disables |
| Pressed | Valid press begins | Small compression or lift response; highlight changes coherently | Release, cancel, drag, disable |
| Dragging | Continuous pointer/touch manipulation | Shape follows input with bounded lag/deformation | Release or cancel |
| Settling | Input ends while shape returns or snaps | Damped return to target geometry | Motion falls within rest tolerance |
| Merging | Two surfaces/regions become one connected body | Gap closes and contour forms a smooth neck | One connected body is reached |
| Splitting | One connected body separates into regions | Neck narrows and surfaces detach without a visual pop | Separate bodies reach target geometry |
| Disabled | Control cannot be activated | Reduced emphasis; action is not suggested as available | Enabled |
| Reduced motion | System/user preference requests reduced motion | Static or minimal transition that preserves state feedback | Preference changes |

Disabled and reduced-motion are modifiers that may coexist with a stable layout; they need not be implemented as literal animation states.

## 3. State and semantic invariants

- The semantic action, selected value, and accessibility identity MUST remain stable through visual morphs.
- Focus and pressed state MUST be perceivable without relying on color, blur, or motion alone.
- Touch, pointer, keyboard, and controller input MUST use the host platform's normal interaction model.
- A decorative lobe MUST NOT intercept input intended for a neighboring action.
- The hit region SHOULD remain predictable even when the visible boundary deforms.
- Release/cancel behavior MUST be deterministic; cancellation must not accidentally activate an action.
- Motion MUST be interruptible. A new input or state change must not wait for an unrelated animation to finish.
- Foreground icons and labels SHOULD stay crisp and remain associated with their controls as the glass contour changes.

## 4. Shape and material motion

### 4.1 Continuous contour

When a glass shape changes, its boundary should move continuously. Avoid hard cuts, sudden jumps, isolated overlapping circles, and visible seams where surfaces connect.

When two regions merge, their connected contour should form a smooth transition. When they split, the connection should narrow and separate coherently. The material response (edge, thickness, highlight, refraction mask) must follow the same evolving geometry.

### 4.2 Control groups and attached bubbles

A long control bar may grow a circular/rounded lobe for a selected or expanded action. The lobe should:
- emerge from the relevant portion of the existing surface;
- maintain a smooth neck/fillet at the connection;
- preserve neighboring action alignment;
- keep the active icon/label readable;
- retract or detach without a sudden contour pop.

The supplied motion reference shows a search affordance expanding from, or reconnecting with, a horizontal navigation surface. Treat this as a useful example of connected-lobe behavior, not a mandatory layout for every app.

### 4.3 Input-following deformation

A draggable or pointer-responsive surface may lag slightly behind input to communicate softness. The response SHOULD:
- follow the active input predictably;
- have bounded displacement and bounded curvature;
- avoid oscillation under high-frequency input;
- settle at a stable target when released;
- avoid changing unrelated layout geometry.

### 4.4 Material continuity

During shape motion, update the mask, transmitted backdrop, distortion field, edge response, and highlights from a coherent shape state. If only the silhouette moves while the refraction/highlight stays behind, the material will appear detached.

## 5. Motion model

Use a damped spring, critically/over-damped interpolation, or another continuous model suited to the platform. Spring dynamics are often useful for soft settling, but they are not mandatory.

The model SHOULD support:
- position and velocity continuity across retargeting;
- configurable stiffness/response and damping;
- clamped geometry and maximum displacement;
- a clear settling threshold;
- deterministic completion/cancellation;
- stable behavior at variable frame rates.

Do not restart every transition from zero velocity if doing so creates visible discontinuities. Do not allow underdamped overshoot to make controls collide, overlap labels, leave their hit areas, or oscillate indefinitely.

### Suggested starting durations

These are tuning starting points, not measured timings from the reference clip and not universal rules:

| Transition | Suggested initial range |
|---|---:|
| Small press/focus response | 100–220 ms |
| Short control-state change | 140–260 ms |
| Connected-lobe or pill morph | 220–480 ms |
| Larger surface reconfiguration | 350–650 ms |

Use the shortest duration that remains legible and feels continuous. Spring-based implementations may be duration-driven only for the purpose of setting expectations; actual settling time can be derived from damping and the completion threshold.

## 6. Motion and optical response

Shape and optical behavior must read as one material:

- Edge thickness and curvature response follow the current geometry.
- Highlights move or deform coherently with the surface, not independently.
- Backdrop displacement remains clipped and tracks the evolving contour.
- Chromatic separation, if used, remains bounded during rapid movement.
- Any parallax is subtle and input-responsive, not random.
- The background itself should not jitter when only the glass moves.

Avoid animating every optical parameter independently. Prefer a small number of shared shape/light/material parameters so the surface remains coherent.

## 7. Reduced motion and accessibility

When reduced motion is requested:
- suppress large shape morphs, spring overshoot, parallax, and nonessential floating;
- use a quick fade, restrained scale, or immediate stable-state change as appropriate;
- preserve clear focus, selected, pressed, and disabled feedback;
- do not hide a control or make a state inaccessible because its animated transition was removed.

The component must still work with keyboard navigation, screen readers, touch, and high-contrast/transparency-reduction settings supported by the platform.

## 8. Performance and interruption

- Avoid full-screen recapture or expensive multi-pass effects on every tiny input event if the platform can reuse a suitable frame or lower-resolution representation.
- Avoid per-frame allocation and unbounded geometry/shader work.
- Coalesce pointer/touch updates when appropriate, without making interaction feel delayed.
- Pause or reduce nonessential motion when the surface is off-screen or the app is inactive.
- Provide a lower-cost stable state when the required GPU or compositor feature is unavailable.
- A transition must never block input, scrolling, navigation, or accessibility services.

## 9. Motion review checklist

- [ ] Rest, focus, pressed, dragging, release, and settled states are visually distinct where applicable.
- [ ] A transition can be interrupted and retargeted without a jump.
- [ ] Connected surfaces form a continuous contour with no obvious seam.
- [ ] Splitting and merging do not pop or leave ghost fragments.
- [ ] The glass mask, refraction, rim, and highlights follow the same geometry.
- [ ] Icons, labels, hit targets, and accessibility semantics remain stable.
- [ ] Motion is bounded and settles without jitter or uncontrolled overshoot.
- [ ] Reduced-motion behavior preserves the same usable states.
- [ ] Frame rate and input responsiveness remain acceptable on target hardware.
- [ ] The final resting shape is stable across repeated interactions.
