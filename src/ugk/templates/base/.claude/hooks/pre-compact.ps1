# Pre-compact hook - snapshot context before compaction
# Windows PowerShell version
$ErrorActionPreference = 'SilentlyContinue'

$ts = Get-Date -Format "yyyy-MM-dd_HHmm"
$snapDir = "Production/session-logs"
New-Item -ItemType Directory -Path $snapDir -Force -ErrorAction SilentlyContinue | Out-Null
$snapFile = Join-Path $snapDir "pre-compact-$ts.md"

"# Pre-Compact Snapshot - $ts" | Out-File $snapFile -Encoding UTF8
"" | Out-File $snapFile -Append -Encoding UTF8

if (Test-Path "Production/session-state/active.md") {
    "## Session State" | Out-File $snapFile -Append -Encoding UTF8
    Get-Content "Production/session-state/active.md" | Out-File $snapFile -Append -Encoding UTF8
}

$branch = git rev-parse --abbrev-ref HEAD 2>$null
if ($branch) {
    "" | Out-File $snapFile -Append -Encoding UTF8
    "## Git State" | Out-File $snapFile -Append -Encoding UTF8
    "Branch: $branch" | Out-File $snapFile -Append -Encoding UTF8
    "" | Out-File $snapFile -Append -Encoding UTF8
    (git status --short) | Out-File $snapFile -Append -Encoding UTF8
}

Write-Output "Pre-compact snapshot saved: $snapFile"
exit 0
