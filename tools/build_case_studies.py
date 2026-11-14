"""Generate the static case-study pages in /case-studies.

The site has no build step: the generated HTML is committed. Run this only
after editing the content below, then commit the regenerated pages:

    python tools/build_case_studies.py

Source of truth for every statement here is the matching write-up in
https://github.com/PreksG/analytics-case-studies. Do not add figures,
outcomes or claims that are not in those write-ups.
"""
from html import escape
from pathlib import Path

SITE = "https://preksg.github.io"
GH = "https://github.com/PreksG/analytics-case-studies/tree/main/"
OUT = Path(__file__).resolve().parent.parent / "case-studies"

STATUS = {
    "done": "status-done",
    "partial": "status-partial",
    "recurring": "status-recurring",
}

STUDIES = [
    {
        "slug": "insurance-sales-revenue-pipeline",
        "title": "Insurance Sales-to-Revenue Reconciliation Pipeline",
        "short": "Sales-to-revenue pipeline",
        "lede": "Turning digital policy sales into finance-reconciled revenue data for Life and General Business, from raw source to production.",
        "category": "Data engineering · Revenue reconciliation",
        "status": ("done", "Implemented, in production"),
        "domain": "Insurance",
        "when": "2026",
        "role": "Led delivery: data availability, business rules, review and production deployment",
        "tools": ["PySpark", "Delta Lake", "Microsoft Fabric", "Databricks", "SQL", "Power BI"],
        "image": "sales-revenue-pipeline.svg",
        "alt": "Illustration of the pipeline: Life and General Business sales land in a Bronze layer, pass business rules into a Gold dataset, and are reconciled on counts and premium.",
        "github": "insurance/insurance-sales-revenue-pipeline",
        "problem": (
            "Digital distribution channels created policy-sales activity across different systems and records. Sales and premium were not brought together consistently, so operations, sales and finance could not work from the same numbers.",
            [
                "No single view of digital policy purchases for Life and General Business.",
                "Week-to-week monitoring was inconsistent because extracts used different dates and rules.",
                "Sales records were hard to reconcile with the related premium.",
                "Channel values were recorded under different codes and spellings.",
                "Duplicated, ineligible or stale records could reach reports unnoticed.",
            ],
        ),
        "data": (
            "Policy-sales and transaction data from digital distribution processes. Source systems, table names and field definitions are internal. These questions were agreed before any transformation was built:",
            [
                "Which record represents a completed digital policy purchase?",
                "Is the analytical record at policy, transaction or payment level?",
                "Which authoritative record supplies the premium used in reporting?",
                "Which date places a sale in a week, and from which date is data in scope?",
                "Which control totals validate the output?",
            ],
        ),
        "approach": (
            "Source data → Bronze (raw, as received) → transformation and business rules → Gold (reporting-ready) → reconciliation of counts and premium → weekly sales and revenue analysis",
            [
                "Keep source data traceable in a raw Bronze layer, with origin and load timing preserved.",
                "Apply types, date normalisation, channel mapping, a reporting start date, a positive-premium filter, deduplication and a latest-load check in one place.",
                "Build the sales dataset at an explicit grain, so joining policy activity to premium cannot inflate amounts.",
            ],
        ),
        "implementation": (
            "I led delivery. A data analyst built the transformation and business-rule logic under my supervision, and a senior business stakeholder sponsored the project.",
            [
                "Landed the source data in the raw (Bronze) layer.",
                "Agreed the business rules and kept the end-to-end process on track.",
                "Supervised and reviewed the transformation work that produced the Gold dataset.",
                "Pushed the pipeline to production on Microsoft Fabric and Databricks.",
            ],
        ),
        "validation": [
            "Fields cast to their expected types; business dates parsed and in period.",
            "Only transactions from the agreed start date, and only positive premium.",
            "Duplicates removed on the agreed business key; channels mapped to the agreed list.",
            "Latest transaction date checked, so stale loads are caught.",
            "Joins made at the declared grain to prevent row multiplication.",
            "Record counts and premium totals reconciled before the data is used.",
        ],
        "insight": "A technically successful pipeline is not evidence that reported revenue is correct. The output has to agree with an authoritative control total, using consistent dates, rules and definitions.",
        "value": [
            "One consistent, reporting-ready view of digital policy purchases and premium for Life and General Business.",
            "A single agreed definition of a sale and of premium, instead of conflicting extracts.",
            "Reconciliation built into the pipeline rather than done by hand afterwards.",
            "Earlier detection of duplicate, ineligible and stale records.",
            "A production foundation that other reports can build on.",
        ],
        "next": "Possible next steps, not yet built: a reusable Silver layer, automated reconciliation alerts, a published KPI dictionary, and a synthetic public demonstration.",
    },
    {
        "slug": "high-value-client-ranking",
        "title": "High-Value Client Ranking Pipeline",
        "short": "Client ranking pipeline",
        "lede": "Ranking an insurance group's most valuable clients across its subsidiaries for executive management, and catching the join that multiplied their premiums.",
        "category": "Data engineering · Customer analytics",
        "status": ("partial", "Partially implemented"),
        "domain": "Insurance",
        "when": "2026",
        "role": "Built the ranking pipelines; found and fixed the join fan-out",
        "tools": ["PySpark", "Databricks", "Microsoft Fabric", "Delta Lake", "Power BI", "HTML prototype"],
        "image": "client-ranking.svg",
        "alt": "Illustration: four subsidiaries feed a client-level step guarded by a row-count check, producing a ranked list; an inflated bar from join fan-out is shown as caught.",
        "github": "bi/high-value-client-ranking",
        "problem": (
            "Executive management wanted a clear answer to a simple question: who are our most valuable clients? A multi-line group serves the same clients through several subsidiaries, each with its own records.",
            [
                "No group-wide view: a client with insurance in one subsidiary and investments in another appeared as two unrelated records.",
                "Different measures of value: premium for insurers, assets for the asset manager, plus tenure.",
                "Name-based rules were classifying some clients as individuals or corporates incorrectly.",
                "A one-to-many join to portfolio data multiplied premium totals, exactly at the top of the list where executives look first.",
            ],
        ),
        "data": (
            "Client, policy, premium and portfolio data from four subsidiaries: general insurance, life, health and asset management. Ranking weights and thresholds are internal. The design questions:",
            [
                "Which key identifies a client within each subsidiary, and which shared identifier links them across subsidiaries?",
                "How are individuals and corporates told apart reliably?",
                "Which premium, asset value and start date represent a client's value and tenure?",
                "How many portfolio rows can one client have, and how are they brought to client level before joining?",
            ],
        ),
        "approach": (
            "Subsidiary data → ingestion → cleaning and client-type classification → client-level aggregation (fan-out control) → shared client identifier → ranking on premium, assets and tenure → ranked output → executive reporting",
            [
                "Aggregate to one row per client before any join, so totals cannot multiply.",
                "Correct the client-type classification rules before ranking.",
                "Combine premium, assets and tenure into one fair ranking across subsidiaries.",
            ],
        ),
        "implementation": (
            "Ranking pipelines are built for all four subsidiaries and cover over a thousand clients. The executive Power BI report is specified and prototyped; its build is pending.",
            [
                "Built the ranking pipelines for four subsidiaries in PySpark.",
                "Found and fixed the join fan-out, and added the checks that now catch it.",
                "Corrected the client-type classification rules.",
                "Designed the Gold-layer output and helped create the cross-subsidiary customer table.",
                "Wrote the Power BI build specification and built an interactive HTML prototype.",
            ],
        ),
        "validation": [
            "Grain check: one row per client before ranking.",
            "Join cardinality check: row counts compared before and after each join.",
            "Premium reconciliation: totals after joining equal totals before joining.",
            "Classification check against known individual and corporate clients.",
            "Duplicate check within each subsidiary; unmatched cross-subsidiary clients counted and reviewed.",
            "Key and amount fields cast to their expected types before filtering and joining.",
        ],
        "insight": "A pipeline can run without errors and still produce figures many times too large. Only reconciling totals before and after each join exposes it.",
        "value": [
            "A ranked view of the group's most valuable clients, on correct client-level figures.",
            "A fair ranking combining insurance premium, investment assets and tenure.",
            "Correct individual and corporate segments.",
            "A group-wide client view as a basis for cross-selling and relationship management.",
            "Protection against inflated figures reaching executive reports.",
        ],
        "next": "Still to do: build the executive Power BI report from the approved specification.",
    },
    {
        "slug": "insurance-budgeting-forecasting",
        "title": "Insurance Budgeting, Forecasting & Board Reporting",
        "short": "Budgeting and Board reporting",
        "lede": "Running the planning and performance-reporting cycle of a multi-line insurer, from the annual budget to the Board pack.",
        "category": "Financial planning & analysis · Executive reporting",
        "status": ("recurring", "Recurring, 2022–2024"),
        "domain": "Insurance",
        "when": "April 2022 – December 2024",
        "role": "Lead, Financial Planning & Reporting Analyst",
        "tools": ["Excel", "Prophix", "Power BI", "IFRS 17", "Financial modelling"],
        "image": "fpna-board-reporting.svg",
        "alt": "Illustration with invented shapes: budget and actual bars by period beside a Board pack page listing explained variances.",
        "github": "fpna/insurance-budgeting-forecasting",
        "problem": (
            "An insurance group plans across several businesses, departments and regions. Leadership needs one consistent plan, an early view of where results are heading, and a clear explanation of why actuals differ from plan.",
            [
                "Budgets built in disconnected spreadsheets that are hard to consolidate.",
                "Forecasts updated late or inconsistently across business units.",
                "Variances reported without a clear explanation of what drove them.",
                "Planning that did not line up with the accounting basis, which became critical with IFRS 17.",
                "Manual, repetitive preparation of reporting packs every month.",
            ],
        ),
        "data": (
            "Business-unit budget inputs, general-ledger actuals and enterprise KPIs. The questions the cycle had to answer consistently:",
            [
                "How are business-unit, departmental and regional assumptions collected consistently, and how do they roll up?",
                "Which general-ledger accounts and periods feed the actuals?",
                "How is a variance split into volume, price, timing and one-off effects?",
                "How does the budget template map to the IFRS 17 budget model?",
            ],
        ),
        "approach": (
            "Business-unit inputs → budget template (IFRS 17-aligned) → consolidation in Prophix → rolling forecasts → actuals from the general ledger → variance and scenario analysis → CFO and Board packs and executive dashboard",
            [
                "One template for every unit, aligned to the group's IFRS 17 budget model.",
                "Monthly, quarterly and annual forecasts, each round kept separately so changes can be traced.",
                "Variances explained by driver, with scenarios to support strategic decisions.",
            ],
        ),
        "implementation": (
            "A recurring responsibility rather than a one-off build. Before this role I spent eight years as a financial analyst and payment analyst.",
            [
                "Led the annual budget cycle with business, departmental and regional stakeholders.",
                "Produced monthly, quarterly and annual forecasts, financial models and scenario analyses.",
                "Prepared CFO and Board reporting packs with variance analysis and recommendations.",
                "Built and maintained the CEO / executive dashboard in Power BI.",
                "Led the automation of budgeting and reporting workflows in Prophix, and built the IFRS 17-aligned budget template.",
            ],
        ),
        "validation": [
            "Ledger reconciliation: actuals agree with the general ledger before analysis.",
            "Consolidation check: business-unit budgets add up to the group plan.",
            "Template consistency: every unit plans on the same IFRS 17-aligned template.",
            "Variance completeness: every material variance has an explanation.",
            "Expense and ledger review: unusual postings and trends investigated.",
            "Version control: each forecast round kept separately.",
        ],
        "insight": "Years of reconciling, explaining and defending numbers to a CFO and a Board taught me what decision-makers need from data, and why figures must be right before they are presented.",
        "value": [
            "One consistent group budget aligned with corporate goals.",
            "Regular forecasts that gave leadership an early view of results.",
            "Clear, explained variances in CFO and Board reporting.",
            "Scenario analysis to support strategic decisions.",
            "Less manual effort through Prophix automation, with budgeting kept consistent with IFRS 17.",
        ],
        "next": "",
    },
    {
        "slug": "ai-weekly-management-report",
        "title": "AI-Assisted Weekly Management Intelligence Report",
        "short": "AI weekly management report",
        "lede": "An automated weekly briefing for senior leadership, drafted by AI from six Power BI models, and never sent on stale data.",
        "category": "AI-enabled analytics · Management reporting",
        "status": ("done", "Implemented, weekly in 2026"),
        "domain": "Automotive lending",
        "when": "2026",
        "role": "Designed and built the whole workflow",
        "tools": ["Claude", "Power BI semantic models (XMLA)", "Scheduled task", "HTML email", "KPI dictionary"],
        "image": "ai-management-report.svg",
        "alt": "Illustration: six Power BI models pass a freshness gate; if fresh, an AI assistant drafts a weekly briefing, otherwise the report is held and an alert is sent.",
        "github": "management-intelligence/ai-weekly-management-report",
        "problem": (
            "Senior leadership relied on six separate Power BI reports covering credit, portfolio performance, collections, collections operations, credit decisioning and an executive view. Each answered its own question; none said what mattered across the business this week.",
            [
                "Six reports had to be opened and read separately.",
                "Connections across areas, such as credit decisions feeding collections risk, were not visible in any single report.",
                "Reports described the past; leadership wanted a forward view and recommended actions.",
                "Some measures were not yet validated, so a summary could repeat a wrong number with confidence.",
            ],
        ),
        "data": (
            "Six Power BI semantic models, queried directly. The rules the briefing works from:",
            [
                "Which measure in which model is the agreed source for each KPI?",
                "How is it confirmed that every model has refreshed before analysis?",
                "What is the current position compared with? (The prior month.)",
                "How are measures that may be wrong treated, and how does a reader see where each figure came from?",
            ],
        ),
        "approach": (
            "Six semantic models → model inventory and KPI dictionary → freshness gate → AI analysis across models → structured weekly briefing → HTML email to leadership",
            [
                "Document every model, KPI and cross-model link before asking the AI anything.",
                "Gate on freshness: if a model has not refreshed or a connection fails, nothing is sent and the owner gets a \"not sent\" alert.",
                "Draft a fixed structure: executive summary, scorecard, KPI detail, risks, opportunities, actions and a short CEO brief.",
            ],
        ),
        "implementation": (
            "Ran every Monday after the Power BI models refreshed, on a weekly schedule in 2026.",
            [
                "Inventoried the six semantic models and documented what each measures.",
                "Built the KPI dictionary, the KPI-to-source mapping and the cross-model map.",
                "Wrote the analysis framework and data-quality notes the AI works from.",
                "Set up the AI assistant's access to the models and the weekly schedule.",
                "Designed the freshness gate, the failure alert and the \"Monitored\" treatment for unvalidated measures.",
            ],
        ),
        "validation": [
            "Freshness gate: no report is sent unless every model has refreshed and is reachable.",
            "Single source per KPI, as named in the KPI dictionary.",
            "Suspected mis-scaled measures labelled \"Monitored\", not reported as fact.",
            "Every report lists its sources.",
            "Figures always compared with the prior month.",
        ],
        "insight": "An AI summary is only as trustworthy as the data and rules underneath it. The gate and the KPI dictionary matter more than the writing.",
        "value": [
            "One weekly view across six reports, instead of six separate reads.",
            "A forward-looking briefing with risks, opportunities and recommended actions.",
            "Cross-business connections that no single report showed.",
            "Protection against decisions based on stale data.",
            "A reusable foundation (inventory, KPI dictionary, cross-model map) for future reporting.",
        ],
        "next": "",
    },
    {
        "slug": "dashboard-root-cause-analysis",
        "title": "Dashboard Root-Cause Analysis",
        "short": "Dashboard root-cause analysis",
        "lede": "Finding out why a dashboard's numbers are wrong, and fixing the cause at the right layer, not the symptom in the report.",
        "category": "Business intelligence · Data quality",
        "status": ("done", "Implemented, 2026"),
        "domain": "Automotive lending and insurance",
        "when": "2026",
        "role": "BI analyst and analytics engineer: diagnosis, BI-layer fixes, hand-offs",
        "tools": ["Power BI", "DAX", "Power Query", "BigQuery SQL", "Web analytics"],
        "image": "dashboard-root-cause.svg",
        "alt": "Illustration: a dashboard spike is traced down through report, DAX, data model, warehouse table and source load, with the cause isolated at the warehouse layer.",
        "github": "bi/dashboard-root-cause-analysis",
        "problem": (
            "Business teams relied on Power BI dashboards for sales, lending, operations and compliance. When figures were wrong, trust in every dashboard suffered. The symptoms varied:",
            [
                "Historical data missing from a dashboard.",
                "Several measures returning identical values when they should differ.",
                "Two dashboards disagreeing on the same count.",
                "User counts far higher than the web-analytics source.",
                "A dashboard crashing repeatedly, and a compliance report showing outdated status.",
            ],
        ),
        "data": (
            "Dashboards, their DAX and models, warehouse tables in BigQuery, and independent sources such as web analytics. The questions behind every investigation:",
            [
                "What trusted figure can the dashboard be compared with?",
                "Which tables, views and transformations sit between source and visual?",
                "What does one row represent at each step, and can a join multiply it?",
                "Do upstream tables keep full history, and can loads duplicate rows?",
                "Do filters or earlier fixes change what a measure calculates?",
            ],
        ),
        "approach": (
            "Symptom → reproduce → compare with an independent source → trace lineage layer by layer → isolate the cause → fix at the right layer (or hand off) → verify → explain to stakeholders",
            [
                "Reproduce first, then reconcile the headline figure with a trusted source.",
                "Walk the lineage down one layer at a time until the figure changes.",
                "Fix the cause where it starts, or hand a precise diagnosis to the team that owns that layer.",
            ],
        ),
        "implementation": (
            "A series of investigations in 2026. Most causes are fixed; upstream table rebuilds were carried out by data engineering colleagues using my diagnoses.",
            [
                "Reproduced each problem and found its root cause.",
                "Fixed BI-layer causes directly, including a connector migration and a regional filter.",
                "Wrote root-cause documents and technical bug reports for data engineering.",
                "Drafted stakeholder communications explaining each finding in plain language.",
            ],
        ),
        "validation": [
            "Independent comparison: headline figures reconciled with a trusted source.",
            "Grain check before and after each join; distinct-count check per entity.",
            "History check: upstream tables cover the full reporting period.",
            "Load check: no duplicate rows from appended or chunked loads.",
            "Filter check: measures tested with and without filters, especially after interim fixes.",
            "Source check: system or manual file, and how fresh it is.",
        ],
        "insight": "When a dashboard shows the wrong number, the visible problem is in the report but the cause is usually upstream. Patching the report hides the problem; it does not solve it.",
        "value": [
            "Wrong figures found and explained before they drove decisions.",
            "Fixes made at the cause, so problems did not return.",
            "Clear hand-offs to data engineering, with the evidence needed to act.",
            "Stakeholders kept informed in plain language.",
            "A repeatable approach that speeds up future investigations.",
        ],
        "next": "",
    },
]

ICON_EXT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

STEPS = [
    ("problem", "Problem"),
    ("data", "Data"),
    ("approach", "Approach"),
    ("implementation", "Implementation"),
    ("validation", "Validation"),
    ("insight", "Insight"),
    ("value", "Business value"),
]


def e(text):
    return escape(text, quote=True)


def ul(items, cls="list"):
    return f'<ul class="{cls}">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def render(i, s):
    prev_s = STUDIES[i - 1] if i > 0 else None
    next_s = STUDIES[i + 1] if i < len(STUDIES) - 1 else None
    status_cls = STATUS[s["status"][0]]
    url = f"{SITE}/case-studies/{s['slug']}.html"
    toc = "".join(f'<li><a href="#{k}">{e(t)}</a></li>' for k, t in STEPS)
    flow = "".join(f"<li>{e(t)}</li>" for _, t in STEPS)
    tools = e(", ".join(s["tools"]))

    def step(n, key, title, body):
        return (
            f'<section class="cs-step" id="{key}" aria-labelledby="{key}-h" data-reveal>'
            f'<p class="eyebrow"><span class="num">{n:02d}</span> {e(title)}</p>'
            f"{body}</section>"
        )

    p_intro, p_list = s["problem"]
    d_intro, d_list = s["data"]
    a_line, a_list = s["approach"]
    i_intro, i_list = s["implementation"]

    body = "".join([
        step(1, "problem", "Problem", f'<h2 id="problem-h">The business problem</h2><p>{e(p_intro)}</p>{ul(p_list)}'),
        step(2, "data", "Data", f'<h2 id="data-h">The data and the questions agreed first</h2><p>{e(d_intro)}</p>{ul(d_list)}'),
        step(3, "approach", "Approach", f'<h2 id="approach-h">Approach</h2><p class="pipeline-line">{e(a_line)}</p>{ul(a_list)}'),
        step(4, "implementation", "Implementation", f'<h2 id="implementation-h">What I built, and who did what</h2><p>{e(i_intro)}</p>{ul(i_list)}'),
        step(5, "validation", "Validation", f'<h2 id="validation-h">How the output is checked</h2>{ul(s["validation"], "list checks")}'),
        step(6, "insight", "Insight", f'<h2 id="insight-h" class="sr-only">Insight</h2><blockquote class="insight"><p>{e(s["insight"])}</p></blockquote>'),
        step(7, "value", "Business value", (
            f'<h2 id="value-h">Business value</h2>{ul(s["value"])}'
            '<p class="not-quantified"><span class="check" aria-hidden="true" style="background-color:#7c8698"></span>'
            '<span><b>Measured impact: not yet quantified.</b> No revenue, time-saving or accuracy figures are claimed. '
            'Company names, real figures and internal rules are withheld.</span></p>'
            + (f'<p style="margin-top:1rem;color:var(--muted)">{e(s["next"])}</p>' if s["next"] else "")
            + '<div class="cs-cta">'
            f'<a class="btn btn-primary" href="{GH}{s["github"]}" target="_blank" rel="noopener">Read the full write-up on GitHub {ICON_EXT}<span class="sr-only"> (opens in a new tab)</span></a>'
            '<a class="btn btn-secondary" href="../index.html#work">All case studies</a></div>'
        )),
    ])

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
  <meta name="theme-color" content="#ffffff">
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
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Instrument+Sans:wght@400;500;600;700&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,500&display=swap" rel="stylesheet">
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
          <li><a href="../index.html#about">About</a></li>
          <li><a href="../index.html#work" aria-current="true">Case studies</a></li>
          <li><a href="../index.html#process">Approach</a></li>
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
          <li><span class="c-label">My role</span><span>{e(s["role"])}</span></li>
          <li><span class="c-label">Technology</span><span>{tools}</span></li>
        </ul>
        <ol class="cs-toc" aria-label="On this page">{toc}</ol>
      </aside>
      <article>
        <ol class="flow" aria-label="Case study structure">{flow}</ol>
        {body}
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


def main():
    OUT.mkdir(exist_ok=True)
    for i, s in enumerate(STUDIES):
        (OUT / f"{s['slug']}.html").write_text(render(i, s), encoding="utf-8", newline="\n")
        print("wrote", s["slug"])


if __name__ == "__main__":
    main()
