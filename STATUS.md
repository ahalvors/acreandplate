# Acre & Plate - Status

**Last Updated:** September 12, 2026  
**Build Status:** ✅ Passing

## Site Statistics

- **Total Ranches:** 28
- **Active Deals:** 1
- **Farmers Markets:** 3 (new feature!)
- **Featured Ranch Placements:** 0 (feature ready, awaiting first subscribers)
- **Wagyu Ranches:** 16
- **Akaushi Ranches:** 5
- **Heritage Breeds:** 3
- **Texas Ranches:** 6
- **California Ranches:** 8
- **Colorado Ranches:** 1
- **Florida Ranches:** 2
- **Wyoming Ranches:** 2
- **Total Pages:** 42

## Pages Built

### Core Pages
- ✅ Home (`index.html`)
- ✅ All Listings (`/listings/`)
- ✅ Seasonal Deals (`/deals/`) - 1 active deal
- ✅ Local Activity - Markets (`/markets/`) - 3 verified farmers markets (NEW!)
- ✅ Featured Ranch (`/featured/`) - monetization landing page
- ✅ Featured Ranch Thanks (`/featured/thanks/`) - post-checkout page
- ✅ About (`/about/`)

### Hub Pages
- ✅ Wagyu hub (`/wagyu/`) - 16 ranches
- ✅ Akaushi hub (`/akaushi/`) - 5 ranches
- ✅ Texas hub (`/texas/`) - 6 ranches
- ✅ California hub (`/california/`) - 8 ranches
- ✅ Colorado hub (`/colorado/`) - 1 ranch
- ✅ Florida hub (`/florida/`) - 2 ranches
- ✅ Wyoming hub (`/wyoming/`) - 2 ranches

### Guide Pages
- ✅ Wagyu vs Akaushi Guide (`/guides/wagyu-vs-akaushi/`)

### Listing Pages (28 ranches)
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
- ✅ Cross Creek Ranch Premium Meats (CO)
- ✅ 3Z Cattle Co (CA)
- ✅ Midori Ranch (CA)
- ✅ Nyland Herefords (CA)
- ✅ Morris Grassfed (CA)
- ✅ Connolly Ranch Natural Beef (CA)

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

## Markets Feature (NEW!)

### Overview
The new **Local Activity** section at `/markets/` showcases farmers markets where local farmers/ranchers sell beef from named herds. This is a national-scope feature, not limited to Bay Area.

### Current Markets (3)
- **Livermore Farmers Market (Sunday)** - Year-round, 9am–1pm
- **Livermore Thursday Night Farmers Market** - Seasonal (April-October), 4pm–8pm
- **Pleasanton Farmers Market** - Year-round Saturdays, 9am–1pm
  - Verified beef vendor: **Engler Beef** (Sonora, CA) per PCFMA vendor table

### Design Principles
- No fake data: Only verified markets with public information
- Vendor lineups noted as subject to change
- Clear disclaimers: confirm vendors on-site
- Extensible data structure for national expansion

### Data Source
- `data/markets.json` - Farmers markets data (schema: slug, name, url, city, state, schedule, location, beef_vendors[], note, verified_at, source_verified)
- Generated via `build.py` (mirroring listings/deals pattern)

## Data Quality

### Verified Information
All 28 ranch listings and 3 farmers markets on Acre & Plate have been verified from:
- Public ranch websites
- Direct product pages
- Contact information pages
- Shipping policy pages

### Deals & Pricing
- ✅ **1 active deal** verified from ranch website (as of Sept 8, 2026)
- ✅ Sale prices confirmed from ranch sales/clearance pages
- ✅ Regular prices included when shown by ranch
- ⚠️ Deals updated periodically—users should confirm current pricing on ranch sites
- 📅 **Sep 8, 2026 nightly ship:** Added Cross Creek Ranch Premium Meats (Hesperus, CO) — first Colorado ranch, Full Blood + American Wagyu. Re-verified Long Hill 15 lb ground bulk deal still active at $180. No new deals found tonight.
- 📅 **Sep 9, 2026 nightly ship:** Added Colorado state hub at `/colorado/` listing Cross Creek Ranch (Hesperus). Re-verified Long Hill Wagyu 15 lb ground bulk deal still active at $180 (regular $195). Colorado hub now wired in navigation and home page, mirroring California pattern. No new listings or deals added.
- 📅 **Sep 10, 2026 Bay Area/Central Coast expansion:** Added 5 verified California ranches: 3Z Cattle Co (Morgan Hill - American Wagyu F1-F4 + Angus), Midori Ranch (Paicines - F1 Wagyu), Nyland Herefords (San Juan Bautista - horned Hereford), Morris Grassfed (San Juan Bautista - 100% grassfed), Connolly Ranch Natural Beef (Tracy - Black Angus). California hub now shows 8 ranches (up from 3). Total site count: 28 ranches, 39 pages.
- 📅 **Sep 10, 2026 evening ship:** Added Florida state hub at `/florida/` with 2 ranches (Pasture Prime Wagyu, Black Wagyu Beef Co.). Re-verified Long Hill Wagyu 15 lb ground bulk deal still active at $180 (regular $195). Florida hub now wired into home page hub links. No new listings or deals added. Total site count: 28 ranches, 40 pages.
- 📅 **Sep 11, 2026 nightly ship:** Added Wyoming state hub at `/wyoming/` with 2 ranches (Hawks Hill Ranch - Cody, Circle H Ranch - Smoot/Geneva WY/ID). Re-verified Long Hill Wagyu 15 lb ground bulk deal still active at $180 (regular $195). Wyoming hub now wired into home page hub links. No new listings or new deals found. Total site count: 28 ranches, 41 pages.
- 📅 **Sep 12, 2026 - Markets Feature Launch:** Added **Local Activity** section at `/markets/` featuring farmers markets where local farmers/ranchers sell beef. National scope, data-driven from `data/markets.json`. Initial seed: 3 verified Bay Area markets (Livermore Sunday, Livermore Thursday, Pleasanton). Pleasanton market lists verified beef vendor: Engler Beef (Sonora, CA) confirmed on PCFMA vendor table. Markets integrated into main nav as "Markets" + home page teaser section. Design canon preserved (pasture to plate, no fake data). Total site count: 28 ranches, 3 markets, 42 pages.

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
- [x] Add Colorado state hub page
- [x] Add Florida state hub page
- [x] Add Wyoming state hub page
- [ ] Add more state hub pages (as more ranches are added)
- [ ] Add heritage breeds hub page
- [ ] Expand to more ranches (verified genetics only)
- [ ] Add search/filter functionality (JavaScript)
- [ ] Weekly/monthly deal verification cron
- [ ] Consider RSS feed for new listings and deals

## Maintenance

**Data Sources:**
- `data/listings.json` - Ranch listings
- `data/deals.json` - Current deals
- `data/markets.json` - Farmers markets (NEW!)
- `data/featured.json` - Featured Ranch placements (paid)
- `data/stripe.json` - Stripe payment link configuration

**Template Engine:** `build.py` (Python)  
**Styling:** `css/site.css`

To add a ranch, see `ADDING_A_PAGE.md`.  
To add a deal, see `ADDING_A_DEAL.md`.  
For Featured Ranch setup, see `FEATURED.md` (or `/featured/` page).
