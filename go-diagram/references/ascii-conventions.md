# ASCII Board Diagram Conventions

Used in this project's markdown teaching documents.

## Symbols

| Symbol | Meaning |
|:---|:---|
| `.` | Empty intersection |
| `X` | Black stone |
| `O` | White stone |
| `+--+` | Corner / board edge |
| `\|` | Side edge |
| Numbers `1`–`9` | Move sequence |
| `←` `→` `↑` `↓` | Arrows for annotations |

## Board edge patterns

```
+--+--+--+--+
|  |  |  |  |
+--+--+--+--+
|  |  |  |  |
+--+--+--+--+
```

Or minimal (no grid lines):

```
. . . . .
. X . . .
. . O . .
. . . . .
. . . . .
```

## Annotation style

Use `←` or inline labels for key points:

```
. . . . .
. O O . .
O X . . .    ← X has 1 liberty (atari)
. O . . .
. . . . .
```

## Preferred sizes by context

| Use | Board size | Notes |
|:---|:---|:---|
| Concept illustration | 5×5 or 7×7 fragment | Show only relevant area |
| Tsumego | 5×5 to 9×9 | Include all relevant stones |
| Joseki | Corner fragment (6×6) | Top-left corner convention |
| Sente/gote examples | 7×7 fragment | Show full sequence context |

## When to use ASCII vs SL format

| Context | Format |
|:---|:---|
| Teaching docs (lekcija.md, nastavnik.md, vezbe.md) | ASCII |
| Sensei's Library wiki publishing | SL `$$` |
| SGF-generating sequences | SL `$$` (auto-generates SGF) |
| Quick inline illustration | ASCII |
| Diagrams with arrows, links, coordinates | SL `$$` |
