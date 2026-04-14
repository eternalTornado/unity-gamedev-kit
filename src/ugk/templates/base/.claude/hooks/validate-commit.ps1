# Validate commit message - Windows PowerShell version
# Enforces: commit message references a GDD file or story ID.
# When wired under Claude Code PreToolUse, input arrives as JSON on stdin;
# as a git commit-msg hook, $args[0] is the message file.
$ErrorActionPreference = 'SilentlyContinue'

$commitMsgFile = $args[0]
if (-not $commitMsgFile -or -not (Test-Path $commitMsgFile)) {
    # No-op under PreToolUse - nothing to validate silently
    exit 0
}

$msg = Get-Content $commitMsgFile -Raw

# Skip merges
if ($msg -match "^Merge ") { exit 0 }

# Require GDD-ref OR story-id OR bug-id
$hasRef = ($msg -match "GDD-ref:") -or
          ($msg -match "story:") -or
          ($msg -match "bug:") -or
          ($msg -match "#\d+")

if (-not $hasRef) {
    Write-Output "ERROR: commit message must reference a GDD file, story ID, bug ID, or issue number."
    Write-Output "Examples:"
    Write-Output "  GDD-ref: Design/GDD/combat.md"
    Write-Output "  story: combat-parry-impl"
    Write-Output "  bug: bug-2026-0042"
    Write-Output "  Closes #123"
    exit 1
}
exit 0
