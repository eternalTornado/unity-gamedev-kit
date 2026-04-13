# Validate .meta companion files - Windows PowerShell version
# Ensures every non-.meta asset in Assets/ has a matching .meta file.
# Runs as a pre-commit style check; wired under PreToolUse matcher=Bash
# so it fires on Bash tool calls - exits fast if Assets/ is absent.
$ErrorActionPreference = 'SilentlyContinue'

if (-not (Test-Path "Assets")) { exit 0 }

$rootLen = (Get-Location).Path.Length + 1
$orphans = New-Object System.Collections.Generic.List[string]

Get-ChildItem -Path "Assets" -Recurse -File | Where-Object {
    $_.Extension -ne ".meta" -and
    # skip hidden dotted path segments (e.g. Assets/.vs, Assets/.git)
    ($_.FullName -notmatch '[\\/]\.[^\\/]+[\\/]')
} | ForEach-Object {
    $metaPath = $_.FullName + ".meta"
    if (-not (Test-Path $metaPath)) {
        $orphans.Add($_.FullName.Substring($rootLen))
    }
}

if ($orphans.Count -gt 0) {
    Write-Output ("ERROR: {0} asset(s) missing .meta files:" -f $orphans.Count)
    $orphans | Select-Object -First 10 | ForEach-Object { Write-Output ("  " + $_) }
    if ($orphans.Count -gt 10) {
        Write-Output ("  ... and {0} more" -f ($orphans.Count - 10))
    }
    Write-Output ""
    Write-Output "Open the project in Unity Editor to regenerate .meta files."
    exit 1
}
exit 0
