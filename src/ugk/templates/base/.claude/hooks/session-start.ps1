# Claude Code SessionStart hook - Windows PowerShell
# Loads project context at session start
$ErrorActionPreference = 'SilentlyContinue'

Write-Output "=== Unity GameDev Kit - Session Context ==="

# Current branch
$branch = git rev-parse --abbrev-ref HEAD 2>$null
if ($branch) {
    Write-Output "Branch: $branch"
    Write-Output ""
    Write-Output "Recent commits:"
    git log --oneline -5 2>$null | ForEach-Object { "  $_" }
}

# Current sprint
if (Test-Path "Production/sprints") {
    $latestSprint = Get-ChildItem -Path "Production/sprints" -Filter "sprint-*.md" |
        Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if ($latestSprint) {
        Write-Output ""
        Write-Output ("Active sprint: " + $latestSprint.BaseName)
    }
}

# Open bugs
$bugCount = 0
foreach ($dir in @("tests/playtest", "Production")) {
    if (Test-Path $dir) {
        $found = @(Get-ChildItem -Path $dir -Filter "BUG-*.md" -Recurse)
        $bugCount += $found.Count
    }
}
if ($bugCount -gt 0) { Write-Output "Open bugs: $bugCount" }

# Code health (use Get-ChildItem -Recurse; PS does not expand ** in -Path globs)
if (Test-Path "Assets/Scripts") {
    $csFiles = @(Get-ChildItem -Path "Assets/Scripts" -Filter "*.cs" -Recurse)
    if ($csFiles.Count -gt 0) {
        $todos  = @($csFiles | Select-String -Pattern "TODO").Count
        $fixmes = @($csFiles | Select-String -Pattern "FIXME").Count
        if ($todos -gt 0 -or $fixmes -gt 0) {
            Write-Output ""
            Write-Output ("Code health: {0} TODOs, {1} FIXMEs in Assets/Scripts/" -f $todos, $fixmes)
        }
    }
}

# Active session state
$stateFile = "Production/session-state/active.md"
if (Test-Path $stateFile) {
    Write-Output ""
    Write-Output "=== ACTIVE SESSION STATE DETECTED ==="
    Write-Output ("State file: " + $stateFile)
    Write-Output ""
    Write-Output "Quick summary:"
    Get-Content $stateFile -TotalCount 20 | ForEach-Object { "  $_" }
    $total = @(Get-Content $stateFile).Count
    if ($total -gt 20) {
        Write-Output ("  ... ({0} total lines)" -f $total)
    }
    Write-Output "=== END STATE PREVIEW ==="
}

Write-Output "==================================="
exit 0
