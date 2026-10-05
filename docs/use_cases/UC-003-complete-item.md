# Use Case: Complete Item

## Overview

**Use Case ID:** UC-003  
**Use Case Name:** Complete Item  
**Primary Actor:** User  
**Goal:** The user marks an item done, so it leaves the things to do and joins the record of what was done, or brings a done item back to do it next.  
**Trigger:** The user has finished, or wants to take up again, an item in the open list.  
**Status:** Draft  
**Requirements:** none yet; there is no requirements catalog

## Preconditions

- The list is open in a pane (UC-002).

## Main Success Scenario

1. User selects a pending item (UC-002 BR-009).
2. User marks it done.
3. System makes the item the newest done item (BR-001).
4. System saves the list at once.
5. System moves the selection to the pending item that came after it, or to the one before it when it was the last (BR-002).

## Alternative Flows

### A1: Reopen a Done Item

**Trigger:** The user selects a done item instead (step 1)  
**Flow:**

1. User marks it.
2. System makes the item pending again, as the next item to do (BR-003).
3. System saves the list at once and keeps the item selected.
4. Use case ends.

### A2: Nothing Selected

**Trigger:** No item is selected (step 2)  
**Flow:**

1. System changes nothing.
2. Use case ends.

### A3: Item Changed Elsewhere Meanwhile

**Trigger:** Another pane changed or removed the selected item since the list last showed it (step 3)  
**Flow:**

1. System marks the next pending item done instead of the one the user chose, or reopens the newest done item shown when none is pending, and saves the list (S-005).
2. Use case ends.

### A4: The Only Pending Item

**Trigger:** No other pending item is left (step 5)  
**Flow:**

1. System keeps the selection on the item just done, unless the pane is too short to show it (BR-002).
2. Use case ends.

### A5: Done Item Changed Elsewhere Meanwhile

**Trigger:** Another pane changed or removed the selected done item since the list last showed it (A1 step 1)  
**Flow:**

1. System marks the next pending item done instead of reopening the one the user chose, and saves the list (S-005).
2. Use case ends.

### A6: Save Fails

**Trigger:** The list cannot be saved (step 4)  
**Flow:**

1. System stops with an error and closes the list; the list's file keeps its earlier content.
2. Use case ends.

## Postconditions

### Success Postconditions

- The item is done and is the newest done item; the other items keep their order.
- On reopening, the item is pending and is the next item to do.

### Failure Postconditions

- The list is unchanged, except in A3 and A5, where the change falls on another item (S-005).

## Business Rules

### BR-001: Done Items Are Kept, Newest First

A done item stays in the list as the newest done item; done items are never removed by being done, only by deleting them (UC-004 BR-003).
Examples: done items X then Y, then A is marked done: newest first they read A, Y, X.

### BR-002: The Selection Moves On

After an item is marked done, the selection moves to the pending item that came after it; when it was the last pending item, to the one before it; when it was the only one, it stays on the item now done, unless the pane is too short to show that item, when nothing is selected (S-016).
Examples: a wide pane with a single row for items and other done items, the only pending item marked done: nothing is selected. Pending A, B, C with B selected, B done: C is selected. C selected instead, C done: B is selected. Only A pending, A done: A stays selected.

### BR-003: A Reopened Item Comes Next

A done item reopened by marking it becomes the first pending item, the next one to do. An undo of the marking puts it back where it was instead (UC-004 BR-004).
Examples: pending A, B; done X reopened: the order is X, A, B and X is next. Pending A, B, C; B marked done, then undone: A, B, C again.
