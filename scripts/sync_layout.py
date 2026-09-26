#!/usr/bin/env python3
"""Sync shared page markup while retaining article content in public HTML files.

This is a contributor maintenance command, not a deployment build step.
Uses only the Python standard library; never reads docs/internal/.
"""

import argparse
from html import escape
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_FIELDS = {
    "templates/page.html": {"description", "title", "root", "header", "navigation", "content", "footer"},
    "templates/header.html": {"root"},
    "templates/navigation.html": {"root"},
    "templates/footer.html": set(),
}
TOKEN = re.compile(r"\{\{([^{}]+)\}\}")
MAIN = re.compile(r"<main\b[^>]*>(.*?)</main\s*>", re.DOTALL)
FOOTER = re.compile(r'<footer class="site-footer">.*?</footer>', re.DOTALL)


def decode_templates(files):
    """Read templates from the supplied working, staged, or committed snapshot."""
    templates = {}
    for path, fields in TEMPLATE_FIELDS.items():
        if path not in files:
            raise ValueError(f"Missing shared template: {path}")
        try:
            text = files[path].decode("utf-8")
        except UnicodeDecodeError as error:
            raise ValueError(f"{path}: expected UTF-8 text") from error
        if set(TOKEN.findall(text)) != fields:
            raise ValueError(f"{path}: unexpected or missing template fields")
        templates[path] = text.rstrip("\n")
    footer = templates["templates/footer.html"]
    if FOOTER.findall(footer) != [footer]:
        raise ValueError("templates/footer.html: expected exactly one site footer")
    return templates


def substitute(template, values):
    # Replace once: article text and metadata are never interpreted as templates.
    return TOKEN.sub(lambda match: values[match[1]], template)


class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title_count = 0
        self.title = []
        self.descriptions = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "title":
            self.title_count += 1
            self.in_title = True
        if tag == "meta" and attrs.get("name") == "description":
            self.descriptions.append(attrs.get("content", ""))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


def render_page(path, text, templates):
    """Preserve a page's metadata and main content; replace its shared layout."""
    relative = PurePosixPath(path).relative_to("public")
    if relative.suffix != ".html" or ".." in relative.parts:
        raise ValueError(f"{path}: expected a public HTML page")
    metadata = Metadata()
    metadata.feed(text)
    metadata.close()
    title = "".join(metadata.title)
    if metadata.title_count != 1 or not title or len(metadata.descriptions) != 1:
        raise ValueError(f"{path}: expected one title and description")
    mains = MAIN.findall(text)
    if len(mains) != 1:
        raise ValueError(f"{path}: expected exactly one main region")
    footers = list(FOOTER.finditer(mains[0]))
    if len(footers) != 1 or mains[0][footers[0].end():].strip():
        raise ValueError(f"{path}: expected one site footer at the end of main")
    content = mains[0][:footers[0].start()].strip()
    if not content:
        raise ValueError(f"{path}: empty main content")
    # An error response can be served at any URL, so its links are root-relative.
    root = "/" if relative.as_posix() == "404.html" else "../" * (len(relative.parts) - 1)
    header = substitute(templates["templates/header.html"], {"root": root})
    navigation = substitute(templates["templates/navigation.html"], {"root": root})
    current = f'<a href="{root}{relative.as_posix()}">'
    navigation = navigation.replace(current, current[:-1] + ' aria-current="page">')
    return substitute(templates["templates/page.html"], {
        "title": escape(title, quote=False),
        "description": escape(metadata.descriptions[0], quote=True),
        "root": root,
        "header": header,
        "navigation": navigation,
        "content": content,
        "footer": templates["templates/footer.html"],
    }) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="reject layout drift without writing files")
    args = parser.parse_args()
    updates = []
    try:
        files = {}
        for path in TEMPLATE_FIELDS:
            source = ROOT / path
            if source.is_symlink():
                raise ValueError(f"Shared template symlink is not permitted: {path}")
            files[path] = source.read_bytes()
        templates = decode_templates(files)
        # Prepare every change before writing, so a malformed page cannot cause
        # an incomplete sync. Read only the public tree, never private sources.
        for page in sorted((ROOT / "public").rglob("*")):
            if page.is_symlink():
                raise ValueError(f"Public symlink is not permitted: {page.relative_to(ROOT)}")
            if not page.is_file() or page.suffix != ".html":
                continue
            text = page.read_text(encoding="utf-8")
            rendered = render_page(page.relative_to(ROOT).as_posix(), text, templates)
            if rendered != text:
                updates.append((page, rendered))
    except (OSError, ValueError) as error:
        print(f"Layout sync failed: {error}", file=sys.stderr)
        return 1
    if args.check and updates:
        for page, _ in updates:
            print(f"Layout differs: {page.relative_to(ROOT)}", file=sys.stderr)
        return 1
    if not args.check:
        for page, rendered in updates:
            page.write_text(rendered, encoding="utf-8")
    print(f"Shared layout checked; {len(updates)} page(s) " + ("need updating." if args.check else "updated."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
