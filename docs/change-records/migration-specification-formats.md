---
outcome: migration
element: specification formats
---
# Change record: Migration of the specification formats to upspec 1.8.1

## Context

The specifications were in the formats of upspec before 1.1.0: bold Overview fields in each use case, rule examples as prose, database types in the entity model, a PlantUML diagram as the overview. The router answered MIGRATE. The plan listed the entity model and the installed scripts as mechanical (commit `next: mechanical migration to the current formats`), and the use cases and the diagram as judgment work (the diagram converts mechanically once the use cases are in the current format; it has its own commit).

Sign-off test: not applicable. This is a conversion of format with no change to behavior or approval; every use case keeps its Status (Draft).

The orchestrator, by the owner's delegation, said yes to the plan and to the invention list below on 2026-11-14.

## Decision

The invention list: every meaning decided in the conversion.

| # | Decision | Decided by | Lives in |
|---|---|---|---|
| 1 | `requirements: none yet; there is no requirements catalog` becomes `requirements: []`, the value the product's own stubs carry; the nine use cases link no requirement because no catalog exists | the orchestrator, by the owner's delegation, 2026-11-14 | front matter of UC-001 to UC-009 |
| 2 | The columns of every Examples table are my names for the inputs each example already named; every stated example is kept and no stated outcome changed | the same | every `### BR-` Examples table |
| 3 | Contrast rows added where a table needs two rows and one side was not stated: UC-001 BR-003 (one pasted line adds that line), UC-002 BR-003 (a pending item shorter than the pane takes one line), UC-002 BR-004 (a done item that fits its column is shown whole), UC-003 BR-001 (done A, Y, X and B marked done read B, A, Y, X), UC-005 BR-002 (on this machine with its clipboard filled, the terminal is still asked to fill its own, from the rule's wording) | the same | UC-001 BR-003, UC-002 BR-003, UC-002 BR-004, UC-003 BR-001, UC-005 BR-002 |
| 4 | UC-002 BR-010: a second row, fewer than 16 colors gives dim and reversed text, taken from the rule text | the same | UC-002 BR-010 |
| 5 | UC-002 BR-002: the prose "narrower still: ..., then ..., then ..." is split into five rows (wide, narrower, narrower still, narrower again, narrowest) | the same | UC-002 BR-002 |
| 6 | UC-002 BR-005, third example: its list area was not stated, so the cell says "any" | the same | UC-002 BR-005 |
| 7 | UC-003 BR-002: `pane` and `selected` columns added; "any" marks the rows where the pane was not stated | the same | UC-003 BR-002 |
| 8 | UC-008 BR-001 and BR-002: the prefix "as intended, since today delete stops the program (S-010)" becomes a note line under the table | the same | UC-008 BR-001, UC-008 BR-002 |
| 9 | UC-006 BR-002: "capitals" is shown as "a line marked [X] in capitals" | the same | UC-006 BR-002 |
| 10 | Title lines `# Use Case: Name` become `# Name`, and the Overview section is removed, as the product's converter does | the product's converter | UC-001 to UC-009 |

## Specification change

Format only. No step, flow, rule meaning, identifier or Status changed.

## Consequences

No change in behavior. The three retired rules of UC-004 need no Examples table. The use case diagram becomes the generated overview `docs/use_cases.md` in the next commit, and `docs/use_cases.puml` is retired there (git keeps it).
