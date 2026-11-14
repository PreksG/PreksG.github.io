"""Generate the static case-study pages in /case-studies.

The site has no build step: the generated HTML is committed. Edit the
content in tools/case_study_content.py, then run:

    python tools/build_case_studies.py

and commit the regenerated pages.
"""
import sys
from html import escape
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from case_study_content import STUDIES, REDIRECTS  # noqa: E402

SITE = "https://preksg.github.io"
GH = "https://github.com/PreksG/analytics-case-studies/tree/main/"
OUT = Path(__file__).resolve().parent.parent / "case-studies"

STATUS = {
    "done": "status-done",
    "partial": "status-partial",
    "recurring": "status-recurring",
    "prototype": "status-progress",
}

ICON_EXT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

FONTS = "https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&amp;family=Instrument+Sans:wght@400;500;600;700&amp;family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,500&amp;display=swap"


def e(text):
    return escape(text, quote=True)


def ul(items, cls="list"):
    return f'<ul class="{cls}">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def ol(items):
    return '<ol class="list list-num">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ol>"


def subs(blocks):
    """Sub-steps inside a section: [(heading, intro, [items], anchor_id), ...]."""
    out = ""
    for heading, intro, items, anchor in blocks or []:
        aid = f' id="{anchor}"' if anchor else ""
        out += f'<h3 class="cs-sub"{aid}>{e(heading)}</h3>'
        if intro:
            out += f"<p>{e(intro)}</p>"
        if items:
            out += ul(items)
    return out


def build_sections(s):
    """Return [(id, short label, inner html)] for the sections this study has evidence for."""
    sec = []

    def add(key, label, title, inner):
        sec.append((key, label, f'<h2 id="{key}-h">{e(title)}</h2>{inner}'))

    if s.get("overview"):
        add("overview", "Overview", "Project overview", f'<p>{e(s["overview"])}</p>')
    if s.get("context"):
        add("context", "Context", "Business context", f'<p>{e(s["context"])}</p>')
    p_intro, p_list = s["problem"]
    add("problem", "Problem", "Problem statement", f"<p>{e(p_intro)}</p>" + (ul(p_list) if p_list else ""))
    if s.get("objectives"):
        add("objectives", "Objectives", "Objectives", ol(s["objectives"]))
    if s.get("role_detail"):
        r_intro, r_list = s["role_detail"]
        add("role", "My role", "My role and contribution", f"<p>{e(r_intro)}</p>{ul(r_list)}")
    if s.get("architecture"):
        a_line, a_list = s["architecture"]
        add("architecture", "Architecture", "Solution architecture",
            (f'<p class="pipeline-line">{e(a_line)}</p>' if a_line else "") + (ul(a_list) if a_list else ""))
    if s.get("tools_detail"):
        rows = "".join(f'<tr><th scope="row">{e(t)}</th><td>{e(u)}</td></tr>' for t, u in s["tools_detail"])
        add("tools", "Tools", "Technologies and tools",
            f'<table class="cs-table"><thead><tr><th scope="col">Technology</th><th scope="col">Use in this project</th></tr></thead><tbody>{rows}</tbody></table>')
    if s.get("implementation") or s.get("implementation_subs"):
        i_intro, i_list = s.get("implementation") or (None, None)
        add("implementation", "Implementation", "Implementation approach",
            (f"<p>{e(i_intro)}</p>" if i_intro else "") + (ul(i_list) if i_list else "") + subs(s.get("implementation_subs")))
    if s.get("quality"):
        add("quality", "Data quality", "Data quality and validation", ul(s["quality"], "list checks"))

    results = ""
    if s.get("outcome"):
        results += f'<p class="cs-outcome"><b>{e(s["outcome"])}</b></p>'
    if s.get("value"):
        results += ul(s["value"])
    results += (
        '<p class="not-quantified"><span class="check" aria-hidden="true" style="background-color:#7c8698"></span>'
        '<span><b>Measured impact: not yet quantified.</b> No revenue, time-saving or accuracy figures are claimed. '
        'Company names, real figures and internal rules are withheld.</span></p>'
    )
    if s.get("next"):
        results += f'<p class="cs-next">{e(s["next"])}</p>'
    add("results", "Results", "Results and business impact", results)

    if s.get("insight") or s.get("challenges") or s.get("capabilities"):
        inner = ""
        if s.get("insight"):
            inner += f'<blockquote class="insight"><p>{e(s["insight"])}</p></blockquote>'
        if s.get("challenges"):
            inner += f'<h3 class="cs-sub">What this project taught me</h3>{ul(s["challenges"])}'
        if s.get("capabilities"):
            inner += '<h3 class="cs-sub">Capabilities demonstrated</h3><ul class="tags cs-caps">' + "".join(f"<li>{e(c)}</li>" for c in s["capabilities"]) + "</ul>"
        add("lessons", "Lessons", "Key lessons and capabilities", inner)
    return sec


def render(i, s):
    prev_s = STUDIES[i - 1] if i > 0 else None
    next_s = STUDIES[i + 1] if i < len(STUDIES) - 1 else None
    status_cls = STATUS[s["status"][0]]
    url = f"{SITE}/case-studies/{s['slug']}.html"
    tools = e(", ".join(s["tools"]))
    sections = build_sections(s)

    gh_btn = (
        f'<a class="btn btn-primary" href="{GH}{s["github"]}" target="_blank" rel="noopener">Read the full write-up on GitHub {ICON_EXT}<span class="sr-only"> (opens in a new tab)</span></a>'
        '<a class="btn btn-secondary" href="../index.html#work">All case studies</a>'
    ) if s.get("github") else '<a class="btn btn-secondary" href="../index.html#work">All case studies</a>'

    toc = "".join(f'<li><a href="#{k}">{e(t)}</a></li>' for k, t, _ in sections)
    flow = "".join(f"<li>{e(t)}</li>" for _, t, _ in sections)
    body = "".join(
        f'<section class="cs-step" id="{k}" aria-labelledby="{k}-h" data-reveal>'
        f'<p class="eyebrow"><span class="num">{n:02d}</span> {e(t)}</p>{html}</section>'
        for n, (k, t, html) in enumerate(sections, 1)
    )
    role_row = f'<li><span class="c-label">My role</span><span>{e(s["role"])}</span></li>' if s.get("role") else ""

    pager = '<nav class="cs-pager" aria-label="More case studies">'
    pager += (f'<a href="{prev_s["slug"]}.html"><span class="c-label">← Previous</span><b>{e(prev_s["title"])}</b></a>' if prev_s else "<span></span>")
    pager += (f'<a class="next" href="{next_s["slug"]}.html"><span class="c-label">Next →</span><b>{e(next_s["title"])}</b></a>' if next_s else "")
    pager += "</nav>"

    jsonld = (
        '{"@context":"https://schema.org","@type":"Article",'
        f'"headline":"{e(s["title"])}","description":"{e(s["lede"])}",'
        f'"url":"{url}","image":"{SITE}/assets/og-image.png",'
        '"author":{"@type":"Person","name":"Prekeme Paul Pre-Gee","url":"https://preksg.github.io/"}}'
    )

    return f"""<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(s["title"])} — Prekeme Paul</title>
  <meta name="description" content="{e(s["lede"])}">
  <meta name="theme-color" content="#0a0e13">
  <meta name="color-scheme" content="dark">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Prekeme Paul">
  <meta property="og:title" content="{e(s["title"])}">
  <meta property="og:description" content="{e(s["lede"])}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{SITE}/assets/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{e(s["title"])}">
  <meta name="twitter:description" content="{e(s["lede"])}">
  <meta name="twitter:image" content="{SITE}/assets/og-image.png">
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="../assets/apple-touch-icon.png">
  <script type="application/ld+json">{jsonld}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{FONTS}" rel="stylesheet">
  <link rel="stylesheet" href="../styles.css">
  <script>document.documentElement.classList.add('js');</script>
</head>
<body>
  <a class="skip-link" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="wrap header-inner">
      <a class="brand" href="../index.html" aria-label="Prekeme Paul, home">
        <span class="brand-mark" aria-hidden="true">PP</span>
        <span class="brand-text"><span class="brand-name">Prekeme Paul</span><span class="brand-role">Senior Data Analytics Engineer</span></span>
      </a>
      <nav class="site-nav" id="site-nav" aria-label="Main">
        <ul class="nav-list">
          <li><a href="../index.html#about">Journey</a></li>
          <li><a href="../index.html#work" aria-current="true">Case studies</a></li>
          <li><a href="../index.html#skills">Expertise</a></li>
          <li><a href="../index.html#experience">Experience</a></li>
          <li><a href="../index.html#credentials">Credentials</a></li>
          <li class="nav-cv"><a href="../index.html#contact">Contact</a></li>
        </ul>
      </nav>
      <a class="btn btn-primary btn-small header-cta" href="../index.html#contact">Get in touch</a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav"><span class="bars" aria-hidden="true"></span><span class="sr-only">Menu</span></button>
    </div>
  </header>

  <main id="main">
    <div class="wrap cs-hero">
      <ol class="crumbs" aria-label="Breadcrumb"><li><a href="../index.html">Home</a></li><li><a href="../index.html#work">Case studies</a></li><li aria-current="page">{e(s["short"])}</li></ol>
      <p class="cs-meta"><span class="status {status_cls}">{e(s["status"][1])}</span><span>{e(s["category"])}</span></p>
      <h1>{e(s["title"])}</h1>
      <p class="lede">{e(s["lede"])}</p>
    </div>
    <div class="wrap">
      <figure class="cs-figure">
        <div class="frame"><img src="../assets/illustrations/{s["image"]}" alt="{e(s["alt"])}" width="800" height="450" decoding="async" fetchpriority="high"></div>
        <figcaption>Illustration drawn for this site. It shows the shape of the solution, not a screenshot or figures from company systems.</figcaption>
      </figure>
    </div>

    <div class="wrap cs-layout">
      <aside class="cs-aside" aria-label="Project facts">
        <ul class="cs-facts">
          <li><span class="c-label">Status</span><span>{e(s["status"][1])}</span></li>
          <li><span class="c-label">Sector</span><span>{e(s["domain"])}</span></li>
          <li><span class="c-label">Timeframe</span><span>{e(s["when"])}</span></li>
          {role_row}
          <li><span class="c-label">Technology</span><span>{tools}</span></li>
        </ul>
        <ol class="cs-toc" aria-label="On this page">{toc}</ol>
      </aside>
      <article>
        <ol class="flow" aria-label="Case study structure">{flow}</ol>
        {body}
        <div class="cs-cta">{gh_btn}</div>
        {pager}
      </article>
    </div>
  </main>

  <footer class="site-footer">
    <div class="wrap footer-inner">
      <p>© 2026 Prekeme Paul. Case studies are anonymised; any demonstration data is synthetic.</p>
      <ul class="footer-links">
        <li><a href="https://github.com/PreksG" target="_blank" rel="noopener">GitHub</a></li>
        <li><a href="https://www.linkedin.com/in/prekeme-pre-gee-b-sc-fmva%C2%AE-cpmp-mba-26150796/" target="_blank" rel="noopener">LinkedIn</a></li>
        <li><a href="../index.html">Home</a></li>
      </ul>
    </div>
  </footer>
  <script src="../script.js" defer></script>
</body>
</html>
"""


def render_redirect(old_slug, target_slug, anchor):
    target = next(x for x in STUDIES if x["slug"] == target_slug)
    rel = f"{target_slug}.html#{anchor}"
    return f"""<!doctype html>
<html lang="en-GB">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Moved: {e(target["title"])} — Prekeme Paul</title>
  <meta name="robots" content="noindex">
  <link rel="canonical" href="{SITE}/case-studies/{target_slug}.html">
  <meta http-equiv="refresh" content="0; url={rel}">
</head>
<body>
  <p>This case study is now part of <a href="{rel}">{e(target["title"])}</a>.</p>
</body>
</html>
"""


def main():
    OUT.mkdir(exist_ok=True)
    for i, s in enumerate(STUDIES):
        (OUT / f"{s['slug']}.html").write_text(render(i, s), encoding="utf-8", newline="\n")
        print("wrote", s["slug"])
    for old, (target, anchor) in REDIRECTS.items():
        (OUT / f"{old}.html").write_text(render_redirect(old, target, anchor), encoding="utf-8", newline="\n")
        print("redirect", old, "->", target)


if __name__ == "__main__":
    main()
