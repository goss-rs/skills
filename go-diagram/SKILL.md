---
name: go-diagram
description: >-
  Creates Go board diagrams with verbal descriptions from natural language position descriptions.
  Supports ASCII (for markdown), SL $$ format (for Sensei's Library), and SGF.
  Always pairs diagrams with a structured verbal explanation.
  Use when user asks to draw a Go position, create a board diagram, illustrate a concept,
  make a tsumego problem, show a joseki, generate a diagram for a lesson,
  or convert a position description into a visual. Also use when user says
  "nacrtaj poziciju", "prikaži dijagram", "napravi tsumego", "ilustruj koncept".
---

# Go Diagram

Creates Go board diagrams paired with verbal descriptions.

Every output has two parts:
1. **The diagram** — ASCII, SL `$$`, or SGF depending on context
2. **The verbal description** — a structured explanation of what the diagram shows

The verbal part is not optional. A diagram without words leaves the reader doing all the interpretive work. The words tell them what to look for, why it matters, and what to decide.

## References

- `references/sl-syntax.md` — full SL `$$` syntax (read when generating SL format)
- `references/ascii-conventions.md` — ASCII conventions and format selection guide

## Format Selection

| User context | Default format |
|:---|:---|
| Teaching doc (lekcija / nastavnik / vezbe) | ASCII |
| Sensei's Library publishing | SL `$$` |
| Needs move sequence / SGF generation | SL `$$` |
| Needs arrows or coordinate markers | SL `$$` |
| Quick inline illustration | ASCII |
| User says "SGF" | SGF |

When unsure, ask or default to ASCII. State the chosen format.

## Request Types

### 1. Concept illustration
Show a Go concept (liberty, atari, two eyes, sente, false eye, etc.) in a clear, minimal position.
- Use the smallest board that shows the point without noise.
- Highlight the relevant stones/points with markup in SL, or arrows/comments in ASCII.

### 2. Tsumego (life/death or tactical problem)
Show a position where the correct move matters.
- Present the position without the answer.
- In the verbal description, state the problem clearly: "Black to play. Can this group be saved?"
- Add a **Solution** section separately (collapsible if possible, or clearly separated).

### 3. Joseki / shape diagram
Show a standard sequence or shape with move numbers.
- Use SL `$$` with numbered moves when sequence matters.
- ASCII is fine for static shape illustrations.

### 4. Game position
Show a board state from a described game context.
- Include only the relevant area unless full board is requested.
- Note whose turn it is.

### 5. Comparison
Show two positions side by side (before/after, correct/incorrect).
- SL `$$` using `_` separator for side-by-side.
- ASCII: two separate code blocks labeled "Position A" / "Position B".

## Verbal Description Format

Always include all applicable sections. Omit inapplicable ones (e.g. no "Task" for a pure concept illustration).

```
**Setup:** [Board size/fragment. Who has stones where. Whose turn if relevant.]

**Concept:** [What Go concept or principle this position demonstrates.]

**What to notice:** [Specific features — liberty counts, eye shape, key intersection,
  connection status, temperature of moves. Point to marked stones or letters.]

**Task:** [For exercises — what the student must find or decide.]
(omit if not an exercise)

**Explanation:** [Why the key move works, what the principle means in this position.
  For tsumego: the solution line and why alternatives fail.]
(omit when presenting unsolved problems — put in a separate "Solution" block)
```

**Example output (concept illustration):**

````
```
. . . . .
. O O . .
O X . . .    ← X has 1 liberty — this is atari
. O . . .
. . . . .
```

**Setup:** 5×5 fragment. Black stone X is surrounded by white stones on three sides.

**Concept:** Atari — a stone or group reduced to exactly one liberty.

**What to notice:** The only empty point adjacent to X is directly to its right.
  White can fill that point on the next move to capture X. The `←` arrow marks
  the critical liberty.

**Task:** Where does White play to capture X?

**Explanation:** White plays at the point to the right of X. X then has zero liberties
  and is removed from the board. Any other White move gives Black a chance to escape
  by extending into the empty space.
````

## Generation Workflow

1. **Identify request type** (concept / tsumego / joseki / game position / comparison).
2. **Choose format** using the table above, or ask if ambiguous.
3. **Read the relevant reference file:**
   - Generating SL format → read `references/sl-syntax.md`
   - Generating ASCII → read `references/ascii-conventions.md`
4. **Draft the diagram.** Use the smallest board fragment that makes the point.
   - Verify stone placement is internally consistent (no stone claims liberty another stone blocks).
   - For move sequences: verify the sequence is legal.
5. **Draft the verbal description** using the format above.
6. **Review both together.** The words should refer to something visible in the diagram.
   If the diagram doesn't show what the words claim — fix the diagram, not just the words.

## Quality Guardrails

- **Go accuracy first.** If you are unsure whether a position is legal or a claim is correct,
  say so rather than presenting a wrong diagram confidently.
- **Minimal board.** Show only what's needed. A 5×5 fragment is almost always better
  than a half-empty 9×9.
- **Consistent terminology.** Use the same term throughout: liberty (not "freedom" or "breath"
  interchangeably within one diagram's description).
- **Verbal description must add value.** Don't just restate the diagram in words.
  Tell the reader what to look for and why it matters.
- **For tsumego:** never reveal the solution in the same block as the problem.
  Separate clearly.

## Age-group tone (when used inside go-lesson-plan)

| Age group | Verbal description style |
|:---|:---|
| 6–8 | Short sentences. One idea per sentence. Use metaphor ("the stone can't breathe"). |
| 9–12 | Direct. Use challenge framing ("Can you find the killing move?"). |
| 13+ | Analytical. Name the principle, explain the trade-off, invite debate. |
