# Install Liquid Glass in ChatGPT Desktop for Windows

This guide targets **ChatGPT Desktop installed from the Microsoft Store**, using the personal Codex Skills directory reported for that app:

`$HOME\.codex\skills\`

On the Windows profile in the maintainer setup, this resolves to:

`C:\Users\Magd\.codex\skills\`

The installed Skill must end up at:

`%USERPROFILE%\.codex\skills\liquid-glass\SKILL.md`

## Install

1. Clone the public repository, or update an existing clone:

```powershell
git clone https://github.com/majd7772233-a11y/LiquidGlass.git
Set-Location .\LiquidGlass
```

2. From the repository root, run this PowerShell block. It verifies the source, backs up an existing personal copy, and copies the complete Skill directory:

```powershell
$repoRoot = (Get-Location).Path
$source = Join-Path $repoRoot ".agents\skills\liquid-glass"
$skillsRoot = Join-Path $HOME ".codex\skills"
$target = Join-Path $skillsRoot "liquid-glass"

if (-not (Test-Path -LiteralPath (Join-Path $source "SKILL.md"))) {
    throw "Skill source not found. Run this block from the LiquidGlass repository root."
}

New-Item -ItemType Directory -Force -Path $skillsRoot | Out-Null

if (Test-Path -LiteralPath $target) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $backup = Join-Path $skillsRoot "liquid-glass.backup-$stamp"
    Copy-Item -LiteralPath $target -Destination $backup -Recurse
    Remove-Item -LiteralPath $target -Recurse -Force
    Write-Host "Previous Skill backed up to: $backup"
}

Copy-Item -LiteralPath $source -Destination $target -Recurse -Force

if (-not (Test-Path -LiteralPath (Join-Path $target "SKILL.md"))) {
    throw "Installation verification failed: SKILL.md was not copied."
}

Write-Host "Liquid Glass installed at: $target"
```

3. Restart ChatGPT Desktop or start a new Codex session so it reloads the personal Skills directory.

## Use the Skill

Invoke it explicitly in Codex:

```text
$liquid-glass
```

You can then ask it to inspect a project, choose the best available rendering route, implement a material, or review an existing result.

## Update

From the existing repository clone:

```powershell
Set-Location "C:\path\to\LiquidGlass"
git pull --ff-only
```

Then run the installation PowerShell block again. It backs up the installed `liquid-glass` folder before replacing it; other Skills in `$HOME\.codex\skills` are not touched.

## Verify

```powershell
$skill = Join-Path $HOME ".codex\skills\liquid-glass\SKILL.md"
Test-Path -LiteralPath $skill
Get-Content -LiteralPath $skill -TotalCount 8
```

The first command should return `True`, and the header should show the Skill name `liquid-glass`.

## Repository-local versus personal installation

- **Repository copy:** `.agents/skills/liquid-glass/` stays in this Git repository so the Skill can be versioned with the project.
- **ChatGPT Desktop personal copy:** `$HOME\.codex\skills\liquid-glass\` is the install location for the Microsoft Store desktop setup described here.

These are two separate copies. Pulling the Git repository updates the repository copy; rerun the PowerShell installation block to update the personal copy.

This guide documents the user-confirmed ChatGPT Desktop environment. Do not assume that every Codex client or distribution uses the same personal Skills directory.
