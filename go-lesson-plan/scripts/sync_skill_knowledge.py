"""
Sync go-lesson-plan skill knowledge artifacts from all markdown files in a repo.

Usage:
  python sync_skill_knowledge.py                   # uses CWD as repo root
  python sync_skill_knowledge.py --repo-root /path/to/project

Outputs (always written next to this script, in ../reference/):
  knowledge_catalog.json
  knowledge_map.md
  full_corpus.md
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".cursor/plans", "generated"}
DEFAULT_EXCLUDE_PREFIXES: list[str] = []


@dataclass
class Doc:
    rel_path: str
    h1: str
    summary: str
    lines: int
    words: int
    mtime: str
    content: str


def find_repo_root(start: Path) -> Path:
    """Walk up from start looking for a .git dir that is NOT the skills repo itself."""
    skills_git = (Path(__file__).resolve().parents[3] / ".git")
    current = start.resolve()
    for candidate in [current, *current.parents]:
        git_dir = candidate / ".git"
        if git_dir.exists() and git_dir != skills_git:
            return candidate
    return current


def extract_h1(lines: list[str]) -> str:
    for line in lines:
        if line.strip().startswith("# "):
            return line.strip()[2:].strip()
    return ""


def extract_summary(lines: list[str]) -> str:
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith("#") or s.startswith("```") or s.startswith("|"):
            continue
        return s[:180]
    return ""


def is_excluded(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    if any(part in IGNORE_DIRS for part in path.parts):
        return True
    if rel.startswith(".cursor/plans/"):
        return True
    if any(rel.startswith(prefix) for prefix in DEFAULT_EXCLUDE_PREFIXES):
        return True
    return False


def collect_docs(root: Path) -> list[Doc]:
    docs: list[Doc] = []
    for path in sorted(root.rglob("*.md")):
        if is_excluded(path, root):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        docs.append(
            Doc(
                rel_path=path.relative_to(root).as_posix(),
                h1=extract_h1(lines),
                summary=extract_summary(lines),
                lines=len(lines),
                words=len(re.findall(r"\b\w+\b", text)),
                mtime=datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds"),
                content=text,
            )
        )
    return docs


def write_catalog(reference_dir: Path, docs: list[Doc]) -> None:
    payload = [
        {
            "path": d.rel_path,
            "h1": d.h1,
            "summary": d.summary,
            "lines": d.lines,
            "words": d.words,
            "mtime": d.mtime,
        }
        for d in docs
    ]
    out = reference_dir / "knowledge_catalog.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_map(reference_dir: Path, docs: list[Doc]) -> None:
    by_top: dict[str, list[Doc]] = defaultdict(list)
    for d in docs:
        top = d.rel_path.split("/", 1)[0]
        by_top[top].append(d)

    lines: list[str] = []
    lines.append("# Knowledge Map")
    lines.append("")
    lines.append("Mapa svih markdown izvora u projektu, grupisana po top-level folderu.")
    lines.append("")
    lines.append(f"- Ukupno dokumenata: **{len(docs)}**")
    lines.append("")
    for top in sorted(by_top):
        lines.append(f"## {top}")
        lines.append("")
        lines.append("| Path | H1 | Summary | Lines |")
        lines.append("|---|---|---|---:|")
        for d in sorted(by_top[top], key=lambda x: x.rel_path):
            h1 = d.h1.replace("|", "\\|") if d.h1 else "—"
            summary = d.summary.replace("|", "\\|") if d.summary else "—"
            lines.append(f"| `{d.rel_path}` | {h1} | {summary} | {d.lines} |")
        lines.append("")
    (reference_dir / "knowledge_map.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_full_corpus(reference_dir: Path, docs: list[Doc]) -> None:
    lines: list[str] = []
    lines.append("# Full Markdown Corpus")
    lines.append("")
    lines.append("Automatski snapshot svih markdown dokumenata u projektu.")
    lines.append("Svaki dokument je obeležen markerima `SOURCE BEGIN/END`.")
    lines.append("")
    for d in docs:
        lines.append(f"<!-- SOURCE BEGIN: {d.rel_path} -->")
        lines.append("")
        lines.append(d.content.rstrip())
        lines.append("")
        lines.append(f"<!-- SOURCE END: {d.rel_path} -->")
        lines.append("")
    (reference_dir / "full_corpus.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Sync go-lesson-plan knowledge artifacts.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Root of the project to index (default: CWD, or nearest git repo above CWD)",
    )
    args = parser.parse_args()

    # Reference output always lives next to this script → ../reference/
    reference_dir = Path(__file__).resolve().parent.parent / "reference"
    reference_dir.mkdir(parents=True, exist_ok=True)

    # Project to index
    if args.repo_root:
        repo_root = args.repo_root.resolve()
    else:
        repo_root = find_repo_root(Path.cwd())

    docs = collect_docs(repo_root)
    write_catalog(reference_dir, docs)
    write_map(reference_dir, docs)
    write_full_corpus(reference_dir, docs)

    print(f"Repo indexed: {repo_root}")
    print(f"Synced docs:  {len(docs)}")
    print(f"Wrote: {(reference_dir / 'knowledge_catalog.json').as_posix()}")
    print(f"Wrote: {(reference_dir / 'knowledge_map.md').as_posix()}")
    print(f"Wrote: {(reference_dir / 'full_corpus.md').as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
