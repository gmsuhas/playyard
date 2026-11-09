"""Read a loose activity log and say what the day was actually about.

Lines look like `09:10-09:40 review the design`. A line with no clock is
still listed, but it adds no minutes. Themes come from a short word list and
the first match wins, matched on whole words.
"""

import re
from collections import defaultdict

_CLOCK = re.compile(r"^(\d{1,2}):(\d{2})\s*[-\u2013]\s*(\d{1,2}):(\d{2})(?:\s+(.*))?$")
# Earlier themes win. "notes" is not a writing word: "read the notes" should
# be learning, and the writing list already has "readme", "doc" and "draft".
_THEMES = (
    ("learning", ("read", "learn", "course", "tutorial", "study")),
    ("review", ("review", "pull request", "feedback")),
    ("code", ("code", "fix", "bug", "refactor", "test", "implement", "build")),
    ("design", ("design", "spec", "architecture", "diagram")),
    ("writing", ("write", "doc", "readme", "draft")),
)


def _minutes(hours, mins):
    hours, mins = int(hours), int(mins)
    if not (0 <= hours <= 23 and 0 <= mins <= 59):
        raise ValueError(f"not a time: {hours}:{mins:02d}")
    return hours * 60 + mins


def parse_entry(line):
    """Return (minutes, text) for one line. Minutes is None without a clock."""
    text = line.strip()
    if not text or text.startswith("#"):
        return None
    match = _CLOCK.match(text)
    if not match:
        return None, text
    start = _minutes(match.group(1), match.group(2))
    end = _minutes(match.group(3), match.group(4))
    if end < start:  # written across midnight, so the end belongs to the next day
        end += 24 * 60
    span = end - start
    if span > 12 * 60:
        raise ValueError(f"time range is {span // 60}h {span % 60:02d}m, which is longer than a day")
    return span, (match.group(5) or "").strip()


def theme_of(text):
    """First matching theme wins. Words match whole, so "readme" is not "read"."""
    words = set(re.findall(r"[a-z]+", text.lower()))
    for name, keys in _THEMES:
        for key in keys:
            if set(key.split()) <= words:
                return name
    return "other"


def digest(text):
    """Summarize a log. Returns totals plus one row per theme."""
    themes = defaultdict(lambda: {"minutes": 0, "entries": 0, "samples": []})
    total_minutes = 0
    untimed = 0
    for number, line in enumerate(text.splitlines(), start=1):
        try:
            parsed = parse_entry(line)
        except ValueError as exc:
            raise ValueError(f"line {number}: {exc}") from None
        if parsed is None:
            continue
        minutes, body = parsed
        row = themes[theme_of(body)]
        row["entries"] += 1
        if len(row["samples"]) < 3:
            row["samples"].append(body)
        if minutes is None:
            untimed += 1
        else:
            row["minutes"] += minutes
            total_minutes += minutes
    rows = [
        {"theme": name, **row}
        for name, row in themes.items()
    ]
    rows.sort(key=lambda r: (-r["minutes"], -r["entries"], r["theme"]))
    return {"minutes": total_minutes, "untimed": untimed, "themes": rows}
