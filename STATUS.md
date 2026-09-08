# Acre & Plate - Status

**Last Updated:** September 7, 2026  
**Build Status:** ✅ Passing

## Site Statistics

- **Total Ranches:** 22
- **Active Deals:** 1
- **Featured Ranch Placements:** 0 (feature ready, awaiting first subscribers)
- **Wagyu Ranches:** 13
- **Akaushi Ranches:** 5
- **Heritage Breeds:** 3
- **Texas Ranches:** 6
- **California Ranches:** 3
- **Total Pages:** 32

## Pages Built

### Core Pages
- ✅ Home (`index.html`)
- ✅ All Listings (`/listings/`)
- ✅ Seasonal Deals (`/deals/`) - 1 active deal
- ✅ Featured Ranch (`/featured/`) - monetization landing page
- ✅ Featured Ranch Thanks (`/featured/thanks/`) - post-checkout page
- ✅ About (`/about/`)

### Hub Pages
- ✅ Wagyu hub (`/wagyu/`) - 13 ranches
- ✅ Akaushi hub (`/akaushi/`) - 5 ranches
- ✅ Texas hub (`/texas/`) - 6 ranches
- ✅ California hub (`/california/`) - 3 ranches

### Guide Pages
- ✅ Wagyu vs Akaushi Guide (`/guides/wagyu-vs-akaushi/`)

### Listing Pages (22 ranches)
- ✅ Lone Mountain Wagyu (NM)
- ✅ HeartBrand Beef (TX)
- ✅ Long Hill Wagyu (TX)
- ✅ Circle H Ranch (WY/ID)
- ✅ Hawks Hill Ranch (WY)
- ✅ Slickhorn Ranch (Northern Rockies)
- ✅ Pasture Prime Wagyu (FL)
- ✅ Rutledge Ryan Ranch (TX)
- ✅ Mahan Wagyu (TX)
- ✅ Mossyrock Wagyu (WA)
- ✅ Grant Cattle Company (KS)
- ✅ Black Wagyu Beef Co. (FL)
- ✅ Quinn Beef (TX)
- ✅ Tribe Ranch (AR)
- ✅ Hook & Cleaver Ranch (CA/AZ)
- ✅ Chapel Hill Farm (VA)
- ✅ Certified Piedmontese (NE)
- ✅ Mahanaim Farms (UT)
- ✅ Vermont Wagyu (VT)
- ✅ Caroland Farms Wagyu (SC)
- ✅ Koopmann Family Beef (CA)
- ✅ 3 Calhoun Sisters' Ranch (CA)

## Known Gaps & Notes

### Limited Shipping
- **Black Wagyu Beef Co.** - Florida only (beta testing)
- **Mahanaim Farms** - Pickup only in Salt Lake City (no shipping)

### Contact Info Gaps
- Most ranches have public websites and contact info verified
- Grant Cattle Company - form-based inquiry (no direct phone on main site)
- Vermont Wagyu - email contact available (farm@vermontwagyu.com), phone not listed on public site

### Product Availability
- Several ranches list products as "sold out" seasonally
- Availability changes frequently - users should verify on ranch sites

## Data Quality

### Verified Information
All 20 ranch listings on Acre & Plate have been verified from:
- Public ranch websites
- Direct product pages
- Contact information pages
- Shipping policy pages

### Deals & Pricing
- ✅ **1 active deal** verified from ranch website (as of Sept 7, 2026)
- ✅ Sale prices confirmed from ranch sales/clearance pages
- ✅ Regular prices included when shown by ranch
- ⚠️ Deals updated periodically—users should confirm current pricing on ranch sites
- 📅 **Sep 7, 2026 nightly ship:** Removed 13 stale deals (Piedmontese Labor Day sale ended, Pasture Prime summer boxes no longer listed, HeartBrand sale collection empty). Kept Long Hill ground beef bulk deal still active at $180 compare-at $195.

### What We Record
- ✅ Ranch name and location
- ✅ Breed and bloodline claims (DNA-verified, registered, traceable herds)
- ✅ Available products
- ✅ Shipping information
- ✅ Contact details (website, phone where available)
- ✅ Current deals (sale, clearance, overstock)

### What We Don't Include
- ❌ Real-time inventory/stock levels
- ❌ Breeding stock sales
- ❌ Retail products without ranch attribution
- ❌ Fake "sales" with inflated regular prices

## Monetization: Featured Ranch

**Status:** Live, ready for first subscribers  
**Pricing:** 
- Standard: $99/mo - featured on home + listings
- Premium: $199/mo - home + listings + deals hub spotlight

**Implementation:**
- Payment via Stripe Payment Links (placeholders in `data/stripe.json` until real URLs added)
- Featured placements tracked in `data/featured.json`
- Active placements show "Featured Partner" badge
- All outbound ranch links include UTM tracking (`utm_source=acreandplate&utm_medium=referral&utm_campaign=directory&utm_content=<listing_id>`)

**To activate a featured ranch:**
1. Ranch owner subscribes via `/featured/` page
2. Add entry to `data/featured.json` with listing_id, tier, start/end dates
3. Rebuild site - featured ranch appears with badge on home, listings, and (if premium) deals

## Build Process

```bash
python3 build.py
```

**Output:** 30 static HTML pages + CSS

**Publish Directory:** Root (all HTML files in root and subdirectories)

## Next Steps / Future Enhancements

- [x] Add California state hub page
- [ ] Add more state hub pages (Florida, Wyoming, etc.)
- [ ] Add heritage breeds hub page
- [ ] Expand to more ranches (verified genetics only)
- [ ] Add search/filter functionality (JavaScript)
- [ ] Weekly/monthly deal verification cron
- [ ] Consider RSS feed for new listings and deals

## Maintenance

**Data Sources:**
- `data/listings.json` - Ranch listings
- `data/deals.json` - Current deals
- `data/featured.json` - Featured Ranch placements (paid)
- `data/stripe.json` - Stripe payment link configuration

**Template Engine:** `build.py` (Python)  
**Styling:** `css/site.css`

To add a ranch, see `ADDING_A_PAGE.md`.  
To add a deal, see `ADDING_A_DEAL.md`.  
For Featured Ranch setup, see `FEATURED.md` (or `/featured/` page).
