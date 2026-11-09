# playyard

Three small tools for text, in dependency-free Python. Python 3.9 or newer is enough.

```sh
python3 -m playyard bhai   examples/hello.bhai
python3 -m playyard digest examples/day.log
python3 -m playyard page "Playyard" examples/page.txt > page.html
```

`bhai` runs a few words of a toy language: `bol` prints, `name = value` assigns, `+ - *` do arithmetic left to right, and one `jab tak ... bas` loop repeats while a comparison holds. The comparison is checked first, so a loop that is already false never runs.

`digest` reads a day written as `09:10-09:40 write the readme` and adds up the minutes under a theme. Themes match whole words from a short list, so "readme" stays writing and "read" stays learning. A line with no clock still counts, it just adds no time.

`page` turns a text file into one HTML file with the styling inlined. A line starting with `# ` is a heading. An indented block is kept as code. Everything else becomes a paragraph. You write text, not HTML, and the result opens on its own.

## Where the ideas came from

I had forked [DulLabs/bhai-lang](https://github.com/DulLabs/bhai-lang) and [Metroxe/one-html-page-challenge](https://github.com/Metroxe/one-html-page-challenge) and never done anything with either. Rather than keep the forks as bookmarks, I built the smallest version of each idea that I would actually run: an interpreter small enough to read in one sitting, a page builder I can feed plain text, and a digest for the plain-text log I already keep. The code is mine. The ideas are not, and the README of each project says so.

## What you get

- [examples/hello.bhai](examples/hello.bhai) counts to three.
- [examples/day.log](examples/day.log) is a Saturday, and `digest` reports 4h 50m of it.
- [docs/counting.html](docs/counting.html), [docs/saturday.html](docs/saturday.html) and [docs/why.html](docs/why.html) are pages built from the text in `examples/`. On GitHub those links show the HTML source; clone the repo and open the files to see them rendered.

## What it will not do

`bhai` is not bhai-lang. There is one loop, no functions, and no nested expressions, and `2 + 3 * 4` is 20. `digest` guesses, and it will guess wrong on a sentence that uses none of its words. Both limits are there so each tool stays one file.

## Tests

```sh
python3 -m unittest discover -s tests
```

Rebuild the pages after editing an example:

```sh
python3 -m playyard page "Counting in bhai" examples/counting.txt "one loop, then done" > docs/counting.html
python3 -m playyard page "Where Saturday went" examples/saturday.txt "a day log, added up" > docs/saturday.html
python3 -m playyard page "Why playyard" examples/why.txt "small on purpose" > docs/why.html
```
