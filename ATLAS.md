# ATLAS — next

> The architecture map: each part of the repository, what it does, which files it works through, what it depends on and what checks it. A map, not a full file index.

## Map

| Part | What it does | Works through | Depends on | Checked by |
|---|---|---|---|---|
| Command line | `next`, `next <text>`, `next --path`, `--help` | `next` (`main`, the module docstring) | List store | `tests/test_next.py` |
| List store | Finds the folder's scope and reads and writes its Markdown list | `next` (`scope`, `list_file`, `parse`, `render`, `read`, `write`, `stamp`) | Python standard library | `tests/test_next.py` |
| Layout | Wraps, clips and arranges items for a tall or wide pane; header and key grid | `next` (`arrange`, `wrap`, `cells`, `is_wide`, `header`, `key_grid`, `footer`) | — | `tests/test_next.py` (`Mode`, `Wide`, `Tall`, `FooterInPane`) |
| Screen | The curses loop: keys, selection, editing, reload, colors | `next` (`App`, `paint`, `STYLE`) | Layout, List store, Clipboard | `tests/test_next.py` (`Keys`, `Selection`, `Drawn`) |
| Clipboard | Copies an item through the local tool and OSC 52 | `next` (`clipboard`) | `pbcopy`, `wl-copy`, `xclip` or `xsel` when present | `tests/test_next.py` (`Clipboard`) |
| Docs | The user guide and the changelog | `README.md`, `CHANGELOG.md` | — | review |
| Tracking | The A-files and their shape check | `AGENTS.md`, `tools/check_tracking.py`, `.githooks/pre-commit` | — | `tools/check_tracking.py` |
| Specifications | What the system does, written before it is built (upspec 2.0.0, solo profile) | `docs/vision.md`, `docs/use_cases.md`, `docs/use_cases/`, `docs/entity_model.md`, `docs/change-records/`, `docs/test_cases/` | — | `tools/specs/spec_lint.py` and `tools/specs/validate_use_case.py` |
| Specification hooks | The checks run by the commit guard; the agent hooks come with the upspec and a-files plugins | `tools/specs/`, `.githooks/commit-msg` | Specifications | `python3 tools/specs/spec_lint.py` |

## Flow

`main` resolves the scope and the list file. With text it appends an item and
exits; otherwise `App` runs under `curses.wrapper`: each frame reads the file
when its stamp changed, `arrange` lays the items out for the pane size, and the
screen paints them. Every edit writes the whole list back, newest first.

Below: Parts in detail, How to maintain this file.

<!-- hot zone ends -->

## Parts in detail

### List store

The file keeps every item forever; the pane only hides older done items.
Other panes write the same file, so the screen reloads on a changed stamp
rather than holding the list in memory as the truth.

### Layout

The tall/wide switch has `SLACK` columns of hysteresis around `WIDE_AT`, so
dragging a split does not flicker between layouts. Widths are counted in
terminal cells (`cells`), not characters.

## How to maintain this file

- A row per part of the repository, at the level of a folder or a working
  unit, never file by file. "Works through" names the entry points and the
  files an agent opens first; every path in backticks must exist.
- Update it in the same commit that adds, moves, renames or removes a part.
- "Parts in detail" holds only what a row cannot say: data flow, invariants,
  pitfalls.
- The check (`tools/check_tracking.py`) refuses a path in the map that points
  at nothing.
