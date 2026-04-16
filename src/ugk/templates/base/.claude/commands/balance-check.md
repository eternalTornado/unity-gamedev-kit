---
name: balance-check
description: Verify game balance by cross-referencing spec formulas with implementation. Checks tuning knob values, formula correctness, and data-driven config.
---

# /balance-check -- Balance Verification

## What this command does

Cross-references the formulas and tuning knobs defined in design specs against the actual code implementation to catch balance drift.

## Usage

```
/balance-check
/balance-check --gdd Design/GDD/combat.md
```

`--gdd <path>` — optional. Also read the original GDD for additional design context (rationale behind formula choices).

## Process

1. **Read** all specs (check `Docs/Retrofit/` first, fallback `Design/GDD/`) that contain Formulas and Tuning Knobs sections. If `--gdd` provided, also read the original GDD.
2. **Scan** code for implementations of those formulas:
   - Search `Assets/Scripts/` for formula-related class/method names
   - Search `Assets/Data/` or `Resources/` for config files (JSON, ScriptableObjects)
3. **For each formula in GDDs**:
   - Is it implemented in code? (match by name or logic)
   - Does the implementation match the spec formula?
   - Are tuning knob values within the spec-specified ranges?
   - Are values data-driven (config file) or hardcoded?
4. **Flag issues**:
   - DRIFT: Code formula differs from spec formula
   - HARDCODED: Value should be in config but is inline
   - OUT_OF_RANGE: Config value outside spec-specified range
   - MISSING: spec formula has no code implementation
5. **Present** findings with GDD reference, code location, and suggested fix.

## Output

Report printed to conversation. Optionally write to `Production/qa/balance-check-<date>.md`.

## Collaboration protocol

Present findings. For each drift, ask: update the GDD or update the code? Run `/update-gdd` or apply code fix accordingly.
