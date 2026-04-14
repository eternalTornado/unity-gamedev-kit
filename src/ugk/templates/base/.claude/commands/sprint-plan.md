---
name: sprint-plan
description: Plan a sprint by selecting stories from the backlog, estimating capacity, and writing a sprint document. Writes to Production/sprints/.
---

# /sprint-plan -- Sprint Planning

## What this command does

Helps the user plan a development sprint by selecting stories, estimating effort, and producing a sprint plan document.

## Prerequisites

- Stories exist in `Production/epics/` (run `/create-stories` first)
- Previous sprint retrospective reviewed (if not first sprint)

## Process

1. **Read** all epic files and their stories. Identify:
   - Stories marked as ready (have acceptance criteria + design doc reference)
   - Story dependencies and blocking relationships
   - Stories carried over from previous sprint (if any)
2. **Ask** sprint parameters:
   - Sprint duration (1 week / 2 weeks)
   - Team capacity (story points or hours)
   - Sprint goal (one sentence)
3. **Suggest** a story selection based on:
   - Priority (from epic)
   - Dependencies (don't pick stories blocked by unfinished work)
   - Capacity fit
4. **User adjusts** selection -- add, remove, re-order.
5. **Write** sprint plan to `Production/sprints/sprint-<N>.md`:
   - Sprint goal
   - Duration and dates
   - Selected stories with estimates
   - Total estimated effort vs capacity
   - Risks and dependencies
   - Definition of Done reminder

## Output

`Production/sprints/sprint-<N>.md` (auto-increment sprint number).

## Collaboration protocol

Present the suggested story selection as a table. User approves or adjusts before writing.
