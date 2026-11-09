import unittest

from playyard.page import card, from_text, render


class PageTests(unittest.TestCase):
    def test_page_is_one_self_contained_document(self):
        doc = render("Play", "a small page", [card("Notes", "<p>hi</p>")])
        self.assertTrue(doc.startswith("<!doctype html>"))
        self.assertIn("<style>", doc)
        self.assertNotIn("<link", doc)
        self.assertNotIn("<script src", doc)

    def test_plain_text_is_escaped_and_indented_blocks_stay_code(self):
        doc = render("A & B", "lead", [card("x < y", "a < b\n\n  1 < 2")])
        self.assertIn("<title>A &amp; B</title>", doc)
        self.assertIn("<h2>x &lt; y</h2>", doc)
        self.assertIn("<p>a &lt; b</p>", doc)
        self.assertIn("<pre>1 &lt; 2</pre>", doc)

    def test_from_text_splits_on_headings(self):
        doc = from_text("T", "L", "# First\n\none\n\n# Second\n\ntwo")
        self.assertLess(doc.index("First"), doc.index("Second"))
        self.assertIn("<p>one</p>", doc)

    def test_sections_appear_in_order(self):
        doc = render("T", "L", [card("First", "<p>1</p>"), card("Second", "<p>2</p>")])
        self.assertLess(doc.index("First"), doc.index("Second"))


if __name__ == "__main__":
    unittest.main()
