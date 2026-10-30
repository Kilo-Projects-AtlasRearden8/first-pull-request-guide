"""Build the static HTML site from docs/ markdown.

Converts each .md file in docs/ to a matching .html file in site/,
copies assets, and runs a self-contained markdown parser so no external
dependencies are required.
"""

import html
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
SITE = os.path.join(ROOT, "site")

# Mapping from markdown source file to output HTML file.
PAGES = [
    ("index.md", "index.html", "Welcome"),
    ("01-what-is-github.md", "01-what-is-github.html", "1. What is GitHub?"),
    ("02-forking.md", "02-forking.html", "2. Forking"),
    ("03-cloning.md", "03-cloning.html", "3. Cloning"),
    ("04-branches.md", "04-branches.html", "4. Branches"),
    ("05-issues.md", "05-issues.html", "5. Issues"),
    ("06-your-first-pull-request.md", "06-your-first-pull-request.html", "6. Your first pull request"),
    ("checklist.md", "checklist.html", "Contribution checklist"),
]

NAV = [
    ("index.html", "Welcome"),
    ("01-what-is-github.html", "1. What is GitHub?"),
    ("02-forking.html", "2. Forking"),
    ("03-cloning.html", "3. Cloning"),
    ("04-branches.html", "4. Branches"),
    ("05-issues.html", "5. Issues"),
    ("06-your-first-pull-request.html", "6. Your first pull request"),
    ("checklist.html", "Contribution checklist"),
]


def inline(text):
    """Convert inline markdown to HTML."""
    # Code spans first so other markers inside code are protected.
    def code_span(match):
        return "<code>" + html.escape(match.group(1)) + "</code>"

    text = re.sub(r"`([^`]+)`", code_span, text)

    # Links: [text](url)
    def link(match):
        return '<a href="' + html.escape(match.group(2), quote=True) + '">' + match.group(1) + "</a>"

    text = re.sub(r"\[([^\]]*)\]\(([^)]*)\)", link, text)

    # Bold (** or __)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)

    # Italic (* or _)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)

    text = html.escape(text) if False else text
    return text


def block(text):
    """Convert a block of markdown (already split into lines) to HTML."""
    lines = text.split("\n")
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Horizontal rule
        if re.match(r"^---+\s*$", line):
            out.append("<hr>")
            i += 1
            continue

        # Heading
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            level = len(m.group(1))
            content = inline(m.group(2).strip())
            out.append(f"<h{level}>{content}</h{level}>")
            i += 1
            continue

        # Blockquote
        if line.startswith(">"):
            qlines = []
            while i < len(lines) and lines[i].startswith(">"):
                qlines.append(inline(lines[i][1:].strip()))
                i += 1
            out.append("<blockquote>" + "<br>".join(qlines) + "</blockquote>")
            continue

        # Code block
        if line.startswith("```"):
            lang = line[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            escaped = "\n".join(html.escape(c) for c in code_lines)
            class_attr = f' class="language-{lang}"' if lang else ""
            out.append(f"<pre><code{class_attr}>{escaped}</code></pre>")
            continue

        # Ordered list
        m = re.match(r"^(\d+)\.\s+(.*)", line)
        if m:
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i]):
                items.append(inline(re.sub(r"^\d+\.\s+", "", lines[i])))
                i += 1
            out.append("<ol>" + "".join(f"<li>{it}</li>" for it in items) + "</ol>")
            continue

        # Unordered list
        if line.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                raw = lines[i][2:]
                m = re.match(r"\[\s*(x|)\s*\]\s*(.*)", raw, re.IGNORECASE)
                if m:
                    checked = m.group(1) == "x"
                    box = '<input type="checkbox" disabled' + (' checked' if checked else '') + '> '
                    items.append(box + inline(m.group(2)))
                else:
                    items.append(inline(raw))
                i += 1
            out.append("<ul>" + "".join(f"<li>{it}</li>" for it in items) + "</ul>")
            continue

        # Paragraph
        if line.strip() == "":
            i += 1
            continue

        para_lines = []
        while i < len(lines) and lines[i].strip() != "" and not lines[i].startswith(("#", ">", "```", "- ")) and not re.match(r"^\d+\.\s+", lines[i]) and not re.match(r"^---+\s*$", lines[i]):
            para_lines.append(lines[i])
            i += 1
        out.append("<p>" + inline(" ".join(para_lines)) + "</p>")

    return "\n".join(out)


def markdown_to_html(md_text):
    """Convert full markdown text to HTML body content."""
    # Normalize line endings and strip a single trailing newline.
    text = md_text.replace("\r\n", "\n").replace("\r", "\n")
    # Split into blocks separated by blank lines, but keep fenced blocks intact.
    blocks = re.split(r"\n\s*\n", text.strip("\n"))
    return "\n\n".join(block(b) for b in blocks)


def page_template(title, body, page_file):
    nav_items = ""
    for href, label in NAV:
        active = ' class="active"' if href == page_file else ""
        nav_items += f'<li><a href="{href}"{active}>{label}</a></li>'

    print_link = ''
    if page_file == "checklist.html":
        print_link = (
            '<p class="print-hint"><strong>Print this page:</strong> '
            'Use your browser&rsquo;s print command (Ctrl+P / Cmd+P). '
            'The checklist is styled to fit on one printed page.</p>'
        )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} &middot; Your First Pull Request</title>
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="print.css" media="print">
</head>
<body>
<header class="site-header">
<div class="wrapper">
<h1><a href="index.html">Your First Pull Request</a></h1>
<p class="site-deck">A beginner&rsquo;s guide to GitHub &mdash; for non-programmers</p>
</div>
</header>

<nav class="site-nav">
<div class="wrapper">
<ul>{nav_items}</ul>
</div>
</nav>

<main class="wrapper">
{print_link}
{body}
</main>

<footer class="site-footer">
<div class="wrapper">
<p>Written and published by <strong>Asdale Dynamics, LLC</strong>
&middot; Copyright (c) 2026 Asdale Dynamics, LLC &middot;
<a href="LICENSE.html">MIT License</a></p>
</div>
</footer>
</body>
</html>"""


def build():
    os.makedirs(SITE, exist_ok=True)

    for src, dst, title in PAGES:
        with open(os.path.join(DOCS, src), "r", encoding="utf-8") as f:
            md = f.read()

        # Use the first H1 as the page title if present.
        m = re.search(r"^#\s+(.*)", md, re.MULTILINE)
        page_title = m.group(1).strip() if m else title
        full_title = f"{page_title} &middot; Your First Pull Request"

        body = markdown_to_html(md)
        html_doc = page_template(full_title, body, dst)

        with open(os.path.join(SITE, dst), "w", encoding="utf-8") as f:
            f.write(html_doc)

        print(f"built {dst}")


if __name__ == "__main__":
    build()
