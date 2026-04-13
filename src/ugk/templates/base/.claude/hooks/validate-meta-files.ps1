# Validate .meta companion files — Windows PowerShell version
# Ensures every non-.meta asset in Assets/ has a matching .meta file

if (-not (Test-Path "Assets")) { exit 0 }

$orphans = @()
Get-ChildItem -Path "Assets" -Recurse -File | Where-Object {
    $_.Extension -ne ".meta" -and
    -not ($_.FullName -match "\\\.")
} | ForEach-Object {
    $metaPath = "$($_.FullName).meta"
    if (-not (Test-Path $metaPath)) {
        $orphans += $_.FullName.Substring((Get-Location).Path.Length + 1)
    }
}

if ($orphans.Count -gt 0) {
    Write-Output "ERROR: $($orphans.Count) asset(s) missing .meta files:"
    $orphans | Select-Object -First 10 | ForEach-Object { Write-Output "  $_" }
    if ($orphans.Count -gt 10) { Write-Output "  ... and $($orphans.Count - 10) more" }
    Write-Output ""
    Write-Output "Open the project in Unity Editor to regenerate .meta files."
    exit 1
}
exit 0
