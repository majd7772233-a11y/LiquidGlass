# Liquid Glass Skill Validation

Run from the repository root:

~~~bash
python tests/skill-validation/validate_skill.py
~~~

The validator uses only the Python standard library. It checks Codex Skill front matter and name/description constraints; required references, templates, and optional OpenAI UI metadata; relative Markdown links across the package and installation documentation; and two end-to-end workflow fixtures from unrelated platform families:
- Web DOM/GPU composition.
- Native Android Java/XML with API/device capability gates.

Each fixture specifies a project profile, task, discovery requirements, ordered workflow stages, expected strategy constraints, and acceptance outputs. The tests protect the Skill's decision process against assumptions such as "all browsers support WebGPU", "all DOM content can be sampled", "all Android devices expose the same effects", or "a blur is refraction".

## What these tests prove

A passing result proves that the published Skill package is structurally valid and that its written workflow covers the two representative end-to-end scenarios. The scenarios are workflow/decision tests; they do not claim to compile a sample application, run Codex's host activation model, or replace Phase 5 reference implementations and Phase 6 device/visual validation.
