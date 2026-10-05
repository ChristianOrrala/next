# Baseline Review Plan

The recovered drafts become the baseline here. One person holds both kinds of
knowledge (the owner wrote the code and uses the tool), so each sitting is
done in two passes, as the method asks of a solo review:

1. **System pass**, with the code open: is each path reachable, is each rule
   enforced on every way in, is each number a decision or a leftover, what
   happens when it fails halfway.
2. **Business pass**, with the code closed, reading the specification as its
   user: is this what `next` is for, is anything accurate and indefensible,
   what happens in real use that it does not handle, are the words right.

Only `decide` suspects are on the agenda. The one `tidy` suspect (S-009) goes
to the code and its user guide. What a sitting cannot settle goes to
[change-log.md](change-log.md); nothing is fixed on the way. A use case the
review settles moves to `Reviewed`; `Approved` is the owner's to write.

## Sittings

### 1. UC-004 Manage Items, with UC-003 Complete Item

The two use cases that change items, and the two findings that matter most.

- Specifications: [UC-004](../use_cases/UC-004-manage-items.md), [UC-003](../use_cases/UC-003-complete-item.md)
- Ledger rows: `UC-004 …` and `UC-003 …` in [ledger.md](ledger.md)
- Suspects: S-010 (deleting stops the program), S-005 (an action on an item changed elsewhere lands on another item), S-017 (the selection jumps to an identical twin), S-004 (undo discards other panes' changes)
- Entities: ITEM

### 2. UC-001 Note Next Item

- Specification: [UC-001](../use_cases/UC-001-note-next-item.md)
- Suspects: S-003 (two saves at once can lose a change or stop with an error), S-019 (a slow paste runs as keys), S-020 (an unsupported language setting stops every request), S-012 (long folder locations), S-001 (reserved first words), S-002 (line breaks), S-011 (no length limit)
- Entities: LIST, ITEM

### 3. UC-002 Watch the List

The largest specification: layout, key help, selection and colors.

- Specification: [UC-002](../use_cases/UC-002-watch-the-list.md)
- Suspects: S-018 (worktrees get their own list), S-016 (a one-row wide pane shows no done items), S-015 (arrival marks cleared early), S-014 (an unreadable file stops the program)
- Business pass question: the shortest key line leaves out move, other kind and clear selection; AH-001 in `AHEAD.md` already proposes a change, which goes through triage after this sitting.
- Entities: LIST, ITEM

### 4. UC-005 Copy Item and UC-006 Locate the List

- Specifications: [UC-005](../use_cases/UC-005-copy-item.md), [UC-006](../use_cases/UC-006-locate-the-list.md)
- Suspects: S-022 (copying under a non-UTF-8 setting crashes), S-021 (a relative or empty place for lists), S-006 (copy always reports success), S-007 (two folders sharing a list), S-008 (hand-written lines dropped), S-013 (a byte-order mark hides the first item)
- Entities: LIST, ITEM

## Before the first change

Before any recovered use case changes for the first time (the delete fix of
S-010 included), tests pin what it does today, suspect behavior included,
through `up-8-deriving-use-case-tests`; they must pass against the code as it
is. A test that pins the delete crash records it as current behavior, to be
changed by the decided fix.
