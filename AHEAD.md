# AHEAD — next

> Everything not started yet: what comes next, milestones, ideas, research, spikes and proposals. Nothing here is in progress.

## Next up

None scheduled.

## Milestones

None yet.

## Index

| ID | Title | Kind | State | Ability | Write-up |
|---|---|---|---|---|---|
| AH-001 | Keep `J K` in the folded key hint | idea | open | — | — |

Kind: `idea`, `research`, `spike`, `proposal`. State: `open`, `approved`, `next`, `started`, `dropped`.

Below: Items, History, How to maintain this file.

<!-- hot zone ends -->

## Items

### AH-001 Keep `J K` in the folded key hint

- **What:** the narrowest one-line key hint (`a e x y d u q`) drops `J K`; keep them there so reordering stays discoverable when the list is long.
- **Why:** offered on 2026-10-03 and not built; it extends AB-005.
- **Write-up:** none
- **Decided:** —

## History

| ID | Title | Kind | State | Ability | Write-up |
|---|---|---|---|---|---|

## How to maintain this file

- A new idea, research question, spike or proposal gets the next free
  identifier, an index row with state `open`, and an entry under Items. A long
  write-up goes to `docs/research/` and the row links it.
- **Approved:** the state becomes `approved` and the item gets its entry in
  `ABILITIES.md` (status `planned`), named in the Ability column.
- **Scheduled:** the state becomes `next` and the item joins Next up, in order.
- **Started:** the state becomes `started`, the row moves to History, and the
  work appears in `ACTIVE.md`.
- **Dropped:** the state becomes `dropped`, the row moves to History, and the
  entry says why and when. Nothing is deleted; identifiers are never reused.
- Milestones list the items and abilities they include and how we know they
  are reached.
- The check (`tools/check_tracking.py`) refuses a kind or state outside the
  lists, an approved, next or started item without an ability, a link to
  nothing, and a removed identifier.
