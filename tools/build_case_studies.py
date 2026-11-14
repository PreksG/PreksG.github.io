"""Generate the static case-study pages in /case-studies.

The site has no build step: the generated HTML is committed. Run this only
after editing the content below, then commit the regenerated pages:

    python tools/build_case_studies.py

Sources of truth: the matching write-up in
https://github.com/PreksG/analytics-case-studies for studies that link one,
and the owner's Databricks / Azure Data Factory project inventory
(November 2026) for the rest. Do not add figures, outcomes or claims that
are not in those sources. Keep studies anonymised: no company, subsidiary,
client or person names, internal system names, or code and file paths.
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
    "prototype": "status-progress",
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
        "tools": ["PySpark", "Delta Lake", "Microsoft Fabric", "Databricks", "Azure Data Factory", "ADLS Gen2", "SQL", "Power BI"],
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
                "Sales made by brokers and agents through the intermediary web portal could not be tied to recognised revenue, because the portal's data sat in separate databases for general and life business.",
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
        "implementation_subs": [
            ("Intermediary portal ingestion (Azure Data Factory)",
             "Two pipelines, one per business line, bring in sales made by brokers and agents through the intermediary web portal:",
             [
                 "General business: a Lookup finds the policy-transactions table in the portal's product-mapping database, and a sequential ForEach copies it to ADLS Gen2. Three Databricks notebooks then land it, promote it to Silver and build the Gold web revenue-realisation output.",
                 "Life business: the table list (products and proposal details) is held as a pipeline variable that maps each source table to its folder. For each table the pipeline deletes the existing file and then copies to Parquet, so reruns never duplicate data. A notebook then ingests it into the landing workspace.",
             ]),
        ],
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
            "Portal sales for both business lines flowing into a Gold revenue-realisation view, with safe reruns.",
        ],
        "next": "Possible next steps, not yet built: a reusable Silver layer for the digital-sales business rules, automated reconciliation alerts, a published KPI dictionary, and a synthetic public demonstration.",
    },
    {
        "slug": "high-value-client-ranking",
        "title": "High-Value Client Ranking Pipeline",
        "short": "Client ranking pipeline",
        "lede": "Ranking a multi-line insurance group's most valuable clients in each business, building one group-wide view of every client's value and cross-sell gaps, and catching the join that multiplied their premiums.",
        "category": "Data engineering · Customer analytics",
        "status": ("partial", "Partially implemented"),
        "domain": "Insurance and asset management",
        "when": "2026",
        "role": "Built the ranking pipelines and the group single view; found and fixed the join fan-out",
        "tools": ["PySpark", "Databricks", "Microsoft Fabric OneLake", "Delta Lake", "Window functions", "Power BI"],
        "image": "client-ranking.svg",
        "alt": "Illustration: four subsidiaries feed a client-level step guarded by a row-count check, producing a ranked list; an inflated bar from join fan-out is shown as caught.",
        "github": "bi/high-value-client-ranking",
        "problem": (
            "Executive management wanted a clear answer to a simple question: who are our most valuable clients? A multi-line group serves the same clients through several subsidiaries, each with its own records.",
            [
                "Each business ranked its own top clients separately. Leadership could not see one client's total value across general insurance, life, health, asset management and pensions, or which of the group's products that client did not hold yet.",
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
            "Ranking pipelines are built for each business and cover over a thousand clients. A group single view on top of them is in build, and the executive Power BI report is specified and prototyped.",
            [
                "Built the ranking pipelines for four subsidiaries in PySpark.",
                "Found and fixed the join fan-out, and added the checks that now catch it.",
                "Corrected the client-type classification rules.",
                "Designed the Gold-layer output and helped create the cross-subsidiary customer table.",
                "Wrote the Power BI build specification and built an interactive HTML prototype.",
            ],
        ),
        "implementation_subs": [
            ("Rankings for each business", None, [
                "General and life insurance: premium taken from general-ledger entries on gross-premium and inward-reinsurance accounts, linked to policy and customer, with claims paid set against it.",
                "Health: family-level premium and covered lives, grouping members on the enrollee ID and falling back to a primary member where none is flagged.",
                "Asset management: inflow, outflow, net value and turnover per client for FY2025 and H1 2026, ranked with tie-breakers so every position is unique.",
            ]),
            ("Group single view (in build)", None, [
                "Keys every client on a phone-based identity ID, with each business's join key chosen by match rate.",
                "Writes three tables: a summary with one row per client (businesses held, value in each, group rank and cross-sell gaps), a detail table for drill-through, and an unlinked table for data-quality follow-up.",
                "Includes a lookup helper that finds any client by phone number.",
            ]),
        ],
        "validation": [
            "Grain check: one row per client before ranking.",
            "Join cardinality check: row counts compared before and after each join.",
            "Premium reconciliation: totals after joining equal totals before joining.",
            "Classification check against known individual and corporate clients.",
            "Duplicate check within each subsidiary; unmatched cross-subsidiary clients counted and reviewed.",
            "Key and amount fields cast to their expected types before filtering and joining.",
            "Duplicate enrollee rows removed before summing health premium, so premium is not inflated.",
            "Policy lookup deduplicated before the group join, so general-ledger lines and claims do not multiply.",
        ],
        "insight": "A pipeline can run without errors and still produce figures many times too large. Only reconciling totals before and after each join exposes it.",
        "outcome": "One CEO-level view of the group's top clients, with each client's cross-sell gaps and a list of high-value records that can't be linked yet.",
        "value": [
            "A ranked view of the group's most valuable clients, on correct client-level figures.",
            "A fair ranking combining insurance premium, investment assets and tenure.",
            "Correct individual and corporate segments.",
            "A group-wide client view as a basis for cross-selling and relationship management.",
            "Protection against inflated figures reaching executive reports.",
        ],
        "next": "Still to do: finish the group single view, and build the executive Power BI report from the approved specification.",
    },
    {
        "slug": "legacy-erp-gl-crosswalk",
        "title": "Legacy-to-ERP GL Crosswalk & Parallel-Run Reconciliation",
        "short": "GL crosswalk",
        "lede": "Proving, line by line, where every legacy general-ledger account and dimension lands in Dynamics 365 F&O, starting from full copies of the legacy ledgers in the data lake.",
        "category": "Data engineering · Finance systems migration",
        "status": ("done", "Implemented"),
        "domain": "Insurance finance",
        "when": "2026",
        "tools": ["PySpark", "Delta Lake", "Microsoft Fabric", "pandas", "Dynamics 365 F&O ledger tables", "Azure Data Factory", "Azure SQL", "SQL Server", "ADLS Gen2"],
        "image": "gl-crosswalk.svg",
        "alt": "Illustration: general and life legacy ledgers are copied to the lake, transactions from the parallel-run month are matched one to one, and each legacy account is mapped to a Dynamics 365 F&O account with a confidence flag.",
        "problem": (
            "Finance moved from a legacy ledger to Dynamics 365 F&O, and every report built on the old general-ledger accounts and dimensions had to switch over.",
            [
                "The official account-mapping file was incomplete.",
                "Dynamics 365 F&O stores dimensions inside a segmented ledger-account string, so old fields had no obvious new home.",
                "Finance reporting needed complete copies of both legacy ledgers (general insurance and life) in the data lake, and the set of tables to copy kept changing.",
            ],
        ),
        "approach_title": "Solution",
        "approach": (
            "Legacy ledgers → full dumps to the lake → profiling of both ledgers → 1:1 transaction matching in the parallel-run month → evidence-based account crosswalk and dimension map",
            None,
        ),
        "approach_subs": [
            ("Before: full legacy-ledger dumps (Azure Data Factory)", "One control-table-driven pipeline per ledger, general and life:", [
                "A control table in Azure SQL lists the tables to dump, and a Lookup reads it at run time.",
                "A ForEach builds a dynamic SQL statement per table, with the table name safely escaped, and copies it from SQL Server.",
                "Each table lands in ADLS Gen2 as a delimited text file named after the table.",
                "Adding or removing a table is a row change in the control table, not a pipeline change. The dumps were archived once incremental loads took over.",
            ]),
            ("After: read-only profiling and crosswalk on Fabric", "Profiling of both ledgers, general and life:", [
                "Kept only the latest version of each F&O journal row.",
                "Profiled the account-segment structure, mapping-file coverage and column fill rates.",
                "Ran value-overlap tests to find which F&O column carries each legacy field.",
                "Matched transactions in the parallel-run month (same document and same amount, unique 1:1 pairs only) to build a legacy GL to F&O main-account crosswalk. Each row has its match share, the runner-up account and a confidence flag showing whether it agrees with the official mapping file.",
                "Built a dimension value map (for example, class of business) and compared monthly totals per account across the two systems.",
            ]),
        ],
        "outcome": "A GL crosswalk proven line by line, plus a dimension map, so the switchover rested on tested evidence rather than the mapping file alone.",
        "value": [
            "Full legacy-ledger history in the lake: the source for the Silver general-ledger tables behind this crosswalk and behind the group client view's premium by client.",
        ],
    },
    {
        "slug": "weekly-production-vs-budget",
        "title": "Weekly & YTD Production vs Budget Pipeline",
        "short": "Production vs budget",
        "lede": "Replacing a hand-compiled weekly report with a pipeline that sets general-insurance retail production against budget for the week, month and year to date.",
        "category": "BI and reporting · FP&A",
        "status": ("done", "Implemented"),
        "domain": "General insurance",
        "when": "2026",
        "tools": ["PySpark", "Delta Lake", "Microsoft Fabric", "Excel", "Power BI"],
        "image": "production-vs-budget.svg",
        "alt": "Illustration with invented shapes: weekly actual and budget bars on a Friday-to-Thursday calendar, beside a summary of week, month and year-to-date actual against budget by channel.",
        "problem": (
            "Weekly retail production against budget was compiled by hand.",
            [
                "The Excel budget was monthly.",
                "It did not line up with the business's Friday-to-Thursday reporting week.",
            ],
        ),
        "approach_title": "Solution",
        "approach": (
            "A 10-step PySpark pipeline: sales fact table → retail and channel filters → Excel budget → Friday–Thursday calendar → prorated budget → week, month and YTD actuals → validation → output table",
            [
                "Loads the sales fact table, keeps general-business retail using channel logic, and sets the report date from how fresh the source data is.",
                "Parses the Excel budget: finds column positions, merges alternative channels and rolls monthly figures up to full year by channel.",
                "Builds a Friday-to-Thursday reporting calendar and prorates the budget onto it.",
                "Aggregates actuals for the week, month and year to date, adds a total row, runs validation checks and writes the result to a table.",
            ],
        ),
        "outcome": "Week, month and YTD actual vs budget by channel, with data-freshness and validation checks built in.",
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
    {
        "slug": "customer-segmentation-kmeans",
        "title": "Customer Segmentation (K-Means)",
        "short": "Customer segmentation",
        "lede": "Building a clean demographic feature set and clustering customers with K-Means, to give marketing defined customer segments.",
        "category": "AI and machine learning · Customer analytics",
        "status": ("partial", "Partially implemented"),
        "domain": "Insurance",
        "when": "2025–2026",
        "tools": ["PySpark MLlib", "Databricks", "Microsoft Fabric", "Plotly", "matplotlib"],
        "image": "customer-segmentation.svg",
        "alt": "Illustration with invented points: customers plotted in four colour-coded clusters, beside a small chart used to choose the number of clusters.",
        "problem": (
            "Marketing had no defined customer segments.",
            ["Demographic fields were inconsistent across the core systems."],
        ),
        "approach_title": "Solution",
        "approach": (
            "Unified customer table → demographic features → encode and scale → K-Means across a range of k → choose k → profile each cluster",
            [
                "Built a demographic feature set from the unified customer table: age from date of birth, age bands, life stage, gender, marital status and location, with blanks standardised to \"Unknown\".",
                "Encoded and scaled the features with StringIndexer, VectorAssembler and StandardScaler.",
                "Ran K-Means across a range of k, chose k using the silhouette score with a within-cluster sum of squares (elbow) check, then profiled each cluster.",
            ],
        ),
        "next": "The resulting segments and how marketing uses them are not yet written up.",
    },
    {
        "slug": "motor-claims-forecasting",
        "title": "Motor Claims Forecasting",
        "short": "Motor claims forecasting",
        "lede": "A seasonal monthly forecast of motor claims, built on ten years of claims history, to give planning a forward view.",
        "category": "AI and machine learning · Forecasting",
        "status": ("prototype", "Prototype"),
        "domain": "General insurance",
        "when": "2025–2026",
        "tools": ["PySpark", "Prophet", "Plotly", "Databricks", "Microsoft Fabric"],
        "image": "motor-claims-forecast.svg",
        "alt": "Illustration with an invented line: monthly motor claims history with a seasonal pattern, continued by a dashed forecast line.",
        "problem": (
            "Motor claims were planned from prior-year totals, with no forward monthly view.",
            None,
        ),
        "approach_title": "Solution",
        "approach": (
            "10 years of claims → branch and product added → monthly totals → lag features and moving average → Prophet with yearly seasonality → monthly forecast",
            [
                "Pulled 10 years of claims transactions from the policy-admin system and added branch and product.",
                "Aggregated claim amounts monthly and added 1–3-month lag features and a 3-month moving average.",
                "Fitted a Prophet model with yearly seasonality, and built trend views by product.",
            ],
        ),
        "outcome": "A seasonal monthly forecast of motor claims.",
    },
    {
        "slug": "customer-onboarding-feeds",
        "title": "Customer Onboarding Feeds for CX",
        "short": "Customer onboarding feeds",
        "lede": "Automated feeds of newly onboarded general and life insurance customers, behind the customer-experience team's welcome journeys and dashboard.",
        "category": "Data engineering · BI and reporting",
        "status": ("done", "Implemented"),
        "domain": "Insurance",
        "when": "2026",
        "tools": ["PySpark", "Microsoft Fabric", "Power BI"],
        "image": "onboarding-feeds.svg",
        "alt": "Illustration: general and life policy-admin systems each feed a list of new customers into the Gold layer, which supplies the customer-experience dashboard.",
        "problem": (
            "The customer-experience team needed a reliable list of newly onboarded customers in general and life insurance for welcome journeys.",
            ["The data sat in two separate policy-admin systems."],
        ),
        "approach_title": "Solution",
        "approach": (
            "General and life policy-admin data → new-customer feeds → Gold layer (Parquet) → CX Power BI dashboard",
            None,
        ),
        "approach_subs": [
            ("General insurance", None, [
                "Client master joined to the policy register.",
                "New clients since January, with each client's policy count and policy list.",
            ]),
            ("Life", None, [
                "Client table excluding a foreign-currency entity, filtered on policy status.",
                "Group and corporate product codes left out, then joined to policies.",
            ]),
            ("Delivery", None, [
                "Both feeds write to the Gold layer as Parquet, feeding the CX Power BI dashboard.",
            ]),
        ],
        "outcome": "Automated onboarding feeds behind the published CX dashboard, replacing manual extracts.",
    },
    {
        "slug": "cross-sell-ecosystem-analytics",
        "title": "Cross-Sell & Customer Ecosystem Analytics",
        "short": "Cross-sell analytics",
        "lede": "One reusable query pattern on a unified customer model, answering who holds what across the group and who to approach next.",
        "category": "BI and reporting · Customer analytics",
        "status": ("recurring", "Recurring, 2025–2026"),
        "domain": "Insurance and financial services",
        "when": "2025–2026",
        "tools": ["PySpark", "Microsoft Fabric", "Databricks"],
        "image": "cross-sell-ecosystem.svg",
        "alt": "Illustration: one customer at the centre linked to the group's products, with held products shown as solid links and cross-sell gaps as dashed links.",
        "problem": (
            "Sales, partnerships, audit and leadership kept asking the same kind of question: who holds what across the group, and who should we approach next?",
            None,
        ),
        "approach_title": "Solution",
        "approach": (
            "Customer + policy + production + transactions → client-type classifier → active-policy and value-band filters → target lists",
            [
                "A reusable query pattern on the unified customer Gold layer that joins customer, policy, production and transactions.",
                "A keyword-based classifier separates corporate from individual clients.",
                "Active-policy filters and transaction-value bands.",
                "Finds multi-policy holders, savings customers without motor cover, householder customers, and retail clients above 1m premium, with a choice of premium basis (written or paid).",
                "Branch-level lists for a mortgage partnership, and staff-to-customer matching on the golden record.",
            ],
        ),
        "outcome": "Campaign, partnership and audit lists turned around from one consistent customer model rather than one-off extracts.",
    },
    {
        "slug": "annuitant-biometrics-replication",
        "title": "Annuitant Biometrics Database Replication",
        "short": "Annuitant database replication",
        "lede": "A metadata-driven Azure Data Factory pipeline that copies every table of an on-premises application database into the lakehouse, picking up new tables automatically.",
        "category": "Data engineering · Ingestion",
        "status": ("done", "Implemented"),
        "domain": "Pensions and annuities",
        "when": "2026",
        "tools": ["Azure Data Factory", "On-premises SQL Server", "ADLS Gen2 (Parquet)", "Azure Databricks", "Microsoft Fabric"],
        "image": "database-replication.svg",
        "alt": "Illustration: an on-premises SQL Server database, a lookup that discovers its tables, a loop that copies each table to Parquet in ADLS Gen2, and a load into Microsoft Fabric.",
        "problem": (
            "The annuitant biometrics application kept its data in an on-premises SQL Server database, out of reach of the analytics platform.",
            ["Its tables changed over time, so a hand-maintained table list would keep breaking."],
        ),
        "approach_title": "Solution",
        "approach": (
            "Master pipeline: application tables → background-job tables → push to Fabric",
            [
                "Application schema: a Lookup reads the current table list from the database's system catalogue, and a ForEach copies every table from the on-premises SQL Server to Parquet in ADLS Gen2, one file per table.",
                "Background-job schema: the same discover-then-copy pattern for the application's job-scheduler tables.",
                "Push to Fabric: a Databricks notebook loads the landed files into the Fabric workspaces.",
                "Because tables are discovered at run time, new tables are picked up without changing the pipeline.",
            ],
        ),
        "outcome": "The annuitant data refreshed on schedule into the lakehouse with no manual table upkeep.",
    },
    {
        "slug": "digital-quote-platform-ingestion",
        "title": "Digital Quote Platform Ingestion",
        "short": "Digital quote ingestion",
        "lede": "Landing the group's digital quoting data in the lakehouse, so quote volumes and conversion can be analysed.",
        "category": "Data engineering · Ingestion",
        "status": ("done", "Implemented"),
        "domain": "Insurance (digital sales)",
        "when": "2026",
        "tools": ["Azure Data Factory", "SQL Server", "ADLS Gen2", "Azure Databricks", "Microsoft Fabric"],
        "image": "quote-ingestion.svg",
        "alt": "Illustration: five tables from a digital quoting app's database are found by a lookup, copied one by one to ADLS Gen2, and promoted to the Silver layer.",
        "problem": (
            "Quotes from the group's digital quoting app sat in the app's SQL database, so nobody could analyse quote volumes or conversion.",
            ["Five tables were in scope: the product list, quotes, quoting clients, and vehicle and travel quotes."],
        ),
        "approach_title": "Solution",
        "approach": (None, None),
        "approach_subs": [
            ("Version 1", None, [
                "A single Copy activity moved the vehicle-quote table from SQL Server to ADLS Gen2 as delimited text.",
            ]),
            ("Version 2: multi-table load", None, [
                "A Lookup on the database's information schema returns the five in-scope tables.",
                "A ForEach copies each table to ADLS Gen2.",
                "Two Databricks notebooks then promote the data from the landing workspace to the Silver workspace.",
            ]),
        ],
        "outcome": "Quote data landed and cleaned in Silver, ready for quote-to-policy reporting.",
        "next": "The pipeline has since been archived.",
    },
]

ICON_EXT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def e(text):
    return escape(text, quote=True)


def ul(items, cls="list"):
    return f'<ul class="{cls}">' + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def render(i, s):
    prev_s = STUDIES[i - 1] if i > 0 else None
    next_s = STUDIES[i + 1] if i < len(STUDIES) - 1 else None
    status_cls = STATUS[s["status"][0]]
    url = f"{SITE}/case-studies/{s['slug']}.html"
    tools = e(", ".join(s["tools"]))

    def subs(blocks):
        # Optional sub-steps inside a section: [(heading, intro, [items]), ...]
        out = ""
        for heading, intro, items in blocks or []:
            out += f'<h3 class="cs-sub">{e(heading)}</h3>'
            if intro:
                out += f"<p>{e(intro)}</p>"
            if items:
                out += ul(items)
        return out

    # Sections are optional: pages built from shorter source notes show only
    # what the source supports (Problem, Approach/Solution, Business value).
    sections = []
    p_intro, p_list = s["problem"]
    sections.append(("problem", "Problem", f'<h2 id="problem-h">The business problem</h2><p>{e(p_intro)}</p>{ul(p_list) if p_list else ""}'))
    if s.get("data"):
        d_intro, d_list = s["data"]
        sections.append(("data", "Data", f'<h2 id="data-h">The data and the questions agreed first</h2><p>{e(d_intro)}</p>{ul(d_list)}'))
    a_line, a_list = s["approach"]
    a_title = s.get("approach_title", "Approach")
    sections.append(("approach", a_title, (
        f'<h2 id="approach-h">{e(a_title)}</h2>'
        + (f'<p class="pipeline-line">{e(a_line)}</p>' if a_line else "")
        + (ul(a_list) if a_list else "")
        + subs(s.get("approach_subs"))
    )))
    if s.get("implementation"):
        i_intro, i_list = s["implementation"]
        sections.append(("implementation", "Implementation", f'<h2 id="implementation-h">What I built, and who did what</h2><p>{e(i_intro)}</p>{ul(i_list)}{subs(s.get("implementation_subs"))}'))
    if s.get("validation"):
        sections.append(("validation", "Validation", f'<h2 id="validation-h">How the output is checked</h2>{ul(s["validation"], "list checks")}'))
    if s.get("insight"):
        sections.append(("insight", "Insight", f'<h2 id="insight-h" class="sr-only">Insight</h2><blockquote class="insight"><p>{e(s["insight"])}</p></blockquote>'))
    value_body = ul(s["value"]) if s.get("value") else ""
    if s.get("outcome"):
        value_body = f'<p class="cs-outcome"><b>{e(s["outcome"])}</b></p>' + value_body
    gh_btn = (
        f'<a class="btn btn-primary" href="{GH}{s["github"]}" target="_blank" rel="noopener">Read the full write-up on GitHub {ICON_EXT}<span class="sr-only"> (opens in a new tab)</span></a>'
        '<a class="btn btn-secondary" href="../index.html#work">All case studies</a>'
    ) if s.get("github") else '<a class="btn btn-secondary" href="../index.html#work">All case studies</a>'
    sections.append(("value", "Business value", (
        f'<h2 id="value-h">Business value</h2>{value_body}'
        '<p class="not-quantified"><span class="check" aria-hidden="true" style="background-color:#7c8698"></span>'
        '<span><b>Measured impact: not yet quantified.</b> No revenue, time-saving or accuracy figures are claimed. '
        'Company names, real figures and internal rules are withheld.</span></p>'
        + (f'<p style="margin-top:1rem;color:var(--muted)">{e(s["next"])}</p>' if s.get("next") else "")
        + f'<div class="cs-cta">{gh_btn}</div>'
    )))

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
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&amp;family=Instrument+Sans:wght@400;500;600;700&amp;family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;1,6..72,500&amp;display=swap" rel="stylesheet">
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
          {role_row}
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
