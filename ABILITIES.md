# ABILITIES — next

> Every ability of the product: planned, in progress, done or retired. One entry each, never deleted. Not the agent's abilities.

Status: `planned` (approved, not built), `in progress`, `done` (built, checked, evidence linked), `retired` (removed; the reason stays).

## Index

| ID | Ability | Status | Area |
|---|---|---|---|
| AB-001 | A list per folder | in progress | list |
| AB-002 | Add from any pane | in progress | list |
| AB-003 | Manage the items | in progress | list |
| AB-004 | Copy an item cleanly | in progress | clipboard |
| AB-005 | A layout that fits the pane | in progress | pane |
| AB-006 | The terminal's own colors | in progress | pane |

Below: Planned, Built, Retired, How to maintain this file.

<!-- hot zone ends -->

## Planned

None yet.

## Built

### AB-001 A list per folder

- **Status:** in progress
- **What it does:** inside a git repository the list belongs to the repository root, so every pane in it shares one list; outside a repository it belongs to the folder. Lists live in `~/.local/share/next/` (or `NEXT_DIR`) as plain Markdown, newest first, never inside the repository; `next --path` prints the file.
- **Specs:** UC-002, UC-006
- **Known limits:** the file name turns `/` into `-`, so two folders such as `/a/b-c` and `/a-b/c` share one list.
- **Next:** nothing planned
- **Evidence:** [README.md](README.md) ("Where the lists live"), `scope` and `list_file` in [next](next)

### AB-002 Add from any pane

- **Status:** in progress
- **What it does:** `next <text>` adds an item without opening the list; an open list reloads when its file changes and highlights the new arrival for a few seconds.
- **Specs:** UC-001
- **Known limits:** none known
- **Next:** nothing planned
- **Evidence:** [README.md](README.md) ("Stays open", "Shows what arrived"), `main` and `App` in [next](next)

### AB-003 Manage the items

- **Status:** in progress
- **What it does:** add, edit, mark done, reopen, move, delete and undo from the keyboard; pending items first with the next one on top, done items kept forever; nothing selected until the cursor moves, `Esc` clears it. A paste of several lines keeps only the first.
- **Specs:** UC-003, UC-004, UC-007, UC-008, UC-009
- **Known limits:** deleting an item stops the program with an error and deletes nothing, since 2026-10-02 (docs/recovery/suspects.md, S-010); an action on an item another pane just changed lands on the next pending item (S-005); undo walks back only through the changes made from the same open list, and is lost when it closes.
- **Next:** nothing planned
- **Evidence:** [README.md](README.md) (the key table), [tests/test_next.py](tests/test_next.py) (`Keys`, `Selection`)

### AB-004 Copy an item cleanly

- **Status:** in progress
- **What it does:** `y` copies the selected item as plain text, without `[ ]` and without the wrapping, through `pbcopy`, `wl-copy`, `xclip` or `xsel`, and always sends OSC 52 so a remote pane's own terminal fills its clipboard too.
- **Specs:** UC-005
- **Known limits:** OSC 52 works only where the terminal (and any multiplexer) allows it.
- **Next:** nothing planned
- **Evidence:** [tests/test_next.py](tests/test_next.py) (`Clipboard`)

### AB-005 A layout that fits the pane

- **Status:** in progress
- **What it does:** tall panes put done items below the pending ones (at least 3 rows, at most half the pane, `… +N older` for the rest); wide panes (70 or more columns and more than twice as wide as tall) give done items their own right column, with slack so a dragged split does not flicker. The keys sit in an aligned grid while there is room and fold to one line when the list needs the rows.
- **Specs:** UC-002
- **Known limits:** the folded one-line hint drops `J K` in the narrowest form (see AH-001).
- **Next:** AH-001
- **Evidence:** [tests/test_next.py](tests/test_next.py) (`Mode`, `Wide`, `Tall`, `Header`, `Footer`, `FooterInPane`, `Cells`)

### AB-006 The terminal's own colors

- **Status:** in progress
- **What it does:** uses the 16 ANSI slots only, never RGB values, so the terminal's or multiplexer's theme colors it: the selection is a full-width bar in color 0 with its box in yellow, done items in bright black, new arrivals in green. With fewer than 16 colors it falls back to dim and reverse video.
- **Specs:** UC-002
- **Known limits:** none known
- **Next:** nothing planned
- **Evidence:** [README.md](README.md) ("Wears your terminal's colors"), `paint` in [next](next)

## Retired

None.

## How to maintain this file

- An ability gets its entry when an item of `AHEAD.md` is approved, with
  status `planned`, under Planned. It moves to Built when work starts.
- The status changes in the same commit as the work, in the index row and in
  the entry together.
- Nothing is deleted. A removed ability becomes `retired`, moves under
  Retired, and keeps the reason. Identifiers are never reused.
- **Next** names the AHEAD item that continues the ability, or says
  "nothing planned". **Evidence** links the spec, tests or evaluation.
- When the index outgrows the hot zone, keep the planned and in-progress rows
  and one row per area in the hot zone, and move the full index below it.
- The check (`tools/check_tracking.py`) refuses a missing entry, a status
  outside the list, a mismatch between index and entry, and a removed
  identifier.
