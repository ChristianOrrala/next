# ACTIVE — next

> What is being done now, and what must be resolved before new work starts. Not ideas, not future abilities.

## Now

- **Current work:** bringing the recovered specifications to Reviewed after the baseline review: UC-001 to UC-009, all Draft
- **Progress:** baseline review held 2026-10-05: fresh-context review in `docs/reviews/all-review-1.md`, 25 decisions in `docs/recovery/change-log.md`, none open
- **Next step:** a second fresh-context review of all nine specifications (`up-6-reviewing-specifications`); when it is clean, they move to Reviewed
- **Blocked by:** nothing
- **Waiting on owner:** nothing until the specs are Reviewed; then the Approved signature on each Status line, and whether to give AB-001 to AB-006 their `Specs` lines
- **Restart:** `python3 tools/specs/workflow_state.py`, then open `docs/recovery/baseline-review.md`
- **Plan:** none
- **Updated:** 2026-10-05

## Pending

- [ ] Prove the agent hooks in a new session and add the `**Hooks:**` line to `AGENTS.md` (the specification check has not yet been seen blocking)

## Debt

- Deleting an item stops the program (S-010): `d` is unusable until the fix decided in change-log entry 1, which waits for the specs to be Approved and for tests that pin today's behavior.

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
