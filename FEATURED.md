# Featured Ranch - Setup & Management

**Featured Ranch** is Acre & Plate's monetization model—paid monthly placement for ranches on the directory.

## Pricing Tiers

- **Standard** — $99/mo — Featured on home page + all listings browse
- **Premium** — $199/mo — Home + listings + seasonal deals hub spotlight

## How It Works

### For Ranch Owners

1. Visit [acreandplate.com/featured/](https://acreandplate.com/featured/)
2. Choose Standard or Premium tier
3. Subscribe via Stripe Payment Link (monthly recurring)
4. Placement activated within 24 hours

### For Site Maintainers

#### Initial Setup (One-Time)

1. Create Stripe Payment Links:
   - Log into Stripe Dashboard
   - Create Product: "Featured Ranch - Standard" ($99/mo recurring)
   - Create Product: "Featured Ranch - Premium" ($199/mo recurring)
   - Generate Payment Links for each
   - Set success URL to `https://acreandplate.com/featured/thanks/`

2. Update `data/stripe.json`:
   ```json
   {
     "standard_payment_link": "https://buy.stripe.com/YOUR_STANDARD_LINK",
     "premium_payment_link": "https://buy.stripe.com/YOUR_PREMIUM_LINK",
     "success_url": "https://acreandplate.com/featured/thanks/",
     "currency": "usd",
     "standard_price_display": "$99/mo",
     "premium_price_display": "$199/mo"
   }
   ```

3. Rebuild and deploy (`python3 build.py`)

#### Adding a Featured Placement

When a ranch subscribes:

1. Edit `data/featured.json`:
   ```json
   {
     "featured": [
       {
         "listing_id": "lone-mountain-wagyu",
         "tier": "premium",
         "starts_at": "2026-09-07T00:00:00",
         "ends_at": null,
         "note": "Monthly recurring, started Sept 2026"
       }
     ]
   }
   ```

2. Fields:
   - `listing_id` (required): Must match a slug in `listings.json`
   - `tier` (required): `"standard"` or `"premium"`
   - `starts_at` (optional): ISO 8601 date/time when placement begins
   - `ends_at` (optional): ISO 8601 date/time when placement ends (null = active indefinitely)
   - `note` (optional): Internal note (not shown to users)

3. Rebuild site: `python3 build.py`

4. Commit and push to deploy

#### What Gets Featured

**Standard Tier:**
- "Featured Partner" badge on listing card
- Shown in Featured Ranch section on home page (up to 4 displayed)
- Priority in listings browse

**Premium Tier:**
- Everything in Standard, plus:
- Top placement in Featured Ranch section (premium shown first)
- Spotlight section on `/deals/` page (up to 2 displayed)

**Both tiers:**
- All outbound links to ranch website include UTM tracking
- Monthly traffic reports (manual for now—check analytics for `utm_source=acreandplate`)

#### Managing Placements

**Pause/Cancel:**
- Set `ends_at` to today's date in ISO 8601 format
- Rebuild and deploy
- Listing stays in directory, just loses featured badge/placement

**Reactivate:**
- Update `starts_at` and clear `ends_at` (or set to future date)
- Rebuild and deploy

**Track Expiring Placements:**
- Check `data/featured.json` for `ends_at` dates
- Set up calendar reminder to contact ranch for renewal

## UTM Tracking

All outbound ranch links include UTM parameters:
```
?utm_source=acreandplate
&utm_medium=referral
&utm_campaign=directory
&utm_content=<listing_id>
```

Ranches can track Acre & Plate referrals in Google Analytics, Plausible, or any analytics tool.

**Generating Monthly Reports:**
1. Use Google Analytics (or similar) to filter by `utm_source=acreandplate`
2. Report visits and clicks for each featured ranch
3. Email report to ranch owner

## Design

Featured placements are clearly labeled:
- "Featured Partner" badge (not ads-looking spam)
- Editorial tone—"ranches committed to traceable bloodlines"
- Honest empty state when no featured ranches exist

## Empty State

If `data/featured.json` has an empty array (no active placements):
- Home page does NOT show Featured Ranch section
- Deals page does NOT show Featured Ranch spotlight
- `/featured/` page still works for ranch owners to subscribe

## Testing

Before deploying real Stripe links:

1. Verify placeholder state works:
   - Visit `/featured/` with `REPLACE_ME` in `data/stripe.json`
   - CTAs should say "Contact Us (Checkout Coming Soon)"

2. Test with a sample placement:
   ```json
   {
     "featured": [
       {
         "listing_id": "lone-mountain-wagyu",
         "tier": "premium",
         "starts_at": "2026-09-01T00:00:00",
         "note": "Test placement"
       }
     ]
   }
   ```
   - Rebuild and check home page for Featured Ranch section
   - Check deals page for spotlight
   - Verify "Featured Partner" badge appears

3. Test UTM links:
   - Click "Visit Ranch" on any listing
   - Verify URL includes `?utm_source=acreandplate&utm_medium=referral&utm_campaign=directory&utm_content=<listing_id>`

## Questions?

- Stripe setup questions: [Stripe Payment Links docs](https://stripe.com/docs/payments/payment-links)
- Site questions: Open an issue on GitHub or see [STATUS.md](STATUS.md)
