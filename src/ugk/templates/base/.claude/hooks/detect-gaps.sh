#!/bin/bash
# detect-gaps.sh - SessionStart
# Non-blocking warning when GDD and code drift apart.
# Paths: Design/GDD, Assets/Scripts (Unity conventions used by the ugk template).
set +e

echo "=== Checking for Documentation Gaps ==="

# Fresh project detection
FRESH_PROJECT=true
if [ -f ".claude/docs/technical-preferences.md" ]; then
    if grep -qE "^- \*\*Engine\*\*:" .claude/docs/technical-preferences.md 2>/dev/null; then
        if ! grep -qE "^- \*\*Engine\*\*:.*TO BE CONFIGURED" .claude/docs/technical-preferences.md 2>/dev/null; then
            FRESH_PROJECT=false
        fi
    fi
fi
[ -f "Design/GDD/game-concept.md" ] && FRESH_PROJECT=false
if [ -d "Assets/Scripts" ]; then
    CODE_CHECK=$(find Assets/Scripts -type f -name "*.cs" 2>/dev/null | head -1)
    [ -n "$CODE_CHECK" ] && FRESH_PROJECT=false
fi

if [ "$FRESH_PROJECT" = true ]; then
    echo ""
    echo "NEW PROJECT: no engine configured, no game concept, no source code."
    echo "   Run: /start"
    echo "==================================="
    exit 0
fi

# Substantial codebase vs sparse design docs
if [ -d "Assets/Scripts" ]; then
    CODE_FILES=$(find Assets/Scripts -type f -name "*.cs" 2>/dev/null | wc -l | tr -d ' ')
else
    CODE_FILES=0
fi
if [ -d "Design/GDD" ]; then
    DESIGN_FILES=$(find Design/GDD -type f -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
else
    DESIGN_FILES=0
fi

if [ "$CODE_FILES" -gt 50 ] && [ "$DESIGN_FILES" -lt 5 ]; then
    echo "GAP: large codebase ($CODE_FILES .cs files) but sparse design docs ($DESIGN_FILES)."
    echo "    Try: /code-audit Design/GDD/"
fi

# Gameplay systems without design docs
if [ -d "Assets/Scripts/Gameplay" ]; then
    for system_dir in Assets/Scripts/Gameplay/*/; do
        [ -d "$system_dir" ] || continue
        system_name=$(basename "$system_dir")
        file_count=$(find "$system_dir" -type f -name "*.cs" 2>/dev/null | wc -l | tr -d ' ')
        if [ "$file_count" -ge 5 ]; then
            if [ ! -f "Design/GDD/${system_name}.md" ] && [ ! -f "Design/GDD/${system_name}-system.md" ]; then
                echo "GAP: Assets/Scripts/Gameplay/${system_name}/ ($file_count .cs files) has no Design/GDD/${system_name}.md"
            fi
        fi
    done
fi

# ADR coverage
if [ -d "Assets/Scripts/Core" ] || [ -d "Assets/Scripts/Networking" ]; then
    if [ ! -d "Docs/architecture" ]; then
        echo "GAP: Core/Networking code exists but no Docs/architecture/ directory."
    else
        ADR_COUNT=$(find Docs/architecture -type f -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
        if [ "$ADR_COUNT" -lt 3 ]; then
            echo "GAP: Core systems exist but only $ADR_COUNT ADR(s) in Docs/architecture/."
        fi
    fi
fi

echo ""
echo "Tip: run /code-audit for a full GDD <-> code gap report."
echo "==================================="
exit 0
