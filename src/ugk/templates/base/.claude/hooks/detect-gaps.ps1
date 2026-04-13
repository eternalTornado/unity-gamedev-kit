# Detect GDD ↔ code gaps — Windows PowerShell version
# Warns (non-blocking) when GDD mentions systems without corresponding code folders

if (-not (Test-Path "design/gdd")) { exit 0 }
if (-not (Test-Path "Assets/Scripts")) { exit 0 }

$gddFiles = Get-ChildItem -Path "design/gdd" -Filter "*.md" -ErrorAction SilentlyContinue
foreach ($gdd in $gddFiles) {
    $system = $gdd.BaseName
    # Look for a matching script folder or file
    $match = Get-ChildItem -Path "Assets/Scripts" -Recurse -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match $system -or $_.BaseName -match $system }
    if (-not $match) {
        Write-Output "GAP: design/gdd/$($gdd.Name) has no matching code in Assets/Scripts (run /code-audit)"
    }
}
exit 0
