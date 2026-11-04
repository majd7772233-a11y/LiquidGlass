# Liquid Glass Studio workflow contracts

These are the seven Studio operations required by Phase 4. They are **agent workflow contracts**, not separately deployed MCP endpoints. The implementation uses the GitHub connector bound in `.app.json`, supplied reference assets, and packaged shared knowledge.

Every operation returns evidence, confidence/unknowns, and actionable outcomes. For write workflows it also returns exact changed paths, branch/commit/PR references, and verification status.

## 1. `analyze_reference`

**Purpose:** inspect supplied screenshots or accessible video frames.

**Input:** one or more supplied visual assets/frames; optionally target platform, reference intent, and named component/screen.

**Output:** observations grouped by transmission, distortion/refraction, surface geometry, thickness/depth, edge response, specular lighting, spectral effects, shape motion, and interaction; each observation is labelled `observed`, `inferred`, or `unknown`, with missing evidence and unresolved ambiguities.

**Rules:** describe visible evidence only. A screenshot cannot prove the original API, shader, or physics. Do not invent missing frames or infer implementation details that are not visible.

## 2. `create_visual_brief`

**Purpose:** turn reference observations into an implementation-ready brief.

**Input:** reference observations or a textual visual goal; optional fidelity target, platform family, constraints, and component states.

**Output:** material anatomy, geometry, backdrop behavior, motion/state model, foreground/semantic requirements, target fidelity L0–L3, acceptance checks, unknowns, and validation plan.

**Rules:** separate mandatory visual criteria from optional embellishment; preserve confidence and unknowns.

## 3. `diagnose_project`

**Purpose:** inspect a user-authorized GitHub project before changing it.

**Input:** repository owner/name; optional branch/ref, target folder/module, screen/component, and constraints.

**Output:** repository/branch identity, project tree evidence, language/framework/build system, rendering/backdrop ownership, dependencies, minimum platform/device requirements, accessibility/performance constraints, target files, and tests/CI workflows found in source.

**GitHub adapter:** read repository metadata, branch/tree, instructions, manifests/build files, relevant source files, and connected workflows. For Android, keep effective minSdk and supplied runtime API evidence separate.

## 4. `select_strategy`

**Purpose:** select an implementation that matches the brief and actual project.

**Input:** visual brief and project diagnosis; optional fidelity/compatibility priorities and allowed dependencies.

**Output:** recommended renderer and rationale; viable alternatives; API/dependency requirements; backdrop data path; shape/mask/motion plan; fallback by supported runtime; accessibility/performance risks; test matrix; expected tier and evidence needed to claim it.

**Rules:** compare native, existing-library, custom GPU/drawing, and fallback routes. Preserve an existing Android minSdk. For a new Android project with no specified minimum, ask before selecting/writing it. Blur is not refraction; L2 requires visible shape-aware displacement of actual backdrop samples; L3 also needs demonstrated coherent dynamic behavior.

## 5. `implement_glass`

**Purpose:** make requested changes in the connected repository, not merely produce a code sample.

**Input:** repository, target branch/branch strategy, approved visual brief and scope; optional target paths, dependency policy, PR preference, and validation depth.

**Output:** changed paths, concise implementation summary, branch, commit SHA, PR URL if created, actual test/workflow results, and exact unverified gaps.

**GitHub adapter:** inspect the branch head immediately before writing. For a narrow safe change use a guarded file update. For coordinated multi-file work, create an isolated branch and atomic Git tree/commit, then update the ref with an expected-head check. Trigger/observe CI where available.

**Boundaries:** write only after an explicit implementation request. Never overwrite unrelated work, change secrets/permissions, force-push, or delete substantial data without explicit approval. A successful write is not a successful application build.

## 6. `review_implementation`

**Purpose:** evaluate source changes and captures against the brief.

**Input:** repository/branch/commit or supplied diff; visual brief; optional screenshots/video frames and target environment.

**Output:** severity-ranked findings with source path/visual evidence, violated criterion, likely cause, proposed fix, and status; demonstrated tier by feature and overall; items that require a build, capture, or device to verify.

**Rules:** review the actual result, not just whether code compiles. Do not report pixel parity without comparable captures.

## 7. `audit_performance_accessibility`

**Purpose:** review performance and inclusive interaction.

**Input:** target project and implementation commit/source; optional device class, runtime API, profiling output, and accessibility settings.

**Output:** risks for GPU/CPU work, overdraw, full-screen capture, allocations, memory, frame pacing, battery/thermal behavior, multiple surfaces, semantics, contrast, focus, keyboard/touch, screen readers, reduced motion, and transparency/high-contrast modes; prioritized fixes and validation checklist.

**Rules:** distinguish static code risks from measured runtime data. Never claim measured frame rates, GPU cost, battery use, or accessibility certification without actual tests.

## Error and completion contract

Every operation returns:
- `status`: `complete`, `partial`, or `blocked`;
- `evidence`: exact paths, refs, captures, tool results, or runtime observations;
- `unknowns`: requirements that could not be verified;
- `next_action`: the smallest useful next step.

For implementation, `complete` requires a published commit (or requested PR) and verification of the exact resulting state. If CI is queued, report `partial` until its result is read. Never label a phase or implementation complete from generated code alone.
