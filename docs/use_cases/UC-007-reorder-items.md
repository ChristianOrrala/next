# Use Case: Reorder Items

## Overview

**Use Case ID:** UC-007  
**Use Case Name:** Reorder Items  
**Primary Actor:** User  
**Goal:** The user puts an item where it belongs in the order of the list, so the next item is the one to do next.  
**Trigger:** The user sees an item in the open list that is out of order.  
**Status:** Draft  
**Requirements:** none yet; there is no requirements catalog

## Preconditions

- The list is open in a pane (UC-002).

## Main Success Scenario

1. User selects an item, pending or done (UC-002 BR-009).
2. User asks to move it one place up or down.
3. System swaps the item with its neighbor in that direction (BR-001).
4. System saves the list at once and keeps the item selected.

## Alternative Flows

### A1: Move After a Change Elsewhere

**Trigger:** Another pane changed or removed the selected item since the list last showed it (step 3)  
**Flow:**

1. System moves the next pending item instead of the one the user chose, or the newest done item shown when none is pending, and saves the list (S-005).
2. Use case ends.

### A2: Move Past the End of Its Kind

**Trigger:** No item of the same kind is shown in that direction; done items behind the line of older ones cannot be reached (step 3)  
**Flow:**

1. System changes nothing.
2. Use case ends.

### A3: Nothing Selected

**Trigger:** No item is selected (step 2)  
**Flow:**

1. System changes nothing.
2. Use case ends.

### A4: Save Fails

**Trigger:** The list cannot be saved (step 4)  
**Flow:**

1. System stops with an error and closes the list; the list's file keeps its earlier content.
2. Use case ends.

## Postconditions

### Success Postconditions

- The item and its neighbor have swapped places; every other item keeps its place.

### Failure Postconditions

- The list is unchanged, except in A1, where another item moves (S-005).

## Business Rules

### BR-001: Items Move Among Their Own Kind

An item moves one place at a time and only among the items of its own kind that are shown: a pending item among pending items, a done item among the done items shown.
Examples: pending A, B, C; move B up: B, A, C. Move the last pending item down toward the done items: nothing changes. Move the last done item shown down while older ones are hidden: nothing changes.
