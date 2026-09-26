#!/usr/bin/env python3
"""Validate the public guide and reject tracked private/source documents.

Uses only the Python standard library. It never traverses docs/internal/.
"""

import argparse
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_PREFIXES = ("docs/internal/", "internal-docs/")
SOURCE_EXTENSIONS = {".pdf", ".epub", ".djvu", ".djv", ".zip", ".rar", ".7z", ".cbz", ".cbr"}
SOURCE_SIGNATURES = (b"%PDF-", b"PK\x03\x04", b"Rar!", b"7z\xbc\xaf\x27\x1c", b"AT&TFORM")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def entries(staged):
    command = ("ls-files", "--stage", "-z") if staged else ("ls-tree", "-r", "-z", "HEAD")
    for row in git(*command).split(b"\0"):
        if row:
            metadata, path = row.split(b"\t", 1)
            fields = metadata.split()
            yield path.decode("utf-8"), fields[0].decode(), fields[1 if staged else 2].decode()


def private_or_document(path):
    lower = path.casefold()
    return lower.startswith(PRIVATE_PREFIXES) or lower.rstrip("/") in {"docs/internal", "internal-docs"} or PurePosixPath(lower).suffix in SOURCE_EXTENSIONS


class Article(HTMLParser):
    def __init__(self, path, errors):
        super().__init__(convert_charrefs=True)
        self.path, self.errors = path, errors
        self.ids, self.links, self.stack = set(), [], []
        self.h1_count = self.main_count = self.title_count = 0
        self.h1_text = []
        self.language = self.viewport = self.charset = self.doctype = False

    def error(self, message):
        self.errors.append(f"{self.path}: {message}")

    def handle_decl(self, declaration):
        self.doctype = declaration.casefold() == "doctype html"

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag not in VOID:
            self.stack.append(tag)
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.error(f"duplicate ID: {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag in {"script", "iframe", "object", "embed", "img", "svg", "video", "audio", "base"}:
            self.error(f"embedded or executable material is not permitted in this index: {tag}")
        if any(key.casefold().startswith("on") for key in attrs):
            self.error("inline event handler")
        if "style" in attrs:
            self.error("inline style; use the shared stylesheet")
        self.h1_count += tag == "h1"
        self.main_count += tag == "main"
        self.title_count += tag == "title"
        self.language |= tag == "html" and attrs.get("lang") == "en"
        self.viewport |= tag == "meta" and attrs.get("name") == "viewport"
        self.charset |= tag == "meta" and attrs.get("charset", "").casefold() == "utf-8"
        if tag == "a":
            if not attrs.get("href"):
                self.error("anchor without a destination")
            else:
                self.links.append(attrs["href"])
        if tag == "link":
            self.links.append(attrs.get("href", ""))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.error(f"unmatched closing tag: {tag}")
        else:
            self.stack.pop()

    def handle_data(self, data):
        if "h1" in self.stack:
            self.h1_text.append(data)

    def finish(self):
        self.close()
        if self.stack:
            self.error(f"unclosed tags: {self.stack}")
        if (self.h1_count, self.main_count, self.title_count) != (1, 1, 1):
            self.error("expected exactly one h1, main, and title")
        if not all([self.doctype, self.language, self.viewport, self.charset]):
            self.error("missing HTML5 doctype, language, viewport, or UTF-8 declaration")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged", action="store_true", help="validate the Git index, including staged HTML")
    parser.add_argument("--history", action="store_true", help="also check all reachable commits for private/source files")
    args = parser.parse_args()
    if args.staged and args.history:
        parser.error("choose either --staged or --history")
    errors, files, checked_blobs = [], {}, set()
    snapshots = list(entries(staged=not args.history))
    for path, mode, sha in snapshots:
        if private_or_document(path):
            errors.append(f"Private/source document is tracked: {path}")
            continue
        if mode != "100644" and mode != "100755":
            errors.append(f"Symlinks and submodules are not permitted: {path}")
            continue
        data = git("cat-file", "blob", sha)
        checked_blobs.add(sha)
        if data.lstrip().startswith(SOURCE_SIGNATURES):
            errors.append(f"Source-document signature found in: {path}")
        files[path] = data

    if args.history:
        # Check every historical tree, including a private file later deleted.
        # Inspect each distinct blob once so renaming a PDF does not evade checks.
        for commit in git("rev-list", "--all").decode().splitlines():
            for row in git("ls-tree", "-r", "-z", commit).split(b"\0"):
                if not row:
                    continue
                metadata, raw_path = row.split(b"\t", 1)
                mode, kind, raw_sha = metadata.split()
                path, sha = raw_path.decode(), raw_sha.decode()
                if private_or_document(path) or mode == b"120000" or kind != b"blob":
                    errors.append(f"Private/source path or non-file in history ({commit[:8]}): {path}")
                elif sha not in checked_blobs:
                    checked_blobs.add(sha)
                    if git("cat-file", "blob", sha).lstrip().startswith(SOURCE_SIGNATURES):
                        errors.append(f"Source-document signature in history ({commit[:8]}): {path}")

    if not args.staged and not args.history:
        # Working-tree checks include new public pages before they are staged.
        files = {path: data for path, data in files.items() if not path.startswith("public/")}
        for path in (ROOT / "public").rglob("*"):
            if path.is_symlink():
                errors.append(f"Public symlink is not permitted: {path.relative_to(ROOT)}")
            elif path.is_file():
                files[path.relative_to(ROOT).as_posix()] = path.read_bytes()

    articles = {}
    for path, data in files.items():
        if not path.startswith("public/"):
            continue
        if PurePosixPath(path).suffix not in {".html", ".css"}:
            errors.append(f"Public site accepts HTML/CSS only: {path}")
            continue
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"Public file is not UTF-8 text: {path}")
            continue
        if path.endswith(".css"):
            if re.search(r"@import\b|url\s*\(", text, re.IGNORECASE):
                errors.append(f"CSS embeds an external or private resource: {path}")
            continue
        article = Article(path, errors)
        article.feed(text)
        article.finish()
        articles[path] = article

    part_titles = {}
    for path, article in articles.items():
        if path.startswith("public/parts/"):
            title = " ".join("".join(article.h1_text).casefold().split())
            if title in part_titles:
                errors.append(f"Duplicate part-article title: {path} and {part_titles[title]}; use one shared page")
            else:
                part_titles[title] = path
        for href in article.links:
            destination = urlsplit(href)
            if destination.scheme:
                if destination.scheme not in {"https", "http", "mailto"}:
                    errors.append(f"{path}: prohibited URL scheme: {href}")
                continue
            if destination.netloc:
                errors.append(f"{path}: use an explicit HTTPS external link: {href}")
                continue
            target = (PurePosixPath(path).parent / unquote(destination.path)) if destination.path else PurePosixPath(path)
            # Resolve dot segments without opening or following the target.
            parts = []
            for component in target.parts:
                if component == "..":
                    if parts:
                        parts.pop()
                elif component != ".":
                    parts.append(component)
            target = "/".join(parts)
            if not target.startswith("public/") or target not in files:
                errors.append(f"{path}: missing or non-public destination: {href}")
            elif destination.fragment and (target not in articles or unquote(destination.fragment) not in articles[target].ids):
                errors.append(f"{path}: missing fragment: {href}")

    if not articles:
        errors.append("No public HTML articles found")
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in dict.fromkeys(errors):
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"Validated {len(articles)} HTML pages, internal links and source-document boundaries" + ("; reachable history checked." if args.history else "."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
