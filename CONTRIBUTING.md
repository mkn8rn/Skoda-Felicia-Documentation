# Editing the guide

Write an encyclopedia reference, with neutral prose, descriptive article titles,
ordinary headings, numbered citations, and useful cross-links. Keep the public
guide in HTML and CSS. There is no framework, generated content system, or build
step. Edit the HTML files directly and reuse `public/style.css`.

## Hard rule: self-contained knowledge

The repository is the one-stop reference for ALL Felicia information. Its
technical content must remain usable if every source website disappears.
Document verified information here in compact, standard technical English.
Use original prose, precise quantities with units, and locally recorded
application conditions. Sources provide evidence; they do not supply missing
content on behalf of this guide. Do not copy or directly quote their text or
reproduce their tables, photographs, or diagrams.

A technical article must contain the facts and explanations it claims to cover.
A repair article must contain its applicable instructions, prerequisites,
specifications, and checks, rather than directing the reader to a manual.
An index links to internal articles. Unwritten subjects remain clearly labelled
gaps. A supplier or manual link does not count as documentation of a component.
Place external technical links in references; the source bibliography may
describe source coverage and access without becoming the reader's learning path.

Before publication, read the article with all external links unavailable. If an
explanation, dimension, identification condition, or required step is only on a
cited site, the article is incomplete. Record exactly what remains unknown;
never fill it with an assumption or imply that a citation resolves the gap.

## Subjects and paths

| Directory | Subject |
| --- | --- |
| `public/history/` | Development, factories, production, exports, and historical context |
| `public/models/` | Body styles, engines, transmissions, editions, and identification |
| `public/parts/` | Components, assemblies, part numbers, and compatibility |
| `public/repairs/` | Fault finding, repairs, electrical diagnosis, and restoration |
| `public/maintenance/` | Scheduled service, inspections, adjustments, and preservation |
| `public/ownership/` | Operating controls, daily use, loading, seasons, and ownership records |
| `public/upgrades/` | Evidenced modifications and conversions |
| `public/sources/` | Bibliographic descriptions and source entry points |

Each subject's `index.html` is its category index. Add substantive articles as
descriptive lowercase filenames, such as `parts/oil-filter.html` or
`repairs/oil-filter-replacement.html`. Do not create an empty article for every
possible subject: list unwritten subjects as plain text in their category index.

`public/parts/original.html` indexes original equipment and factory service
replacements. `public/parts/compatible.html` indexes evidenced alternatives and
interchanges. Both link to the same canonical component articles; classification
does not create a second copy of an article. An unverified fit is not an entry.

Do not create a dedicated catalogue or diagram index. Each component article
cites relevant diagram sources in its own References section, identifying the
assembly, item, and applicability. Preserve the actual technical explanation
and verified facts in the article; a source diagram must not supply its missing
content.

## One article per part

A part has one canonical article in `public/parts/`, shared by every Felicia
version that uses it. Never create copies under different model, year, engine,
trim, repair, or system directories. Model and repair articles link to that same
page. A part appearing in several systems is linked from each relevant system
index, without duplicating the article.

Before adding a part article, search existing titles and documented OE and
manufacturer identifiers, including revision suffixes, alternate numbers, and
confirmed aliases or supersessions. Reuse the existing page for the same part.
Record alternate names and identifiers in that article so later contributors can
find it. Do not infer identity from appearance, a similar name, or a similar
number: distinct parts must remain distinguishable, and an unverified match
remains unresolved.

Each part article lists its evidenced applications together, preferably in an
**Applications** table with the relevant model/body, engine/gearbox, production
or VIN limits, equipment, and source. Different vehicle applications are rows
in that table, not separate copies of the page. Keep the canonical article's
filename stable when another compatible Felicia version is documented.

## Article layout

Copy the document shell, navigation, and footer from an existing article at the
same directory depth. Update its title, description, relative links, and the
navigation link marked `aria-current="page"`; a new article need not mark a
category-index link as the current page.

Use this order, omitting sections that have no content:

1. A single `h1` with the article title.
2. A concise introduction identifying the subject and applicable variants.
3. A contents list for a longer article, linked to actual heading IDs.
4. Descriptive `h2` sections and, where needed, `h3` subsections.
5. **See also** for related internal articles.
6. **References** for the sources supporting statements in the article.
7. Optional links to internal source descriptions for further research.

Use tables for comparable specifications or part applications, with a caption,
column headings, and row headings. Include units and source citations. Use
ordered lists for an actual procedure. Label stubs explicitly; distinguish
missing evidence from evidence that a feature is absent.

## Citations and evidence

Place a numbered citation beside the claim it supports. Use a superscript link
to an ordered reference list, following the pattern in the existing parts pages:

```html
<sup id="cite-ref-1" class="reference"><a href="#cite-note-1">[1]</a></sup>
```

The matching reference has `id="cite-note-1"`, a backlink to `#cite-ref-1`,
publisher or author, title, URL, publication date if known, and access date.
For subsequent uses of the same source, use distinct marker IDs and link to the
same reference entry; add the corresponding backlinks. Never repeat an HTML ID.
Print/manual citations identify the author, title, edition, publication year,
and page, chapter, or section actually consulted. Do not infer an edition or
page from another edition's product listing.

Prefer primary records and identified technical publications. Attribute retailer
application claims and owner reports. Do not treat several sites repeating the
same catalogue data as independent confirmation. Preserve conflicts with
attribution until evidence resolves them. The bibliography is a directory of
sources, not a substitute for citations next to technical claims or for the
actual technical information in an article.

Part articles distinguish an OE/OEM number, supplier stock code, manufacturer
number, and diagram callout. Keep revision suffixes and cite application limits,
supersessions, and interchangeability. State relevant body, engine, gearbox,
production/VIN limits, market, steering side, and equipment. Similar appearance
is not proof of compatibility. An ECU hardware claim identifies the unit number,
board revision, component markings, and the evidence for that identification.

Production totals must define the period and vehicles counted. Repair articles
identify applicability, symptoms, diagnosis, prerequisites, tools, parts,
procedure, cited torque/test specifications, and final checks as appropriate.
Do not publish an instruction or specification that is not supported by evidence.
Upgrade articles identify the original report, author, vehicle, donor parts,
fabrication/wiring changes, observed results, and limitations. A reported build
is not automatically a generally compatible or approved conversion.

## Stable links

Keep published filenames and meaningful heading IDs stable. Link related repair
and maintenance articles to the component article and its category index. Until a
component article exists, use a system anchor, such as
`../parts/index.html#fuel-and-exhaust`.

In the component article's References, cite the exact external assembly or
application entry supporting the claim. Record its model selection, diagram
number/title, item callout, and applicable notes.
Use a provider's model selector as an alternative when its deep link requires a
session. If a system grows into its own article, retain the original index anchor
and replace its summary with a link to the new article.

Use relative internal links with explicit `.html` filenames so the guide works
from a local file, a static server, and a deployment under a URL subdirectory.
External sources are ordinary links, never embedded images, iframes, or downloads
stored in this repository.

## Copyright and private sources

Public articles contain original descriptions and links. Do not reproduce or
closely paraphrase a manual's prose, procedures, photographs, or diagrams. Do not
copy catalogue tables, scans, website screenshots, or bulk data. Facts may be
described in original words with a precise citation; retain the source's scope.
Do not assume that purchase, attribution, or a publicly readable webpage grants
republication rights. Direct source quotations are not permitted in this guide.

Keep purchased publications and all protected extracts, OCR, working notes,
screenshots, and scans **only in `docs/internal/`**. This directory is ignored by
Git and is outside the site's document root. Never force-add it or copy its
contents to a tracked path. Do not publish local links to private references.
Public bibliographic entries may link to the publisher and state access limits.

The owner's locally preserved Haynes manual is a private reference. Cite the
actual edition and locator when consulting it; do not reuse its text or diagrams.
The bibliography identifies the consulted copy by its manual number, ISBN, and
title-page copyright year, separately from the publisher's current digital
listing. Do not transfer an edition's scope or page numbering to another edition.

## Before committing and pushing

Install the guards with `git config core.hooksPath .githooks`. Run
`python3 scripts/check_repository.py`, stage explicit public paths, and inspect
`git diff --cached --name-status` and `git diff --cached` before committing. Check
that `git ls-files -- docs/internal` is empty and that `git check-ignore -v`
identifies the ignore rule for private files. Do not use `git add .`, `git add -A`,
`git add -f`, or skip hooks in this repository.

The validator checks internal files and anchors, duplicate part-article titles,
basic HTML structure, placement of external technical links only in references
or source bibliographies, absence of scripts and embedded external material,
protected paths, source-document file types, and source-document signatures.
The commit check reads the staged version,
not an unstaged revision. The push check additionally inspects reachable history.
These checks do not establish copyright compliance: review the actual prose and
the provenance of every public file. Identifier and alias searches remain
necessary to detect the same part described under different titles. Push each
completed commit.

Serve and publish **only `public/`**. Never package or deploy the repository root,
`docs/`, or private reference material.
