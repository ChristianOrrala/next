# Changelog

All notable changes to this project are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). There are no version
tags yet, so each push of user-visible changes is a dated section.

## [Unreleased]

Nothing yet.

## 2026-10-03

### Added

- `y` copies the selected item as plain text, through the local clipboard tool and OSC 52, so it works in a remote pane too (AB-004).
- The keys sit in an aligned grid while there is room and fold to one line when the list needs the rows (AB-005).

### Changed

- In a tall pane, done items sit below the pending ones, newest first (AB-005).
- Nothing is selected until the cursor moves; `Esc` clears the selection (AB-003).
- Colors come from the terminal's 16-color palette: a full-width selection bar with a box (AB-006).

## 2026-10-02

### Added

- A per-folder todo pane: a list per repository or folder, `next <text>` from any pane, live reload (AB-001, AB-002, AB-003).
- A layout that fits the pane: done items in a right column when the pane is wide (AB-005).
