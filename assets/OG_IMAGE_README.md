# Default OG Image for News Stories

This directory contains the default Open Graph image (`og-news-default.png`) used for news stories that don't have a custom image.

## Current Image

**Filename:** `og-news-default.png`

**Dimensions:** 1200×630 pixels (standard OG image size)

**Content:** Branded Acre & Plate image with cow silhouette, "Acre & Plate" text, and "Pasture to plate" tagline.

This image is automatically used for any news story that doesn't specify a custom `image` or `og_image` field in `data/news.json`.

## Per-Story Custom Images

Individual news stories can override the default by adding an `image` or `og_image` field to the news item in `data/news.json`. See `ADDING_NEWS.md` for complete documentation on adding custom images to news stories.
