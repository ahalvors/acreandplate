# Adding a News Item

This guide explains how to add a news update to the Acre & Plate news feed.

## Overview

News items are stored in `data/news.json` and displayed at `/news/` with automatic grouping by day and time (e.g., "Monday afternoon").

## News Schema

Each news item in `data/news.json` has these fields:

```json
{
  "id": "unique-slug",
  "published_at": "2026-09-12T14:30:00-07:00",
  "headline": "Concise headline (8-12 words)",
  "body": "<p>HTML paragraph content with optional <a href=\"/path/\">inline links</a>.</p><p>Multiple paragraphs supported.</p>",
  "icon": "🐂",
  "tags": ["optional", "tags"]
}
```

### Field Details

- **id**: Unique slug identifier (lowercase, hyphens)
- **published_at**: ISO 8601 timestamp with Pacific timezone offset (`-07:00` for PDT, `-08:00` for PST)
- **headline**: Brief, descriptive headline (appears with icon in card header)
- **body**: HTML content using `<p>` tags for paragraphs; use `<a href="">` for inline links (styled in blue)
- **icon**: Single emoji or path to icon image (appears beside headline)
- **image** (optional): Full URL or path to image (displays full-width below body)
- **tags** (optional): Array of tags for categorization

## Content Guidelines

### What to Post

News items should cover **real, verifiable Acre & Plate progress** or **cited cattle/beef market news**:

**Directory Updates:**
- New ranch listings added to the directory
- New features or sections launched (markets, deals, guides)
- Directory milestones (ranch count, geographic coverage)
- Significant updates to existing features

**Cattle Market Briefs:**
- Cattle futures, cash markets, or boxed beef price movements
- USDA reports (WASDE, cattle inventory, beef production forecasts)
- Feed grain markets as they relate to cattle costs
- Industry trends affecting ranch-direct supply or pricing

**Important for market briefs:**
- Always cite public sources with inline `<a href>` links (USDA, CME, IndexBox, trade press)
- Never copy paywalled articles verbatim—write original summaries citing the facts
- Never invent CME futures prices, USDA data, or wholesale beef cutout values
- Include one sentence connecting the news to ranch-direct buyers (feed costs, supply, etc.)

### What NOT to Post

- Invented market data or futures prices (unless cited from public sources like USDA/CME with links)
- Speculative content or projections without attribution
- Individual ranch news (direct customers to ranch websites)
- Personal opinions or commentary
- Verbatim copies of paywalled articles (write original summaries citing facts)

### Tone & Style

- **Factual and direct**: State what happened, when, and why it matters
- **User-focused**: Explain how the update helps customers find ranch-direct beef
- **Links**: Include inline links to relevant sections (`/markets/`, `/deals/`, `/listings/`)
- **Brevity**: 2-4 short paragraphs per item

## Adding a News Item

### 1. Edit data/news.json

Open `data/news.json` and add your entry to the `news` array:

```json
{
  "news": [
    {
      "id": "new-feature-launch",
      "published_at": "2026-09-15T10:30:00-07:00",
      "headline": "New feature makes finding local ranches easier",
      "body": "<p>We've launched a <a href=\"/state-filter/\">state filter</a> making it simple to find ranches near you. Browse by California, Texas, Wyoming, and more.</p><p>The directory now groups ranches by state with shipping details clearly noted. Local pickup options are highlighted for customers who prefer to visit ranch properties.</p>",
      "icon": "🗺️",
      "tags": ["launch", "features"]
    },
    // ... existing items
  ]
}
```

**Note on dates**: The feed groups items by day and time automatically. Use Pacific timezone timestamps. Items are sorted newest-first.

### 2. Validate JSON

Run Python's JSON validator to catch syntax errors:

```bash
python3 -m json.tool data/news.json > /dev/null && echo "JSON is valid"
```

If you see errors, check for:
- Missing or extra commas
- Unescaped quotes in HTML (use `\"` inside JSON strings)
- Unclosed brackets or braces

### 3. Rebuild the site

```bash
python3 build.py
```

This regenerates `/news/index.html` with your new item.

### 4. Preview locally

```bash
python3 -m http.server 8000
open http://localhost:8000/news/
```

Check:
- Day-part grouping label appears correctly ("Thursday morning", etc.)
- Icon displays beside headline
- Inline links are styled in blue
- Content is readable on mobile and desktop

### 5. Commit and deploy

```bash
git add data/news.json
git commit -m "Add news: [headline]"
git push
```

Netlify auto-deploys on push to `main`.

## Optional: Adding Images

To add an image to a news item:

1. Place the image in `/assets/news/` (create folder if needed)
2. Add the `image` field to your news item:

```json
{
  "id": "feature-with-image",
  "published_at": "2026-09-15T14:00:00-07:00",
  "headline": "Visual guide to ranch directory",
  "body": "<p>See how to find ranches by breed, state, and shipping options.</p>",
  "icon": "📸",
  "image": "/assets/news/directory-screenshot.jpg"
}
```

The image displays full-width below the body text.

## Troubleshooting

**Build fails with JSON error**:
- Run `python3 -m json.tool data/news.json` to identify syntax issues
- Check for smart quotes (`"` instead of `"`) in headlines or body content
- Ensure commas separate array items (but no trailing comma after last item)

**Day label doesn't match expected time**:
- Verify your `published_at` timestamp includes timezone offset (`-07:00`)
- Timestamp uses the hour to determine "morning" (5-11), "afternoon" (12-16), "evening" (17-20), "night" (21-4)

**Icon doesn't display**:
- Use a single emoji character (most common emojis work)
- Alternatively, provide a path to an image file

## Examples

### Simple announcement

```json
{
  "id": "wyoming-ranches-added",
  "published_at": "2026-09-18T09:00:00-07:00",
  "headline": "Wyoming ranches join the directory",
  "body": "<p>Three new <a href=\"/wyoming/\">Wyoming ranches</a> are now listed, bringing Greater Yellowstone Wagyu and heritage beef to the directory. All three offer nationwide shipping.</p>",
  "icon": "🏔️",
  "tags": ["wyoming", "new-listings"]
}
```

### Multi-paragraph with external link

```json
{
  "id": "usda-beef-report",
  "published_at": "2026-09-20T14:30:00-07:00",
  "headline": "USDA reports record demand for grass-fed beef",
  "body": "<p>The USDA's <a href=\"https://www.ams.usda.gov/reports/\" target=\"_blank\" rel=\"noopener\">latest market report</a> shows a 23% year-over-year increase in grass-fed beef sales, with ranch-direct channels leading growth.</p><p>This aligns with what we're seeing on Acre & Plate: more ranches reporting sold-out inventory and longer lead times for quarter-cow shares. The directory now lists 20 ranches, with half offering waitlist signups for popular cuts.</p>",
  "icon": "📊",
  "tags": ["market-data", "usda"],
  "source_url": "https://www.ams.usda.gov/reports/",
  "source_name": "USDA Agricultural Marketing Service"
}
```

### Cattle market brief with cited sources

```json
{
  "id": "cattle-futures-firm-sept-15",
  "published_at": "2026-09-15T16:30:00-07:00",
  "headline": "Cattle futures push higher as corn digests WASDE",
  "body": "<p>Live cattle futures rallied to start the week, with cash trade firming to around <a href=\"https://www.agricultureofamerica.com/2026/09/15/cattle-rally-builds-momentum-as-grains-digest-wasde-hogs-and-dairy-stay-under-pressure/\" target=\"_blank\" rel=\"noopener\">$222 in the North and $226 in the South</a> according to analysts on Monday. The rally follows a technical breakout from a declining wedge pattern earlier this month.</p><p>Wholesale beef values held steady, with USDA boxed beef cutouts showing <a href=\"https://www.indexbox.io/blog/usda-boxed-beef-cutout-report-choice-values-above-select-on-september-15-2026/\" target=\"_blank\" rel=\"noopener\">Choice at $376.08 and Select at $356.36</a> per hundredweight on September 15.</p><p>For ranch-direct buyers, the firming cash market reflects tighter cattle supply heading into fall. Corn futures settled into a post-WASDE holding pattern after Friday's yield cut, which could ease feed costs for ranchers finishing cattle on grain.</p>",
  "icon": "📈",
  "tags": ["cattle-markets", "futures", "prices"]
}
```

**Key points for market briefs:**
- Cite every data point with inline links to public sources (USDA AMS, Agriculture of America, CME, IndexBox, etc.)
- Write original summaries—never copy paywalled articles verbatim
- Never invent futures prices, cash cattle values, or USDA data
- Include connection to ranch-direct buyers (feed costs, supply, pricing context)
- Use `target="_blank" rel="noopener"` for external links

---

**Questions?** Open an issue on GitHub or email hello@acreandplate.com.
