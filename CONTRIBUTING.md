# Contributing

Thank you for helping improve LiquidGlass. Keep changes focused, evidence-based, and compatible with the platform-neutral engineering goals.

## Before changing code or guidance

1. Read [GPT.md](GPT.md) and the relevant phase in [ROADMAP.md](ROADMAP.md).
2. Read the matching specification and platform guide before changing a renderer or recommending an API.
3. Preserve the distinction between L0/L1 fallbacks and real L2/L3 refraction.
4. Do not add user-supplied reference images, recordings, secrets, or private connector data to release packages.
5. Keep platform limitations and unverified assumptions explicit.

## Local validation

Run the repository contract suites:

    python -m unittest discover -s .agents/skills/liquid-glass/tests -v
    python -m unittest discover -s studio/tests -v
    python -m unittest discover -s examples/tests -v
    python -m unittest discover -s scripts/tests -v
    python scripts/build_skill_package.py --check
    python studio/scripts/build_plugin_package.py --check

For runnable examples, also follow the WebGL2 and Android build/run instructions in their respective README files. Physical-device and human accessibility checks must be recorded using the Phase 6 visual review template; CI emulator results are not a substitute.

## Documentation and packaging

- Edit canonical specifications under `docs/`; do not edit generated copies in a packaged ZIP.
- Edit the canonical Skill under `.agents/skills/liquid-glass/`.
- Edit Studio source under `studio/package-source/` and rebuild its private archive with the checked-in builder.
- Bump the Skill VERSION and update CHANGELOG when shipping a Skill change.
- Keep the Studio manifest version aligned with the Skill VERSION when a paired Studio release is deliberately prepared.
- Run both package builders and inspect archive contents before publishing.

## Pull requests

Explain the user-visible behavior, affected platforms, fidelity tier, tests run, and any remaining visual, accessibility, or performance limitations. Do not claim physical-device validation unless the device, OS, GPU, build, procedure, and actual evidence are recorded.
