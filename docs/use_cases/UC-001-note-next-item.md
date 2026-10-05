# Use Case: Note Next Item

## Overview

**Use Case ID:** UC-001  
**Use Case Name:** Note Next Item  
**Primary Actor:** User  
**Goal:** The user writes down the next thing to do without leaving what they are doing, and it waits in the folder's list behind what was already there.  
**Trigger:** The user thinks of something to do next while working in a folder.  
**Status:** Draft  
**Requirements:** none yet; there is no requirements catalog

## Preconditions

- The user is working in a folder on this machine.

## Main Success Scenario

1. User gives the text of the item from any pane working in the folder, without opening the list.
2. System finds the folder's list (UC-002 BR-001).
3. System adds the text as a pending item after every other pending item (BR-001, BR-002).
4. System saves the list at once, so every open view of the same list shows the item and marks it as just arrived (UC-002 BR-007).

## Alternative Flows

### A1: Added from the Open List

**Trigger:** The user adds the item from a view of the list that is already open (step 1)  
**Flow:**

1. User asks the open list for a new item and writes its text.
2. User confirms the text.
3. System adds the item as in step 3 and saves the list.
4. System moves the selection to the new item if an item was selected, and leaves nothing selected otherwise (BR-004).
5. Use case ends.

### A2: Empty Text

**Trigger:** The text holds nothing once the blank characters at its ends are removed (step 1)  
**Flow:**

1. System adds nothing and leaves the list unchanged.
2. Use case ends.

### A3: Writing Cancelled

**Trigger:** The user cancels while writing the text in the open list (A1 step 2)  
**Flow:**

1. System discards the text and leaves the list unchanged.
2. Use case ends.

### A4: Several Lines Pasted

**Trigger:** The user pastes text of several lines while writing in the open list (A1 step 1)  
**Flow:**

1. System keeps the first line and discards the rest that has arrived when the line is confirmed; a rest that arrives later acts as keys (BR-003, S-019).
2. Use case continues at step 3.

### A5: Text That Starts With a Reserved Word

**Trigger:** The first piece given is exactly a word the command reserves for asking for help or for the list's location; quoted together with more text as one piece, it is added (step 1)  
**Flow:**

1. System answers that request instead, as in UC-006 or with its usage summary, and adds nothing (S-001).
2. Use case ends.

### A6: Text With a Line Break

**Trigger:** The text given without opening the list holds a line break, or another character that ends a line (step 1)  
**Flow:**

1. System saves the text as it is: its first line becomes the item, a later line written in the form of an item becomes an item of its own, and the other lines are dropped the next time the list changes (S-002).
2. Use case ends.

### A7: No List Yet

**Trigger:** The folder has no list yet (step 2)  
**Flow:**

1. System starts the folder's list with this item as its only pending item.
2. Use case ends.

### A8: Another Change at the Same Moment

**Trigger:** Another pane changes the same list while this item is being saved (step 4)  
**Flow:**

1. System keeps whichever of the two lists was saved last; the other change can be lost, or the pane saving second can stop with an error (S-003).
2. Use case ends.

### A9: List Cannot Be Read or Saved

**Trigger:** The list cannot be read or saved, for example because the folder's location is too long (steps 2-4)  
**Flow:**

1. System stops with an error and saves nothing (S-012).
2. Use case ends.

### A10: Unsupported Language Setting

**Trigger:** The machine does not support the language setting the pane passes on (step 1)  
**Flow:**

1. System stops with an error and adds nothing (S-020).
2. Use case ends.

## Postconditions

### Success Postconditions

- The list holds the new item as its last pending item, and every item it held before is unchanged.

### Failure Postconditions

- The list is unchanged.

## Business Rules

### BR-001: A New Item Waits Behind the Others

A new item is pending and goes after every other pending item, so the next item stays the same unless the list had no pending item.
Examples: pending items A and B, add C: the order is A, B, C and A is still next. No pending items, add C: C is next.

### BR-002: The Text Is Kept as Written

The item's text is what the user wrote, with blank characters (spaces, tabs, line breaks, no-break and wide spaces) removed from its two ends only; in the open list only spaces can be typed there, since it takes visible keys and spaces only. When adding without opening the list, the separate pieces given are joined with one space between each, and spaces inside a piece are kept. Keys that write nothing visible are not taken into the text.
Examples: three separate words fix, the and test give "fix the test". The pieces fix, an empty piece and test give "fix  test" with two spaces. Text with only spaces adds nothing (A2).

### BR-003: One Line Per Item

An item is one line. When the user pastes several lines into the open list, only the first is kept; what of the paste arrives after the line is confirmed acts as keys (S-019).
Examples: pasting two lines "check the parser" and "then the docs" in one burst adds "check the parser" and nothing else.

### BR-004: The Selection After Adding

After adding from the open list, the selection lands on the new item when an item was selected before, and nothing is selected when nothing was.
Examples: item B selected, add C: C is selected. Nothing selected, add C: nothing is selected.
