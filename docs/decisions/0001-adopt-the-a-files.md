# 0001. Track the work in the A-files

Status: Accepted. Date: 2026-10-04. Decided by: owner.

## Context

The repository had no tracking files and no agent instruction file: the
state of the work lived in commit messages and in the README. Agents working
on `next` started every session without the rules (one file, standard library
only, ANSI colors only, the noreply address on a public repository) and
without a list of what was planned. Spec-driven development with use cases is
being set up next, and its rules need a guideline file to live in.

## Decision

The five A-files at the root carry the rules and the state: `AGENTS.md`,
`ACTIVE.md`, `ABILITIES.md`, `AHEAD.md`, `ATLAS.md`. `CLAUDE.md` imports
`AGENTS.md`. `tools/check_tracking.py` checks their shape before every
commit through `.githooks/pre-commit` (`git config core.hooksPath .githooks`,
once per clone). A `CHANGELOG.md` records user-visible changes as dated
sections until there are version tags.

What moved, was kept or was left out:

- Moved or merged: nothing; there were no tracking files.
- Created: the five A-files, `CLAUDE.md`, `CHANGELOG.md`, this record, the
  check and the hook.
- Abilities AB-001 to AB-006 were taken from the README, all `done`, with the
  README and the tests as evidence.
- AH-001 records an open idea from 2026-10-03: keep `J K` in the folded key hint.
- Left out: `README.md` stays the user guide; `.claude/settings.local.json` is
  local and untracked.

## Consequences

Every session starts from the hot zones instead of the history. Each change
of an ability, an item or a part has to land in the same commit as the work,
and the hook refuses a commit that breaks the files' shape. The use-case
specifications, when written, join the abilities through `Specs` lines and
the rules section in `AGENTS.md`. Revisit if the files cost more upkeep than a
one-file tool earns.
