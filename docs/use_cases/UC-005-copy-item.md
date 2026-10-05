# Use Case: Copy Item

## Overview

**Use Case ID:** UC-005  
**Use Case Name:** Copy Item  
**Primary Actor:** User  
**Secondary Actors:** Local Clipboard, Viewing Terminal  
**Goal:** The user takes an item's text to paste elsewhere, typically into the prompt of the agent they are working with, clean and in one piece.  
**Trigger:** The user wants to paste an item's text somewhere else.  
**Status:** Draft  
**Requirements:** none yet; there is no requirements catalog

## Preconditions

- The list is open in a pane (UC-002).

## Main Success Scenario

1. User selects an item (UC-002 BR-009).
2. User asks to copy it.
3. System gives the item's text to the Local Clipboard of the machine the list runs on (BR-001).
4. System asks the Viewing Terminal to put the same text on its own clipboard (BR-002).
5. System confirms for a moment that the item was copied.

## Alternative Flows

### A1: Nothing Selected

**Trigger:** No item is selected (step 2)  
**Flow:**

1. System tells the user to select an item to copy.
2. Use case ends.

### A2: No Local Clipboard

**Trigger:** The machine offers no clipboard the list can reach, or it refuses the text (step 3)  
**Flow:**

1. Use case continues at step 4.

### A3: Nothing Could Be Asked

**Trigger:** The request to the Viewing Terminal cannot be sent and the Local Clipboard was not reached (step 5)  
**Flow:**

1. System tells the user for a moment that it could not copy.
2. Use case ends.

### A4: The Viewing Terminal Ignores the Request

**Trigger:** The Viewing Terminal does not honor the request (step 5)  
**Flow:**

1. System confirms that the item was copied all the same, since it cannot tell (S-006).
2. Use case ends.

### A5: Text the Language Setting Cannot Carry

**Trigger:** The pane's language setting cannot write a character of the item's text for the Local Clipboard (step 3)  
**Flow:**

1. System stops with an error (S-022).
2. Use case ends.

## Postconditions

### Success Postconditions

- The item's text is on the clipboard of this machine, of the terminal the user is looking at, or both. The list is unchanged.

### Failure Postconditions

- The list is unchanged, and no clipboard was changed.

## Business Rules

### BR-001: The Copied Text Is the Item Alone

The copied text is exactly the item's text: no mark of pending or done, and none of the line breaks the pane added to fit it. A done item is copied whole even when the pane shows it cut short.
Examples: a pending item shown over two lines is copied as one line. A done item shown with an ellipsis is copied in full.

### BR-002: Both Clipboards, Every Time

The list always asks the terminal the user is looking at to fill its own clipboard, even when this machine's clipboard was filled, so that copying works when the pane is viewed from another machine.
Examples: a pane on a remote machine viewed over a remote session: the text lands on the viewing machine's clipboard.
