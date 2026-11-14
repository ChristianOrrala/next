---
id: UC-009
name: Undo Change
primary_actor: User
goal: The user takes back a change they made in the open list by mistake, so the list is as it was before it.
trigger: The user regrets a change made from the open list.
status: Draft
requirements: []
---
# Undo Change

## Preconditions

- The list is open in a pane (UC-002).

## Main Success Scenario

1. User asks to undo, with or without a selection.
2. System puts the whole list back as it was before the latest change made from this open list, and saves it (BR-001, S-004).
3. System keeps the selection on the same item when it is still in the list (BR-002).

## Alternative Flows

### A1: Nothing to Undo

**Trigger:** No change was made from this open list, or every one was already undone (step 2)  
**Flow:**

1. System changes nothing.
2. Use case ends.

### A2: Selected Item Not in the Restored List

**Trigger:** The selected item is not in the list as it was put back (step 3)  
**Flow:**

1. System selects the next pending item, or the first item shown when none is pending (BR-002).
2. Use case ends.

### A3: Save Fails

**Trigger:** The list cannot be saved (step 2)  
**Flow:**

1. System stops with an error and closes the list; the list's file keeps its content.
2. Use case ends.

## Postconditions

### Success Postconditions

- The list is as it was before the latest change made from this open list, and that change is no longer offered for undo. Marks on items that just arrived are cleared (S-015).

### Failure Postconditions

- The list is unchanged.

## Business Rules

### BR-001: Undo Walks Back Through This Pane's Changes

Each undo takes back one more change made from this open list, back to the moment it opened. Changes made from other panes are not undone one by one; the list put back is the whole list as it was, so what arrived from elsewhere since is lost (S-004). The undo history is lost when the list closes. A change that left the list as it was is not recorded.

| changes made in one sitting | undo | result |
|---|---|---|
| mark A done, then edit B | once | B has its old text |
| mark A done, then edit B | twice | A is pending again |
| mark A done, then edit B | a third time | nothing changes |

### BR-002: The Selection After an Undo

After an undo, the selection stays on the first item with the same text and mark when the restored list holds one (S-017); otherwise the next pending item is selected, or the first item shown when none is pending. Nothing selected stays nothing selected.

| selected | undo of | result |
|---|---|---|
| B | marking A done | B stays selected |
| nothing | any change | nothing is selected |
