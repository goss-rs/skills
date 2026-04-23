#!/usr/bin/env python3
"""sgf_check.py — Verify an SGF file by rendering it back as ASCII.

Reads one or more SGF files and prints a minimal ASCII representation of
each root position (AB/AW setup stones) so you can visually confirm the
ascii_to_sgf.py conversion was correct.

Does NOT require any external libraries — uses only stdlib regex parsing.

Usage:
  python sgf_check.py position.sgf
  python sgf_check.py *.sgf
  python sgf_check.py sgf_output/
"""

import argparse
import re
import sys
from pathlib import Path

# SGF property value extractor
_PROP = re.compile(r"([A-Z]{1,2})((?:\[[^\]]*\])+)")
_COORD_VALUES = re.compile(r"\[([^\]]*)\]")


def _parse_coords(raw: str) -> list[tuple[int, int]]:
    """Extract list of (row, col) from an SGF property value string like [aa][bc]."""
    result = []
    for m in _COORD_VALUES.finditer(raw):
        val = m.group(1)
        if len(val) < 2 or val == "tt":  # 'tt' = pass
            continue
        col = ord(val[0]) - ord("a")
        row = ord(val[1]) - ord("a")
        result.append((row, col))
    return result


def _render(black: list, white: list, moves: dict, size: int) -> str:
    """Render stones on a grid."""
    grid = [["." for _ in range(size)] for _ in range(size)]

    for r, c in black:
        if 0 <= r < size and 0 <= c < size:
            grid[r][c] = "X"
    for r, c in white:
        if 0 <= r < size and 0 <= c < size:
            grid[r][c] = "O"

    symbols = "123456789"
    for num, (r, c, _color) in sorted(moves.items()):
        if 0 <= r < size and 0 <= c < size:
            grid[r][c] = symbols[num - 1] if num <= 9 else str(num)

    col_labels = "  " + " ".join(chr(ord("a") + i) for i in range(size))
    lines = [col_labels]
    for r, row in enumerate(grid):
        lines.append(f"{chr(ord('a') + r)} {' '.join(row)}")
    return "\n".join(lines)


def check_sgf(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")

    # Parse properties directly from the full SGF text — handles both single-node
    # (setup-only) and multi-node (move-sequence) SGFs without fragile root extraction.
    root = text

    # Parse properties
    size = 19
    black: list[tuple[int, int]] = []
    white: list[tuple[int, int]] = []
    moves: dict[int, tuple[int, int, str]] = {}
    title = ""
    comment = ""

    for prop_match in _PROP.finditer(root):
        name = prop_match.group(1)
        values_raw = prop_match.group(2)
        if name == "SZ":
            m = re.search(r"\[(\d+)\]", values_raw)
            if m:
                size = int(m.group(1))
        elif name == "AB":
            black = _parse_coords(values_raw)
        elif name == "AW":
            white = _parse_coords(values_raw)
        elif name == "GN":
            title = re.sub(r"\[|\]", "", values_raw).strip()
        elif name == "C":
            comment = re.sub(r"\[|\]", "", values_raw).strip()[:80]

    # Parse moves (child nodes after root)
    move_num = 1
    for m in re.finditer(r";([BW])\[([a-s]{2})\]", text):
        color = m.group(1)
        coord = m.group(2)
        col = ord(coord[0]) - ord("a")
        row = ord(coord[1]) - ord("a")
        moves[move_num] = (row, col, color)
        move_num += 1

    # Report
    divider = "-" * 40
    print(f"\n{divider}")
    print(f"File   : {path.name}")
    print(f"Title  : {title or '(none)'}")
    print(f"Size   : {size}x{size}")
    print(f"Black  : {len(black)} stone(s)  |  White: {len(white)} stone(s)  |  Moves: {len(moves)}")
    if comment:
        print(f"Comment: {comment}")
    print()
    print(_render(black, white, moves, size))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render SGF file(s) as ASCII to verify ascii_to_sgf.py output."
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        type=Path,
        metavar="PATH",
        help="SGF files or a directory containing .sgf files.",
    )
    args = parser.parse_args()

    files: list[Path] = []
    for inp in args.inputs:
        inp = inp.resolve()
        if inp.is_dir():
            files.extend(sorted(inp.glob("*.sgf")))
        elif inp.suffix.lower() == ".sgf":
            files.append(inp)
        else:
            print(f"Skipping {inp.name} (not .sgf)", file=sys.stderr)

    if not files:
        print("No SGF files found.", file=sys.stderr)
        return 1

    for f in files:
        check_sgf(f)

    print(f"\n{'-' * 40}")
    print(f"Checked {len(files)} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
