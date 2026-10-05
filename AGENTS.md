# AGENTS.md

`next` is a tiny terminal list of what to do next, one per folder, meant to stay open in
a side pane next to an AI agent. It is a single Python 3 file, `next`, using only the
standard library (`curses`); its tests are in `tests/test_next.py`, and `README.md` is the
user guide. The repository is public on GitHub.

## Warm-up

At the start of every session, read in this order:

1. this file's hot zone (it ends at the line `<!-- hot zone ends -->`);
2. the hot zones of `ACTIVE.md`, `ABILITIES.md`, `AHEAD.md` and `ATLAS.md`;
3. `git log --oneline -15`.

Open anything else only when the task needs it; the index says where it is.

## Index

| File | Holds | Updated |
|---|---|---|
| `ACTIVE.md` | The work in progress and what blocks new work | At every session end |
| `ABILITIES.md` | Every ability of the product: planned, in progress, done, retired | When an ability changes state |
| `AHEAD.md` | Everything not started: next up, milestones, ideas, research, spikes | When an item is proposed, approved, scheduled or dropped |
| `ATLAS.md` | The architecture map: parts, files, dependencies, checks | When a part is added, moved or removed |
| `docs/decisions/` | Decisions and standing rules | When a decision is made |
| docs/plans/ | One plan per piece of work that spans sessions (created with the first one) | During that work |
| docs/research/ | Research and spike write-ups (created with the first one) | When one is finished |
| `CHANGELOG.md` | Release history | At each push of user-visible changes |
| `README.md` | The user guide: features, keys, install, where lists live | When a key or a visible behavior changes |

## Keep in step

In the same commit as the work, an agent updates:

- `ACTIVE.md` when it starts, finishes, defers or drops work;
- `ABILITIES.md` when an ability changes state;
- `AHEAD.md` when an item is proposed, approved, scheduled or dropped, or a
  spike ends (and `ABILITIES.md` when an item is approved);
- `ATLAS.md` when a part of the repository is added, moved, renamed or removed;
- `README.md` and the docstring at the top of `next` when a key or a visible
  behavior changes;
- `docs/decisions/` for a decision or a standing rule, never only an A-file.

Only the main session edits the A-files; parallel workers report to it.
Run `python3 tools/check_tracking.py` before every commit: it checks their
shape. Where the repository installed the hook in `.githooks/`, the hook runs
it (enable it once per clone: `git config core.hooksPath .githooks`).

## Commands

- Build: none (a single script; run it as `./next`)
- Test: `python3 -m unittest discover -s tests`
- Lint: `python3 tools/check_tracking.py` (the A-files' shape)

## Rules

- **Always:** keep `next` one file on the standard library; colors through the 16 ANSI slots only, never RGB; check a layout change in a narrow side pane as well as in the tests.
- **Ask first:** a dependency, a change to the list file's format or location, a push to GitHub.
- **Never:** write a list inside the repository; commit secrets or personal data (the repository is public); commit with an address other than the GitHub noreply one.

Below: Before committing, Naming.

<!-- hot zone ends -->

## Before committing

```bash
python3 -m unittest discover -s tests
python3 tools/check_tracking.py
```

## Naming

| What | Convention | Example |
|---|---|---|
| Files at the root that people and tools look for | Uppercase name, `.md` | `README.md`, `AGENTS.md`, `ACTIVE.md`, `ABILITIES.md`, `AHEAD.md`, `ATLAS.md`, `CHANGELOG.md` |
| Files under `docs/` | Lowercase, words joined by hyphens | `docs/research/01-terminal-palettes.md` |
| Decision records | Four digits, never reused, then the subject | `docs/decisions/0001-adopt-the-a-files.md` |
| Plans | The date the work started, then the subject | `docs/plans/2026-10-04-key-hint.md` |
| Research and spikes | Two digits, then the subject | `docs/research/01-terminal-palettes.md` |
| Abilities and AHEAD items | `AB-` or `AH-` and three digits, never reused | `AB-007`, `AH-002` |
| Dates | ISO 8601 | `2026-10-04` |
| Commit subjects | `next`, colon, what changed (the history's convention) | `next: layout that fits the pane` |
| Branches | Kind, slash, subject; kinds `feat`, `fix`, `docs`, `chore` | `feat/key-hint` |
| Release tags | `v` and a semantic version (none yet) | `v0.1.0` |
