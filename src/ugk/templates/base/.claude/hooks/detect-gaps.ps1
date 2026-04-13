# Detect GDD <-> code gaps - Windows PowerShell
# Warns (non-blocking) when GDD mentions systems without corresponding code folders
$ErrorActionPreference = 'SilentlyContinue'

# Accept either casing; project template uses Design/GDD
$gddDir = $null
foreach ($p in @("Design/GDD", "design/gdd")) {
    if (Test-Path $p) { $gddDir = $p; break }
}
if (-not $gddDir) { exit 0 }
if (-not (Test-Path "Assets/Scripts")) { exit 0 }

$scriptFiles = @(Get-ChildItem -Path "Assets/Scripts" -Recurse -File)
if ($scriptFiles.Count -eq 0) { exit 0 }

$gddFiles = @(Get-ChildItem -Path $gddDir -Filter "*.md")
foreach ($gdd in $gddFiles) {
    $system = $gdd.BaseName
    if ($system -eq "README" -or $system -eq "index") { continue }
    $pattern = [regex]::Escape($system)
    $match = $scriptFiles | Where-Object { $_.Name -match $pattern -or $_.BaseName -match $pattern } | Select-Object -First 1
    if (-not $match) {
        Write-Output ("GAP: {0}/{1} has no matching code in Assets/Scripts (run /code-audit)" -f $gddDir, $gdd.Name)
    }
}
exit 0
