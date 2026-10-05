# Use Case: Edit Item

## Overview

**Use Case ID:** UC-004  
**Use Case Name:** Edit Item  
**Primary Actor:** User  
**Goal:** The user rewords an item in the open list, so it says what is to be done.  
**Trigger:** The user sees an item in the open list that is worded wrong.  
**Status:** Draft  
**Requirements:** none yet; there is no requirements catalog

## Preconditions

- The list is open in a pane (UC-002).

## Main Success Scenario

1. User selects an item, pending or done (UC-002 BR-009).
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

**Trigger:** The confirmed text holds nothing once the blank characters at its ends are removed (step 4)  
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

### A5: Retired, moved to UC-007 main success scenario

### A6: Retired, moved to UC-007 A1

### A7: Retired, moved to UC-007 A2

### A8: Retired, moved to UC-008 A1

### A9: Retired, moved to UC-009 main success scenario

### A10: Retired, moved to UC-009 A1

### A11: Nothing Selected

**Trigger:** No item is selected (step 2)  
**Flow:**

1. System changes nothing.
2. Use case ends.

### A12: Save Fails

**Trigger:** The list cannot be saved (step 5)  
**Flow:**

1. System stops with an error and closes the list; the list's file keeps its earlier content.
2. Use case ends.

## Postconditions

### Success Postconditions

- The item holds the new text and keeps its place and its kind; every other item is unchanged.

### Failure Postconditions

- The list is unchanged, except in A4, where the new text goes to another item (S-005).

## Business Rules

### BR-001: An Edit Keeps the Text as Written

The new text replaces the old, kept as written in the sense of UC-001 BR-002. An edit that leaves nothing keeps the old text.
Examples: editing "fix test" to "fix the flaky test": the item reads "fix the flaky test". Editing it down to spaces: it still reads "fix test".

### BR-002: Retired, moved to UC-007 BR-001

Moved when Manage Items was split; it is now UC-007 BR-001 of Reorder Items.

### BR-003: Retired, moved to UC-008 BR-001

Moved when Manage Items was split; it is now UC-008 BR-001 of Delete Item.

### BR-004: Retired, moved to UC-009 BR-001

Moved when Manage Items was split; it is now UC-009 BR-001 of Undo Change.
