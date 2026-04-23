---
name: go-lesson-plan
description: Generates Go lesson plans using a 5E-inspired structure adapted to age groups (6-8, 9-12, 13+). Use when user asks to draft a new Go class plan, lesson content, teacher notes, or exercises. Also use when user says "napravi čas", "plan časa", "priprema za čas", "nastavnik.md", "lekcija", "vežbe", "napravi lekciju", "osmisli čas", or specifies an age group and a Go topic together.
---
# Go Lesson Plan

## Purpose

Create reusable lesson packages for Go teaching, aligned to repository conventions:
- `lekcija.md` (student-facing lesson)
- `nastavnik.md` (teacher script and facilitation notes)
- `vezbe.md` (practice tasks and mini-drills)

Reference style:
- `kurikulum/uzrast_3_stariji/cas_01/lekcija.md`

## Skill Package Structure

This skill is intentionally split into multiple files:

- `SKILL.md` (execution workflow)
- `README.md` (how to maintain and reuse the skill)
- `reference/knowledge_catalog.json` (all markdown sources metadata)
- `reference/knowledge_map.md` (grouped source map for fast discovery)
- `reference/full_corpus.md` (full markdown corpus snapshot)
- `templates/lesson_pack_template.md` (starter lesson-pack template)
- `scripts/sync_skill_knowledge.py` (rebuild knowledge files from project sources)

Before drafting new lesson material, refresh the knowledge package:

- `python .cursor/skills/go-lesson-plan/scripts/sync_skill_knowledge.py`

## Language

Default output language is **English**. Exception: if generating into an existing folder that is already in Serbian (e.g. `kurikulum/`), match that folder's language. Per `docs/CONVENTIONS.md` §Naming — keep language consistent within a folder.

## Input Checklist

Before writing, collect:
- age group: `6-8`, `9-12`, or `13+`
- class duration in minutes → maps to `trajanje_min` in frontmatter
- lesson focus (e.g., liberties, life and death, yose) → maps to `teme`
- prerequisites: what concepts must students already know → maps to `predznanje` — ask if not provided
- target output files (`lekcija`, `nastavnik`, `vezbe`)

Frontmatter rules are defined in `docs/CONVENTIONS.md` §Frontmatter. Valid `status` values: `draft | reviewed | approved`. Valid `uloga` values: `lekcija | nastavnik | vezbe | resurs | ideja | syllabus`.

## Adaptation Rules by Age

- **6-8**: short segments, story and play-first framing, immediate interaction.
- **9-12**: challenge loops, clear goals, progression levels, mini-competitions.
- **13+**: analytical language, strategy trade-offs, AI/human comparative framing.

## Suggested Structure

### `lekcija.md`

1. H1 title for class.
2. Prerequisites ("Before this class you should know…") — brief, student-facing list.
3. Learning goals ("What we'll learn today").
4. Core concept explanation.
5. Worked examples or board snippets.
6. Student tasks.
7. Short recap + optional homework.

### `nastavnik.md`

1. Class objective and timing plan.
2. Facilitation script per segment.
3. Expected misunderstandings.
4. Intervention tactics for disengagement.
5. Evaluation prompts and exit questions.

### `vezbe.md`

1. Warm-up drills (easy).
2. Core tactical/strategic exercises (medium).
3. Challenge section (hard).
4. Quick answer key or hints.

## Quality Guardrails

- Keep terminology consistent (atari, sente, gote, joseki, tesuji, yose).
- Prefer concrete board decisions over abstract lecture text.
- Include at least one measurable success criterion.
- Keep sections scannable with clear headings and bullet lists.

## Mandatory Source-First Flow

1. Refresh and inspect `reference/knowledge_map.md`.
2. **Check for existing content:** search `reference/knowledge_catalog.json` for lessons with matching `teme` tags at the same age group. If a lesson already covers the topic, flag it to the user and ask whether to generate a follow-up / deeper lesson instead of duplicating.
3. Open relevant source paths from the map (age, topic, format).
4. Draft `lekcija.md`, `nastavnik.md`, `vezbe.md` from the template.
5. Ensure the `predznanje` frontmatter field is populated and that the prerequisite section appears in `lekcija.md`.
