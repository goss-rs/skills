---
name: go-accuracy-checker
description: >-
  Evaluates Go term accuracy in teaching documents against Sensei's Library
  definitions. Use when user asks to check Go accuracy, verify terminology,
  find mistakes in Go content, review Go pojmove, proveriti tačnost go pojmova,
  or validate that a lesson uses correct Go definitions.
---

# Go Accuracy Checker

## Purpose

Cross-check Go terminology in a document against authoritative definitions from
[Sensei's Library](https://senseis.xmp.net/) (26,000+ pages, de facto Go wiki).

## Required References — Read First

Before evaluating any document, read:

1. `tools/go_accuracy_reference.md` — curated SL definitions, error table, age-group rules
2. `tools/go_terms_taxonomy.md` — **80 pojmova** by game phase and intro age (use to check if a concept is appropriate for the target age group)
3. `tools/sl_definitions.md` — full cached SL definitions grouped by category (optional, load on demand)

If any reference file is missing, run:
```
python tools/fetch_sl_references.py
```

Fetch a single category only:
```
python tools/fetch_sl_references.py --category zivot_i_smrt
python tools/fetch_sl_references.py --list-categories
```

## Evaluation Workflow

### Step 1 — Identify Go claims in the document

Scan for:
- definitions of rules or concepts (liberty, capture, eyes, ko, sente…)
- moves / tactics described as "correct" or "optimal"
- life-and-death claims ("this group is alive/dead")
- terminology translations (Japanese→Serbian)

### Step 2 — Check each claim against the reference

For every claim, apply the test from `go_accuracy_reference.md`:

| Claim type | Check against |
|---|---|
| Liberty definition | Must be **orthogonal** adjacent empty points only |
| Two eyes = alive | Must be **two separate** eye spaces, not two adjacent liberties |
| Ko rule | Prohibits recreating the **same board position**, not just repeating a move |
| Sente / Gote | Sente = opponent **must answer or suffer losses** |
| Reverse sente | Move that forestalls opponent sente, ends in **gote** |
| False eye | Looks like eye, but surrounding stones can be **put into atari** |
| Seki | Mutual life — neither side can fill shared liberties **without dying** |
| Atari | Group has exactly **one liberty** |

### Step 3 — Distinguish error from pedagogical adaptation

See `go_accuracy_reference.md` §4. Key rule:

- **OK**: metaphor / simplification that does **not** contradict the rule
- **Error**: statement that is factually wrong regardless of audience

Examples:
- "Slobode su dah kamena" ✅ (Chinese etymology, pedagogically valid)
- "Dijagonalna polja su slobode" ✗ (factual error at any age level)
- "Ko je komplikovano" ✅ vs. "Ko = ne možeš ponoviti potez" ✗

### Step 4 — Apply age-group tolerance

From `go_accuracy_reference.md` §5:

| uzrast | May simplify | Must always be accurate |
|---|---|---|
| uzrast_1_mladi (6–8) | Joseki, ko types, yose | Liberties (orthogonal!), capture, two eyes |
| uzrast_2_srednji (9–12) | Complex ko types, seki edge cases | Sente/gote, false eye, moyo ≠ territory |
| uzrast_3_stariji (13+) | Professional nuances | Everything above + ko types, reverse sente |

### Step 5 — Output findings

Use the report structure in [checklist.md](checklist.md).

## Severity levels

| Level | Meaning |
|---|---|
| 🔴 GREŠKA | Factually incorrect — must fix regardless of audience |
| 🟡 NETAČNO ZA UZRAST | Acceptable for younger students, needs fix for older |
| 🟢 ADAPTACIJA | Pedagogically simplified but not wrong |
| ℹ️ NAPOMENA | Suggestion for added precision |

## Integration with LLM pipeline

The `tacnost_go` dimension in `tools/llm_review.py` already uses
`tools/go_accuracy_reference.md` as context.

To run automated review:
```bash
python tools/llm_review.py --folder kurikulum/<path> [--force]
python tools/_show_review.py <folder_path>
```

To update the SL cache:
```bash
python tools/fetch_sl_references.py --force
```
