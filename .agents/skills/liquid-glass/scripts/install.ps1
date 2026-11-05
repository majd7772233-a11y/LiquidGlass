[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "Medium")]
param([string]$InstallRoot = (Join-Path $HOME ".codex\skills"))

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"
$packageRoot = Split-Path -Parent $PSScriptRoot
$sourceRoot = $packageRoot
$temporaryPackageRoot = $null

# A repository checkout keeps canonical documentation outside the Skill folder.
# A release ZIP already has its documentation bundled and needs no build step.
if (-not (Test-Path -LiteralPath (Join-Path $packageRoot "references\project-docs") -PathType Container)) {
    $repoRoot = Split-Path -Parent (Split-Path -Parent (Split-Path -Parent $packageRoot))
    $builder = Join-Path $repoRoot "scripts\build_skill_package.py"
    if (-not (Test-Path -LiteralPath $builder -PathType Leaf)) {
        throw "Project documentation is not bundled and the repository package builder was not found."
    }
    $python = Get-Command python -ErrorAction SilentlyContinue
    if (-not $python) {
        throw "Python 3.9 or later is required when installing from a repository checkout. Install Python or use the standalone ZIP."
    }

    $temporaryPackageRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("liquid-glass-install-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $temporaryPackageRoot -Force | Out-Null
    $temporaryZip = Join-Path $temporaryPackageRoot "liquid-glass-skill.zip"
    & $python.Source $builder --output $temporaryZip
    if ($LASTEXITCODE -ne 0) {
        Remove-Item -LiteralPath $temporaryPackageRoot -Recurse -Force
        throw "The Skill package builder failed with exit code $LASTEXITCODE."
    }
    Expand-Archive -LiteralPath $temporaryZip -DestinationPath $temporaryPackageRoot -Force
    $sourceRoot = Join-Path $temporaryPackageRoot "liquid-glass"
}

$skillFile = Join-Path $sourceRoot "SKILL.md"
$versionFile = Join-Path $sourceRoot "VERSION"
if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf) -or
    -not (Test-Path -LiteralPath $versionFile -PathType Leaf)) {
    if ($temporaryPackageRoot -and (Test-Path -LiteralPath $temporaryPackageRoot)) {
        Remove-Item -LiteralPath $temporaryPackageRoot -Recurse -Force
    }
    throw "Skill package is incomplete: SKILL.md or VERSION is missing."
}

$version = (Get-Content -LiteralPath $versionFile -Raw).Trim()
if ($version -notmatch '^\d+\.\d+\.\d+$') {
    throw "Invalid Skill version: $version"
}

$resolvedRoot = [System.IO.Path]::GetFullPath($InstallRoot)
$target = Join-Path $resolvedRoot "liquid-glass"
$staging = Join-Path $resolvedRoot (".liquid-glass.installing-" + $PID)
$backup = $null

try {
    if (-not $PSCmdlet.ShouldProcess($target, ("Install Liquid Glass Skill " + $version))) {
        return
    }
    New-Item -ItemType Directory -Path $resolvedRoot -Force | Out-Null
    if (Test-Path -LiteralPath $staging) {
        Remove-Item -LiteralPath $staging -Recurse -Force
    }
    New-Item -ItemType Directory -Path $staging -Force | Out-Null
    Get-ChildItem -LiteralPath $sourceRoot -Force | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $staging -Recurse -Force
    }

    if (-not (Test-Path -LiteralPath (Join-Path $staging "SKILL.md") -PathType Leaf)) {
        throw "Staged package verification failed: SKILL.md is missing."
    }
    if (-not (Test-Path -LiteralPath (Join-Path $staging "references\project-docs\platform-adaptation\README.md") -PathType Leaf)) {
        throw "Staged package verification failed: bundled platform documentation is missing."
    }

    if (Test-Path -LiteralPath $target) {
        $stamp = Get-Date -Format "yyyyMMdd-HHmmss-fff"
        $backup = $target + ".backup-" + $stamp
        Move-Item -LiteralPath $target -Destination $backup
    }

    try {
        Move-Item -LiteralPath $staging -Destination $target
    }
    catch {
        if ($backup -and (Test-Path -LiteralPath $backup)) {
            if (Test-Path -LiteralPath $target) {
                Remove-Item -LiteralPath $target -Recurse -Force
            }
            Move-Item -LiteralPath $backup -Destination $target
        }
        throw
    }

    $installedVersion = (Get-Content -LiteralPath (Join-Path $target "VERSION") -Raw).Trim()
    if ($installedVersion -ne $version) {
        throw "Post-install verification failed: expected $version, found $installedVersion."
    }
    Write-Host ("Liquid Glass Skill " + $version + " installed at: " + $target)
    if ($backup) {
        Write-Host ("Previous installation preserved at: " + $backup)
    }
}
catch {
    if (Test-Path -LiteralPath $staging) {
        Remove-Item -LiteralPath $staging -Recurse -Force
    }
    throw
}
finally {
    if ($temporaryPackageRoot -and (Test-Path -LiteralPath $temporaryPackageRoot)) {
        Remove-Item -LiteralPath $temporaryPackageRoot -Recurse -Force
    }
}
