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
- `ABILITIES.md` when a use case changes Status: the ability whose `Specs` line names it follows it;
- `ABILITIES.md` when a use case is mapped: it joins an ability's `Specs` line;
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

Below: Before committing, Naming, Working from specifications.

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
| Commit subjects | The use case worked on, colon, what changed; `next:` for work outside any use case | `UC-003: copy without the wrapping`, `next: adopt the A-files` |
| Branches | Kind, slash, subject; kinds `feat`, `fix`, `docs`, `chore` | `feat/key-hint` |
| Release tags | `v` and a semantic version (none yet) | `v0.1.0` |

## Working from specifications

**Profile:** solo

The specifications under `docs/` are the source of truth for what this system does. Code follows them.

1. **Read before deciding.** Before changing behavior, read the use case in `docs/use_cases/`, the rows it links in `docs/requirements.md`, and the entities it names in `docs/entity_model.md`.
2. **Name the use case.** Every instruction, commit subject and pull request names the use case it works on, for example `UC-012: allow team leads to assign inactive users`.
3. **Specification first.** A behavior change starts as a change to the specification. Code that changes behavior without one is not accepted. A change without a behavior change says so on its own line, naming the use case it stays within or `none`: `No behavior change: UC-012`.
4. **Not before approval.** Do not implement a use case whose Status is `Draft` or `Reviewed`. Agents never set `Approved` or `Done`; a person does.
5. **Stay inside the use case.** Change only what the named use case requires. Anything else you find goes on a list for the owner, not into the change.
6. **Synchronize, do not regenerate.** When a specification changes, change only the code and tests its changed elements touch.
7. **Do not decide silently.** Where the specification leaves something open, list what you decided with each change (the invention list). If it concerns behavior a user can observe, stop and ask.
8. **Observable behavior only.** Specifications describe what actors do and what the system answers. Technical choices live in this file or in `docs/decisions/`.
9. **Identifiers are permanent.** Never reuse or renumber an identifier. Code that enforces a business rule carries `UC-XXX BR-YYY: <rule>` above it; tests carry the use case id and name the flow or rule they cover.
10. **Status follows evidence.** Change a Status line only when the evidence for that step exists: a clean validator for `Reviewed`, merged code with markers for `Implemented`, passing tests for every flow and rule for `Tested`.

Where skills for specification-first work are installed, start with the one that matches the task, even when the task looks simple: implementing or synchronizing a use case goes through `up-7-implementing-use-cases` (its finish check runs before the code and before the report), tests through `up-8-deriving-use-case-tests` (its guard check proves each test), a bug report or a change request through `up-triaging-change-requests`, which classifies it against the specification before any code is read.

<!-- Stack rules (languages, frameworks, commands, naming) belong in their own section of this file, not in this one. -->
