# Recovery Ledger

Where every recovered element came from. Specifications carry no code
vocabulary; this file carries the link to the code instead.

Element is a use case (`UC-001`), a flow (`UC-001 A1`), a rule
(`UC-001 BR-002`) or an entity (`ENTITY CUSTOMER`). Evidence is one or more
`path:line` locations, separated by semicolons, relative to the repository
root. State is `recovered`, `verified` (a second reader checked the claim
against its evidence), `suspect` or `discarded`; the last two need a note, and
a suspect's note names its entry in the suspect list (`S-012`), which the
specification also names where it describes that behavior. A limit of
the implementation (a timeout, a retry count) is a note on the row of the rule
or flow it affects. Write no counts here: the ledger check prints them.

| Element | Evidence | State | Note |
|---|---|---|---|
| UC-001 | next:584; next:588; next:589; next:381 | recovered | `next <text>` from any pane; `a` in the open list |
| UC-001 Post-F-1 | next:586; next:383; next:264 | verified | empty text or cancel skips the save; the save replaces the file whole |
| UC-001 A1 | next:382; next:386 | verified | the `a` key; prompt `add: ` |
| UC-001 A2 | next:586; next:383 | verified | |
| UC-001 A3 | next:520; next:383 | verified | Esc cancels the prompt |
| UC-001 A4 | next:518 | suspect | S-019 |
| UC-001 A5 | next:578; next:581 | suspect | S-001; the first argument is compared whole, so quoted with more text it is added |
| UC-001 A6 | next:585; next:589; next:239 | suspect | S-002 |
| UC-001 A7 | next:255; next:260 | verified | a missing file reads as empty; its folder is created on save |
| UC-001 A8 | next:587; next:589; next:337; next:344; next:261; next:264 | suspect | S-003 |
| UC-001 A9 | next:76; next:253; next:255; next:261; next:262 | suspect | S-012 |
| UC-001 A10 | next:575 | suspect | S-020 |
| UC-001 BR-001 | next:588; next:108; next:386; next:340 | recovered | appended after the pending items, which come after the done ones in memory |
| UC-001 BR-002 | next:585; next:519; next:529 | recovered | arguments joined with spaces, then stripped of all whitespace |
| UC-001 BR-003 | next:517; next:518; next:519 | suspect | S-019 |
| UC-001 BR-004 | next:385; next:386 | verified | |
| UC-002 | next:593; next:539; next:540 | recovered | `next` with no arguments; the curses loop |
| UC-002 A1 | next:494; next:495; next:220 | verified |  |
| UC-002 A2 | next:217; next:223 | verified | reserves 2/5 of the width up to 60 columns (at least 26 in practice); the column is drawn one narrower |
| UC-002 A3 | next:215; next:220; next:222; next:229; next:233; next:479 | suspect | S-016 for the wide pane; tall rows past the list area show only when the selection scrolls there |
| UC-002 A4 | next:292; next:294; next:297; next:189 | recovered |  |
| UC-002 A5 | next:290; next:464 | verified | layout recomputed on every draw |
| UC-002 A6 | next:367; next:369; next:483; next:477 | recovered | j/k and arrows; the view scrolls to keep the selection |
| UC-002 A7 | next:554; next:375; next:379 | recovered | Tab, h, l, left and right arrows |
| UC-002 A8 | next:353 | verified | Esc; tests/test_next.py:230 |
| UC-002 A9 | next:254; next:255 | suspect | S-014 |
| UC-002 A10 | next:326; next:327; next:313; next:314 | recovered | falls back to the first item shown; S-017 for twins |
| UC-002 A11 | next:220; next:222; next:494 | suspect | S-016 |
| UC-002 A12 | next:575 | suspect | S-020 |
| UC-002 BR-001 | next:68; next:70; next:72 | suspect | S-018; git top level of the working tree, else the working folder |
| UC-002 BR-002 | next:160; next:161; next:164 | recovered |  |
| UC-002 BR-003 | next:207; next:208; next:134 | recovered | continuation lines indented four columns; runs of spaces shown as one |
| UC-002 BR-004 | next:212; next:221; next:230 | recovered |  |
| UC-002 BR-005 | next:228; next:229; next:232 | recovered | SHOW_DONE is 3; the separating line is at most 40 columns; rows can run past the visible area |
| UC-002 BR-006 | next:175; next:189; next:33; next:34 | recovered | |
| UC-002 BR-007 | next:537; next:540; next:331; next:37; next:320; next:325; next:319; next:487; next:448; next:506 | suspect | S-015; refreshes once a second outside the prompt; arrivals marked up to 3 seconds, cleared by the next arrival |
| UC-002 BR-008 | next:156; next:35; next:36 | recovered | WIDE_AT 70, SLACK 3 |
| UC-002 BR-009 | next:284; next:309; next:314; next:326; next:327 | suspect | S-017; tests/test_next.py:220; tests/test_next.py:268 |
| UC-002 BR-010 | next:53; next:56; next:42 | recovered | 16 ANSI slots: 0, 2, 3, 8 and the default |
| UC-003 | next:400; next:560 | recovered | x or Space |
| UC-003 A1 | next:413; next:414 | verified | |
| UC-003 A2 | next:401 | verified | tests/test_next.py:236 |
| UC-003 A3 | next:337; next:327; next:309; next:404 | suspect | S-005; next:404 guards only an empty view |
| UC-003 A4 | next:409; next:414 | verified | |
| UC-003 Post-F-1 | next:401; next:342; next:344; next:264 | verified | nothing selected returns before any change; the save happens only if the rendered list differs and replaces the file whole; A3 (S-005) is the exception |
| UC-003 BR-001 | next:413 | verified | inserted just after the last done item |
| UC-003 BR-002 | next:409; next:414; next:200; next:220; next:347 | suspect | S-016 |
| UC-003 BR-003 | next:413 | verified | inserted just before the first pending item |
| UC-004 | next:388; next:417; next:431; next:442 | recovered | e or Enter, J and K, d or Delete, u |
| UC-004 A1 | next:520; next:392 | verified |  |
| UC-004 A2 | next:519; next:392 | recovered | |
| UC-004 A3 | next:518 | suspect | S-019 |
| UC-004 A4 | next:327; next:309; next:396 | suspect | S-005 |
| UC-004 A5 | next:424; next:427 | verified | |
| UC-004 A6 | next:327; next:309; next:423 | suspect | S-005 |
| UC-004 A7 | next:424 | verified | only the shown items count |
| UC-004 A8 | next:437; next:438 | suspect | S-010; the selection rule at next:439 is never reached |
| UC-004 A9 | next:444; next:445 | suspect | S-004 |
| UC-004 A10 | next:443 | verified | |
| UC-004 A11 | next:389; next:418; next:432 | verified | tests/test_next.py:236 |
| UC-004 Post-F-1 | next:437; next:438; next:344 | suspect | S-010; the abort at next:438 comes before the save, so the file is untouched; S-005 for A4 and A6 |
| UC-004 BR-001 | next:519; next:392 | verified | |
| UC-004 BR-002 | next:424; next:427 | verified | only the shown items count |
| UC-004 BR-003 | next:437; next:438; README.md:70; next:12 | suspect | S-009, S-010 |
| UC-004 BR-004 | next:343; next:444; next:281 | recovered | history kept in memory only |
| UC-005 | next:358; next:562 | recovered | y |
| UC-005 A1 | next:359; next:360 | verified |  |
| UC-005 A2 | next:89; next:94 | verified | pbcopy, then wl-copy under Wayland, then xclip or xsel under X; 2 second limit per tool |
| UC-005 A3 | next:100; next:362 | verified | |
| UC-005 A4 | next:99 | suspect | S-006 |
| UC-005 Post-F-1 | next:359; next:362; next:100 | verified | copied is false only when no tool returned success and the OSC 52 write raised; a tool that fills the clipboard and then fails or passes 2 seconds would break it |
| UC-005 A5 | next:91; next:94 | suspect | S-022 |
| UC-005 BR-001 | next:362; tests/test_next.py:245 | verified | |
| UC-005 BR-002 | next:97 | recovered | OSC 52 escape |
| UC-006 | next:581; next:582 | recovered | `next --path` |
| UC-006 A1 | next:582 | verified | prints without creating |
| UC-006 A2 | next:29; next:76; next:260 | suspect | S-021; NEXT_DIR, default ~/.local/share/next, never made absolute |
| UC-006 A3 | next:239; next:244; next:253; next:254 | suspect | S-008, S-013, S-014 |
| UC-006 A4 | next:575 | suspect | S-020 |
| UC-006 Post-S-1 | next:581; next:582; next:583 | verified | returns before any write |
| UC-006 Post-F-1 | next:581; next:582; next:583 | verified | returns before any write; nothing before it writes |
| UC-006 BR-001 | next:76; next:29 | suspect | S-007, S-012, S-021; the default place lies under the home folder |
| UC-006 BR-002 | next:238; next:244 | recovered | Markdown task lines - [ ], - [x] and - [X]; done items newest first unless moved (UC-004 BR-002) |
| ENTITY LIST | next:72; next:76 | recovered | |
| ENTITY LIST required | next:72; next:76; next:261; next:593 | verified | scope; name is the folder's base name; the list is found by its file name, so scopes can collide (S-007) |
| Length of a folder location | next:76; next:253; next:255; next:261; next:262 | suspect | S-012; set by the temporary name (name and .tmp): saving fails from 250 characters, reading from 254 |
| ENTITY ITEM | next:238 | recovered | |
| ENTITY ITEM required | next:238; next:240; next:577; next:277; next:261 | verified | status from the mark (a two-valued flag in the code), text from the rest of the line, position from the line order (not stored), list_scope from the file it is read from |
| ENTITY ITEM lifecycle | next:411 | verified | Pending and Done, flipped by marking |
| Length of item text | next:238; next:585 | suspect | S-011 |
| ESCDELAY set to 25 | next:591 | discarded | a terminal timing so Esc answers at once; no business meaning |
| Note shown for 1.5 seconds | next:38 | discarded | screen timing of the copy confirmation |
