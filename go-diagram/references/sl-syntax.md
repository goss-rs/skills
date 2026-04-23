# Sensei's Library Diagram Syntax — Reference

Source: https://senseis.xmp.net/?HowDiagramsWork

## First line options

```
$$(B|W)(c)(size)(mNUM) title
```

| Option | Meaning | Example |
|:---|:---|:---|
| `B` | Black plays first (default) | `$$B` |
| `W` | White plays first | `$$W` |
| `c` | Show coordinate markers | `$$c` |
| `13` | Specify board size for partial board | `$$13` |
| `mNUM` | Starting move number | `$$Wm67` |
| title | Diagram caption | `$$B Two eyes` |

## Board symbols (per intersection)

| Symbol | Meaning |
|:---|:---|
| `.` | Empty intersection |
| `X` | Black stone |
| `O` | White stone |
| `,` | Star point (hoshi) — empty |
| `\|` `+` `-` | Board edge / empty border space |
| `_` | Empty space (gaps between sub-boards) |
| `1`–`9`, `0` | Move sequence (0 = move 10) |

## Markup symbols

| In diagram | In text | Meaning |
|:---|:---|:---|
| `B` | `BC` | Black stone + circle |
| `W` | `WC` | White stone + circle |
| `#` | `BS` | Black stone + square |
| `@` | `WS` | White stone + square |
| `Y` | `BT` | Black stone + triangle |
| `Q` | `WT` | White stone + triangle |
| `C` | `EC` | Circle on empty point |
| `S` | `ES` | Square on empty point |
| `T` | `ET` | Triangle on empty point |
| `a`–`z` | `a`–`z` | Letter label on empty point |
| `?` | — | Empty point not in search pattern |

## Board edges

- `|` — left/right sides
- `+` — corners
- `-` — top/bottom
- All three are interchangeable; the board edge is automatically placed at the outermost dots with space outside them.

## Moves at the same point (ko, passes)

Put collisions in the title: `Ko (5 at 1, 8 at 2)` — this is also included in generated SGF.

## Lines and arrows

```
$$ {AR point1 point2}    ← arrow from point1 to point2
$$ {LN point1 point2}    ← line between points
```

Two coordinate systems:
- Board coordinates: `A1` to `T19` (requires anchored corner)
- Absolute: `X:Y` from upper-left at `1:1`

## Links in diagrams

```
$$ [MarkupChar | PageName]
$$ [2 | NadareJoseki]
$$ [a | http://external.url]
```

## Comparison diagrams

Use `_` for blank space between two sub-boards placed side by side on the same diagram.

## Full example

```
$$B Two eyes — alive group
$$  ---------
$$ | . X X X .
$$ | X . X . X
$$ | X X X X X
$$  ---------
```

```
$$Wm67 Sente sequence
$$  -------
$$ | . . 7 3 X d
$$ | . . O 1 O 6
$$ | . . 4 2 5 c
$$ | . . 8 X a .
```
