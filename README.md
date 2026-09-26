# Škoda Felicia Documentation

An independent, open-source reference for the 1994–2001 Škoda Felicia range.
Its scope is all Felicia information: history and production, models and
identification, parts, repairs, maintenance, everyday use, documented upgrades,
and manufacturing and component details.

**Hard rule: the knowledge lives in this repository.** Articles preserve verified
information in original, compact, standard technical English. They must remain
usable if every cited website disappears. External sources provide evidence;
links to them never stand in for technical content. Do not copy or directly
quote source text or reproduce protected tables, photographs, or diagrams.

Each part has one shared article across every model that uses it; model and
repair pages link to that article rather than duplicating it.
The [Original parts](public/parts/original.html) and
[Compatible parts](public/parts/compatible.html) indexes classify those links
separately, without creating duplicate component pages.
Original parts also contains the vehicle-system index. There is no third,
general Parts page.

Start at [the main page](public/index.html), [Original parts](public/parts/original.html),
[Compatible parts](public/parts/compatible.html), or [engines](public/parts/engine.html).
Diagram sources are cited on the component article they support; there is no
separate diagram or catalogue index.

**Hard rule: the wiki contains car information only.** All agents and contributors
must keep process information, repository status, progress reports, editing
instructions, personal commentary, and future-work promises out of public
articles and indexes. Process belongs in AGENTS.md and CONTRIBUTING.md;
documentation status and outstanding research belong here. Technical
qualifications and source citations remain with the car information they explain.

## Documentation status and outstanding research

The site currently contains subject and parts indexes, a technical overview of
the production engines, and a source bibliography. Individual component,
compatibility, historical, repair, maintenance, ownership, and upgrade articles
remain to be researched and written. No manuals or source diagrams are reproduced.

Outstanding parts research includes original identifiers, factory supersessions,
assembly identification, and exact body, engine, gearbox, production/VIN,
market, steering-side, and equipment applications. Compatible parts need
verified product identities, donor applications, and installation conditions.

The engine overview does not yet cover complete variant/output mappings,
component numbers, engineering drawings, material grades, manufacturing
tolerances, surface finishes, lubrication and cooling specifications, injection
and ignition systems, ECU circuitry, assembly sequences, fastening specifications,
or diagnostic and overhaul procedures. History requires substantiated factory,
series, and annual production records, with defined counting methods.
Repair and maintenance instructions, operating guidance, and upgrade case
studies need their own verified technical content and precise source citations.

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
