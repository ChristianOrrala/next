---
id: UC-002
name: Watch the List
primary_actor: User
goal: The user keeps the folder's list in view beside their work, sees what comes next and what is done, and sees changes made from other panes as they happen.
trigger: The user opens the list in a pane.
status: Draft
requirements: []
---
# Watch the List

## Preconditions

- The user is working in a folder on this machine, in a terminal pane.

## Main Success Scenario

1. User opens the list in a pane while working in a folder.
2. System finds the folder's list (BR-001).
3. System shows a title naming the program and the list, with how many items are to do and how many are done, in the terminal's own colors (BR-002, BR-010).
4. System shows the pending items in their order, the next one first, each one whole (BR-003).
5. System shows the done items below them, newest first, as many as the pane has room for (BR-004, BR-005).
6. System shows the keys and what each one does, below the list (BR-006).
7. System keeps the list open and shows every change made to its file from elsewhere, by another pane or by hand, as it happens, marking the items that just arrived (BR-007, BR-011).
8. User closes the list.

## Alternative Flows

### A1: Empty List

**Trigger:** Nothing is shown in the list area: the list has no items, or the folder has no list yet (step 4)  
**Flow:**

1. System tells the user there is nothing yet and that the add key adds the first item; a tall pane holding only done items shows them instead.
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

1. System selects an item of the other kind: from a pending item, the newest done item shown; from a done item, the pending item nearest it in the list, which is the last pending item; with nothing selected, the newest done item shown, or the next pending item when no done item is shown (BR-009).
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

**Trigger:** The machine does not support the language and region setting the terminal passes on (step 1)  
**Flow:**

1. System stops with an error (S-020).
2. Use case ends.

### A13: List File Becomes Unreadable

**Trigger:** The list's file is no longer readable as text when the open list refreshes it (step 7)  
**Flow:**

1. System stops with an error (S-014).
2. Use case ends.

## Postconditions

### Success Postconditions

- The list is unchanged by watching it.

### Failure Postconditions

- The list is unchanged.

## Business Rules

### BR-001: One List Per Repository or Folder

Inside a repository, the list belongs to the top folder of the working tree the pane is in, so every pane working anywhere in that tree shares one list. A linked working tree of the same repository has its own list, a nested repository has its own list, and a pane inside the repository's own records folder, or one where the repository cannot be asked for its top folder, counts as outside a repository (S-018). Outside a repository, the list belongs to the folder itself.

| working in | result |
|---|---|
| the folder lib inside the repository app | the list of app |
| a folder that is in no repository | that folder's own list |

### BR-002: The Title Shortens With the Pane

The title reads the program's name, the list's name (the last part of its folder) and how many items are to do and done. As the pane narrows, it shows the program's name, the list's name and the to-do count only; then the list's name and the to-do count; then cuts that from the right with an ellipsis, so the count disappears before the name is shortened.

| pane | result |
|---|---|
| wide | the program's name, the list's name, 3 to do and 12 done |
| narrower | the program's name, the list's name and 3 |
| narrower still | the list's name and 3 |
| narrower again | the list's name alone |
| narrowest | the name cut short |

### BR-003: Pending Items Are Shown Whole

A pending item is shown in full, wrapped at spaces, with its later lines aligned under its text; runs of spaces inside it are shown as one space. A word longer than the line is broken across lines.

| pending item | result |
|---|---|
| longer than the pane | takes two lines, the second indented under the first's text |
| shorter than the pane | takes one line |

### BR-004: Done Items Take One Line

A done item is shown on one line, newest first, and cut short with an ellipsis when it is longer than the line.

| done item | result |
|---|---|
| longer than its column | ends in an ellipsis; the copied text is still whole (UC-005 BR-001) |
| fits its column | shown whole on its one line |

### BR-005: Room for Done Items in a Tall Pane

The list area is the rows between the title and the keys. In a tall pane the done items get the free rows of the list area, those not taken by the pending items and the separating line, at least 3 and at most half of the list area. When more done items exist than that room, the line saying how many older ones are not shown takes one row of the room, but at least 3 done items are kept. A line separates the pending items from the done ones when both are shown. When the pending items fill the pane, the done items and that line come after them, below the visible part, and show only when the selection moves down to them.

| list area | pending items | done items | result |
|---|---|---|---|
| 20 rows | 2 | 15 | 9 done items and a line saying 6 older |
| 20 rows | fill the area | 5 | 3 done items and a line saying 2 older, below the visible part |
| any | fill the pane | exactly 3 | all 3, with no line about older ones |

### BR-006: The Keys Are Spelled Out While There Is Room

The keys are, with their words: a add, e edit, x done, y copy, J/K move, tab col (other kind), d delete, u undo, esc deselect, q quit. They are shown in aligned columns, as many columns as the width allows, while the list fits above them. When the list needs those rows, or the keys fit on one row anyway, they fold into a single line that shortens as the pane narrows: every key with its word; then the keys alone, a e x y J K tab d u esc q; then a e x y d u q; and nothing when even that does not fit.

| pane | list | result |
|---|---|---|
| narrow | short | the keys in a grid |
| the same narrow pane | long | one line of letters |
| under 14 columns | any | no keys |

### BR-007: Changes From Elsewhere Appear on Their Own

The open list shows what other panes add or change within 1 second, without the user doing anything, and marks items that arrived for 3 seconds, or until the next change from elsewhere arrives or the user undoes a change (S-015). Opening the list marks nothing, and neither does a change made from this pane. While the user is writing an item or an edit, changes from elsewhere wait until the writing ends.

| change from elsewhere | result |
|---|---|
| the user adds an item from another pane | it appears in the open list, marked, within 1 second, and the mark is gone 3 seconds later |
| a second item arrives a moment later | only the second is marked |

### BR-008: Wide Pane Layout

A pane is wide when it is at least 70 columns wide and more than twice as wide as it is tall. To keep a dragged split from flickering, the layout changes only 3 columns past that line in either direction, on both measures. When the list opens, it counts as tall.

| layout now | pane (columns by rows) | result |
|---|---|---|
| tall | 72 by 20 | stays tall |
| tall | 73 by 20 | becomes wide |
| wide | 67 by 20 | stays wide |
| wide | 66 by 20 | becomes tall |
| tall | 100 by 60 | tall, being less than twice as wide as tall |

### BR-009: Nothing Is Selected Until the User Moves

When the list opens, after a change from elsewhere arrives with nothing selected, and after the user clears it, no item is selected. The first move selects the next pending item, or the first item shown when none is pending. When the selected item is gone, the next pending item is selected, or the first item shown when none is pending. When a change arrives from elsewhere, the selection lands on the first item with the same text and mark, which may be a twin of the one selected (S-017).

| situation | result |
|---|---|
| the list is opened and the user moves down | the next pending item is selected |
| the selection is cleared and another pane adds an item | still nothing selected |

### BR-010: The Terminal's Own Colors

The list uses the colors of the terminal's own theme and none of its own. In a terminal with fewer than 16 colors it uses dim and reversed text instead.

| terminal | result |
|---|---|
| its theme is changed | the list's colors change with it |
| fewer than 16 colors | dim and reversed text instead |

### BR-011: The File Is Read as It Is

The open list reads its file again whenever the file changes, edited by another pane or by hand, in the form of UC-006 BR-002. A first line that starts with a byte-order mark is not read as an item (S-013), and lines that are not items are dropped the next time the list changes (S-008).

| change to the file | result |
|---|---|
| the user adds a line marked done by hand | the open list shows it as a done item within 1 second |
| a heading is written into the file | it disappears at the next change |
