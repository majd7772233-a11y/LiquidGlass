# Install Liquid Glass in ChatGPT Desktop for Windows

This is the verified install target for the Microsoft Store version of ChatGPT
Desktop. The default personal Skills directory is $HOME/.codex/skills. The
installer uses the current Windows profile automatically; it does not require
a hard-coded username or administrator rights.

## Install from a repository clone

    git clone https://github.com/majd7772233-a11y/LiquidGlass.git
    Set-Location .\LiquidGlass
    .\.agents\skills\liquid-glass\scripts\install.ps1

When run from a repository checkout, the script invokes the repository's
package builder to include the canonical platform documentation before
installing. Python 3.9 or later is required for this path.

## Install from a standalone package

Download the versioned liquid-glass-skill ZIP from the project's release
artifacts, extract it, then run:

    .\liquid-glass\scripts\install.ps1

The standalone ZIP already contains the self-contained documentation and can
be installed without Python.

The installer verifies SKILL.md, VERSION, and bundled platform guidance, copies
into a staging directory, and replaces only the liquid-glass Skill. If a
previous installation exists, it is preserved in a timestamped
liquid-glass.backup-* directory. The backup is not removed automatically.

## Update

For a repository installation:

    Set-Location C:\path\to\LiquidGlass
    git pull --ff-only
    .\.agents\skills\liquid-glass\scripts\install.ps1

For a ZIP installation, extract the new version and run its
liquid-glass\scripts\install.ps1. The current installed copy is backed up
before replacement. The script never removes other Skills.

Restart ChatGPT Desktop or start a new Codex session so the updated Skill is
loaded. Invoke it explicitly with:

    $liquid-glass

## Verify

    $skill = Join-Path $HOME ".codex\skills\liquid-glass"
    Test-Path (Join-Path $skill "SKILL.md")
    Get-Content (Join-Path $skill "VERSION")
    Get-Content (Join-Path $skill "SKILL.md") -TotalCount 8

The path check should return True and VERSION should show the installed
package version.

## Uninstall

Run this from the repository clone or extracted package, not from another
Skill's directory:

    .\.agents\skills\liquid-glass\scripts\uninstall.ps1 -ConfirmUninstall

The script requires the explicit -ConfirmUninstall switch and removes only
$HOME/.codex/skills/liquid-glass. It does not delete sibling Skills or
timestamped backups. Remove backups manually only after verifying that they
are no longer needed.

## Scope

The repository-local copy remains under .agents/skills/liquid-glass. The
personal ChatGPT Desktop copy lives under $HOME/.codex/skills/liquid-glass.
These are independent copies: pulling the repository does not update the
personal installation until the installer is run.

The path above is the verified ChatGPT Desktop Windows setup. Do not assume
other Codex clients or application distributions use this same location.
