import unittest

from playyard.bhai import run


class BhaiTests(unittest.TestCase):
    def test_prints_a_string(self):
        self.assertEqual(run('bhai bol "namaste"'), ["namaste"])

    def test_does_arithmetic_and_remembers_variables(self):
        source = "\n".join([
            "bhai age = 20",
            "age = age + 1",
            "bhai bol age",
        ])
        self.assertEqual(run(source), ["21"])

    def test_loop_prints_until_the_condition_fails(self):
        source = "\n".join([
            "n = 0",
            "jab tak n < 3",
            "bhai bol n",
            "n = n + 1",
            "bas",
        ])
        self.assertEqual(run(source), ["0", "1", "2"])

    def test_rejects_an_unclosed_loop(self):
        with self.assertRaises(SyntaxError):
            run("n = 0\njab tak n < 1\nbhai bol n")

    def test_rejects_an_unknown_name(self):
        with self.assertRaises(NameError):
            run("bhai bol missing")

    def test_skips_a_loop_whose_condition_is_already_false(self):
        source = "jab tak 5 < 3\nbhai bol 1\nbas"
        self.assertEqual(run(source), [])

    def test_rejects_a_second_open_loop(self):
        source = "jab tak 0 < 1\njab tak 0 < 1\nbas\nbas"
        with self.assertRaises(SyntaxError):
            run(source)

    def test_stops_a_loop_that_never_ends(self):
        with self.assertRaises(RuntimeError):
            run("jab tak 1 < 2\nbas")

    def test_rejects_a_dangling_operator(self):
        with self.assertRaises(ValueError):
            run("bhai bol 1 +")

    def test_keeps_non_ascii_text_intact(self):
        self.assertEqual(run('bhai bol "café"'), ["café"])

    def test_other_comparisons_and_operators(self):
        source = "\n".join([
            "n = 2",
            "jab tak n > 0",
            "bhai bol n",
            "n = n - 1",
            "bas",
            "bhai bol 3 * 4",
        ])
        self.assertEqual(run(source), ["2", "1", "12"])


if __name__ == "__main__":
    unittest.main()
