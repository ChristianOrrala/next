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
        self.assertEqual(texts(left), ["[ ] todo 0", "[ ] todo 1"])
        self.assertEqual(texts(right), ["[x] done 3", "[x] done 2", "[x] done 1", "[x] done 0"])

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
        self.assertLessEqual(nx.cells(right[0][1]), panels[1][1] - 2)


class Tall(unittest.TestCase):
    def test_done_fills_free_rows_up_to_half(self):
        view, panels = nx.arrange(items(40, 2), 45, 50, False)
        rows = panels[0][2]
        done_rows = [r for r in rows if r[2] == "done"]
        self.assertEqual(len(done_rows), 47 // 2)
        self.assertEqual(rows[0][1], f"… +{40 - 47 // 2} older")
        self.assertEqual(texts(rows)[-2:], ["[ ] todo 0", "[ ] todo 1"])
        self.assertEqual(view[len(done_rows) - 1], [True, "done 39"])  # oldest to newest, newest last

    def test_at_least_three_done_when_full(self):
        _, panels = nx.arrange(items(10, 60), 45, 20, False)
        self.assertEqual(sum(1 for r in panels[0][2] if r[2] == "done"), 3)

    def test_no_older_note_when_everything_fits(self):
        _, panels = nx.arrange(items(2, 2), 45, 50, False)
        self.assertEqual(texts(panels[0][2]), ["[x] done 0", "[x] done 1", "-" * 39, "[ ] todo 0", "[ ] todo 1"])

    def test_pending_wraps(self):
        _, panels = nx.arrange([[False, "word " * 20]], 30, 20, False)
        self.assertGreater(len(panels[0][2]), 1)
        self.assertTrue(texts(panels[0][2])[1].startswith("    "))


if __name__ == "__main__":
    unittest.main()
