---
name: hotfix
description: Guided hotfix workflow -- triage, branch, fix, test, cherry-pick, release. For critical post-release bugs.
---

# /hotfix -- Critical Hotfix Workflow

## What this command does

Guides the user through a structured hotfix process for critical bugs found after a release.

## When to use

- Critical bug in a released build (crashes, data loss, security issues)
- Bug that needs to ship faster than the next regular release

## Process

1. **Triage** -- ask:
   - What is the bug? (description, repro steps)
   - Severity: Critical / High / Medium
   - Affected build version
   - Number of users affected (if known)
2. **Branch** -- suggest git workflow:
   - Create `hotfix/<bug-id>` branch from the release tag
   - Not from `main` (which may have unreleased changes)
3. **Fix** -- help implement the fix:
   - Identify the root cause
   - Write the minimal fix (smallest possible change)
   - Add a regression test for the specific bug
4. **Test** -- verify:
   - Regression test passes
   - Full test suite passes on the hotfix branch
   - Manual verification of the fix
5. **Merge strategy** -- present options:
   - Cherry-pick fix back to `main`
   - Merge hotfix branch to `main`
6. **Release** -- suggest:
   - Bump patch version
   - Run `/release-checklist` (abbreviated for hotfix)
   - Write hotfix entry in changelog
7. **Document** -- write post-incident note:
   - Root cause
   - Fix applied
   - How to prevent similar issues
   - Write to `Production/qa/hotfix-<bug-id>.md`

## Output

- Code fix with regression test
- `Production/qa/hotfix-<bug-id>.md` -- post-incident document

## Collaboration protocol

Every step requires user approval. The fix must be reviewed before merging. Never force-push or skip tests for a hotfix.
