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


if __name__ == "__main__":
    unittest.main()
