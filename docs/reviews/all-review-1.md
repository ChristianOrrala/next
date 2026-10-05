## Spec Review: whole specification set (UC-001 to UC-006, entity model, diagram)

**Lint:** 0 errors, 0 warnings, 1 info — passes
**Reader review:** 21 warnings, 16 info — advisory

Review date 2026-10-05. Reviewed by a fresh context that read the files itself; the author's intentions were not passed in. Lint ran on the working tree, which holds an uncommitted edit of `docs/use_cases.puml` (the diagram name only). `docs/test_cases/` holds no journey test case, so none was reviewed. There is no requirements catalog (the lint info below); a "quality requirement that applies but is not linked" cannot be judged until one exists.

### Lint findings

```text
AGENTS.md:0: INFO CATALOG_PENDING [-]: the rules block reads use cases against docs/requirements.md, which is not written yet; write it, or record the skip on the **Skipped:** line
0 errors, 0 warnings, 1 infos
```

Exit code 0.

### Reader findings

All six use cases describe recovered behavior; where a finding touches behavior already named as suspect (S-nnn), the finding is about how the specification words it, not about whether the behavior is right.

| Severity | File:Line | Element | Reader or check | Finding |
|---|---|---|---|---|
| warning | docs/use_cases/UC-001-note-next-item.md:90 | UC-001 A8 | Engineer | The flow ends with a change that "can be lost" or a pane that "can stop with an error": two outcomes, neither deterministic, and neither postcondition (lines 113, 117) allows a list that lost another pane's change, so no test can decide the end (S-003). |
| warning | docs/use_cases/UC-001-note-next-item.md:59 | UC-001 A4 | Engineer | A4 branches from A1 step 1 but "continues at step 3" of the main scenario, which skips A1 step 4 and BR-004, so the selection after a multi-line paste into the open list is not decided. |
| warning | docs/use_cases/UC-001-note-next-item.md:66 | UC-001 A5 | Implementer | The reserved words are never named, nor what the "usage summary" says; the user can observe both, and UC-006 step 1 (line 19) has the same gap for how the location is asked. |
| warning | docs/use_cases/UC-001-note-next-item.md:74 | UC-001 A6 | Implementer | Where the extra items go, and whether they are pending or done, is not stated, and the success postcondition (line 113) speaks of one new item only (S-002). |
| warning | docs/use_cases/UC-002-watch-the-list.md:147 | UC-002 BR-002 | Contradiction (rule against step 3 and its own examples) | The rule drops "the program's name" while narrowing, but step 3 (line 21) and the examples show a title of list name and counts only, so whether the title carries the program's name, and where, is undecided. |
| warning | docs/use_cases/UC-002-watch-the-list.md:172 | UC-002 BR-007 | Engineer | "A few seconds" and "within about a second" are not testable values; state the numbers (or an NFR row once a catalog exists). |
| warning | docs/use_cases/UC-002-watch-the-list.md:98 | UC-002 A9 | Engineer | A9 is anchored to step 2 only, but step 7 also reads the file on every refresh and S-014 records the same stop on refresh; that path has no flow. |
| warning | docs/use_cases/UC-002-watch-the-list.md:85 | UC-002 A7 | Implementer | "Nearest item of the other kind" has no measure (distance in what, which way on a tie), and the cited BR-009 defines neither it nor the case of nothing selected. |
| warning | docs/use_cases/UC-002-watch-the-list.md:162 | UC-002 BR-005 | Engineer | "List area" is not defined, and the rule does not say whether the separating line and the older-ones line count inside the room; the examples fix only the case where free rows exceed half the area, so the boundary tests cannot be written. |
| warning | docs/use_cases/UC-002-watch-the-list.md:24 | UC-002 step 6 / BR-006 | Implementer | Which keys exist, which word goes with each and in what order is stated nowhere (BR-006 only says how they fold); the README is not linked as the owner of that list. |
| warning | docs/use_cases/UC-003-complete-item.md:46 | UC-003 A3 / A1 | Engineer | A3 covers only the main path (a pending item chosen); reopening a done item that another pane changed (A1) has no flow, and it is unclear what the "instead" falls on then (S-005). |
| warning | docs/use_cases/UC-003-complete-item.md:22 | UC-003 step 4 | Engineer | The save can fail and no flow is anchored to it; UC-001 A9 names a save that cannot complete (S-012), which the open list can also meet. |
| warning | docs/use_cases/UC-004-manage-items.md:8 | UC-004 goal | Stakeholder | One use case holds four goals (reword, reorder, remove, take back); the main scenario shows only the edit, and the success postconditions are three unrelated bullets; the owner decides whether to split it on the map. |
| warning | docs/use_cases/UC-004-manage-items.md:142 | UC-004 BR-003 / A8 | Engineer | BR-003 says a deleted item is gone, but A8 never deletes (S-010), so no path reaches the rule, no success postcondition covers a delete, and the undo of a delete in BR-003 cannot happen. |
| warning | docs/use_cases/UC-004-manage-items.md:132 | UC-004 BR-001 / A2 | Contradiction (same rule, other words) | Trimming here is "surrounding spaces"; UC-001 BR-002 (line 128) trims blank characters (tabs, line breaks, no-break and wide spaces); an item that holds such a character at an end is trimmed differently by add and by edit. |
| warning | docs/use_cases/UC-004-manage-items.md:97 | UC-004 A9 | Implementer | What is selected after an undo (kept, cleared, the restored item) is not stated, while edit and move say "keeps the item selected". |
| warning | docs/use_cases/UC-004-manage-items.md:23 | UC-004 step 5 | Engineer | The save (also A5 step 2 and A9 step 1) can fail and no flow is anchored to it. |
| warning | docs/use_cases/UC-005-copy-item.md:56 | UC-005 A4 (with A2) | Engineer | With no local clipboard (A2) and a terminal that ignores the request (A4) the flow confirms a copy that put the text nowhere, which the success postcondition (line 71, "or both") and the failure postcondition (line 75) both rule out (S-006). |
| warning | docs/use_cases/UC-006-locate-the-list.md:72 | UC-006 BR-001 / A2 | Implementer | The default place for lists, how the user chooses another place, and the pattern of the file's name are not stated, although the answer to the user is exactly that location. |
| warning | docs/use_cases/UC-006-locate-the-list.md:77 | UC-006 BR-002 | Implementer / data | The file's mark for pending and for done is never given (only "done in capitals counts as done"), yet A3 and UC-001 A6 depend on "the form of an item"; the user edits this file by hand. |
| warning | docs/use_cases/UC-006-locate-the-list.md:46 | UC-006 A3 | Stakeholder | The trigger is an edit that happens after the use case has ended, and the flow describes what UC-002 and the changing use cases do the next time; this is not part of locating the list. |
| info | docs/use_cases/UC-001-note-next-item.md:82 | UC-001 A7 | Engineer | A7 ends instead of continuing at step 4, so saving the first item and showing it in a pane that shows "nothing yet" is implied, not said. |
| info | docs/use_cases/UC-001-note-next-item.md:33 | UC-001 A1 step 3 | Implementer | Whether the pane that adds the item marks it as just arrived is not stated (step 4 says it only for the other open views). |
| info | docs/use_cases/UC-001-note-next-item.md:39 | UC-001 A2 | Engineer | Anchored to step 1 only; an empty text confirmed in the open list (A1 step 2) is not named. |
| info | docs/use_cases/UC-002-watch-the-list.md:35 | UC-002 A1 | Implementer | Whether the "nothing yet" message also shows when only done items exist in a tall pane is not stated (A11 says it only for the one-row wide pane), and the message's content is not given. |
| info | docs/use_cases/UC-002-watch-the-list.md:177 | UC-002 BR-008 / A2 | Engineer | The layout at the moment the list opens has no earlier layout to hold, the ratio branch of the 3-column margin is not worked in an example, and A2's "wide enough for two columns" (line 40) restates BR-008 in other words. |
| info | docs/use_cases/UC-002-watch-the-list.md:22 | UC-002 steps 4, 5, 7 | Implementer | What an item line shows besides its text (a pending or done mark, which UC-005 BR-001 implies) and how an arrived item is marked are not described; no mockup is linked. |
| info | docs/use_cases/UC-002-watch-the-list.md:25 | UC-002 step 7 | Actors | "Other panes" change the list in UC-001 A8, UC-002 step 7, UC-003 A3 and UC-004 A4 but are not named as an actor (the same user, or an agent working beside them, per AGENTS.md); say which. |
| info | docs/use_cases/UC-001-note-next-item.md:103 | UC-001 A10 | Stakeholder | "The language setting the pane passes on" needs technical knowledge; the same wording is in UC-002 A12 (line 122), UC-006 A4 (line 52) and UC-005 A5 (line 61). |
| info | docs/use_cases/UC-003-complete-item.md:54 | UC-003 A4 | Contradiction | A4 says the selection stays on the item just done; BR-002 (line 80) makes an exception (a pane too short to show it), which A4 omits. |
| info | docs/use_cases/UC-003-complete-item.md:29 | UC-003 A1 | Engineer | Anchored to step 2, but step 1 says the user selects a pending item, so the done item is selected in a step the main scenario forbids. |
| info | docs/use_cases/UC-005-copy-item.md:45 | UC-005 A3 / A4 | Engineer | A3's cause lies in step 4 but it is anchored to step 5, and A4's trigger is one the system "cannot tell" (line 56), so no test can produce it. |
| info | docs/use_cases/UC-005-copy-item.md:24 | UC-005 step 5 | Engineer | "For a moment" (also A3 line 48) is not a testable duration. |
| info | docs/use_cases/UC-006-locate-the-list.md:72 | UC-006 BR-001 | Engineer | "Too long" has its number only in the entity model (LIST.scope, 249); cite it here and in UC-001 A9. |
| info | docs/entity_model.md:30 | ITEM.position / UC-006 BR-002 | Entity model | The entity gives pending items in the order they are to be done, but the file (UC-006 BR-002, line 77) lists them the other way round; say which order `position` follows. |
| info | docs/entity_model.md:31 | ITEM.text | Entity model | The length column says 4096 while the description says no limit is set (S-011); mark the number as a placeholder or remove it. |
| info | docs/vision.md:1 | Vision | Stakeholder | The file is still the unfilled template (no mission, users, terms, scope), so the use cases have no stated purpose to be read against. |

### Verdict

Ready for Reviewed: yes. Ready for Approved: no.

The lint exits 0, so the set can move to Reviewed. Approval waits on the 21 open Part B warnings.

What fixes what:
- `up-5-writing-use-case-specs`: every warning above that is about a step, flow, rule or wording, in UC-001 to UC-006. The UC-006 mark and file-name findings may also need `up-3-modeling-domain-entities` (ITEM.status).
- `up-4-mapping-use-cases`: the UC-004 four-goal finding (split or keep) and the placement of UC-006 A3.
- Owner decisions first, since the specification cannot settle them: UC-004 BR-003 against A8 (S-010), UC-005 A4 (S-006), UC-001 A8 (S-003), UC-002 A7 "nearest". These belong to the baseline review in `docs/recovery/baseline-review.md`.

The reader review is a judgment; a second run may word or rank findings differently.
