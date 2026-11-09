"""Command line for the playgrounds.

    python -m playyard bhai   examples/hello.bhai
    python -m playyard digest examples/day.log
    python -m playyard page   "My page" examples/page.txt
"""

import sys

from . import bhai, digest, page


def _read(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as handle:
        return handle.read()


def _cmd_bhai(args):
    if len(args) != 1:
        return "usage: playyard bhai FILE"
    for line in bhai.run(_read(args[0])):
        print(line)
    return None


def _cmd_digest(args):
    if len(args) != 1:
        return "usage: playyard digest FILE"
    report = digest.digest(_read(args[0]))
    hours, mins = divmod(report["minutes"], 60)
    print(f"tracked {hours}h {mins:02d}m across {len(report['themes'])} themes")
    if report["untimed"]:
        print(f"{report['untimed']} entries had no time range")
    print()
    for row in report["themes"]:
        row_hours, row_mins = divmod(row["minutes"], 60)
        print(f"{row['theme']:<10} {row_hours}h {row_mins:02d}m   {row['entries']} entries")
        for sample in row["samples"]:
            print(f"             - {sample}")
    return None


def _cmd_page(args):
    if len(args) != 2:
        return "usage: playyard page TITLE FILE"
    title, path = args
    sections = []
    heading = None
    buffer = []
    for line in _read(path).splitlines():
        if line.startswith("# "):
            if heading:
                sections.append(page.card(heading, "\n".join(buffer)))
            heading, buffer = line[2:].strip(), []
        else:
            buffer.append(line)
    if heading:
        sections.append(page.card(heading, "\n".join(buffer)))
    print(page.render(title, "a single file, no build step", sections))
    return None


COMMANDS = {"bhai": _cmd_bhai, "digest": _cmd_digest, "page": _cmd_page}


def main(argv):
    if not argv or argv[0] in {"-h", "--help"} or argv[0] not in COMMANDS:
        names = ", ".join(COMMANDS)
        print(f"usage: python -m playyard <{names}> ...", file=sys.stderr)
        return 2
    error = COMMANDS[argv[0]](argv[1:])
    if error:
        print(error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
