# Provenance and redistribution notes

## Project-authored material

The LiquidGlass Skill instructions, project-authored specifications, platform decision guides, workflow fixtures, package builders, tests, and reference-demo source code are maintained in this repository by the project authors. Platform API descriptions link to the relevant vendor documentation; those links do not transfer ownership of vendor names, marks, or documentation.

## User-supplied visual references

The images under `examples/references/` were supplied to the project as visual references. Their original creators, original publication locations, and redistribution permissions have not been independently established. Four additional images remain deliberately unclassified. The motion clip discussed in the reference matrix was inspected but is not included in this repository. No permission to redistribute those visual materials is asserted here.

The standalone Skill and private Studio package builders intentionally exclude the image references and the motion clip. Do not copy the images into a release bundle or describe them as project-owned assets without separate provenance and permission records.

## External software and generated artifacts

The Skill package uses Python's standard library and PowerShell for packaging and installation; it does not bundle third-party runtime libraries. The WebGL2 demo's npm development dependencies and the Android build toolchain are used by their respective examples and CI workflows, not embedded in the Skill package.

APK files, emulator screenshots, browser screenshots, profiler traces, and GitHub Actions artifacts are generated test evidence. They are not included in the installable Skill ZIP. The private Studio package includes the existing GitHub connector binding in `.app.json`; that archive is account-bound and must not be uploaded as a public plugin package.

## License boundary

See [LICENSE](LICENSE). No general open-source, modification, or redistribution license has been selected for project-authored material. The user-supplied visual references and private connector data have separate restrictions and are excluded from generated packages.
