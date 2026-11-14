# preksg.github.io

Portfolio of Prekeme "Pre-Gee" Paul, Senior Data Analytics Engineer. A static site (HTML, CSS and a little vanilla JavaScript) served by GitHub Pages. There is no build step and no dependencies.

## Structure

```text
index.html                 Homepage: hero, overview, case studies, approach, expertise, experience, credentials, contact
case-studies/*.html        One page per case study (generated, committed)
styles.css                 Design system and all page styles
script.js                  Navigation, scroll reveals, filters, counters, ledger animation
404.html, robots.txt, sitemap.xml
favicon.svg
assets/                    Headshot, CV, social image, illustrations (see assets/ASSET-INVENTORY.md)
tools/case_study_content.py  Content for every case-study page (edit this)
tools/build_case_studies.py  Renders case-studies/*.html, plus redirects for merged studies
```

## Preview locally

From the repository root:

```bash
python -m http.server 8000
```

Then open http://localhost:8000. (Opening `index.html` directly also works, but the 404 page uses root paths and only behaves correctly on a server.)

## Editing a case study page

Case study pages are generated so they all share one layout. Edit the content in `tools/case_study_content.py`, then run:

```bash
python tools/build_case_studies.py
```

and commit the regenerated HTML. Sources of truth are the write-ups in [PreksG/analytics-case-studies](https://github.com/PreksG/analytics-case-studies) and the owner's project inventory. Do not add figures or outcomes that are not in those sources. A section with no evidence is left out, not written up.

## Deploy

GitHub Pages serves the default branch. Merge the working branch into `main` through a pull request; Pages republishes within a minute or two.

## Content rules

- Case studies are anonymised: no company data, real figures, internal names or screenshots of company systems.
- Every project shows its honest status: Implemented, Partially implemented, Recurring, In progress.
- Measured impact is marked "Not yet quantified" until a figure is approved for publication.
