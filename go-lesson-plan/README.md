# go-lesson-plan Skill Package

Ovaj skill folder je proširen tako da ne bude samo jedan `SKILL.md`, već kompletna baza znanja i šablona.

## Sadržaj

- `SKILL.md`  
  Glavna pravila korišćenja skilla.

- `reference/knowledge_catalog.json`  
  Katalog svih `.md` izvora u repozitorijumu (putanja, H1, sažetak, metrika).

- `reference/knowledge_map.md`  
  Pregled izvora grupisan po folderima za brzo pronalaženje tema.

- `reference/full_corpus.md`  
  Snapshot markdown korpusa iz sadržajnih zona projekta (bez `generated/`).

- `templates/lesson_pack_template.md`  
  Šablon za `lekcija.md` + `nastavnik.md` + `vezbe.md`.

- `scripts/sync_skill_knowledge.py`  
  Skripta koja regeneriše `reference/*` fajlove iz trenutnog stanja projekta.

## Održavanje

Kad god dodaš/menjaš `.md` dokumente u projektu, osveži knowledge paket:

```powershell
python .cursor/skills/go-lesson-plan/scripts/sync_skill_knowledge.py
```

Skripta trenutno automatski isključuje:

- `generated/`
- `gemini_ideje/skolski_program/resursi/` (privremena stabilizacija)

## Napomena

`full_corpus.md` može biti veliki fajl. To je očekivano: cilj je da skill paket sadrži centralizovan snapshot znanja za lesson planning bez generisanih artefakata.
