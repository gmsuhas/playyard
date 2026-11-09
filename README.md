# playyard

Three small tools for text. Python 3.9 or newer, nothing else to install.

```sh
python3 -m playyard bhai   examples/hello.bhai
python3 -m playyard digest examples/day.log
python3 -m playyard page "Playyard" examples/page.txt > page.html
```

## bhai

Runs a few lines of a toy language.

```
n = 1
jab tak n < 4
bhai bol n
n = n + 1
bas
bhai bol "done"
```

That prints 1, 2, 3, done. `bol` prints. `name = value` assigns. `+`, `-` and `*` work left to right, so `2 + 3 * 4` is 20. `jab tak ... bas` is one loop: the comparison is checked before the body runs, and a second loop inside the first is an error rather than a hang.

`examples/hello.bhai` is the whole language in one file.

## digest

Reads a day written one line at a time and says where the time went.

```
09:00-10:30 read the grammar notes
10:30-12:00 implement the loop
13:40-14:30 write the readme
sketch the page layout
```

A line is `HH:MM-HH:MM what I did`. An en dash works too, and a range with nothing after it still counts. A line with no clock is listed and adds no minutes. A range that runs backwards, or longer than 12 hours, is reported with its line number instead of being counted. Each line is filed under the first theme whose words all appear in it: learning, review, code, design, writing, or other. Matching is on whole words, so "readme" is writing and "read" is learning.

`examples/day.log` is a Saturday. The tool reports 4h 50m, mostly code and learning. The guess is only as good as the word list in `playyard/digest.py`, and a line that uses none of those words lands in "other".

## page

Turns a text file into one HTML file, styling included, with nothing to fetch.

```
# What this is

A page that ships as one file.

# The program

  n = 1
  jab tak n < 4
  bhai bol n
  bas
```

A line that starts with `# ` is a heading. A block indented by two spaces is kept as code. Everything else is a paragraph, and `<` and `&` are escaped for you, so the file you write is text.

## The pages in docs/

[docs/counting.html](docs/counting.html), [docs/saturday.html](docs/saturday.html) and [docs/why.html](docs/why.html) are built from `examples/counting.txt`, `examples/saturday.txt` and `examples/why.txt`. A test renders those three files and checks the saved HTML still matches, and another checks that `examples/day.log` still totals 4h 50m in the order the README describes, so neither can quietly drift. On GitHub the links show source. Clone the repo and open the files to see them.

```sh
python3 -m unittest discover -s tests
```

## Where it came from

I had forked [DulLabs/bhai-lang](https://github.com/DulLabs/bhai-lang) and [Metroxe/one-html-page-challenge](https://github.com/Metroxe/one-html-page-challenge) and never opened either one. This is the small version of each idea that I will actually run: an interpreter you can read in one sitting, a digest for a log I already keep as text, and a page builder that takes text instead of markup. The ideas are theirs. The code here is mine, and it is not a port.

## What it will not do

`bhai` is not bhai-lang. One loop, no functions, no nested expressions. `digest` will misfile a sentence that happens to contain one of its words. Both stay one file on purpose.
