# Use Case: Locate the List

## Overview

**Use Case ID:** UC-006  
**Use Case Name:** Locate the List  
**Primary Actor:** User  
**Goal:** The user finds where the folder's list is kept, to read it, edit it by hand or keep a copy.  
**Trigger:** The user asks where the folder's list is kept.  
**Status:** Draft  
**Requirements:** none yet; there is no requirements catalog

## Preconditions

- The user is working in a folder on this machine.

## Main Success Scenario

1. User asks where the folder's list is kept.
2. System finds the folder's list (UC-002 BR-001).
3. System answers with the location of the file that holds it (BR-001).

## Alternative Flows

### A1: No List Yet

**Trigger:** The folder has no list yet (step 3)  
**Flow:**

1. System answers with the location the list will have once it holds an item, and creates nothing.
2. Use case ends.

### A2: Lists Kept Elsewhere

**Trigger:** The user has chosen another place for the lists (step 3)  
**Flow:**

1. System answers with the location inside that place, read as given: an empty or relative place is not made absolute, so the list can land inside the folder and adding can fail (BR-001, S-021).
2. Use case ends.

### A3: The File Edited by Hand

**Trigger:** The user edits the file at that location by hand (step 3)  
**Flow:**

1. System reads the items from the edited file the next time the list is shown or changed, in the form of BR-002; a first line that starts with a byte-order mark is not read as an item (S-013), and a file that is not readable as text stops the list with an error (S-014).
2. System drops every line that is not an item the next time the list changes (S-008).
3. Use case ends.

### A4: Unsupported Language Setting

**Trigger:** The machine does not support the language setting the pane passes on (step 1)  
**Flow:**

1. System stops with an error and answers nothing (S-020).
2. Use case ends.

## Postconditions

### Success Postconditions

- The user knows where the list is kept. Nothing is created or changed.

### Failure Postconditions

- Nothing is created or changed.

## Business Rules

### BR-001: Lists Live Outside the Folder

Every list is kept in one place of the user's own, outside the folder it belongs to, so it never shows among the folder's files, unless the chosen place is given relative to the folder or lies inside it, or the folder is the user's home folder or another folder that contains the place (S-021). Each folder's list is a file named after the folder's full location; the user may choose that place. Two folders whose locations read the same once separators become dashes share one file (S-007), and a folder whose location is too long to name a file after cannot keep a list (S-012).
Examples: the list of a repository never appears among the repository's changes. The folders a/b-c and a-b/c share one list.

### BR-002: The List Is Plain Text, Newest First

The file holds one item per line, each marked as pending or done, pending items first from the one added last down to the next one, then done items newest first.
Examples: pending A then B added, X done: the file reads B, A, then X, each with its mark. A line marked done in capitals counts as done.
