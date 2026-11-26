# Prime rib price board (`/prime-rib-price/`)

Holiday-themed market price page plus a reusable scrolling ticker. Every figure is read from a published source and shown with its source name, link and as-of date. Nothing is estimated.

## Files

- `scripts/update_prime_rib.py` reads the sources and writes `data/prime_rib.json`.
- `data/prime_rib_ranches.json` lists the directory ranches whose own Shopify product feed is checked for a rib roast (slug, shop URL, product handle).
- `build.py` (`build_prime_rib_page`, `prime_rib_ticker`, `prime_rib_home_banner`) renders `/prime-rib-price/` and the homepage ticker. The ticker and the cross-links (site footer, deals page, listings index, state/breed hubs, ranch pages with a rib roast in stock, Wagyu vs Akaushi guide) only show Nov 15 – Dec 31 (`prime_rib_season_active()`); the page itself stays up all year.
- SEO: `build_prime_rib_page` sets the title, meta description, canonical, OG/Twitter tags (card at `social/prime-rib/prime-rib-og-1200x630.png`) and four JSON-LD blocks (WebPage, BreadcrumbList, Dataset, FAQPage). Figures in the title, description and FAQ come from `data/prime_rib.json`, so they update on rebuild.
- Social card images for posts live in `social/prime-rib/` (1200x630, 1080x1350, 1080x1920).
- Styles: the `.pr-*` block at the end of `css/site.css`. Snowfall, ticker scroll and garland respect `prefers-reduced-motion`.

## Sources

| Block | Source | Notes |
| --- | --- | --- |
| Retail (headline, by grade, by region) | USDA AMS My Market News slug 3228, "Weekly Grocery Store Beef Feature Activity" (formerly National Retail Report - Beef), `https://www.ams.usda.gov/mnreports/ams_3228.pdf` | Advertised prices, weekly. The PDF URL is lowercase `ams_` (the uppercase form 500s). |
| Wholesale, Choice | USDA AMS LM_XB403 National Daily Boxed Beef Cutout, slug 2453 | IMPS 109E rib, ribeye, lip-on, bone-in, and Primal Rib; prices are $/cwt, divided by 100 for $/lb. |
| Wholesale, Prime | USDA AMS LM_XB456 National Weekly Boxed Beef Cuts for Prime Product, slug 2460 | Weekly. |
| Ranch-direct | Each ranch's `/products/<handle>.js` | $/lb only when the weight is in the variant title, or in text the config quotes and the page still contains. Otherwise left blank. |

## Refreshing

```
python3 scripts/update_prime_rib.py     # needs pdftotext (poppler-utils); ~1-2 min, polite delays between ranch shops
python3 build.py
```

If a source fails to load or parse, that block keeps its previous values and as-of date, and the failure is listed in `errors` inside `data/prime_rib.json` (the script exits 1). The page then shows the old date rather than a fresh-looking one. If the retail report is more than 10 days old the page shows a stale notice.

Sanity check built into the data: the regional bone-in rows' store counts add up to the national store count (11,266 on the Nov 20, 2026 report).

## Adding a ranch

Add an entry to `data/prime_rib_ranches.json`. Use `weights` (quoted weight text per variant) or `stated_per_lb` (quoted price-per-lb text) when the weight is not in the variant title. The quoted `text` must appear verbatim on the product page or the per-lb figure is dropped.
