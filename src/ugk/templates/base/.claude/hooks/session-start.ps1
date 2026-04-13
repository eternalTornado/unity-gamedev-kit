# Claude Code SessionStart hook — Windows PowerShell version
# Loads project context at session start

Write-Output "=== Unity GameDev Kit — Session Context ==="

# Current branch
$branch = (git rev-parse --abbrev-ref HEAD 2>$null)
if ($branch) {
    Write-Output "Branch: $branch"
    Write-Output ""
    Write-Output "Recent commits:"
    git log --oneline -5 2>$null | ForEach-Object { "  $_" }
}

# Current sprint
$latestSprint = Get-ChildItem -Path "production/sprints" -Filter "sprint-*.md" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($latestSprint) {
    Write-Output ""
    Write-Output "Active sprint: $($latestSprint.BaseName)"
}

# Open bugs
$bugCount = 0
foreach ($dir in @("tests/playtest", "production")) {
    if (Test-Path $dir) {
        $bugCount += (Get-ChildItem -Path $dir -Filter "BUG-*.md" -Recurse -ErrorAction SilentlyContinue).Count
    }
}
if ($bugCount -gt 0) { Write-Output "Open bugs: $bugCount" }

# Code health
if (Test-Path "Assets/Scripts") {
    $todos = (Select-String -Path "Assets/Scripts/**/*.cs" -Pattern "TODO" -ErrorAction SilentlyContinue).Count
    $fixmes = (Select-String -Path "Assets/Scripts/**/*.cs" -Pattern "FIXME" -ErrorAction SilentlyContinue).Count
    if ($todos -gt 0 -or $fixmes -gt 0) {
        Write-Output ""
        Write-Output "Code health: $todos TODOs, $fixmes FIXMEs in Assets/Scripts/"
    }
}

# Active session state
$stateFile = "production/session-state/active.md"
if (Test-Path $stateFile) {
    Write-Output ""
    Write-Output "=== ACTIVE SESSION STATE DETECTED ==="
    Write-Output "State file: $stateFile"
    Write-Output ""
    Write-Output "Quick summary:"
    Get-Content $stateFile -TotalCount 20 | ForEach-Object { "  $_" }
    $total = (Get-Content $stateFile).Count
    if ($total -gt 20) {
        Write-Output "  ... ($total total lines)"
    }
    Write-Output "=== END STATE PREVIEW ==="
}

Write-Output "==================================="
exit 0
