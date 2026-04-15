---
name: dev-story
description: DEPRECATED. Use /implement instead. Kept as a shim that redirects Jira-style story workflows to the speckit-based /implement flow.
---

# /dev-story — DEPRECATED

This command is **deprecated**. It was part of the old 7-phase workflow that tracked Jira-style stories under `Production/stories/<story-id>.md`. The new 5-phase workflow implements modules directly from GDDs via speckit.

## Use `/implement` instead

```
/implement <module-name>
```

See [`implement.md`](implement.md) for the full flow: GDD → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement` → `/code-review`.

## Migration

If you have existing `Production/stories/*.md` files:

1. For each story, identify the parent module (the system it belongs to in `systems-index.md`).
2. Run `/implement <module>` instead of `/dev-story <story-id>`.
3. If the story contains implementation details not yet in the GDD (acceptance criteria, edge cases), fold them into the GDD first via `/update-gdd`.
4. Archive or delete `Production/stories/` once all stories are migrated.

If a team member wants to keep Jira-style tracking (e.g., for external project management), that is orthogonal — track stories in Jira, but let Claude implement modules end-to-end via `/implement`.

## Suggested next step

- `/implement <module-name>` — the new canonical flow
- `/update-gdd <module>` — fold story-level acceptance criteria back into the GDD before implementing
