---
name: story-done
description: Close a story after implementation. Verifies tests pass, runs /verify-against-doc, updates session state, archives story.
model: haiku
---

# /story-done — Close the story cleanly

## Pre-requisites (all must pass)

1. `/verify-against-doc` ran with PASS or accepted PARTIAL
2. Automated tests pass (engine-specific runner)
3. Code reviewed (either `/code-review` or human reviewer approved)
4. No unresolved TODOs in changed files tagged `BLOCKING`

## Workflow

1. Read story file from `production/sprints/current/stories/`.
2. Check each prerequisite — if any fails, refuse to close and list failures.
3. Ask approval: "Close story <id>? Move to `production/sprints/current/done/`?"
4. Move story file, append done-timestamp + commit SHA.
5. Update `production/session-state/active.md`:
   - Remove from "in progress"
   - Add to "completed this sprint"
6. Suggest next story from Ready queue (read `/sprint-status`).

## Output

```
✅ Story closed: combat-parry-impl
- Moved to: production/sprints/current/done/combat-parry-impl.md
- Commit: 4e5f6g7
- Tests: 42/42 pass
- Verified: PASS (production/verification/combat-parry-impl.md)

Next ready: combat-block-tune  (run /story-readiness or /dev-story)
```

## Rules

- Do not close if any prerequisite fails — that's the whole point
- Keep done stories for the sprint; archive to sprint-archive on `/sprint-close`
