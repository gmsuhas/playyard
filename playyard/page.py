"""Build one self-contained HTML page from a title and a body of markup.

Inspired by the one-html-page-challenge (github.com/Metroxe/one-html-page-challenge):
everything, including the styling, lives in the single file that comes out.
No build step, no assets to fetch.
"""

import html


_STYLE = """
:root { color-scheme: light dark; }
* { box-sizing: border-box; }
body { margin: 0; font: 16px/1.6 ui-sans-serif, system-ui, sans-serif; }
main { max-width: 42rem; margin: 0 auto; padding: 3rem 1.25rem 4rem; }
h1 { font-size: 2rem; line-height: 1.2; margin: 0 0 0.5rem; }
.lead { margin: 0 0 2rem; opacity: 0.75; }
section { margin: 0 0 1.5rem; padding: 1rem 1.1rem; border: 1px solid rgba(127,127,127,.35); border-radius: 12px; }
h2 { font-size: 1.05rem; margin: 0 0 0.4rem; }
pre { overflow: auto; padding: 0.8rem 1rem; border-radius: 8px; background: rgba(127,127,127,.12); }
footer { margin-top: 2.5rem; font-size: 0.85rem; opacity: 0.6; }
"""


def card(title, body):
    """One section. The body is trusted markup; the title is escaped."""
    return f"<section><h2>{html.escape(title)}</h2>\n{body}\n</section>"


def paragraph(text):
    return f"<p>{html.escape(text)}</p>"


def render(title, lead, sections, footer="made with playyard"):
    """Return a complete HTML document as a string."""
    body = "\n".join(sections)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{_STYLE}</style>
</head>
<body>
<main>
<h1>{html.escape(title)}</h1>
<p class="lead">{html.escape(lead)}</p>
{body}
<footer>{html.escape(footer)}</footer>
</main>
</body>
</html>
"""
