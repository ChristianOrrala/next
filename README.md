# next

A tiny terminal list of what to do next, one per folder. Keep it open in a side pane
next to an AI agent (or anything that keeps you waiting) and jot down the next thing
while it works.

```
 next: my-project  (3 to do, 12 done)

 then: update the README
 check the error path when the file is
   missing
 added from another pane
 ---------------------------------------
 review the migration it wrote
 ask it to add tests for the parser
 wire the config loader
 … +9 older

 a e x y J K tab d u esc q
```

Pending items come first, the next one on top. Done items sit below the line, dimmed,
newest first. Rows carry only the item's text, so what you copy from the pane is the item; `y` copies
the selected item whole, without the wrapping, through `pbcopy`, `wl-copy`, `xclip` or `xsel`,
or the terminal's OSC 52 escape when none is there (that one works over SSH too).

In a wide pane (a split below the agent, say) the done items move to their own column on
the right, newest on top, and the pending ones get the left:

```
 next: my-project  (3 to do, 12 done)

 then: update the README                       │ review the migration it wrote
 check the error path when the file is         │ ask it to add tests for the parser
   missing                                     │ wire the config loader
 added from another pane                       │ … +9 older
 a add  e edit  x done  y copy  J/K move  tab col  d delete  u undo  esc unselect  q quit
```

- **Scoped to the folder.** Inside a git repo the list belongs to the repo root, so every
  pane in that repo shares it; outside a repo it belongs to the current folder.
- **Stays open.** It reloads when the file changes, so `next <text>` from any other pane
  shows up at once.
- **Fits the pane on its own.** Tall: pending on top, done items below them, newest first,
  filling the free rows (at least 3, at most half the pane), with `… +N older` for the rest. Wide (70 or more
  columns and more than twice as wide as tall): pending on the left, done on the right. The
  switch has a few columns of slack, so dragging a split doesn't flicker; the footer shortens
  in narrow panes.
- **Selects nothing until you move.** The cursor shows up on `j`/`k`, the arrows or `Tab`;
  `Esc` takes it away again, so the pane stays clean to read and copy from.
- **Shows what arrived.** An item added from another pane is highlighted for a few seconds.
- **Nothing is lost.** The file keeps every item forever, newest first.
- **No dependencies.** One Python 3 file using the standard library's `curses`
  (macOS and Linux).

## Install

```sh
git clone https://github.com/ChristianOrrala/next.git ~/src/next
ln -s ~/src/next/next ~/.local/bin/next     # any folder on your PATH works
```

`git pull` in the clone updates it. Or just copy the single file:

```sh
curl -fsSL https://raw.githubusercontent.com/ChristianOrrala/next/main/next -o ~/.local/bin/next
chmod +x ~/.local/bin/next
```

## Use

```sh
next              # open this folder's list; leave it running in a pane
next fix the flaky test     # add an item from any pane, without opening the list
next --path       # print the file that holds this folder's list
```

| Key | Does |
|---|---|
| `a` | add an item at the bottom (the furthest future) |
| `e` or `Enter` | edit the item under the cursor |
| `x` or `Space` | mark done; on a done item, reopen it on top of the pending ones |
| `y` | copy the item, whole and unwrapped, to the clipboard |
| `J` / `K` | move the item down / up |
| `Tab`, `h` / `l` or arrows | jump to the other column (to the done or pending items in a tall pane) |
| `j` / `k` or arrows | move the cursor (the first move selects the next pending item) |
| `Esc` | clear the selection |
| `d` | delete the item |
| `u` | undo the last change |
| `q` or `Ctrl-C` | quit |

While typing: `Enter` saves, `Esc` cancels, `Ctrl-U` clears the line. Pasting several
lines keeps only the first, so the rest never runs as keys.

### Open it in a side pane

```sh
tmux split-window -h -l 45 next        # tmux
zellij run -d right -- next            # zellij
wezterm cli split-pane --right --percent 30 -- next   # WezTerm
```

## Where the lists live

`~/.local/share/next/<folder-path-with-dashes>.md` (set `NEXT_DIR` to move them). They
never go inside your repo, so they don't show up in `git status`.

Each list is plain Markdown, newest first, and safe to read or edit by hand:

```markdown
- [ ] added from another pane
- [ ] check the error path when the file is missing
- [ ] then: update the README
- [x] review the migration it wrote
- [x] ask it to add tests for the parser
- [x] wire the config loader
- [x] an older done item, kept but not shown
```

## Tests

```sh
python3 -m unittest discover -s tests
```

## License

MIT
