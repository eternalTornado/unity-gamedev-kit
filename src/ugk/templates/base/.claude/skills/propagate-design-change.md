---
name: propagate-design-change
description: When a GDD change affects multiple systems, identify downstream docs and code that need updates. Prevents orphaned references and silent drift.
model: sonnet
---

# /propagate-design-change — Cross-system impact analysis

## When to use

- After `/design-system` or major `/update-gdd` where Dependencies section changed
- Before `/create-stories` — ensure downstream work is scoped too

## Inputs

- `<gdd-file>` — the changed GDD
- `<change-summary>` — optional (from `/diff-design` output)

## Workflow

1. **Extract Dependencies section** from changed GDD.
2. **For each dependency**:
   - Find target GDD in `design/gdd/`
   - Grep code in `Assets/Scripts/` for references to the new/changed concept
   - Check balance configs, UI screens, save data schema
3. **Classify impact**:
   - **UPDATE_GDD** — another GDD needs revision
   - **UPDATE_CODE** — code in another system needs change
   - **UPDATE_CONFIG** — config/data file needs update
   - **UPDATE_TEST** — existing test will fail with new design
   - **UPDATE_UI** — UI screen needs to reflect change
4. **Draft propagation plan** → approve → write to `production/propagation/<system>-<date>.md`.
5. **Recommend**: usually add the propagation items as additional stories in `/create-stories`.

## Propagation report format

```markdown
# Propagation: daily-login-reward → affected systems
**Source:** design/gdd/daily-login-reward.md (new)
**Date:** 2026-04-13

## Downstream impact

### design/gdd/inventory.md — UPDATE_GDD
Reason: New reward types (gem, loot-box) not defined in Inventory item schema.
Action: Add `LoginRewardItem` subtype under §3 Item Hierarchy.

### design/gdd/save.md — UPDATE_GDD
Reason: New field `last_claim_date` needed.
Action: Add to save schema §4.

### Assets/Scripts/UI/MainMenu.cs — UPDATE_CODE
Reason: Needs claim button + notification badge.
Action: Implement via new story.

### Tests — UPDATE_TEST
`test_save_schema_migration` will fail → add new field, bump schema version.

## Recommended stories to add
- inventory-loot-box-type (S, gameplay-code)
- save-migration-v3 (M, engine-code)
- ui-main-menu-claim-button (M, ui-code)
- test-save-schema-v3 (S, engine-code)
```

## Rules

- Always grep code AND read sibling GDDs — don't rely on Dependencies list alone
- Silent drift is the #1 cost of missing this step — be thorough
