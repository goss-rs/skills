# go-teaching-skills

Cursor Agent Skills for Go (baduk) teaching and curriculum development.

## Skills

| Skill | What it does |
|---|---|
| [`go-lesson-plan`](go-lesson-plan/) | Generates lesson packs (lekcija / nastavnik / vezbe) for age groups 6–8, 9–12, 13+ |
| [`go-accuracy-checker`](go-accuracy-checker/) | Cross-checks Go terminology in teaching docs against Sensei's Library definitions |
| [`doc-quality-review`](doc-quality-review/) | Audits markdown document quality (objective metrics + LLM rubric scoring) |
| [`md-indexer`](md-indexer/) | Regenerates per-folder INDEX.md files and master index artifacts |

## Install

### Windows (PowerShell)

```powershell
.\install.ps1
```

Or manually:

```powershell
git clone https://github.com/goss-rs/skills.git "$env:USERPROFILE\.cursor\skills\go-teaching-skills"
```

### macOS / Linux

```bash
bash install.sh
```

Or manually:

```bash
git clone https://github.com/goss-rs/skills.git ~/.cursor/skills/go-teaching-skills
```

After install, skills are available in **all** your Cursor projects automatically.

## Update

```powershell
# Windows
git -C "$env:USERPROFILE\.cursor\skills\go-teaching-skills" pull

# macOS / Linux
git -C ~/.cursor/skills/go-teaching-skills pull
```

## First-time setup for `go-lesson-plan`

After installing, run the knowledge sync from your Go teaching repo to populate the reference corpus:

```bash
python .cursor/skills/go-teaching-skills/go-lesson-plan/scripts/sync_skill_knowledge.py
```

This builds `reference/knowledge_map.md` and `reference/full_corpus.md` locally (they are gitignored — generated from your project content).

## Using in a specific project (submodule, optional)

If you want the skills version-pinned to a project rather than user-global:

```bash
git submodule add https://github.com/goss-rs/skills.git .cursor/skills/go-teaching-skills
git submodule update --init
```

## Repository layout

```
go-teaching-skills/
├── go-lesson-plan/
│   ├── SKILL.md
│   ├── README.md
│   ├── templates/
│   │   └── lesson_pack_template.md
│   ├── scripts/
│   │   └── sync_skill_knowledge.py
│   └── reference/          ← populated locally by sync script, gitignored
├── go-accuracy-checker/
│   ├── SKILL.md
│   └── checklist.md
├── doc-quality-review/
│   └── SKILL.md
├── md-indexer/
│   └── SKILL.md
├── install.ps1
└── install.sh
```
