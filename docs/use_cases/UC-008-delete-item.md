# Use Case: Delete Item

## Overview

**Use Case ID:** UC-008  
**Use Case Name:** Delete Item  
**Primary Actor:** User  
**Goal:** The user removes an item that no longer applies, so the list holds only what is still worth doing or remembering.  
**Trigger:** The user sees an item in the open list that is no longer wanted.  
**Status:** Draft  
**Requirements:** none yet; there is no requirements catalog

## Preconditions

- The list is open in a pane (UC-002).

## Main Success Scenario

1. User selects an item, pending or done (UC-002 BR-009).
2. User asks to delete it.
3. System removes the item from the list (BR-001, S-010).
4. System saves the list at once and selects the item that took its place (BR-002).

## Alternative Flows

### A1: The Program Stops

**Trigger:** Today every delete reaches this point, whatever item is selected (step 3)  
**Flow:**

1. System stops with an error and closes the list before saving anything, so the item stays in the list (S-010).
2. Use case ends.

### A2: Nothing Selected

**Trigger:** No item is selected (step 2)  
**Flow:**

1. System changes nothing.
2. Use case ends.

## Postconditions

### Success Postconditions

- The item is no longer in the list; every other item keeps its place. Today no delete reaches this end (S-010).

### Failure Postconditions

- The list is unchanged. In A1, the list has also closed (S-010).

## Business Rules

### BR-001: A Deleted Item Is Gone

Deleting removes the item from the list for good, done or pending; only an undo from the same open list brings it back (UC-009 BR-001, S-009).
Examples: as intended, since today delete stops the program (S-010), delete pending B from A, B, C: A, C remain. Close the list, open it again: B cannot be brought back.

### BR-002: The Selection After a Delete

After a delete, the selection moves to the item that took the deleted item's place, or to the one before it when the deleted item was the last shown, or to nothing when the list is empty. Today this is never reached (S-010).
Examples: as intended, pending A, B, C with B selected, B deleted: C is selected. C deleted instead: B is selected.
