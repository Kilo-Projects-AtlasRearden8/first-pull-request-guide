"""Validate the built static site: HTML parses, all pages exist,
internal links resolve, LICENSE copyright line is exact, README credits
Asdale Dynamics, LLC."""

import html.parser
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "site")

PAGES = [
    "index.html",
    "01-what-is-github.html",
    "02-forking.html",
    "03-cloning.html",
    "04-branches.html",
    "05-issues.html",
    "06-your-first-pull-request.html",
    "checklist.html",
]

errors = []


VOID = {"meta", "link", "hr", "br", "img", "input", "area", "base", "col", "embed", "source", "track", "wbr"}
INLINE_CLOSE = {"strong", "em", "b", "i", "code", "span", "a"}


class HTMLChecker(html.parser.HTMLParser):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        elif tag in INLINE_CLOSE:
            # lenient: misnested inline tags are legal HTML (b/i classic case)
            for idx in range(len(self.stack) - 1, -1, -1):
                if self.stack[idx] == tag:
                    del self.stack[idx]
                    return
            errors.append(f"{self.name}: closing </{tag}> with no matching opener")
        else:
            errors.append(f"{self.name}: unexpected closing tag </{tag}> (stack: {self.stack[-5:]})")


print("== HTML parse check ==")
for page in PAGES:
    path = os.path.join(SITE, page)
    if not os.path.exists(path):
        errors.append(f"missing: {path}")
        continue
    with open(path, encoding="utf-8") as f:
        content = f.read()
    checker = HTMLChecker(page)
    try:
        checker.feed(content)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{page}: parse error: {exc}")
    if checker.stack:
        errors.append(f"{page}: unclosed tags: {checker.stack[-5:]}")
    # required elements
    for needle in ("<title>", "<main", "<footer", "Asdale Dynamics"):
        if needle not in content:
            errors.append(f"{page}: missing {needle}")
    # internal nav links resolve
    for href in PAGES:
        if f'href="{href}"' not in content:
            errors.append(f"{page}: missing nav link to {href}")
    print(f"ok   {page}")

print("\n== LICENSE copyright line ==")
with open(os.path.join(ROOT, "LICENSE"), encoding="utf-8") as f:
    license_text = f.read()
expected = "Copyright (c) 2026 Asdale Dynamics, LLC"
if expected in license_text:
    print("ok   exact copyright line present")
else:
    errors.append("LICENSE: exact copyright line missing")
    print("FAIL exact copyright line missing")

print("\n== README credit ==")
with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
    readme = f.read()
if "Asdale Dynamics, LLC" in readme:
    print("ok   README credits Asdale Dynamics, LLC")
else:
    errors.append("README: does not credit Asdale Dynamics, LLC")

print("\n== No .github/workflows ==")
if os.path.exists(os.path.join(ROOT, ".github", "workflows")):
    errors.append(".github/workflows exists (should not)")
    print("FAIL .github/workflows present")
else:
    print("ok   no .github/workflows")

print("\n== No secrets patterns ==")
secret_patterns = [r"sk-", r"AKIA", r"password\s*=\s*", r"api_key\s*=\s*"]
for dirpath, _, files in os.walk(ROOT):
    if ".git" in dirpath:
        continue
    for fn in files:
        if fn.endswith((".gitkeep",)):
            continue
        p = os.path.join(dirpath, fn)
        if fn.endswith(".py"):
            continue
        try:
            with open(p, encoding="utf-8", errors="ignore") as f:
                data = f.read()
        except Exception:
            continue
        for pat in secret_patterns:
            if re.search(pat, data, re.IGNORECASE):
                errors.append(f"possible secret in {p}: {pat}")

if errors:
    print(f"\nVERIFICATION FAILED ({len(errors)} errors):")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("\nALL CHECKS PASSED")
