---
name: doc-quality-review
description: Audits markdown document quality using objective checks and a rubric-aligned LLM review flow. Use when user asks for document quality assessment, scoring, audit, or prioritized improvements. Also use when user says "proveri kvalitet", "oceni dokument", "pregled kvaliteta", "koji fajlovi su loši", "audit", or asks which documents need the most work.
---
# Doc Quality Review

## Purpose

Assess markdown quality with a two-layer method:
- objective metrics from script (0–40 pts)
- subjective rubric scoring via LLM prompt (0–60 pts)

The rubric is in `tools/quality_rubric.md` — read it before scoring to understand what each dimension rewards.

## Required Inputs

- Rubric file: `tools/quality_rubric.md`
- Audit script: `tools/quality_audit.py`
- LLM prompt template: `tools/llm_review_prompt.md`

## Workflow

1. Run objective audit:
   - `python tools/quality_audit.py`
2. Inspect outputs:
   - `generated/quality/quality_report.csv`
   - `generated/quality/quality_report.md`
3. Prioritize files for LLM review:
   - low `auto_score_40` (below 25)
   - flagged `mrtvi_linkovi`, `todo_markeri`, `bez_naslova`
4. For each selected file, run LLM review with template in `tools/llm_review_prompt.md`.
5. Compute final score:
   - `final_score_100 = auto_score_40 + jasnoća_20 + pedagogija_20 + go_tačnost_20`

## Report Format

Present findings using this structure:

```
## [filename] — final: XX/100

| Dimenzija       | Skor | Napomena |
|-----------------|------|----------|
| Struktura       | /20  |          |
| Kompletnost     | /20  |          |
| Jasnoća         | /20  |          |
| Pedagogija      | /20  |          |
| Go tačnost      | /20  |          |

### 🔴 Kritični problemi (moraju se popraviti)
- …

### 🟡 Poboljšanja kvaliteta
- …

### 🟢 Polishing (opciono)
- …
```

**Example merged score:**
```
auto_score_40 = 28   (struktura: 15, kompletnost: 13)
jasnoća       = 14
pedagogija    = 16
go_tačnost    = 18
─────────────────────
final_score   = 76/100
```

## Safety Notes

- Do not silently rewrite content while auditing.
- Preserve source intent and audience (nastavnik/učenik).
- Treat LLM scores as review input, not absolute truth; keep confidence visible.
- When running a bulk audit, report the bottom 5 files first — those are the highest-priority fixes.
