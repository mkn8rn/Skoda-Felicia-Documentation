# Škoda Felicia Documentation

An independent, open-source reference for the 1994–2001 Škoda Felicia range.
The guide covers history and production, models and identification, parts,
repairs, maintenance, everyday use, and documented upgrades.

The initial edition contains a parts-system index, an annotated index of
external parts catalogues and diagrams, and subject indexes for future articles.
Unwritten subjects are labelled as stubs. No manuals or diagrams are reproduced.
Each part has one shared article across every model that uses it; model and
repair pages link to that article rather than duplicating it.

Start at [the main page](public/index.html), [parts](public/parts/index.html),
or [parts catalogues and diagrams](public/parts/catalogues.html).

## Reading locally

Open `public/index.html` in a browser, or serve only the public directory:

```sh
python3 -m http.server 8000 --directory public --bind 127.0.0.1
```

Then visit <http://127.0.0.1:8000/>. The site is plain HTML and CSS, with no
JavaScript, external fonts, dependencies, or build step. Never serve the
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

The commit hook checks the staged tree, and the push hook also checks reachable
history for private paths and source-document files. These checks supplement
manual review; they cannot determine whether prose was copied from a source.

## Private references

Purchased publications, including the owner's Haynes manual, belong exclusively
in `docs/internal/`, which is ignored by Git. Extracts, OCR, scans, and research
notes containing protected source material belong there too. They must never be
staged, committed, pushed, linked from the public site, or copied into `public/`.

Public bibliographies may cite a publication and link to its publisher. A paid
reference does not become openly licensed because its owner purchased a copy.

## Licence and contact

Original project material is licensed under [AGPL-3.0](LICENSE). External sources
retain their own rights. See [NOTICE](NOTICE) for the project notice and contact:
`mkn8rn@hotmail.com`.
