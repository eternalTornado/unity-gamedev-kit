# Backport Plan: CCGS Quality Standards → ugk v1.2.0

> **Generated**: 2026-04-16
> **Updated**: 2026-04-16 (applied user decisions)
> **Baseline**: CCGS `/design-system` SKILL.md (latest main), `/adopt` SKILL.md, GDD template, `qa-lead` agent
> **Target**: unity-gamedev-kit v1.2.0 (MINOR — changes behavior of existing commands)
> **Scope**: Retrofit quality, section quality rubrics, GDD-to-spec pipeline correctness

---

## Tại sao cần backport

ugk v1.0.0 port 3 rules từ CCGS (`design-docs`, `test-standards`, `prototype-code`) nhưng **bỏ hầu hết quality rubric** trong các skill/command. Kết quả:

- **AC chỉ có 1 dòng** "must be testable" — không format, không minimum coverage, không agent review
- **Formulas không có completion steering** — agent bịa formula thiếu variable table
- **Edge Cases không có format** — agent viết "handle gracefully" vì không có rubric ngăn
- **GDD được gọi là "feature spec" ở mọi nơi** — sai: raw GDD ≠ spec, chỉ sau retrofit + gate-check mới đủ
- **`/adopt` thiếu severity classification** — CCGS phân BLOCKING/HIGH/MEDIUM/LOW, ugk chỉ đánh ✅/🟡/❌
- **Không có cơ chế "section N/A"** — system đơn giản không có formula → agent bịa formula → implement sai

---

## User Decisions (confirmed)

| Decision | Kết quả |
|----------|---------|
| B1–B6, B8 | ✅ Approved |
| B7 (GDD template) | ❌ Rejected — GD gửi bất kỳ format nào, /adopt chuyển đổi. Template sẽ ép format cứng |
| Game Feel section | ❌ Dropped entirely — không thêm, không đề cập |
| AC coverage | 1:1 rules + player-facing formulas (internal formulas exempt) |
| N/A mechanism | Allowed with justification + user confirm. Cannot N/A: Overview, Detailed Rules, Dependencies, AC. Can N/A: Formulas, Edge Cases, Tuning Knobs |
| Context 70% warning | ALL long-running commands: design-system, adopt, review-all-gdds, implement, create-architecture |
| design-system.md split | Split 2 files: flow (design-system.md) + rubrics (design-system-rubrics.md) |
| Version | 1.2.0 (MINOR) |

---

## Phân loại thay đổi

| ID | Thay đổi | Files affected | Breaking? | Status |
|----|----------|---------------|-----------|--------|
| B1 | Sửa ngôn ngữ "GDD is the feature spec" → "GDD becomes spec after retrofit + gate" | 4 files | Semantic only | Approved |
| B2 | AC quality rubric: Given-When-Then, minimum coverage | `design-docs.md`, `adopt.md`, `design-system.md`, `design-system-rubrics.md`, `review-all-gdds.md` | Behavior change | Approved |
| B3 | Formulas completion steering: variable table template | `design-docs.md`, `design-system-rubrics.md` | Behavior change | Approved |
| B4 | Edge Cases format: "If [condition]: [exact outcome]" | `design-docs.md`, `design-system-rubrics.md` | Behavior change | Approved |
| B5 | `/adopt` severity classification: BLOCKING/HIGH/MEDIUM/LOW | `adopt.md` | Behavior change | Approved |
| B6 | Section N/A mechanism: explicit "N/A — [reason]" allowed | `design-docs.md`, `adopt.md`, `design-system.md`, `gate-check.md` | New capability | Approved |
| ~~B7~~ | ~~GDD template update~~ | ~~New template file~~ | ~~Additive~~ | **REJECTED** |
| B8 | `/start.md` fix: "8 GDD sections" → "7" | `start.md` | Bug fix | Approved |

---

## Chi tiết từng thay đổi

### B1. Sửa ngôn ngữ "GDD is the feature spec"

**Vấn đề**: Nhiều chỗ trong codebase nói "GDD is the feature spec" hoặc "the GDD already contains everything." Điều này sai vì raw GDD chưa qua retrofit/cross-review/gate-check thì không phải spec.

**Sửa**: Đổi thành "After retrofit and `/gate-check systems` PASS, the completed GDD serves as the feature spec for Phase 4."

**Files cần sửa** (4 files — `docs/WORKFLOW.md` không tồn tại):

| File | Dòng hiện tại (trích) | Sửa thành |
|------|----------------------|-----------|
| `rules/design-docs.md` line 9 | "The GDD is the feature spec for Phase 4 implementation" | "After retrofit and `/gate-check systems` PASS, the completed GDD serves as the feature spec for Phase 4 implementation" |
| `commands/adopt.md` line 12 | "The 7-section GDD is the implementation spec consumed by speckit in Phase 4" | "After retrofit (all 7 sections complete, cross-reviewed, gate passed), the GDD serves as the implementation spec consumed by speckit in Phase 4" |
| `commands/implement.md` line 20 | "The GDD acts as the feature spec (no /speckit.specify needed — GDDs already contain…)" | "The completed GDD (post-retrofit, post-gate) acts as the feature spec (no /speckit.specify needed — completed GDDs contain…)" |
| `CLAUDE.md` (template) line 68 | "the GDD already contains the feature spec" | "the completed GDD (post-retrofit) contains the feature spec" |

---

### B2. Acceptance Criteria quality rubric

**Vấn đề**: Package chỉ có 1 dòng: "Acceptance criteria must be testable." CCGS gốc có rubric đầy đủ.

**Nguồn gốc**: CCGS `design-system/SKILL.md` Section H (lines 572-593)

**Sửa — `rules/design-docs.md`**: Thay dòng AC hiện tại bằng:

```
- Acceptance criteria MUST use Given-When-Then format:
  GIVEN [initial state], WHEN [action or trigger], THEN [measurable outcome]
- Minimum coverage: at least 1 AC per core rule (from Detailed Rules) + 1 AC per player-facing formula (from Formulas). Internal-only formulas (no direct player impact) are exempt from mandatory AC coverage.
- Every criterion must be independently verifiable by a QA tester WITHOUT reading the GDD
- Cross-system interaction criteria required for systems with dependencies
- Performance budget criterion required: frame time, memory, or "N/A — no runtime cost"
- "The system works as designed" is NOT a valid acceptance criterion
```

**Sửa — `commands/adopt.md`**: Khi retrofit AC section, agent phải:
1. Check format Given-When-Then — nếu thiếu thì flag gap
2. Count AC vs core rules vs player-facing formulas — nếu coverage < 1:1 thì flag gap
3. Check independently verifiable — nếu AC reference "as described in Overview" thì flag

**Sửa — `commands/review-all-gdds.md`** Phase 2: Thêm explicit AC quality check:
- "Are acceptance criteria in Given-When-Then format?"
- "Does each core rule have at least one AC?"
- "Does each player-facing formula have at least one AC?"
- "Are criteria verifiable without reading the rest of the GDD?"

**Sửa — `design-system-rubrics.md`** (new file, split from design-system): AC guidance:
- Completion steering format
- Agent delegation note: "When qa-lead agent is available, spawn for AC validation"

---

### B3. Formulas completion steering

**Vấn đề**: `design-docs.md` nói "Formulas must include variable definitions, expected value ranges, and example calculations" — nhưng không có template. Agent thường viết formulas thiếu variable table.

**Nguồn gốc**: CCGS `design-system/SKILL.md` Section D (lines 468-506)

**Sửa — `rules/design-docs.md`**: Thêm completion steering:

```
- Formulas MUST follow this structure — prose-only formulas are not accepted:
  1. Formula expression: `formula_name = expression`
  2. Variable table: Variable | Type | Range | Description
  3. Output range: min to max under normal play
  4. Example: worked example with real numbers
```

**Sửa — `design-system-rubrics.md`** (new file): Formulas guidance:
- Variable table template
- "Do NOT write `[Formula TBD]` or describe a formula in prose without the variable table"
- Cross-reference rule: "If a dependency GDD defines a formula whose output feeds into this system, reference it explicitly"

---

### B4. Edge Cases format

**Vấn đề**: `design-docs.md` nói "Edge cases must explicitly state what happens, not just 'handle gracefully'" — nhưng không có format.

**Nguồn gốc**: CCGS `design-system/SKILL.md` Section E (lines 508-533)

**Sửa — `rules/design-docs.md`**: Thêm format:

```
- Edge cases MUST use this format:
  If [exact condition]: [exact outcome]. [rationale if non-obvious]
- Do NOT write "handle appropriately" — each must name the exact condition and the exact resolution
- An edge case without a resolution is an open design question, not a specification
```

**Sửa — `design-system-rubrics.md`**: Edge Cases guidance + examples

---

### B5. `/adopt` severity classification

**Vấn đề**: `/adopt` hiện tại chỉ dùng ✅/🟡/❌. CCGS có 4-tier severity: BLOCKING/HIGH/MEDIUM/LOW.

**Nguồn gốc**: CCGS `adopt/SKILL.md` Phase 3 (lines 170-191)

**Sửa — `commands/adopt.md`**: Sau gap report table, thêm severity classification:

```
4. **Classify gaps by severity** (after the gap report table):
   - **BLOCKING**: Missing AC or Detailed Rules — cannot generate implementation spec without these
   - **HIGH**: Missing Formulas on a system that performs calculations — stories will have wrong acceptance criteria
   - **MEDIUM**: Missing Tuning Knobs, partial Edge Cases — quality degradation but not pipeline-breaking
   - **LOW**: Missing optional sections — nice-to-have

   Present severity summary: "BLOCKING: N, HIGH: N, MEDIUM: N, LOW: N"
   If BLOCKING > 0: "⚠️ These GDDs cannot serve as implementation specs until BLOCKING gaps are resolved."
```

**Sửa — Gap report table**: Thêm severity column:

```
| File | Overview | Detailed Rules | Formulas | Edge Cases | Dependencies | Tuning Knobs | AC | Severity |
```

---

### B6. Section N/A mechanism

**Vấn đề**: Package bắt buộc 7 sections cho mọi system, nhưng nhiều system không có Formulas (e.g., Save System, Event Bus), không có Tuning Knobs (e.g., Scene Manager). Agent bịa content hoặc bỏ trống → cả hai đều sai.

**Sửa — `rules/design-docs.md`**: Thêm N/A rule:

```
- A section may be marked "N/A — [one-sentence justification]" if the system genuinely does not have content for it.
  Example: "## Formulas\n\nN/A — this is a pure event-routing system with no calculations."
  The justification must explain WHY, not just state N/A.
  Sections that CANNOT be N/A: Overview, Detailed Rules, Dependencies, Acceptance Criteria.
  Sections that CAN be N/A with justification + user confirmation: Formulas, Edge Cases, Tuning Knobs.
```

**Sửa — `commands/adopt.md`**: Gap report phân biệt "missing" vs "N/A":
- ❌ = missing (no section at all)
- 🟡 = partial (section exists but incomplete)
- ✅ = present
- ➖ = N/A with justification (valid, not a gap)

**Sửa — `commands/design-system.md`**: Cho mỗi N/A-eligible section, agent phải hỏi:
- "Does this system have [formulas/tuning knobs/edge cases]?"
- Nếu user nói không → yêu cầu justification → viết N/A section

**Sửa — `commands/gate-check.md`**: N/A sections must have justification; count as valid if justification exists.

---

### ~~B7. GDD template update~~ — REJECTED

**Lý do**: Game Designers gửi GDD ở bất kỳ format nào. `/adopt` có nhiệm vụ chuyển đổi sang 7-section format. Template sẽ tạo ấn tượng sai rằng GD phải viết đúng format này từ đầu.

**Hệ quả**: Không tạo file `docs/templates/game-design-document.md`. Không reference template trong `design-system.md`.

---

### B8. `/start.md` fix: "8 GDD sections" → "7"

**Vấn đề**: `start.md` line 20 vẫn nói "which of the 8 GDD sections" — lỗi từ v1.1.1 cleanup.

**Sửa**: Đổi thành "which of the 7 required GDD sections are present"

---

### Context 70% Warning (additive, all long-running commands)

**Thêm vào cuối mỗi file** (trước `## Suggested next step`):

```
## Context awareness

This command can consume significant context window space. If context usage exceeds 70%:
1. Write any in-progress section to file immediately
2. Summarize remaining work
3. Suggest the user run `/compact` then resume
```

**Files**: `design-system.md`, `adopt.md`, `review-all-gdds.md`, `implement.md`, `create-architecture.md`

---

## Implementation order

```
Phase 1 — Foundation (không phụ thuộc gì)
  B8  /start.md bug fix                              (~2 min)

Phase 2 — Rules layer
  B6  Section N/A mechanism in design-docs.md          (~15 min)
  B4  Edge Cases format in design-docs.md              (~10 min)
  B3  Formulas completion steering in design-docs.md   (~10 min)
  B2  AC quality rubric in design-docs.md              (~15 min)
  B1  "GDD is the feature spec" language fix           (~15 min, 4 files)

Phase 3 — Commands layer
  B5  /adopt severity classification                   (~30 min)
  B2  /adopt AC quality check in retrofit              (~15 min)
  B6  /adopt N/A handling                              (~10 min)
  Context warning in adopt.md                          (~5 min)
  Split design-system.md → flow + rubrics              (~30 min)
    design-system.md: flow only, ref rubrics, N/A flow, 7 sections
    design-system-rubrics.md: B2+B3+B4 quality guidance
  Context warning in design-system.md                  (~5 min)
  B2  /review-all-gdds AC quality checks               (~15 min)
  Context warning in review-all-gdds.md                (~5 min)
  B6  /gate-check N/A validation                       (~10 min)
  B1  /implement language + context warning             (~10 min)
  B1  CLAUDE.md language fix                           (~5 min)
  Context warning in create-architecture.md            (~5 min)

Phase 4 — Verification
  Version bump → 1.2.0 (pyproject.toml, __init__.py, README, CHANGELOG)
  Diff review: đọc lại mọi file đã sửa, verify consistency
  Cross-check: design-docs rules ↔ adopt behavior ↔ design-system behavior ↔ gate-check requirements
```

**Estimated total**: ~3-4 hours implementation

---

## Files touched (summary)

| File | Changes |
|------|---------|
| `rules/design-docs.md` | B1, B2, B3, B4, B6 — major rewrite |
| `commands/adopt.md` | B1, B2, B5, B6 + context warning |
| `commands/design-system.md` | B1, B6 + flow-only rewrite (rubrics extracted) + context warning |
| `commands/design-system-rubrics.md` | **NEW** — B2, B3, B4 quality guidance |
| `commands/review-all-gdds.md` | B2 + context warning |
| `commands/implement.md` | B1 + context warning |
| `commands/start.md` | B8 — "8" → "7" |
| `commands/gate-check.md` | B6 — N/A validation |
| `commands/create-architecture.md` | Context warning only |
| `CLAUDE.md` (template) | B1 — language fix |
| `pyproject.toml` | Version bump |
| `src/ugk/__init__.py` | Version bump |
| `README.md` | Version bump |
| `CHANGELOG.md` | Release notes |

**Total**: 14 files, 1 new (design-system-rubrics.md)

---

## Risks và mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Existing GDDs fail stricter rules | GDDs viết trước 1.2.0 có thể thiếu Given-When-Then AC | `/adopt` severity classification sẽ flag nhưng không reject — migration path rõ ràng |
| Agent over-enforces N/A | Agent reject section mà user muốn viết | N/A chỉ cho phép khi user confirm — agent không tự quyết |
| Backport quá nhiều CCGS complexity | Context window bloat, agent confused | Chỉ backport rubric format + quality bar, KHÔNG backport entity registry, agent routing, director gates, review modes |
| design-system.md quá dài | Đã dài, thêm guidance sẽ bloat | **Mitigated**: Split thành flow + rubrics (2 files). Flow ~80 lines, rubrics ~75 lines |
| Context window overflow trên long-running commands | Agent mất context giữa chừng, output bị cắt | **Mitigated**: 70% warning + immediate write + /compact suggestion trên ALL 5 long-running commands |

---

## Những gì KHÔNG backport (và tại sao)

| CCGS Feature | Lý do không backport |
|---|---|
| GDD template file | **B7 REJECTED** — GD gửi format tự do, /adopt convert |
| Game Feel section | **User decision**: dropped entirely |
| Entity registry (`design/registry/entities.yaml`) | Quá complex cho scope này |
| Agent routing table (specialist per section) | ugk có ít agent hơn CCGS (14 vs 49) |
| Director gates (`director-gates.md`) | Cần review mode system — scope riêng |
| Recovery/resume protocol | Đã có phần nào, cần audit riêng |
| Visual/Audio + UI Requirements sections | Không phải 7 required sections |
| Player Fantasy section | **Removed in v1.1.2** — never re-introduce |
