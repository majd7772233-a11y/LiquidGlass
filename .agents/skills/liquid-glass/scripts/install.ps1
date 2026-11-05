[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "Medium")]
param(
    [string]$InstallRoot = (Join-Path $HOME ".codex\skills")
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$packageRoot = Split-Path -Parent $PSScriptRoot
$skillFile = Join-Path $packageRoot "SKILL.md"
$versionFile = Join-Path $packageRoot "VERSION"

if (-not (Test-Path -LiteralPath $skillFile -PathType Leaf)) {
    throw "Skill package is incomplete: SKILL.md was not found beside the scripts directory."
}
if (-not (Test-Path -LiteralPath $versionFile -PathType Leaf)) {
    throw "Skill package is incomplete: VERSION was not found."
}

$version = (Get-Content -LiteralPath $versionFile -Raw).Trim()
if ($version -notmatch '^\d+\.\d+\.\d+$') {
    throw "Invalid Skill version: $version"
}

$resolvedRoot = [System.IO.Path]::GetFullPath($InstallRoot)
$target = Join-Path $resolvedRoot "liquid-glass"
$staging = Join-Path $resolvedRoot (".liquid-glass.installing-" + $PID)
$backup = $null

if (-not $PSCmdlet.ShouldProcess($target, ("Install Liquid Glass Skill " + $version))) {
    return
}

New-Item -ItemType Directory -Path $resolvedRoot -Force | Out-Null

try {
    if (Test-Path -LiteralPath $staging) {
        Remove-Item -LiteralPath $staging -Recurse -Force
    }
    New-Item -ItemType Directory -Path $staging -Force | Out-Null

    Get-ChildItem -LiteralPath $packageRoot -Force | ForEach-Object {
        Copy-Item -LiteralPath $_.FullName -Destination $staging -Recurse -Force
    }

    if (-not (Test-Path -LiteralPath (Join-Path $staging "SKILL.md") -PathType Leaf)) {
        throw "Staged package verification failed: SKILL.md is missing."
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
}
catch {
    if (Test-Path -LiteralPath $staging) {
        Remove-Item -LiteralPath $staging -Recurse -Force
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
