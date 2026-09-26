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

## Cloudflare Pages

In [Workers & Pages](https://dash.cloudflare.com/?to=/:account/workers-and-pages),
create a **Pages** project and import the existing GitHub repository
`mkn8rn/Skoda-Felicia-Documentation`. Authorise access to this repository and use:

| Setting | Value |
| --- | --- |
| Project name | `skoda-felicia-documentation` |
| Production branch | `main` |
| Framework preset | None |
| Root directory | Repository root; leave blank |
| Build command | `python3 scripts/check_repository.py --history` |
| Build output directory | `public` |

The build command validates the committed site and available Git history; it
does not generate the HTML. `wrangler.toml` records the same public asset
directory. No environment variables, framework, or package installation are
required. Use Cloudflare's current build image, which includes Python.

Select **Save and Deploy**. Git integration deploys production changes pushed
to `main`; Cloudflare supplies the live `pages.dev` address after deployment.
Only `public/` is published. Never change the output directory to the repository
root, `docs/`, or `docs/internal/`. `public/404.html` provides an error page for
missing paths instead of Cloudflare's default single-page application fallback.

`public/_headers` adds `Cache-Control: no-transform` to static responses, retaining
the default browser revalidation directives. This prevents Cloudflare from
rewriting the contact link or injecting email-decoding and JavaScript-detection
scripts. Pages consumes this configuration file without serving it as an asset;
the guide remains HTML and CSS only. The repository validator permits only this
specific response-header rule. Keep automatic Web Analytics and other script
injection features disabled if they are configured separately in the account.

On this deployment, Pages does not apply this header to missing-path 404
responses; Cloudflare still injects email-decoding and JavaScript-detection
scripts into those responses. To keep error pages script-free too, turn off
**Email Address Obfuscation** and **JavaScript Detections** in the domain's
**Security > Settings**. Bot Fight Mode automatically enables JavaScript
Detections and must be disabled if it is the active bot-protection mode.
These account settings cannot be changed by the repository configuration.

After deployment, check the main page, Original parts, Compatible parts, and AEF
engine replacement; check a nonexistent address and `/docs/internal/` return
HTTP 404. Project setup and account authorisation happen in Cloudflare, not in
this configuration file.

References: [Cloudflare static HTML deployment](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/),
[Pages configuration](https://developers.cloudflare.com/pages/functions/wrangler-configuration/),
[build image](https://developers.cloudflare.com/pages/configuration/build-image/),
and [serving and 404 behaviour](https://developers.cloudflare.com/pages/configuration/serving-pages/).
Response configuration: [Pages headers](https://developers.cloudflare.com/pages/configuration/headers/),
[Email Address Obfuscation](https://developers.cloudflare.com/waf/tools/scrape-shield/email-address-obfuscation/),
and [JavaScript Detections](https://developers.cloudflare.com/cloudflare-challenges/challenge-types/javascript-detections/).

## Licence and contact

Original project material is licensed under [AGPL-3.0](LICENSE). External sources
retain their own rights. See [NOTICE](NOTICE) for the project notice and contact:
`mkn8rn@hotmail.com`.
