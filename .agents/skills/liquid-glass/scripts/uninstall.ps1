[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = "Medium")]
param(
    [string]$InstallRoot = (Join-Path $HOME ".codex\skills"),
    [switch]$ConfirmUninstall
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not $ConfirmUninstall) {
    throw "Uninstall is destructive. Re-run with -ConfirmUninstall to remove only the liquid-glass Skill folder."
}

$resolvedRoot = [System.IO.Path]::GetFullPath($InstallRoot)
$target = Join-Path $resolvedRoot "liquid-glass"

if (-not (Test-Path -LiteralPath $target)) {
    Write-Host ("No Liquid Glass Skill installation exists at: " + $target)
    return
}

if ($PSCmdlet.ShouldProcess($target, "Remove only the liquid-glass Skill folder")) {
    Remove-Item -LiteralPath $target -Recurse -Force
    Write-Host ("Liquid Glass Skill removed from: " + $target)
    Write-Host "Timestamped backup folders, when present, were left untouched."
}
