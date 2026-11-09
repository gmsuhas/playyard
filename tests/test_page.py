import unittest

from playyard.page import card, render


class PageTests(unittest.TestCase):
    def test_page_is_one_self_contained_document(self):
        doc = render("Play", "a small page", [card("Notes", "<p>hi</p>")])
        self.assertTrue(doc.startswith("<!doctype html>"))
        self.assertIn("<style>", doc)
        self.assertNotIn("<link", doc)
        self.assertNotIn("<script src", doc)

    def test_title_is_escaped_but_body_markup_is_kept(self):
        doc = render("A & B", "lead", [card("x < y", "<em>kept</em>")])
        self.assertIn("<title>A &amp; B</title>", doc)
        self.assertIn("<h2>x &lt; y</h2>", doc)
        self.assertIn("<em>kept</em>", doc)

    def test_sections_appear_in_order(self):
        doc = render("T", "L", [card("First", "<p>1</p>"), card("Second", "<p>2</p>")])
        self.assertLess(doc.index("First"), doc.index("Second"))


if __name__ == "__main__":
    unittest.main()
