# Packaging and release

Current package version: **0.1.0** (prepared; no stable Git tag or GitHub Release has been published).

This page describes the two deliverables and the release gates. The standalone Skill ZIP is a versioned package prepared for installation in the maintainer's verified ChatGPT Desktop environment. Liquid Glass Studio remains a private, account-bound ChatGPT plugin; its archive is not a public plugin distribution.

## Build the standalone Skill

From a clean clone with Python 3.9 or later:

    python scripts/build_skill_package.py --output dist/liquid-glass-skill-0.1.0.zip

The builder validates the package, copies the canonical platform documentation into the archive, rewrites repository-relative documentation links, and emits a self-contained ZIP with a SHA-256 inventory manifest. It deliberately excludes the supplied reference images, APKs, profiler traces, and private plugin binding.

Run its package tests:

    python -m unittest discover -s scripts/tests -v

## Current verified build artifact

The latest `liquid-glass-skill-0.1.0` artifact is uploaded by the most recent successful [Skill validation workflow](https://github.com/majd7772233-a11y/LiquidGlass/actions/workflows/skill-validation.yml) run. Download the artifact named `liquid-glass-skill-0.1.0`; GitHub Actions retains it for 14 days. The artifact wraps the package ZIP; extract the artifact ZIP first, then extract or run the installer from the inner `liquid-glass-skill.zip` file. A stable GitHub Release and version tag have not been published.

## Install from a clean checkout or ZIP

The supported, user-confirmed host target is ChatGPT Desktop for Windows using the personal Skills directory under $HOME/.codex/skills. The install script does not require administrator rights and changes only the liquid-glass folder.

From a repository checkout:

    .\.agents\skills\liquid-glass\scripts\install.ps1

From the standalone ZIP, extract it and run:

    .\liquid-glass\scripts\install.ps1

The script stages the new copy, verifies its entry point and version, preserves an existing installation in a timestamped backup, then replaces only the liquid-glass folder. Restart ChatGPT Desktop or start a new Codex session to reload the Skill.

Verify:

    Test-Path (Join-Path $HOME ".codex\skills\liquid-glass\SKILL.md")
    Get-Content (Join-Path $HOME ".codex\skills\liquid-glass\VERSION")

Uninstall from the checkout or extracted package:

    .\.agents\skills\liquid-glass\scripts\uninstall.ps1 -ConfirmUninstall

Uninstall removes only $HOME/.codex/skills/liquid-glass. It leaves other Skills and timestamped backups untouched. Review and remove old backup folders manually after confirming the new installation.

The Windows GitHub Actions job exercises clean installation, update/backup, and uninstallation in a fresh runner directory, and separately installs from the generated ZIP. This is an automated PowerShell packaging test, not a claim that every Codex client uses the same Skills directory. Other host paths are not declared supported until verified.

## Liquid Glass Studio

Studio is already installed as a private personal plugin and its actual @Liquid Glass Studio invocation has been confirmed by the user. See [Studio setup](../../studio/INSTALL.md). The package builder is:

    python studio/scripts/build_plugin_package.py --output dist/liquid-glass-studio-private.zip

That archive contains the account-bound .app.json GitHub connector binding. Treat it as private account data: do not attach it to a public GitHub Release, upload it as a workflow artifact, or place it in a public plugin directory. CI runs the Studio package builder in an ephemeral runner only to validate package structure; it does not publish or upload that ZIP. The public repository contains the manifest and connector identifier but no access token or credential.

## Versioning and release gates

The standalone Skill version is in [.agents/skills/liquid-glass/VERSION](../../.agents/skills/liquid-glass/VERSION). The Studio version is in [studio/package-source/plugin.json](../../studio/package-source/plugin.json). Keep these versions aligned for a coordinated release. Record user-visible changes in [CHANGELOG.md](../../CHANGELOG.md).

A stable Git tag and GitHub Release must wait until all acceptance criteria in the roadmap are met. Phase 6 physical-device checks remain maintainer-owned: real GPU timing on representative Android devices and a physical WebGL browser, battery/thermal evidence, and human TalkBack/switch-access/magnification review. CI uses software rendering and emulators, and cannot close those gates. No stable release is implied by a passing package build or clean-install CI run.

Before publishing, review [LICENSE](../../LICENSE) and [PROVENANCE.md](../../PROVENANCE.md). No general open-source, modification, or redistribution license has been selected. The `LICENSE` file is a rights-status notice, not a standard-form license; choose and review an appropriate license before allowing public reuse or redistribution.
