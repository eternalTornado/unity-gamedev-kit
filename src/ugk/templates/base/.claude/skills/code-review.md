---
name: code-review
description: Review changed code files for correctness, standards compliance, test coverage, and alignment with GDD. Deeper than automated linters.
model: sonnet
---

# /code-review — Review code changes

## Inputs

- `<files>` or `<pr>` — list of changed files (default: `git diff HEAD~1` output)
- `<gdd-ref>` — optional GDD section the change implements

## Checklist

### 1. Standards compliance
- [ ] Doc comments on public APIs
- [ ] Naming conventions per `.claude/rules/*-code.md` for this path
- [ ] No hardcoded gameplay values (use ScriptableObject or config)
- [ ] No singletons where DI would work
- [ ] `GDD-ref:` comment present for gameplay code

### 2. Correctness
- [ ] Null-guards where needed
- [ ] Bounds checks on array/list access
- [ ] No tight loops in Update() without frame budget consideration
- [ ] No allocations in hot paths (foreach on List, LINQ, string concat)

### 3. Test coverage
- [ ] Logic → unit test exists and passes
- [ ] Integration → integration test exists or documented playtest
- [ ] No new public method without a test

### 4. GDD alignment (if `<gdd-ref>` provided)
- [ ] Formulas in code match §4
- [ ] Constants match §7 Tuning Knobs
- [ ] Edge cases from §5 handled

### 5. Unity-specifics
- [ ] `.meta` files present for new assets
- [ ] No scene file committed without reason
- [ ] Addressables used for async-loaded assets
- [ ] No GameObject.Find / Resources.Load in Update loops

## Workflow

1. Read all changed files.
2. Run each check. Note findings.
3. Classify: ❌ BLOCKING / ⚠️ CONCERN / 💡 SUGGESTION.
4. Write report → approve → `production/code-reviews/<pr-or-story>-<date>.md`.

## Rules

- BLOCKING issues must be fixed before merge
- Always cite file:line
- Prefer suggesting patches to pointing out problems
- Don't duplicate what the automated linter/CI would catch — focus on semantic issues
