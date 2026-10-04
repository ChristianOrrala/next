import importlib.machinery
import importlib.util
import os
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
loader = importlib.machinery.SourceFileLoader("nextmod", os.path.join(HERE, "..", "next"))
spec = importlib.util.spec_from_loader("nextmod", loader)
nx = importlib.util.module_from_spec(spec)
loader.exec_module(nx)


def items(done, todo):
    return [[True, f"done {n}"] for n in range(done)] + [[False, f"todo {n}"] for n in range(todo)]


def texts(rows):
    return [text for _, text, _ in rows]


class Cells(unittest.TestCase):
    def test_wide_characters_count_twice(self):
        self.assertEqual(nx.cells("ab"), 2)
        self.assertEqual(nx.cells("日本"), 4)

    def test_clip_marks_the_cut(self):
        self.assertEqual(nx.clip("hello", 10), "hello")
        self.assertEqual(nx.clip("hello world", 6), "hello…")
        self.assertEqual(nx.cells(nx.clip("日本語のテキスト", 7)), 7)

    def test_wrap_fits_cells_and_breaks_long_words(self):
        self.assertEqual(nx.wrap("one two three", 7), ["one two", "three"])
        self.assertEqual(nx.wrap("abcdefghij", 4), ["abcd", "efgh", "ij"])
        self.assertTrue(all(nx.cells(l) <= 5 for l in nx.wrap("日本語のテキスト です", 5)))
        self.assertEqual(nx.wrap("", 5), [""])


class Mode(unittest.TestCase):
    def test_wide_needs_width_and_aspect(self):
        self.assertTrue(nx.is_wide(120, 12, False))
        self.assertFalse(nx.is_wide(45, 50, False))    # narrow right split
        self.assertFalse(nx.is_wide(100, 60, False))   # big but tall
        self.assertFalse(nx.is_wide(60, 10, False))    # short but too narrow

    def test_hysteresis_keeps_the_mode_near_the_line(self):
        self.assertFalse(nx.is_wide(71, 10, False))
        self.assertTrue(nx.is_wide(71, 10, True))
        self.assertTrue(nx.is_wide(68, 10, True))
        self.assertFalse(nx.is_wide(66, 10, True))


class Clipboard(unittest.TestCase):
    def test_uses_the_first_tool_found_and_falls_back_to_osc52(self):
        runs, out = [], []
        real = nx.shutil.which, nx.subprocess.run, nx.sys.stdout
        class Out:
            def write(self, s): out.append(s)
            def flush(self): pass
        try:
            nx.shutil.which = lambda name: "/bin/" + name if name == "pbcopy" else None
            nx.subprocess.run = lambda cmd, **kw: runs.append((cmd, kw["input"]))
            self.assertTrue(nx.clipboard("hi"))
            self.assertEqual(runs, [(["pbcopy"], "hi")])
            nx.shutil.which = lambda name: None
            nx.sys.stdout = Out()
            self.assertTrue(nx.clipboard("hi"))
            self.assertEqual(out, ["\x1b]52;c;aGk=\a"])
        finally:
            nx.shutil.which, nx.subprocess.run, nx.sys.stdout = real


class Footer(unittest.TestCase):
    def test_shrinks_with_width(self):
        self.assertEqual(nx.footer(200), nx.KEYS)
        self.assertEqual(nx.footer(40), nx.SHORT_KEYS)
        self.assertEqual(nx.footer(15), "")


class Wide(unittest.TestCase):
    def test_pending_left_done_right_newest_first(self):
        view, panels = nx.arrange(items(4, 2), 120, 12, True)
        self.assertEqual([t for _, t in view], ["todo 0", "todo 1", "done 3", "done 2", "done 1", "done 0"])
        (lx, lw, left), (rx, rw, right) = panels
        self.assertEqual(lx, 1)
        self.assertTrue(24 <= rw <= 60)
        self.assertLess(lx + lw, rx)
        self.assertLessEqual(rx + rw, 119)
        self.assertEqual(texts(left), ["todo 0", "todo 1"])
        self.assertEqual(texts(right), ["done 3", "done 2", "done 1", "done 0"])

    def test_done_column_fills_the_height_and_counts_the_rest(self):
        view, panels = nx.arrange(items(30, 1), 120, 12, True)
        right = panels[1][2]
        self.assertEqual(len(right), 9)  # body is h - 3
        self.assertEqual(right[-1][1], "… +22 older")
        self.assertIsNone(right[-1][0])
        self.assertEqual(len(view), 1 + 8)

    def test_done_items_stay_on_one_line(self):
        _, panels = nx.arrange([[True, "a very long done item " * 5], [False, "x"]], 120, 12, True)
        right = panels[1][2]
        self.assertEqual(len(right), 1)
        self.assertLessEqual(nx.cells(right[0][1]), panels[1][1] - 1)


class Tall(unittest.TestCase):
    def test_pending_on_top_done_below_newest_first(self):
        view, panels = nx.arrange(items(40, 2), 45, 50, False)
        rows = panels[0][2]
        done_rows = [r for r in rows if r[2] == "done"]
        self.assertEqual(len(done_rows), 47 // 2)
        self.assertEqual(texts(rows)[:2], ["todo 0", "todo 1"])
        self.assertEqual(rows[2][2], "rule")
        self.assertEqual(done_rows[0][1], "done 39")
        self.assertEqual(rows[-1][1], f"… +{40 - 47 // 2} older")
        self.assertEqual([t for _, t in view[:3]], ["todo 0", "todo 1", "done 39"])

    def test_at_least_three_done_when_full(self):
        _, panels = nx.arrange(items(10, 60), 45, 20, False)
        self.assertEqual(sum(1 for r in panels[0][2] if r[2] == "done"), 3)

    def test_no_older_note_when_everything_fits(self):
        _, panels = nx.arrange(items(2, 2), 45, 50, False)
        self.assertEqual(texts(panels[0][2]), ["todo 0", "todo 1", "-" * 39, "done 1", "done 0"])

    def test_pending_wraps_with_a_hanging_indent(self):
        _, panels = nx.arrange([[False, "word " * 20]], 30, 20, False)
        lines = texts(panels[0][2])
        self.assertGreater(len(lines), 1)
        self.assertTrue(lines[0].startswith("word"))
        self.assertTrue(lines[1].startswith("  word"))


class Screen:
    def __init__(self, h, w):
        self.size = (h, w)

    def getmaxyx(self):
        return self.size


class Selection(unittest.TestCase):
    def app(self, text="- [ ] b\n- [ ] a\n- [x] old\n"):
        import tempfile
        path = os.path.join(tempfile.mkdtemp(), "list.md")
        nx.write(path, text)
        return nx.App(Screen(40, 45), path, "t")

    def test_starts_with_nothing_selected(self):
        app = self.app()
        self.assertIsNone(app.focus)
        self.assertIsNone(app.cur)

    def test_moving_selects_the_first_pending_item(self):
        app = self.app()
        app.step(1)
        self.assertEqual(app.focus, [False, "a"])

    def test_unselect_clears_the_cursor(self):
        app = self.app()
        app.step(1)
        app.unselect()
        self.assertIsNone(app.focus)

    def test_item_keys_do_nothing_without_a_selection(self):
        app = self.app()
        before = nx.read(app.path)
        app.toggle()
        app.delete()
        app.move(1)
        self.assertEqual(nx.read(app.path), before)
        self.assertIsNone(app.focus)

    def test_copy_takes_the_whole_item(self):
        app = self.app("- [ ] a long item that would wrap in a narrow pane\n")
        copied = []
        real, nx.clipboard = nx.clipboard, lambda text: copied.append(text) or True
        try:
            app.copy()
            app.step(1)
            app.copy()
        finally:
            nx.clipboard = real
        self.assertEqual(copied, ["a long item that would wrap in a narrow pane"])
        self.assertEqual(app.note[0], "copied")

    def test_reload_keeps_nothing_selected(self):
        app = self.app()
        nx.write(app.path, "- [ ] c\n" + nx.read(app.path))
        app.seen = None
        app.reload()
        self.assertIsNone(app.focus)


if __name__ == "__main__":
    unittest.main()
