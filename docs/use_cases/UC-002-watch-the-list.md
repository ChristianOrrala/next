# Use Case: Watch the List

## Overview

**Use Case ID:** UC-002  
**Use Case Name:** Watch the List  
**Primary Actor:** User  
**Goal:** The user keeps the folder's list in view beside their work, sees what comes next and what is done, and sees changes made from other panes as they happen.  
**Trigger:** The user opens the list in a pane.  
**Status:** Draft  
**Requirements:** none yet; there is no requirements catalog

## Preconditions

- The user is working in a folder on this machine, in a terminal pane.

## Main Success Scenario

1. User opens the list in a pane while working in a folder.
2. System finds the folder's list (BR-001).
3. System shows the list's title with how many items are to do and how many are done, in the terminal's own colors (BR-002, BR-010).
4. System shows the pending items in their order, the next one first, each one whole (BR-003).
5. System shows the done items below them, newest first, as many as the pane has room for (BR-004, BR-005).
6. System shows the keys and what each one does (BR-006).
7. System keeps the list open and shows every change made to it from elsewhere as it happens, marking the items that just arrived (BR-007).
8. User closes the list.

## Alternative Flows

### A1: Empty List

**Trigger:** The list has no items, or the folder has no list yet (step 4)  
**Flow:**

1. System tells the user there is nothing yet and how to add the first item.
2. Use case continues at step 6.

### A2: Wide Pane

**Trigger:** The pane is wide enough for two columns (step 4)  
**Flow:**

1. System shows the pending items in a left column and the done items in a right column, newest on top (BR-008).
2. Use case continues at step 6.

### A3: More Done Items Than Room

**Trigger:** The done items do not all fit (step 5)  
**Flow:**

1. In a tall pane, System places the newest done items that fit below the pending items and, after them, a line with how many older ones are not shown; when the pending items fill the pane, these lie below its visible part until the selection moves there (BR-005).
2. In a wide pane, System fills the right column with the newest done items, one row fewer when a line with the older ones is needed, with no minimum (S-016).
3. Use case continues at step 6.

### A4: The List Needs the Rows of the Key Help

**Trigger:** The list would not fit with the keys spelled out, the pane is too narrow for even one column of them, or the keys fit on a single row (step 6)  
**Flow:**

1. System folds the keys into one line of letters, shorter as the pane narrows, and shows none when not even the shortest line fits (BR-006).
2. Use case continues at step 7.

### A5: Pane Resized

**Trigger:** The user changes the size of the pane (step 7)  
**Flow:**

1. System lays the list out again for the new size (BR-008).
2. Use case continues at step 7.

### A6: Item Selected

**Trigger:** The user moves through the list (step 7)  
**Flow:**

1. System selects the next pending item on the first move, and walks the items on every further move, stopping at the first and the last (BR-009).
2. System marks the selected item with a solid bar across its column, and keeps it in view when the list is longer than the pane.
3. Use case continues at step 7.

### A7: Other Kind of Item

**Trigger:** The user asks for the other kind of item (step 7)  
**Flow:**

1. System selects the nearest item of the other kind: a done item from a pending one, a pending item from a done one; with nothing selected, the newest done item shown, or the next pending item when no done item is shown (BR-009).
2. Use case continues at step 7.

### A8: Selection Cleared

**Trigger:** The user clears the selection (step 7)  
**Flow:**

1. System selects nothing.
2. Use case continues at step 7.

### A9: List File Unreadable

**Trigger:** The list's file is not readable as text (step 2)  
**Flow:**

1. System stops with an error (S-014).
2. Use case ends.

### A10: Selected Item Gone

**Trigger:** The selected item is removed or leaves the view, by a change from elsewhere or by the layout (step 7)  
**Flow:**

1. System selects the next pending item instead, or the first item shown when none is pending (BR-009).
2. Use case continues at step 7.

### A11: Wide Pane With a Single List Row

**Trigger:** The pane is wide, leaves room for one row of items, and two or more items are done (step 5)  
**Flow:**

1. System shows no done item, only the line with how many are not shown; with no pending item it also says there is nothing yet (S-016). With exactly one done item, that item is shown on the row instead.
2. Use case continues at step 6.

### A12: Unsupported Language Setting

**Trigger:** The machine does not support the language setting the pane passes on (step 1)  
**Flow:**

1. System stops with an error (S-020).
2. Use case ends.

## Postconditions

### Success Postconditions

- The list is unchanged by watching it.

### Failure Postconditions

- The list is unchanged.

## Business Rules

### BR-001: One List Per Repository or Folder

Inside a repository, the list belongs to the top folder of the working tree the pane is in, so every pane working anywhere in that tree shares one list. A linked working tree of the same repository has its own list, a nested repository has its own list, and a pane inside the repository's own records folder, or one where the repository cannot be asked for its top folder, counts as outside a repository (S-018). Outside a repository, the list belongs to the folder itself.
Examples: working in the folder lib inside the repository app: the list of app. Working in a folder that is in no repository: that folder's own list.

### BR-002: The Title Shortens With the Pane

The title names the list after the last part of its folder and counts the items to do and done. As the pane narrows, it drops the done count, then the program's name, then cuts the name and the to-do count from the right with an ellipsis, so the count disappears before the name is shortened.
Examples: a wide pane shows the name, the to-do count and the done count. A pane too narrow for that shows the name and the to-do count only. Narrower still, the name alone, then the name cut short.

### BR-003: Pending Items Are Shown Whole

A pending item is shown in full, wrapped at spaces, with its later lines aligned under its text; runs of spaces inside it are shown as one space. A word longer than the line is broken across lines.
Examples: a pending item longer than the pane takes two lines, the second indented under the first's text.

### BR-004: Done Items Take One Line

A done item is shown on one line, newest first, and cut short with an ellipsis when it is longer than the line.
Examples: a done item longer than its column ends in an ellipsis; the copied text is still whole (UC-005 BR-001).

### BR-005: Room for Done Items in a Tall Pane

In a tall pane the done items get the rows left free below the pending ones, at least 3 and at most half of the list area. When more done items exist than that room, one row of the room says how many older ones are not shown, but at least 3 done items are kept. A line separates the pending items from the done ones when both are shown. When the pending items fill the pane, the done items and that line come after them, below the visible part, and show only when the selection moves down to them.
Examples: a list area of 20 rows, 2 pending items and 15 done: 9 done items and a line saying 6 older. The same area with pending items filling it and 5 done: 3 done items and a line saying 2 older, below the visible part. Exactly 3 done items and a full pane: all 3, with no line about older ones.

### BR-006: The Keys Are Spelled Out While There Is Room

The keys and what they do are shown in aligned columns, as many columns as the width allows, while the list fits above them. When the list needs those rows, the keys fold into a single line that shortens as the pane narrows: every key with its word, then every key alone, then the keys alone without move, other kind and clear selection; and nothing when even that does not fit.
Examples: a short list in a narrow pane: the keys in a grid. A long list in the same pane: one line of letters.

### BR-007: Changes From Elsewhere Appear on Their Own

The open list shows what other panes add or change without the user doing anything, and marks items that arrived for a few seconds, or until the next change from elsewhere arrives or the user undoes a change (S-015). Opening the list marks nothing. While the user is writing an item or an edit, changes from elsewhere wait until the writing ends.
Examples: the user adds an item from another pane: it appears in the open list, marked, within about a second. A second item arrives a moment later: only the second is marked.

### BR-008: Wide Pane Layout

A pane is wide when it is at least 70 columns wide and more than twice as wide as it is tall. To keep a dragged split from flickering, the layout changes only 3 columns past that line in either direction.
Examples: a tall layout at 72 by 20 stays tall; at 73 by 20 it becomes wide. A wide layout at 67 by 20 stays wide; at 66 by 20 it becomes tall. 100 by 60 is tall, being less than twice as wide as tall.

### BR-009: Nothing Is Selected Until the User Moves

When the list opens, after a change from elsewhere arrives with nothing selected, and after the user clears it, no item is selected. The first move selects the next pending item, or the first item shown when none is pending. When the selected item is gone, the next pending item is selected, or the first item shown when none is pending. When a change arrives from elsewhere, the selection lands on the first item with the same text and mark, which may be a twin of the one selected (S-017).
Examples: open the list and move down: the next pending item is selected. Clear the selection, another pane adds an item: still nothing selected.

### BR-010: The Terminal's Own Colors

The list uses the colors of the terminal's own theme and none of its own. In a terminal with fewer than 16 colors it uses dim and reversed text instead.
Examples: changing the terminal's theme changes the list's colors with it.
