import pathlib
import unittest

from playyard.page import from_text

ROOT = pathlib.Path(__file__).resolve().parents[1]

# The three commands in the README. If an example changes, rebuild the page.
PAGES = (
    ("Counting in bhai", "examples/counting.txt", "one loop, then done", "docs/counting.html"),
    ("Where Saturday went", "examples/saturday.txt", "a day log, added up", "docs/saturday.html"),
    ("Why playyard", "examples/why.txt", "small on purpose", "docs/why.html"),
)


class DocsTests(unittest.TestCase):
    def test_checked_in_pages_match_the_examples(self):
        for title, source, lead, output in PAGES:
            fresh = from_text(title, lead, (ROOT / source).read_text(encoding="utf-8"))
            saved = (ROOT / output).read_text(encoding="utf-8")
            self.assertEqual(saved, fresh, output)


if __name__ == "__main__":
    unittest.main()
