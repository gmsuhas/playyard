import unittest

from playyard.digest import digest, parse_entry, theme_of


class DigestTests(unittest.TestCase):
    def test_reads_a_time_range(self):
        self.assertEqual(parse_entry("09:00-10:30 write the readme"), (90, "write the readme"))

    def test_keeps_lines_without_a_clock(self):
        self.assertEqual(parse_entry("think about the design"), (None, "think about the design"))

    def test_skips_blank_lines_and_comments(self):
        self.assertIsNone(parse_entry("   "))
        self.assertIsNone(parse_entry("# ignored"))

    def test_rolls_past_midnight(self):
        self.assertEqual(parse_entry("23:30-00:15 read a paper"), (45, "read a paper"))

    def test_picks_a_theme_from_keywords(self):
        self.assertEqual(theme_of("fix the flaky test"), "code")
        self.assertEqual(theme_of("lunch"), "other")

    def test_matches_whole_words_so_readme_stays_writing(self):
        self.assertEqual(theme_of("write the readme"), "writing")
        self.assertEqual(theme_of("read the grammar notes"), "learning")

    def test_rejects_a_clock_that_is_not_a_time(self):
        with self.assertRaises(ValueError):
            parse_entry("09:99-10:00 something")

    def test_groups_a_day_and_orders_by_time_spent(self):
        log = "\n".join([
            "09:00-11:00 fix the parser bug",
            "11:00-11:30 review the pull request",
            "13:00-14:00 write docs",
            "skim the tutorial",
        ])
        report = digest(log)
        self.assertEqual(report["minutes"], 210)
        self.assertEqual(report["untimed"], 1)
        self.assertEqual([row["theme"] for row in report["themes"]],
                         ["code", "writing", "review", "learning"])


if __name__ == "__main__":
    unittest.main()
