#!/bin/bash
# Claude Code PreToolUse hook: validate Unity .meta file integrity on commit.
# Unity tracks GUIDs in .meta files. Orphaned .meta or missing .meta cause merge chaos.
#
# Input (PreToolUse for Bash): { "tool_input": { "command": "git commit ..." } }
# Exit 0 = allow, Exit 2 = block (stderr shown to Claude).

INPUT=$(cat)
if command -v jq >/dev/null 2>&1; then
    COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
else
    COMMAND=$(echo "$INPUT" | grep -oE '"command"[[:space:]]*:[[:space:]]*"[^"]*"' | sed 's/.*"command"[[:space:]]*:[[:space:]]*"//;s/"$//')
fi

if ! echo "$COMMAND" | grep -qE '^git[[:space:]]+commit'; then
    exit 0
fi

STAGED=$(git diff --cached --name-only 2>/dev/null)
[ -z "$STAGED" ] && exit 0

WARN=""

# Check for asset files missing their .meta pair
while IFS= read -r file; do
    # Only check under Assets/
    case "$file" in
        Assets/*)
            ;;
        *)
            continue
            ;;
    esac
    # Skip .meta files themselves and .cs.meta we already check below
    if [[ "$file" == *.meta ]]; then
        continue
    fi
    # The expected meta file
    meta="${file}.meta"
    # If the asset is staged-as-added but its .meta is neither staged nor on disk → warn
    if ! echo "$STAGED" | grep -qx "$meta" && [ ! -f "$meta" ]; then
        WARN="$WARN\nMETA: missing companion .meta for: $file"
    fi
done <<< "$STAGED"

# Check for orphaned .meta (staged .meta whose asset doesn't exist)
while IFS= read -r file; do
    [[ "$file" != Assets/*.meta ]] && continue
    asset="${file%.meta}"
    if [ ! -e "$asset" ]; then
        WARN="$WARN\nMETA: orphaned .meta (asset missing): $file"
    fi
done <<< "$STAGED"

if [ -n "$WARN" ]; then
    echo -e "Unity .meta validation warnings:$WARN" >&2
    echo "" >&2
    echo "Fix: ensure every Assets/ file has its .meta committed together." >&2
    exit 2
fi

exit 0
