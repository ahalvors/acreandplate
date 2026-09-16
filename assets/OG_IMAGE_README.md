# Default OG Image for News Stories

This directory needs a default Open Graph image for news stories that don't have a custom image.

## Specification

**Filename:** `og-news-default.png` (or `.jpg`)

**Dimensions:** 1200×630 pixels (standard OG image size)

**Content:** Branded Acre & Plate image suitable for link previews
- Include the Rocking A&P mark (logo)
- Brand name "Acre & Plate"
- Tagline "Pasture to plate"
- Use brand colors (olive, rust, bone from the style guide)
- Simple, clean design that works well in small previews

## Temporary Solution

Until a proper image is created, the build script will use the existing brand mark.
To add the proper default image:

1. Create/obtain a 1200×630 branded image
2. Save as `/assets/og-news-default.png`
3. Rebuild the site with `python3 build.py`

## Per-Story Images

Individual news stories can have custom OG images by adding an `image` or `og_image` field to the news item in `data/news.json`. See `ADDING_NEWS.md` for details.
