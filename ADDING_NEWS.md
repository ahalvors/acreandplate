# Adding News Stories to Acre & Plate

This guide explains how to add news stories to the Cattle News section of Acre & Plate.

## Quick Start

1. Edit `/data/news.json`
2. Add a new entry to the `news` array
3. Run `python3 build.py` to rebuild the site
4. Test the story page at `/news/<id>/`

## News Item Structure

Each news item in `/data/news.json` requires these fields:

```json
{
  "id": "unique-slug-here",
  "published_at": "2026-09-15T16:30:00-07:00",
  "headline": "Story headline goes here",
  "body": "<p>Story body with HTML...</p>",
  "icon": "📈",
  "tags": ["tag1", "tag2"]
}
```

### Required Fields

- **`id`** (string): Unique identifier, used in URL (`/news/<id>/`). Use lowercase with hyphens, e.g., `cattle-futures-firm-sept-15`
- **`published_at`** (ISO 8601 datetime): Publication timestamp with timezone, e.g., `2026-09-15T16:30:00-07:00`
- **`headline`** (string): Story headline (appears in `<h3>` and OG tags)
- **`body`** (HTML string): Full story content with HTML markup
- **`icon`** (string): Emoji or icon for the story (appears next to headline)
- **`tags`** (array of strings): Categories/keywords for filtering (not currently displayed)

### Optional Fields

- **`image`** (string): Path or URL to a story image. Shows in the story card and used for Open Graph previews
  - Can be absolute URL: `"https://example.com/image.jpg"`
  - Or site path: `"/assets/news/story-image.jpg"`
  - Recommended size: 1200×630 pixels minimum
  
- **`og_image`** (string): Override image specifically for Open Graph/social previews
  - Falls back to `image` if not set
  - Falls back to default branded image if neither is set

## Adding Images to News Stories

### Option 1: External Images (Easiest)

Use a direct URL to an image hosted elsewhere:

```json
{
  "id": "cattle-rally-sept-15",
  "headline": "Cattle futures rally continues",
  "body": "<p>Story content...</p>",
  "image": "https://example.com/cattle-chart.jpg",
  "icon": "📈",
  "published_at": "2026-09-15T10:00:00-07:00",
  "tags": ["markets"]
}
```

### Option 2: Local Images (Better)

1. Save the image to `/assets/news/` (create the directory if needed)
2. Use a site-rooted path in the JSON:

```json
{
  "id": "ranch-feature-sept-20",
  "headline": "Featured Ranch: Texas Wagyu Co.",
  "body": "<p>Story content...</p>",
  "image": "/assets/news/texas-wagyu-ranch.jpg",
  "icon": "🐂",
  "published_at": "2026-09-20T14:00:00-07:00",
  "tags": ["ranches", "texas"]
}
```

### Image Guidelines

- **Format:** JPEG or PNG
- **Dimensions:** At least 1200×630 pixels (Open Graph standard)
- **File size:** Keep under 500KB for fast loading
- **Content:** Relevant to the story; should work in small previews

### Stories Without Images

Stories without an `image` field will use the default branded Open Graph image (`/assets/og-news-default.png`). This is fine for most text-based news updates.

## Open Graph Preview Behavior

When someone shares a news story link:

- **Headline** → `og:title` and Twitter card title
- **Plain-text excerpt** (first ~155 chars of body) → `og:description`
- **Image** → `og:image` (custom image, or falls back to default)
- **URL** → `https://acreandplate.com/news/<id>/`

Test previews with:
- [Facebook Sharing Debugger](https://developers.facebook.com/tools/debug/)
- [Twitter Card Validator](https://cards-dev.twitter.com/validator)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)

## HTML in Story Body

The `body` field accepts HTML. Common patterns:

```html
<p>Paragraph text with <a href="https://example.com" target="_blank" rel="noopener">a link</a>.</p>
<p><strong>Bold text</strong> and <em>italic text</em>.</p>
<ul>
  <li>Bullet point one</li>
  <li>Bullet point two</li>
</ul>
```

Keep it simple: paragraphs, links, bold/italic, lists. Avoid complex styling.

## Date/Time Format

Use ISO 8601 with timezone:

```
2026-09-15T16:30:00-07:00
         ↑   ↑   ↑    ↑
       date time mins timezone (PDT = -07:00)
```

Pacific times:
- **PDT** (summer): `-07:00`
- **PST** (winter): `-08:00`

## Icon Selection

Choose an emoji that fits the story:

- 📈 Market/price movements
- 🐂 Cattle/ranch stories
- 💰 Deals/pricing
- 🏪 Markets/butchers
- 🗺️ Geography/locations
- 📰 General news
- ⚠️ Warnings/important notices

## Example: Complete News Item with Image

```json
{
  "id": "usda-beef-report-oct-2026",
  "published_at": "2026-10-12T09:00:00-07:00",
  "headline": "USDA reports record beef exports in Q3",
  "body": "<p>The USDA released its quarterly beef export data today, showing <strong>record exports</strong> for Q3 2026. Total beef shipments reached 780 million pounds, up 12% year-over-year.</p><p>Key markets driving growth include <a href=\"https://example.com\" target=\"_blank\" rel=\"noopener\">Japan and South Korea</a>, which increased purchases of high-quality U.S. beef.</p><p>For ranch-direct sellers, this signals continued strong demand for premium domestic beef as international buyers compete for supply.</p>",
  "image": "/assets/news/usda-beef-exports-chart.jpg",
  "icon": "📈",
  "tags": ["usda", "exports", "markets"]
}
```

## Testing

After editing `data/news.json`:

1. Run the build script:
   ```bash
   python3 build.py
   ```

2. Check the news hub: `/news/index.html`
   - Headline should link to the story page
   - Story appears in chronological order

3. Check the story page: `/news/<id>/index.html`
   - Full content displays
   - Share button works
   - View source to confirm OG tags

4. Test Open Graph preview with sharing debuggers (links above)

## Common Issues

**Story doesn't appear:**
- Check JSON syntax (commas, quotes)
- Verify `id` is unique
- Ensure `published_at` is valid ISO 8601

**Image doesn't show:**
- Verify path is correct (site-rooted `/assets/...` or absolute `https://...`)
- Check file exists and is readable
- Confirm image dimensions (at least 1200×630)

**OG preview shows wrong image:**
- Clear cache on social platforms (use sharing debuggers)
- Verify `og_image` or `image` field is set correctly
- Default image fallback should always work

## Questions?

Contact the Acre & Plate team or check the repository documentation.
