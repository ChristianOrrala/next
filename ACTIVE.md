# ACTIVE — next

> What is being done now, and what must be resolved before new work starts. Not ideas, not future abilities.

## Now

- **Current work:** the specifications recovered from the code (UC-001 to UC-006, all Draft), waiting for their baseline review
- **Progress:** map, entity model, six full specifications, ledger and suspect list written; checks clean; the eighth verification sample came back clean
- **Next step:** baseline review, sitting 1 (UC-004 with UC-003), as `docs/recovery/baseline-review.md` lays out
- **Blocked by:** nothing
- **Waiting on owner:** the baseline review (21 suspects to decide, `docs/recovery/suspects.md`), and whether to give AB-001 to AB-006 their `Specs` lines now or after the review
- **Restart:** `python3 tools/specs/workflow_state.py`, then open `docs/recovery/baseline-review.md`
- **Plan:** none
- **Updated:** 2026-10-05

## Pending

- [ ] Prove the agent hooks in a new session and add the `**Hooks:**` line to `AGENTS.md` (the specification check has not yet been seen blocking)

## Debt

- Deleting an item stops the program (S-010): `d` is unusable until the decided fix; the fix waits for the review and for tests that pin today's behavior.

## Next new work

none: the current work is not finished

Below: How to maintain this file.

<!-- hot zone ends -->

## How to maintain this file

- **Now** is rewritten at the end of every session. Every field stays, with
  "none", "nothing" or "—" when empty. The hot zone stays under 60 lines.
- **Pending** holds unfinished or deferred items of the current work, and the
  owner's decisions it waits on. An item is deleted when it is done and
  committed; git keeps it.
- **Debt** holds debt that blocks new work or will bite it. Debt that can wait
  is an idea in `AHEAD.md`.
- **Next new work** is filled only when Now has no current work: the first
  item of AHEAD's Next up. This file never invents new work.
- Ideas, future abilities and milestones belong in `AHEAD.md`; abilities and
  their state in `ABILITIES.md`.
