# Škoda Felicia Documentation

An independent, open-source reference for the 1994–2001 Škoda Felicia range.
Its scope is all Felicia information: history and production, models and
identification, parts, repairs, maintenance, everyday use, documented upgrades,
and manufacturing and component details.

Read the [live guide](https://skoda-felicia-documentation.mkn8rn.com/).

Start at [the main page](public/index.html), [Original parts](public/parts/original.html),
[Compatible parts](public/parts/compatible.html), or [engines](public/parts/engine.html).

Documentation coverage and outstanding research are recorded in
[COVERAGE.md](COVERAGE.md). Required content and source rules are in
[CONTRIBUTING.md](CONTRIBUTING.md); agent instructions are in
[AGENTS.md](AGENTS.md).

## Reading locally

Open `public/index.html` in a browser, or serve only the public directory:

```sh
python3 -m http.server 8000 --directory public --bind 127.0.0.1
```

Then visit <http://127.0.0.1:8000/>. The site is plain HTML and CSS, with no
JavaScript, external fonts, dependencies, or build step. The screen theme is dark;
print pages use dark text on white paper. Never serve the
repository root: private reference material lives outside `public/`.

## Editing

Read [CONTRIBUTING.md](CONTRIBUTING.md) for article structure, references,
stable links, and copyright rules. Public pages are edited directly in `public/`.

Install the repository's local Git guards once after cloning:

```sh
git config core.hooksPath .githooks
```

Check the site before committing:

```sh
python3 scripts/check_repository.py
```

The commit hook checks the staged tree, including internal links and placement
of external technical links in references or source bibliographies. The push
hook also checks reachable history for private paths and source-document files.
These checks supplement manual review; they cannot determine whether prose was
copied or whether an article contains all the information it claims to cover.

## Licence and contact

Original project material is licensed under [AGPL-3.0](LICENSE). External sources
retain their own rights. See [NOTICE](NOTICE) for the project notice and contact:
`mkn8rn@hotmail.com`.
