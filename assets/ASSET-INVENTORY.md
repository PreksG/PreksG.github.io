# Asset inventory

Every image and file the site serves, what it is for, where it came from and its licence. Update this list whenever an asset is added, replaced or removed.

| File | Purpose | Source | Licence / rights |
|---|---|---|---|
| `headshot.jpg` (560×560) | Portrait fallback; JSON-LD `image` | Supplied by Prekeme Paul | Owner's own photograph, used with permission |
| `img/headshot-360.webp`, `img/headshot-560.webp` | Responsive WebP portrait (hero, overview) | Resized from `headshot.jpg` (Pillow, quality 82) | As above |
| `og-image.png` (1200×630) | Open Graph / social sharing preview | Designed for this site from the headshot and site typography; rendered with headless Edge | Owner's own; fonts under SIL Open Font Licence |
| `apple-touch-icon.png` (180×180) | Home-screen icon | Drawn for this site (charcoal tile, green check mark) | Original work |
| `../favicon.svg` | Browser tab icon | Drawn for this site | Original work |
| `illustrations/sales-revenue-pipeline.svg` | Cover: Insurance Sales-to-Revenue Reconciliation Pipeline | Original SVG drawn from the published case study | Original work. **Illustrative, not a screenshot** |
| `illustrations/client-ranking.svg` | Cover: High-Value Client Ranking Pipeline | Original SVG | Original work. **Illustrative; no real figures** |
| `illustrations/fpna-board-reporting.svg` | Cover: Insurance Budgeting, Forecasting & Board Reporting | Original SVG; bar heights are invented shapes | Original work. **Illustrative; no real figures** |
| `illustrations/ai-management-report.svg` | Cover: AI-Assisted Weekly Management Intelligence Report | Original SVG | Original work. **Illustrative, not a screenshot** |
| `illustrations/dashboard-root-cause.svg` | Cover: Dashboard Root-Cause Analysis | Original SVG | Original work. **Illustrative, not a screenshot** |
| `Prekeme-Paul-CV.pdf` | Downloadable CV | Supplied by Prekeme Paul | Owner's own document |

## Fonts

Loaded from Google Fonts, all under the SIL Open Font Licence 1.1: Newsreader (display), Instrument Sans (text), IBM Plex Mono (labels).

## Rules for adding images

- No screenshots, extracts or dashboards from company systems, and no real figures. Use synthetic data and label it.
- Mark conceptual graphics as illustrations on the page (the `cover-label` badge and caption do this).
- Store images in this folder; do not hotlink.
- Prefer SVG for diagrams and WebP (with a JPEG fallback) for photographs. Always set `width`, `height` and descriptive `alt` text, and `loading="lazy"` for anything below the first screen.
- Stock photography: only from a source whose licence permits commercial use without attribution conflicts (for example Unsplash or Pexels), and record the photographer, URL and licence in the table above.
