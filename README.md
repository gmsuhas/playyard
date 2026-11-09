# playyard

Small text playgrounds, written in one Python file each. Nothing to install
beyond Python 3.9.

The ideas come from three projects I had forked and never touched:

- [DulLabs/bhai-lang](https://github.com/DulLabs/bhai-lang), a toy language
  whose keywords are Hindi. `playyard bhai` runs a small slice of it.
- the habit of keeping a plain-text log of the day. `playyard digest` adds up
  where the time went.
- [Metroxe/one-html-page-challenge](https://github.com/Metroxe/one-html-page-challenge).
  `playyard page` emits one HTML file with the styling inlined, so there is
  nothing to build and nothing to fetch.

## Try it

```sh
python3 -m playyard bhai   examples/hello.bhai
python3 -m playyard digest examples/day.log
python3 -m playyard page "Playyard" examples/page.txt > page.html
```

`bhai` understands `bol` (print), `name = value`, arithmetic with `+ - *`, and
a single `jab tak ... bas` loop. `digest` reads lines like
`09:10-09:40 write the readme` and groups them into themes.

## Tests

```sh
python3 -m unittest discover -s tests
```

## What it deliberately does not do

`bhai` is not a faithful bhai-lang: there is one loop, no functions, and no
nested expressions. `digest` guesses themes from a short word list. Both are
small enough to read straight through, which was the point.
