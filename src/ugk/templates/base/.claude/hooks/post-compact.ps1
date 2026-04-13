# Post-compact hook — remind Claude to re-read active session state
# Windows PowerShell version

Write-Output "=== Post-compact reminder ==="
Write-Output "Context was just compacted. Recover full state by reading:"
Write-Output "  1. production/session-state/active.md"
Write-Output "  2. The file(s) you were actively working on"
Write-Output "  3. Latest snapshot in production/session-logs/"
Write-Output "==========================="
exit 0
