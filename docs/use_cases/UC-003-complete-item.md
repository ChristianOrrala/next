---
id: UC-003
name: Complete Item
primary_actor: User
goal: The user marks an item done, so it leaves the things to do and joins the record of what was done, or brings a done item back to do it next.
trigger: The user has finished, or wants to take up again, an item in the open list.
status: Draft
requirements: []
---
# Complete Item

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

| done items | marked done | result |
|---|---|---|
| X then Y | A | newest first they read A, Y, X |
| A, Y, X | B | newest first they read B, A, Y, X |

### BR-002: The Selection Moves On

After an item is marked done, the selection moves to the pending item that came after it; when it was the last pending item, to the one before it; when it was the only one, it stays on the item now done, unless the pane is too short to show that item, when nothing is selected (S-016).

| pending items | selected | pane | marked done | result |
|---|---|---|---|---|
| A, B, C | B | any | B | C is selected |
| A, B, C | C | any | C | B is selected |
| A | A | shows the item now done | A | A stays selected |
| only one | that one | wide, with a single row for items and other done items | that one | nothing is selected |

### BR-003: A Reopened Item Comes Next

A done item reopened by marking it becomes the first pending item, the next one to do. An undo of the marking puts it back where it was instead (UC-004 BR-004).

| pending items | action | result |
|---|---|---|
| A, B | done X is reopened by marking it | the order is X, A, B and X is next |
| A, B, C | B is marked done, then the marking is undone | A, B, C again |
