import contextlib
import io
import unittest
from unittest import mock

from playyard.__main__ import main


class CliTests(unittest.TestCase):
    def test_help_names_the_commands(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = main(["--help"])
        self.assertEqual(code, 2)
        self.assertIn("bhai", err.getvalue())
        self.assertIn("digest", err.getvalue())

    def test_a_missing_file_is_a_message_not_a_traceback(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = main(["bhai", "no-such-file.bhai"])
        self.assertEqual(code, 1)
        self.assertTrue(err.getvalue().startswith("error:"))
        self.assertNotIn("Traceback", err.getvalue())

    def test_a_program_error_is_a_message(self):
        err = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO("bhai bol 1 +\n")):
            with contextlib.redirect_stderr(err):
                code = main(["bhai", "-"])
        self.assertEqual(code, 1)
        self.assertTrue(err.getvalue().startswith("error:"))
        self.assertNotIn("Traceback", err.getvalue())

    def test_bhai_prints_the_program_output(self):
        out = io.StringIO()
        with mock.patch("sys.stdin", io.StringIO('bhai bol "hi"\n')):
            with contextlib.redirect_stdout(out):
                code = main(["bhai", "-"])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), "hi")


if __name__ == "__main__":
    unittest.main()
