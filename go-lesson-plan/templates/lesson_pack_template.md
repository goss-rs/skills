# Lesson Pack Template

Use this template to create three linked files:
- `lekcija.md`
- `nastavnik.md`
- `vezbe.md`

Default language: **English**. Switch to Serbian only when the user writes in Serbian or explicitly requests it.

---

## 1) `lekcija.md` (student-facing)

```md
---
uloga: lekcija
uzrast: [uzrast_1_mladi | uzrast_2_srednji | uzrast_3_stariji]
cas: [number]
teme: [topic_tag_1, topic_tag_2]
predznanje: [prerequisite_topic_1, prerequisite_topic_2]
trajanje_min: [duration]
status: draft             # draft | reviewed | approved
# review_date: YYYY-MM-DD   (add when reviewed)
# skorovi: [s, j, p, t, k, ukupno]  (add after QA)
---
# Class X: [Title]

## Before This Class
You should already know:
- [Prerequisite concept 1]
- [Prerequisite concept 2]

*Not sure? Review: [link or class number where this was covered]*

## What We'll Learn Today
- [Outcome 1]
- [Outcome 2]
- [Outcome 3]

## Key Concept
[Short, clear explanation]

## Example / Position
[One concrete situation + explanation of the decision]

## Activities
1. [Activity A]
2. [Activity B]

## Quick Recap
- [Question 1]
- [Question 2]
```

## 2) `nastavnik.md` (teacher script)

```md
---
uloga: nastavnik
uzrast: [uzrast_1_mladi | uzrast_2_srednji | uzrast_3_stariji]
cas: [number]
teme: [topic_tag_1, topic_tag_2]
predznanje: [prerequisite_topic_1, prerequisite_topic_2]
trajanje_min: [duration]
status: draft             # draft | reviewed | approved
---
# Class X: [Title] — Teacher Notes

## Class Objective
[What students must be able to do by the end of class]

## Prerequisite Check
Before the hook, quickly confirm students know:
- [Prerequisite 1] — ask: "[quick verification question]"
- [Prerequisite 2] — ask: "[quick verification question]"

If most students can't answer: run a 5-minute recap before proceeding.

## Timing Plan
| Time | Activity |
|:---|:---|
| 0–5 min | [Hook] |
| 5–12 min | [Explanation] |
| 12–18 min | [Guided practice] |
| 18–20 min | [Wrap-up] |

## Expected Mistakes and Interventions
- Mistake: [description]
  - Intervention: [action]

## Success Criteria
- [Measurable indicator 1]
- [Measurable indicator 2]
```

## 3) `vezbe.md` (drill tasks)

```md
---
uloga: vezbe
uzrast: [uzrast_1_mladi | uzrast_2_srednji | uzrast_3_stariji]
cas: [number]
teme: [topic_tag_1, topic_tag_2]
predznanje: [prerequisite_topic_1, prerequisite_topic_2]
trajanje_min: [duration]
status: draft             # draft | reviewed | approved
---
# Class X: Exercises

## Warm-Up
1. [Easy task]
2. [Easy task]

## Core Exercises
1. [Medium]
2. [Medium]

## Challenge
1. [Hard]

## Hints / Answer Key
- [Hint 1]
- [Hint 2]
```

---

## Age Adaptation (quick reference)

- **6-8**: shorter blocks, more visual narrative, story-first framing.
- **9-12**: mini-challenges, clear progression levels, mini-competitions.
- **13+**: analytical language, decision trade-offs, debate and variant discussion.
