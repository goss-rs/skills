# Project Skills

Ovaj folder sadrži projektne skills-ove koji su verzionisani u repozitorijumu.

## Trenutni skills

- `md-indexer`
- `doc-quality-review`
- `go-lesson-plan`

## Kako ih koristiš u ovom projektu

Cursor ih automatski učitava iz `.cursor/skills/<skill-name>/SKILL.md`.

## Kako da ih preneseš u druge projekte

Ako želiš da budu globalno dostupni u svim projektima, kopiraj svaki skill folder u:

- `~/.cursor/skills/<skill-name>/`

Primer:

```bash
cp -r .cursor/skills/md-indexer ~/.cursor/skills/md-indexer
cp -r .cursor/skills/doc-quality-review ~/.cursor/skills/doc-quality-review
cp -r .cursor/skills/go-lesson-plan ~/.cursor/skills/go-lesson-plan
```

Na Windows-u (PowerShell):

```powershell
Copy-Item -Recurse ".cursor/skills/md-indexer" "$HOME/.cursor/skills/md-indexer"
Copy-Item -Recurse ".cursor/skills/doc-quality-review" "$HOME/.cursor/skills/doc-quality-review"
Copy-Item -Recurse ".cursor/skills/go-lesson-plan" "$HOME/.cursor/skills/go-lesson-plan"
```

## Preporuka za održavanje

- Menjaj skill prvo projektno (ovde), testiraj na realnim zahtevima.
- Kad stabilizuješ tekst i workflow, promoviši ga u `~/.cursor/skills/`.
- Drži `name` i `description` kratko i specifično zbog boljeg auto-aktiviranja.
