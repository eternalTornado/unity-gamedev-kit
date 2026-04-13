# Team Configurations

How to use unity-gamedev-kit with different team sizes and compositions.

## Solo dev

**Setup:** Bootstrap with `ugk init`. Use all skills directly. Skip `producer-lite` agent.

**Cadence:**
- Weekly sprint (instead of 2-week)
- Self-review via `/code-review` and `/design-review` before `/story-done`
- `/schedule` a weekly `/gate-check` reminder

## GD + Dev (2 people, no Producer)

**The config this kit is optimized for.** Most of the doc-code-sync skills exist because of this pair.

**Setup:** Both people work in the same repo. GD owns `design/gdd/**`. Dev owns `Assets/Scripts/**`.

**Flow:**
1. GD updates a GDD → notifies Dev
2. Dev runs the reconcile loop (`/diff-design` → `/code-audit` → `/gap-report` → `/clarify-gaps`)
3. Dev sends question list to GD asynchronously (Slack/email/Notion)
4. GD answers → Dev runs `/update-gdd` → `/create-stories`
5. Dev implements (`/story-readiness` → `/dev-story` → `/story-done`)
6. End of sprint: `/design-lock` to freeze the baseline

**Key agents:**
- `producer-lite` — use as needed for coordination
- `game-designer` — GD invokes this
- `programmer` + `tester` + `code-reviewer` — Dev invokes these

**Tips:**
- Never rely on verbal decisions — use `/update-gdd` to write them down
- Run `/code-audit` weekly (schedule it!) to catch drift early
- When GD is unavailable, log "Dev-decided, pending GD confirm" in gap-report

## Small team (3–10, with Producer)

**Setup:** Add `producer` role (real person), promote `producer-lite` to full `producer` agent workflow.

**Flow:** Follows the full 7-phase pipeline from `.claude/docs/`:
```
Concept → Systems Design → Technical Setup → Pre-Production →
Production → Polish → Release
```

**Roles map to agents:**
| Team role | Agent |
|-----------|-------|
| Creative Director | `creative-director` |
| Tech Lead | `technical-director` |
| Game Designer | `game-designer` |
| Level Designer | `level-designer` |
| Writer | `narrative-designer` |
| UI Designer | `ui-designer` |
| QA Lead | `qa-lead` |
| Programmer | `programmer` + specialists |

## Remote / async team

Everything in the kit is async-friendly. Specifics:

- `/clarify-gaps` produces batch question lists
- `/schedule` for daily/weekly automated reports
- Git commit hooks enforce traceable references
- Gate-checks run in CI as well as manually

## Roles for different engines

The kit is Unity-first but the workflow is engine-agnostic. For Godot / Unreal:

- Replace `unity-specialist` agent with `godot-specialist` or `unreal-specialist`
- Update `.claude/rules/engine-code.md` for the engine's idioms
- Keep all other skills and workflow the same
