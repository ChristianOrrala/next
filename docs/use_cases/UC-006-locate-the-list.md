---
id: UC-006
name: Locate the List
primary_actor: User
goal: The user finds where the folder's list is kept, to read it, edit it by hand or keep a copy.
trigger: The user asks where the folder's list is kept.
status: Draft
requirements: []
---
# Locate the List

## Preconditions

- The user is working in a folder on this machine.

## Main Success Scenario

1. User asks where the folder's list is kept, with the word --path.
2. System finds the folder's list (UC-002 BR-001).
3. System answers with the location of the file that holds it, a plain text file the user can read and edit (BR-001, BR-002).

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

### A3: Retired, moved to UC-002 BR-011

Moved when the review found it describes what happens after this use case ends: reading a file edited by hand is now UC-002 BR-011, and the file's form stays BR-002.

### A4: Unsupported Language Setting

**Trigger:** The machine does not support the language and region setting the terminal passes on (step 1)  
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

Every list is kept in one place of the user's own, outside the folder it belongs to, so it never shows among the folder's files, unless the chosen place is given relative to the folder or lies inside it, or the folder is the user's home folder or another folder that contains the place (S-021). The place is the folder .local/share/next in the user's home folder, or the one the user names in the setting NEXT_DIR. Each folder's list is a file in that place named after the folder's full location, without its leading separator, each separator turned into a dash, with .md at the end; the top folder of the machine gives root.md. Two folders whose locations read the same once separators become dashes share one file (S-007), and a folder whose location is longer than 249 characters cannot keep a list (S-012).

| folder | result |
|---|---|
| /home/ana/app | its list is kept in home-ana-app.md |
| a repository | its list never appears among the repository's changes |
| a/b-c and a-b/c | they share one list (S-007) |

### BR-002: The List Is Plain Text, Newest First

The file holds one item per line, pending items first from the one added last down to the next one, then done items newest first. A pending item's line starts with a dash, a space and an open box, [ ] and a space; a done item's line with [x] or [X] in its place. The text follows on the same line.

| list | result |
|---|---|
| pending A then B added, X done | the file reads B, A, then X, each with its mark |
| a line marked [X] in capitals | counts as done |
