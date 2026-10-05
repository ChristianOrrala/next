# Use Case: Manage Items

## Overview

**Use Case ID:** UC-004  
**Use Case Name:** Manage Items  
**Primary Actor:** User  
**Goal:** The user keeps the list right: rewords an item, puts it in the order it is to be done, removes one that no longer applies, or takes back a change.  
**Trigger:** The user sees an item in the open list that is worded wrong, out of order or no longer wanted, or regrets a change.  
**Status:** Draft  
**Requirements:** none yet; there is no requirements catalog

## Preconditions

- The list is open in a pane (UC-002).

## Main Success Scenario

1. User selects an item (UC-002 BR-009).
2. User asks to edit it.
3. System offers the item's current text for editing.
4. User changes the text and confirms it.
5. System replaces the item's text (BR-001), saves the list at once and keeps the item selected.

## Alternative Flows

### A1: Edit Cancelled

**Trigger:** The user cancels the edit (step 4)  
**Flow:**

1. System leaves the item unchanged.
2. Use case ends.

### A2: Edit Left Empty

**Trigger:** The confirmed text holds nothing once surrounding spaces are removed (step 4)  
**Flow:**

1. System leaves the item unchanged (BR-001).
2. Use case ends.

### A3: Several Lines Pasted

**Trigger:** The user pastes text of several lines while editing (step 4)  
**Flow:**

1. System keeps the first line and discards the rest that has arrived when the line is confirmed (UC-001 BR-003, S-019).
2. Use case continues at step 5.

### A4: Item Changed Elsewhere Meanwhile

**Trigger:** Another pane changed or removed the selected item since the list last showed it, or while the user was editing it (step 5)  
**Flow:**

1. System gives the new text to the next pending item instead of the one the user chose, or to the newest done item shown when none is pending, and saves the list (S-005).
2. Use case ends.

### A5: Move the Item

**Trigger:** The user asks to move the item one place up or down (step 2)  
**Flow:**

1. System swaps the item with its neighbor in that direction, when that neighbor is of the same kind (BR-002).
2. System saves the list at once and keeps the item selected.
3. Use case ends.

### A6: Move After a Change Elsewhere

**Trigger:** Another pane changed or removed the selected item since the list last showed it (A5 step 1)  
**Flow:**

1. System moves the next pending item instead of the one the user chose, or the newest done item shown when none is pending, and saves the list (S-005).
2. Use case ends.

### A7: Move Past the End of Its Kind

**Trigger:** No item of the same kind is shown in that direction; done items behind the line of older ones cannot be reached (A5 step 1)  
**Flow:**

1. System changes nothing.
2. Use case ends.

### A8: Delete the Item

**Trigger:** The user asks to delete the item (step 2)  
**Flow:**

1. System stops with an error and closes the list before saving anything, so the item stays in the list (BR-003, S-010).
2. Use case ends.

### A9: Undo

**Trigger:** The user asks to undo, with or without a selection (step 1)  
**Flow:**

1. System puts the whole list back as it was before the latest change made from this open list, and saves it (BR-004, S-004).
2. Use case ends.

### A10: Nothing to Undo

**Trigger:** No change was made from this open list, or every one was already undone (A9 step 1)  
**Flow:**

1. System changes nothing.
2. Use case ends.

### A11: Nothing Selected

**Trigger:** No item is selected (step 2)  
**Flow:**

1. System changes nothing for an edit, a move or a delete.
2. Use case ends.

## Postconditions

### Success Postconditions

- After an edit, the item holds the new text and keeps its place and its kind.
- After a move, the item and its neighbor have swapped places; every other item keeps its place.
- After an undo, the list is as it was before the change undone.

### Failure Postconditions

- The list is unchanged, except in A4 and A6, where the change falls on another item (S-005). After a delete, the list has also closed (S-010).

## Business Rules

### BR-001: An Edit Keeps the Text as Written

The new text replaces the old with surrounding spaces removed. An edit that leaves nothing keeps the old text.
Examples: editing "fix test" to "fix the flaky test": the item reads "fix the flaky test". Editing it down to spaces: it still reads "fix test".

### BR-002: Items Move Among Their Own Kind

An item moves one place at a time and only among the items of its own kind that are shown: a pending item among pending items, a done item among the done items shown.
Examples: pending A, B, C; move B up: B, A, C. Move the last pending item down toward the done items: nothing changes. Move the last done item shown down while older ones are hidden: nothing changes.

### BR-003: A Deleted Item Is Gone

Deleting removes the item from the list for good, done or pending; only an undo from the same open list brings it back (S-009). Today no delete completes (S-010).
Examples: as intended, since today delete stops the program (S-010), delete pending B from A, B, C: A, C remain. Close the list, open it again: B cannot be brought back.

### BR-004: Undo Walks Back Through This Pane's Changes

Each undo takes back one more change made from this open list, back to the moment it opened. Changes made from other panes are not undone one by one, and the undo history is lost when the list closes.
Examples: in one sitting, mark A done then edit B; undo once: B has its old text; undo again: A is pending again; undo a third time: nothing changes.

