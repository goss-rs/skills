#!/usr/bin/env python3
"""ascii_to_sgf.py — Convert ASCII Go board diagrams to SGF format.

Supports the project's ASCII diagram conventions:
  - Simple dot-space notation  (. X O, space-separated)
  - Grid-box notation          (+--+--+ borders)
  - SL $$ notation             ($$B Title / $$ . X . lines)
  - Move-sequence numbers      (1–9 encoded as B/W moves)
  - Inline annotations         (stripped: ← X has 1 liberty)

SGF coordinate system:
  [column_letter][row_letter] — both start at 'a' = top-left of the diagram.
  e.g. top-left stone → AB[aa], column 2 row 3 → [bc]

Usage:
  # Extract all diagrams from a markdown file
  python ascii_to_sgf.py lesson.md

  # Process a whole directory (recursively)
  python ascii_to_sgf.py kurikulum/

  # Parse a diagram string directly (use \\n for newlines)
  python ascii_to_sgf.py --text ". X .\\nX . O\\n. O ."

  # Override board size and add a comment
  python ascii_to_sgf.py --text "..." --size 9 --comment "Black to play. Find the vital point."

  # Write SGF files to a specific output directory
  python ascii_to_sgf.py lesson.md --out sgf_output/
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Symbol tables
# ---------------------------------------------------------------------------

_BLACK = frozenset("X")
_WHITE = frozenset("O")
_EMPTY = frozenset(".,:_")
_MOVE_MAP = {str(d): d for d in range(1, 10)}  # '1'–'9' → 1–9
_MOVE_MAP["0"] = 10                              # '0' → move 10 (SL convention)
_LABEL = frozenset("abcdefghijklmnopqrstuvwxyz")
_EDGE_ONLY = re.compile(r"^[\s+\-|]+$")          # lines that are pure grid edges
_ANNOTATION = re.compile(r"\s*[←→↑↓]+.*$")       # trailing annotation after the cells
_SL_PREFIX = re.compile(r"^\$\$\S*\s?")           # $$ or $$B, $$W, $$C etc.

STANDARD_SIZES = [5, 7, 9, 13, 19]


# ---------------------------------------------------------------------------
# Diagram parsing
# ---------------------------------------------------------------------------

def _clean_line(line: str) -> Optional[list[str]]:
    """Strip prefixes/annotations from one diagram line; return list of cell tokens
    or None if the line is a pure edge/separator that carries no stones."""
    # Strip SL prefix ($$ $$B $$W $$C $$T ...)
    line = _SL_PREFIX.sub("", line)
    # Strip trailing annotation arrow (← comment)
    line = _ANNOTATION.sub("", line)
    # Drop pure edge lines (+--+--+, ----, |||)
    if _EDGE_ONLY.match(line):
        return None
    # Split into tokens; skip edge characters inside the line
    tokens = [t for t in line.split() if t not in ("|", "+", "-", "--", "---")]
    return tokens if tokens else None


def parse_diagram(text: str) -> Optional[dict]:
    """Parse raw ASCII/SL diagram text into a structured position dict.

    Returns:
        dict with keys:
            rows, cols       — grid dimensions of the parsed area
            board_size       — inferred standard board size (5/7/9/13/19)
            black            — list of (row, col) for static black stones
            white            — list of (row, col) for static white stones
            moves            — dict {move_num: (row, col, color_str)}
            labels           — dict {letter: (row, col)}
        or None if the text cannot be parsed.
    """
    lines = text.strip().splitlines()

    # Handle SL title line: first $$ line with only prose (no board symbols)
    # e.g. "$$B Atari example" — skip it.
    # Check the text AFTER stripping the $$ prefix, using word-boundary logic
    # so that 'O' inside a word ("Corner") is not mistaken for a stone symbol.
    cleaned_rows: list[list[str]] = []
    for line in lines:
        if _SL_PREFIX.match(line):
            after_prefix = _SL_PREFIX.sub("", line).strip()
            has_dot = "." in after_prefix
            has_digit = any(c.isdigit() for c in after_prefix)
            # Stone symbol only counts if isolated (not inside a word)
            has_stone = bool(re.search(r"(?<![A-Za-z])[XO](?![A-Za-z])", after_prefix))
            if not has_dot and not has_digit and not has_stone:
                continue  # this is a title/separator line
        tokens = _clean_line(line)
        if tokens is not None:
            cleaned_rows.append(tokens)

    if not cleaned_rows:
        return None

    # Normalize column count (pad shorter rows with '.')
    max_cols = max(len(r) for r in cleaned_rows)
    for row in cleaned_rows:
        row += ["."] * (max_cols - len(row))

    rows = len(cleaned_rows)
    cols = max_cols

    black: list[tuple[int, int]] = []
    white: list[tuple[int, int]] = []
    moves: dict[int, tuple[int, int, str]] = {}
    labels: dict[str, tuple[int, int]] = {}

    for r, row_tokens in enumerate(cleaned_rows):
        for c, cell in enumerate(row_tokens):
            if cell in _BLACK:
                black.append((r, c))
            elif cell in _WHITE:
                white.append((r, c))
            elif cell in _MOVE_MAP:
                num = _MOVE_MAP[cell]
                color = "B" if num % 2 == 1 else "W"
                moves[num] = (r, c, color)
            elif cell in _LABEL:
                labels[cell] = (r, c)
            # '.' and other empties: nothing to record

    if not black and not white and not moves:
        return None  # no stones — probably not a diagram

    return {
        "rows": rows,
        "cols": cols,
        "board_size": _infer_size(rows, cols),
        "black": black,
        "white": white,
        "moves": moves,
        "labels": labels,
    }


def _infer_size(rows: int, cols: int) -> int:
    """Return the smallest standard board size >= max(rows, cols)."""
    dim = max(rows, cols)
    for s in STANDARD_SIZES:
        if dim <= s:
            return s
    return 19


# ---------------------------------------------------------------------------
# SGF generation
# ---------------------------------------------------------------------------

def _sgf_coord(row: int, col: int) -> str:
    """Convert 0-indexed (row, col) from top-left to SGF coordinate string."""
    return f"[{chr(ord('a') + col)}{chr(ord('a') + row)}]"


def _escape(text: str) -> str:
    """Escape brackets for SGF text properties."""
    return text.replace("\\", "\\\\").replace("]", "\\]")


def build_sgf(
    parsed: dict,
    title: str = "",
    comment: str = "",
    board_size: Optional[int] = None,
    first_move_color: str = "B",
) -> str:
    """Build a complete SGF string from a parsed diagram dict.

    Args:
        parsed:           Output of parse_diagram().
        title:            Optional game/problem name (GN property).
        comment:          Optional comment on root node (C property).
        board_size:       Override the inferred board size.
        first_move_color: 'B' or 'W' — colour of move 1 if sequence found.
    Returns:
        SGF string.
    """
    sz = board_size or parsed["board_size"]

    # Root node properties
    props: list[str] = [
        "GM[1]FF[4]CA[UTF-8]",
        f"SZ[{sz}]",
    ]
    if title:
        props.append(f"GN[{_escape(title)}]")

    # Setup stones
    if parsed["black"]:
        coords = "".join(_sgf_coord(r, c) for r, c in parsed["black"])
        props.append(f"AB{coords}")
    if parsed["white"]:
        coords = "".join(_sgf_coord(r, c) for r, c in parsed["white"])
        props.append(f"AW{coords}")

    # Labels (LB property)
    if parsed["labels"]:
        lb_values = "".join(
            f"{_sgf_coord(r, c)[:-1]}:{letter}]"
            for letter, (r, c) in sorted(parsed["labels"].items())
        )
        props.append(f"LB{lb_values}")

    if comment:
        props.append(f"C[{_escape(comment)}]")

    root_node = "(;" + "\n".join(props)

    # Move sequence (each move becomes a child node)
    if parsed["moves"]:
        move_nodes: list[str] = []
        for num in sorted(parsed["moves"]):
            r, c, color = parsed["moves"][num]
            move_nodes.append(f";{color}{_sgf_coord(r, c)}")
        return root_node + "\n" + "\n".join(move_nodes) + ")"
    else:
        return root_node + ")"


# ---------------------------------------------------------------------------
# Markdown extraction
# ---------------------------------------------------------------------------

# Matches fenced code blocks (``` ... ```)
_CODE_BLOCK = re.compile(r"```[^\n]*\n(.*?)```", re.DOTALL)
# Matches SL diagram blocks (consecutive $$ lines)
_SL_BLOCK = re.compile(r"(?m)^(\$\$.*(?:\n\$\$.*)+)")
# Heading or bold text that might serve as diagram title
_PRECEDING_TITLE = re.compile(r"(?:^#{1,4}\s+(.+)|(?:^|\n)\*\*(.+?)\*\*)\s*$")


def _extract_title_before(text: str, match_start: int) -> str:
    """Find the last heading or bold title before match_start."""
    preceding = text[:match_start].rstrip()
    if not preceding:
        return ""
    last_line = preceding.rsplit("\n", 1)[-1].strip()
    # Strip markdown formatting characters
    clean = re.sub(r"[#*_`>]", "", last_line).strip()
    return clean if clean and len(clean) < 80 else ""


def _looks_like_diagram(content: str) -> bool:
    """Heuristic: does this code block look like a Go board diagram?"""
    # Must have at least 2 non-empty lines
    lines = [l.strip() for l in content.strip().splitlines() if l.strip()]
    if len(lines) < 2:
        return False
    joined = " ".join(lines)
    # Must contain dots AND at least one stone/move symbol
    has_dot = "." in joined
    has_stone = bool(re.search(r"\b[XO]\b", joined))
    has_move = bool(re.search(r"\b[1-9]\b", joined))
    return has_dot and (has_stone or has_move)


def extract_diagrams(markdown_text: str) -> list[tuple[str, str]]:
    """Extract all Go diagrams from markdown text.

    Returns list of (title, raw_diagram_text) tuples.
    """
    results: list[tuple[str, str]] = []

    # Fenced code blocks
    for match in _CODE_BLOCK.finditer(markdown_text):
        content = match.group(1)
        if _looks_like_diagram(content):
            title = _extract_title_before(markdown_text, match.start())
            results.append((title, content.strip()))

    # SL $$ blocks
    for match in _SL_BLOCK.finditer(markdown_text):
        content = match.group(1)
        # Extract title from first $$ line
        first_line = content.split("\n", 1)[0]
        title = _SL_PREFIX.sub("", first_line).strip()
        results.append((title, content.strip()))

    return results


# ---------------------------------------------------------------------------
# File I/O
# ---------------------------------------------------------------------------

def _safe_stem(title: str, max_len: int = 30) -> str:
    """Turn a title into a safe filename stem."""
    s = re.sub(r"[^\w\s-]", "", title).strip()
    s = re.sub(r"[\s-]+", "_", s).lower()
    return s[:max_len] if s else ""


def process_file(
    path: Path,
    output_dir: Optional[Path] = None,
    verbose: bool = True,
) -> list[Path]:
    """Extract diagrams from a markdown file and write .sgf files.

    Returns the list of paths written.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"  Error reading {path}: {e}", file=sys.stderr)
        return []

    diagrams = extract_diagrams(text)
    if not diagrams:
        if verbose:
            print(f"  (no diagrams found)")
        return []

    out_dir = output_dir or path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = path.stem
    written: list[Path] = []

    for i, (title, content) in enumerate(diagrams, start=1):
        parsed = parse_diagram(content)
        if parsed is None:
            if verbose:
                print(f"  [{i}] parse failed: {title!r}")
            continue

        sgf_text = build_sgf(parsed, title=title or f"Diagram {i} from {stem}")

        safe = _safe_stem(title)
        fname = f"{stem}_{safe}.sgf" if safe else f"{stem}_diagram_{i:02d}.sgf"
        out_path = out_dir / fname
        # Avoid overwriting duplicates from same file
        if out_path.exists():
            out_path = out_dir / f"{stem}_diagram_{i:02d}.sgf"
        out_path.write_text(sgf_text, encoding="utf-8")

        if verbose:
            label = title or "(untitled)"
            print(f"  [{i}] {label} -> {out_path.name}  ({parsed['rows']}x{parsed['cols']}, sz={parsed['board_size']})")
        written.append(out_path)

    return written


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert ASCII Go board diagrams from markdown files to SGF.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        type=Path,
        metavar="PATH",
        help="Markdown files or directories to process.",
    )
    parser.add_argument(
        "--text",
        type=str,
        default=None,
        metavar="DIAGRAM",
        help="Parse a diagram string directly (use \\\\n for newlines). Prints SGF to stdout.",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="",
        help="Title/name for --text mode.",
    )
    parser.add_argument(
        "--comment",
        type=str,
        default="",
        help="Comment/task description for --text mode.",
    )
    parser.add_argument(
        "--size",
        type=int,
        default=None,
        metavar="N",
        help="Override board size (e.g. 9, 13, 19).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        metavar="DIR",
        help="Output directory for SGF files (default: same directory as input).",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-diagram output.",
    )
    args = parser.parse_args()

    # --text mode: parse inline and print
    if args.text is not None:
        raw = args.text.replace("\\n", "\n")
        parsed = parse_diagram(raw)
        if parsed is None:
            print("Error: could not parse diagram — no recognizable stones found.", file=sys.stderr)
            print("Tip: stones must be X or O, empty points must be dots (.).", file=sys.stderr)
            return 1
        sgf_text = build_sgf(parsed, title=args.title, comment=args.comment, board_size=args.size)
        print(sgf_text)
        return 0

    if not args.inputs:
        parser.print_help()
        return 0

    total_written: list[Path] = []
    for inp in args.inputs:
        inp = inp.resolve()
        if inp.is_dir():
            md_files = sorted(inp.rglob("*.md"))
            print(f"Scanning {len(md_files)} markdown files in {inp.name}/")
            for f in md_files:
                rel = f.relative_to(inp)
                if not args.quiet:
                    print(f"{rel}:")
                written = process_file(f, args.out, verbose=not args.quiet)
                total_written.extend(written)
        elif inp.suffix.lower() == ".md":
            if not args.quiet:
                print(f"{inp.name}:")
            total_written.extend(process_file(inp, args.out, verbose=not args.quiet))
        else:
            print(f"Skipping {inp.name} (not a .md file or directory).", file=sys.stderr)

    if not args.quiet:
        print(f"\nTotal SGF files written: {len(total_written)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
