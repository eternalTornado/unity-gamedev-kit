---
name: create-epics
description: Break approved GDDs and architecture docs into implementation epics. Each epic maps to one system or cross-cutting concern. Writes to Production/epics/.
---

# /create-epics -- Epic Generation from Design

## What this command does

Reads approved GDDs and architecture docs, then generates implementation epics that break the project into shippable increments.

## Prerequisites

- Approved GDDs in `Design/GDD/`
- Architecture docs in `Docs/architecture/`
- `/gate-check 3` passed (Phase 3 complete)

## Process

1. **Read** all GDDs, systems index, and architecture docs.
2. **Generate epic list** -- one epic per system, plus cross-cutting epics:
   - Each epic has: title, description, scope (which GDD sections it implements), estimated story count, dependencies on other epics
3. **Present epic list** for user review. Ask:
   - Are the boundaries right?
   - Should any epic be split or merged?
   - What's the priority order?
4. **For each approved epic**, write to `Production/epics/<epic-name>.md`:
   - Epic title and goal
   - Source GDD references
   - High-level acceptance criteria (derived from GDD acceptance criteria)
   - Story breakdown placeholder (filled by `/create-stories`)
   - Dependencies on other epics
5. Suggest next: `/create-stories <epic>` for the first epic, or `/sprint-plan`.

## Output

`Production/epics/<epic-name>.md` per epic.

## Collaboration protocol

Present all epics as a table first. Write individual epic files only after the full list is approved.
