# ACTIVE — next

> What is being done now, and what must be resolved before new work starts. Not ideas, not future abilities.

## Now

- **Current work:** bringing the recovered specifications to Reviewed after the baseline review: UC-001 to UC-009, all Draft
- **Progress:** baseline review held 2026-10-05: fresh-context review in `docs/reviews/all-review-1.md`, 25 decisions in `docs/recovery/change-log.md`, none open
- **Next step:** run the second fresh-context review of all nine specifications (`up-6-reviewing-specifications`, routed with `railhand route --stage adhoc`); the run of 2026-10-05 was stopped before it wrote a report. When it is clean, the nine move to Reviewed
- **Blocked by:** nothing
- **Waiting on owner:** nothing until the specs are Reviewed; then the Approved signature on each Status line, and whether to give AB-001 to AB-006 their `Specs` lines
- **Restart:** ask the upspec router for the state (`up-0-navigating-spec-driven-work`), then read `docs/reviews/all-review-1.md` and `docs/recovery/change-log.md`
- **Plan:** none
- **Updated:** 2026-10-05

## Pending

- Nothing pending.

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
