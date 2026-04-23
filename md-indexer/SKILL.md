---
name: md-indexer
description: Regenerates per-folder INDEX.md files and writes master index artifacts under generated/index for markdown repositories. Use when user asks to build, refresh, update, or repair markdown indexes or table of contents. Also use when user says "osvezi indeks", "napravi sadržaj", "ažuriraj index", "pregled fajlova", "nedostaje index", or asks why navigation is broken or out of date.
---
# MD Indexer

## Purpose

Use this skill to rebuild project navigation for markdown files with automatic index blocks.

## Default Workflow

1. Run dry-run first:
   - `python tools/build_indexes.py --dry-run`
2. Review which files would change.
3. Apply changes:
   - `python tools/build_indexes.py`
4. Verify output artifacts:
   - `generated/index/INDEX_ALL.md`
   - `generated/index/index.json`
   - updated or created `INDEX.md` files

## Scope and Behavior

- Script path: `tools/build_indexes.py`
- Root default: current repository root.
- Folder rule: creates/updates `INDEX.md` where folder has at least 2 markdown files.
- Existing content is preserved. Auto section is managed only inside:
  - `<!-- AUTO-INDEX:BEGIN -->`
  - `<!-- AUTO-INDEX:END -->`
- Extra exclusions can be added with:
  - `python tools/build_indexes.py --exclude-prefix some/path/`

## Expected Outputs

- `generated/index/INDEX_ALL.md` (master index across repo)
- `generated/index/index.json` (machine-readable listing)
- multiple folder-level `INDEX.md`

A generated auto-index block looks like this:

```markdown
<!-- AUTO-INDEX:BEGIN -->
## Auto Index: `kurikulum/uzrast_1_mladi`

| Fajl | Opis |
|------|------|
| [cas_01/lekcija.md](cas_01/lekcija.md) | Uvod u Go — slobode i hvatanje |
| [cas_01/nastavnik.md](cas_01/nastavnik.md) | Nastavnički vodič za čas 1 |
| [cas_01/vezbe.md](cas_01/vezbe.md) | Vežbe: slobode i atari |

*Automatski generisano — ne menjati ručno.*
<!-- AUTO-INDEX:END -->
```

## Safety Notes

- Do not delete user-authored sections outside auto-index markers.
- Do not auto-delete duplicates; only report potential duplicates.
- Prefer running from repo root for consistent relative links.
