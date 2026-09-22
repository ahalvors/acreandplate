# Acre & Plate - Status

**Last Updated:** September 22, 2026  
**Build Status:** ✅ Passing

## Site Statistics

- **Total Ranches:** 40
- **Ranch Contact Sheet:** 28 of 38 have public business emails (74%)
- **Active Deals:** 4
- **Farmers Markets:** 3
- **Butcher Shops:** 19
- **Featured Ranch Placements:** 0 (feature ready, awaiting first subscribers)
- **Wagyu Ranches:** 19
- **Akaushi Ranches:** 6
- **Heritage Breeds:** 3
- **Texas Ranches:** 6
- **California Ranches:** 17
- **Colorado Ranches:** 1
- **Florida Ranches:** 2
- **Oregon Ranches:** 1
- **Washington Ranches:** 2
- **Wyoming Ranches:** 3
- **Total Pages:** 63

## Pages Built

### Core Pages
- ✅ Home (`index.html`)
- ✅ All Listings (`/listings/`)
- ✅ Seasonal Deals (`/deals/`) - 4 active deals
- ✅ Local Activity (`/markets/`) - 3 farmers markets + 19 butcher shops (UPDATED!)
- ✅ Featured Ranch (`/featured/`) - monetization landing page
- ✅ Featured Ranch Thanks (`/featured/thanks/`) - post-checkout page
- ✅ About (`/about/`)

### Hub Pages
- ✅ Wagyu hub (`/wagyu/`) - 16 ranches
- ✅ Akaushi hub (`/akaushi/`) - 5 ranches
- ✅ Heritage Breeds hub (`/heritage/`) - 2 ranches (NEW!)
- ✅ Texas hub (`/texas/`) - 6 ranches
- ✅ California hub (`/california/`) - 17 ranches
- ✅ Colorado hub (`/colorado/`) - 1 ranch
- ✅ Florida hub (`/florida/`) - 2 ranches
- ✅ Oregon hub (`/oregon/`) - 1 ranch
- ✅ Washington hub (`/washington/`) - 2 ranches
- ✅ Wyoming hub (`/wyoming/`) - 3 ranches

### Guide Pages
- ✅ Wagyu vs Akaushi Guide (`/guides/wagyu-vs-akaushi/`)

### Listing Pages (40 ranches)
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
- ✅ Stemple Creek Ranch (CA)
- ✅ The Hufeisen-Ranch (WYO Wagyu) (WY)
- ✅ Rascal Ranch Farms (CA)
- ✅ Ells Cattle Ranch (CA)
- ✅ Kirk Cattle Company (CA)
- ✅ Salmon Creek Ranch (CA)
- ✅ Marin Coast Ranch (CA)
- ✅ StarWalker Organic Farms (CA)
- ✅ Oreganic Beef Co. (Rocker 3 Ranch) (OR)
- ✅ Yocha Dehe Ranch (CA)
- ✅ Mariposa Ranch (CA)
- ✅ Lone Crow Ranch (WA)

## Known Gaps & Notes

### Parked Ranches (Pending Verification)
- **Good Life Beef (German Lepe)** - Noted on Livermore Livestock Instagram card as est. 2022, claiming grass-fed/finished, USDA inspected, Bay Area delivery. Multiple web searches found NO verifiable CA direct-to-consumer operation. GoodLife Beef (Nebraska) and Good Life Beef (Australia) are different businesses. Parked pending website or verifiable primary source contact.

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

## Local Activity Feature

### Overview
The **Local Activity** section at `/markets/` showcases:
1. **Farmers markets** where local farmers/ranchers sell beef from named herds (national scope, not limited to Bay Area)
2. **Butcher shops** where Bay Area residents buy quality beef (Bay Area focus)

### Current Markets (3)
- **Livermore Farmers Market (Sunday)** - Year-round, 9am–1pm
- **Livermore Thursday Night Farmers Market** - Seasonal (April-October), 4pm–8pm
- **Pleasanton Farmers Market** - Year-round Saturdays, 9am–1pm
  - Verified beef vendor: **Engler Beef** (Sonora, CA) per PCFMA vendor table

### Current Butcher Shops (19)
Organized by county across the Bay Area:
- **Alameda County (3):** Livermore Butcher Shop, Baron's Quality Meats & Seafood, The Local Butcher Shop
- **Contra Costa County (2):** Brentwood Fine Meats, Diablo Foods
- **Marin County (2):** Rocky's Quality Meats, Flannery Beef
- **Napa County (2):** Fatted Calf, Browns Valley Meat
- **San Francisco (2):** Avedano's Holly Park Meat Market, Olivier's Butchery
- **San Mateo County (2):** Pape Meat Company, Gambrel & Co
- **Santa Clara County (2):** Los Gatos Meats & Smokehouse, Custom Cut Butcher
- **Sonoma County (3):** Sonoma County Meat Co., Willowside Meats, Bud's Custom Meats
- **Solano County (1):** Gates Ranch Meat Company

### Design Principles
- No fake data: Only verified locations with public information
- Markets: Vendor lineups noted as subject to change
- Butchers: No invented claims about grass-fed/ranch-direct sourcing
- Clear disclaimers throughout
- Extensible data structure for expansion

### Data Sources
- `data/markets.json` - Farmers markets data (schema: slug, name, url, city, state, schedule, location, beef_vendors[], note, verified_at, source_verified)
- `data/butchers.json` - Butcher shops data (schema: slug, name, url, city, state, county, note, specialties[], gaps, verified_at, source_verified)
- Generated via `build.py` (mirroring listings/deals pattern)

## Data Quality

### Verified Information
All 28 ranch listings and 3 farmers markets on Acre & Plate have been verified from:
- Public ranch websites
- Direct product pages
- Contact information pages
- Shipping policy pages

### Deals & Pricing
- ✅ **4 active deals** verified from ranch websites (as of Sept 19, 2026)
- ✅ Sale prices confirmed from ranch sales/clearance pages
- ✅ Regular prices included when shown by ranch
- ⚠️ Deals updated periodically—users should confirm current pricing on ranch sites
- 📅 **Sep 8, 2026 nightly ship:** Added Cross Creek Ranch Premium Meats (Hesperus, CO) — first Colorado ranch, Full Blood + American Wagyu. Re-verified Long Hill 15 lb ground bulk deal still active at $180. No new deals found tonight.
- 📅 **Sep 9, 2026 nightly ship:** Added Colorado state hub at `/colorado/` listing Cross Creek Ranch (Hesperus). Re-verified Long Hill Wagyu 15 lb ground bulk deal still active at $180 (regular $195). Colorado hub now wired in navigation and home page, mirroring California pattern. No new listings or deals added.
- 📅 **Sep 10, 2026 Bay Area/Central Coast expansion:** Added 5 verified California ranches: 3Z Cattle Co (Morgan Hill - American Wagyu F1-F4 + Angus), Midori Ranch (Paicines - F1 Wagyu), Nyland Herefords (San Juan Bautista - horned Hereford), Morris Grassfed (San Juan Bautista - 100% grassfed), Connolly Ranch Natural Beef (Tracy - Black Angus). California hub now shows 8 ranches (up from 3). Total site count: 28 ranches, 39 pages.
- 📅 **Sep 10, 2026 evening ship:** Added Florida state hub at `/florida/` with 2 ranches (Pasture Prime Wagyu, Black Wagyu Beef Co.). Re-verified Long Hill Wagyu 15 lb ground bulk deal still active at $180 (regular $195). Florida hub now wired into home page hub links. No new listings or deals added. Total site count: 28 ranches, 40 pages.
- 📅 **Sep 11, 2026 nightly ship:** Added Wyoming state hub at `/wyoming/` with 2 ranches (Hawks Hill Ranch - Cody, Circle H Ranch - Smoot/Geneva WY/ID). Re-verified Long Hill Wagyu 15 lb ground bulk deal still active at $180 (regular $195). Wyoming hub now wired into home page hub links. No new listings or new deals found. Total site count: 28 ranches, 41 pages.
- 📅 **Sep 12, 2026 - Markets Feature Launch:** Added **Local Activity** section at `/markets/` featuring farmers markets where local farmers/ranchers sell beef. National scope, data-driven from `data/markets.json`. Initial seed: 3 verified Bay Area markets (Livermore Sunday, Livermore Thursday, Pleasanton). Pleasanton market lists verified beef vendor: Engler Beef (Sonora, CA) confirmed on PCFMA vendor table. Markets integrated into main nav as "Markets" + home page teaser section. Design canon preserved (pasture to plate, no fake data). Total site count: 28 ranches, 3 markets, 42 pages.
- 📅 **Sep 12, 2026 evening - Butcher Shops Added:** Extended Local Activity (`/markets/`) with new **Butcher Shops** section. Added 19 verified Bay Area butcher shops organized by county (Alameda, Contra Costa, Marin, Napa, San Francisco, San Mateo, Santa Clara, Sonoma, Solano). Data in `data/butchers.json`. Page now shows two sections: Farmers Markets (3) and Butcher Shops (19). Design canon preserved—no fake phones/hours/grass-fed claims. Gaps noted for Rocky's Quality Meats, Pape Meat Company (Yelp only), and Gates Ranch Meat (by reservation only). Home page teaser updated to mention butchers. Total site count: 28 ranches, 3 markets, 19 butchers, 42 pages.
- 📅 **Sep 13, 2026 nightly ship:** Added **Heritage Breeds hub** at `/heritage/` featuring 2 ranches: Chapel Hill Farm (VA - critically endangered Randall Lineback) and Mahanaim Farms (UT - rare Dexter cattle). Hub integrated into home page "Browse by Breed or State" section and main navigation pattern. All data compiled from existing verified listings. No new listings or deals added tonight. Total site count: 28 ranches, 1 active deal, 3 markets, 19 butchers, 42 pages.
- 📅 **Sep 13, 2026 PT evening ship:** Added **Stemple Creek Ranch** (Tomales, CA) - fourth-generation West Marin ranch with 100% grass-fed and grass-finished beef. Ships to all 50 U.S. states with free CA shipping. Re-verified Long Hill Wagyu 15 lb ground bulk deal still active at $180 (regular $195). California hub now shows 9 ranches (up from 8). No new deals found. Total site count: 29 ranches, 1 active deal, 3 markets, 19 butchers, 43 pages.
- 📅 **Sep 14, 2026 PT nightly ship:** Added **The Hufeisen-Ranch (WYO Wagyu)** (Weston, WY) - woman-owned family ranch raising 100% DNA-Verified Fullblood Japanese Black Wagyu, regeneratively pastured with grass-fed and managed fermented grain finish. Ships nationwide frozen. Preparing move from Wyoming to Florida; current DTC beef marketed as Wyoming Last Harvest. Wyoming hub now shows 3 ranches (Circle H WY/ID, Hawks Hill, Hufeisen). Re-verified Long Hill Wagyu 15 lb ground bulk deal still active at $180 (regular $195) and updated verified_at to 2026-09-14. No new deals added. Total site count: 30 ranches, 1 active deal, 3 markets, 19 butchers, 44 pages.
- 📅 **Sep 15, 2026 PT nightly ship:** Added **Rascal Ranch Farms** (Yolo County, CA) - family ranch (Janice & Mike Hester; Tyler & Megan Hester) raising Purebred Akaushi (Red Wagyu), American F1 Akaushi, and specialty Black Wagyu with regenerative practices. Offers cattle shares (quarter/half/whole) and pasture-raised lamb via Barn2Door store. Local delivery within ~60 miles of greater Sacramento/Yolo/Solano/East Bay; butcher pickup available. Registered foundational genetics including D&H Rueshaw Jr. California hub now shows 10 ranches (up from 9); Akaushi hub shows 6 ranches (up from 5); Wagyu hub shows 18 ranches (up from 17). Re-verified Long Hill Wagyu 15 lb ground bulk deal still active at $180 (regular $195) and updated verified_at to 2026-09-15. No new deals added. Total site count: 31 ranches, 1 active deal, 3 markets, 19 butchers, 52 pages.
- 📅 **Sep 16, 2026 - Livermore Livestock Leads:** Added 2 verified ranches from Livermore Livestock Instagram directory cards. **Ells Cattle Ranch** (Paicines, San Benito County) - small family ranch raising 100% Black Angus, pasture-raised and grain-finished (barley/oats/corn), no hormones or antibiotics; half beef shares with butcher pickup at Los Gatos Meats or Freedom Meats. **Kirk Cattle Company** (Gilroy) - conservation grazing and certified natural beef (whole/half shares, grass-fed or grain-finished options); contact via Santa Clara County Cattlemen's Association listing. Parked **Good Life Beef (German Lepe)** pending website verification - no verifiable CA DTC operation found despite Livermore card claims. California hub now shows 12 ranches (up from 10). No new deals added. Total site count: 33 ranches, 1 active deal, 3 markets, 19 butchers, 54 pages.
- 📅 **Sep 16, 2026 PT nightly ship:** Added **Salmon Creek Ranch** (Bodega, CA) - Sonoma coast ranch raising 100% grass-fed and grass-finished beef on certified organic pasture, including Scottish Highland and other British breeds. Retail cuts ship continental USA; whole/half/quarter beef for Sonoma County local pickup; on-farm store pickup and Santa Rosa Farmers Market (Saturdays). California hub now shows 13 ranches (up from 12); Heritage Breeds hub shows 3 ranches (up from 2). Re-verified Long Hill Wagyu 15 lb ground bulk deal still active at $180 (regular $195) and updated verified_at to 2026-09-16. Long Hill 1 lb ground NOT added—no sale price currently, only regular $12.99. Total site count: 34 ranches, 1 active deal, 3 markets, 19 butchers, 55 pages.
- 📅 **Sep 17, 2026 - Deal Hunt:** Systematically checked 30+ ranch websites for verified sales/clearance/overstock deals. Found 2 new genuine deals: **Hufeisen Ranch (WYO Wagyu)** "The Last Harvest Fullblood Wagyu Box" (Family Box) at $199 (regular $299, save $100) - final Wyoming harvest clearance before ranch relocation to Florida, only 6 steers available, ~10-12 lbs mixed cuts; **Mossyrock Wagyu** "WAGYU BBQ BOX" at $395 (regular $475, save $80). Re-verified Long Hill Wagyu 15 lb ground bulk still active at $180 (regular $195). Checked but found no current sales at: Lone Mountain, HeartBrand, Cross Creek Ranch, Stemple Creek, Koopmann Family Beef, 3Z Cattle, Salmon Creek Ranch, Hook & Cleaver (has bundle pricing but not clearance sales), Circle H Ranch, Hawks Hill Ranch, Certified Piedmontese, Vermont Wagyu, Caroland Farms, Slickhorn Ranch, Pasture Prime Wagyu, Rutledge Ryan Ranch, Quinn Beef, Tribe Ranch, Ranch & Trail (Mahan). Updated deals.json with all 3 verified deals. Total site count: 34 ranches, 3 active deals, 3 markets, 19 butchers, 55 pages.
- 📅 **Sep 17, 2026 PT evening ship:** Added **Marin Coast Ranch** (Tomales, CA) - sixth-generation Northern California family ranch in West Marin raising USDA Certified Grassfed, Certified Natural Angus beef on coastal pasture. Ships nationwide (recommend 8+ lb for long distance); local delivery in eligible Marin/Sonoma zip codes; ranch pickup in Tomales by pre-order. Also sells grass-fed lamb. Re-verified all 3 active deals still live: Long Hill 15 lb ground at $180, Hufeisen Last Harvest Family Box at $199, Mossyrock WAGYU BBQ BOX at $395. California hub now shows 14 ranches (up from 13). Good Life Beef still parked pending website verification. Total site count: 35 ranches, 3 active deals, 3 markets, 19 butchers, 56 pages.
- 📅 **Sep 18, 2026 PT nightly ship:** Added **StarWalker Organic Farms** (Fort Jones, CA) - third-generation Walker family farm (est. 1970) raising Regenerative Organic Certified® grass-fed and grass-finished beef on pasture year-round, marketed as first Regenerative Organic Certified® beef and pork producers in America; USDA/CCOF organic. Ships nationwide including Alaska and Hawaii (frozen; free shipping on frozen orders $325+). Also sells Regenerative Organic Certified® heritage pork and organic chicken. Re-verified all 3 active deals still live: Long Hill 15 lb ground at $180, Hufeisen Last Harvest Family Box at $199, Mossyrock WAGYU BBQ BOX at $395 (updated verified_at to 2026-09-18). California hub now shows 15 ranches (up from 14). Good Life Beef still parked pending website verification. Total site count: 36 ranches, 3 active deals, 3 markets, 19 butchers, 57 pages.
- 📅 **Sep 19, 2026 PT nightly ship:** Added **Oreganic Beef Co. (Rocker 3 Ranch)** (Madras, OR) - family-owned Central Oregon ranch selling ranch-direct USDA Certified Organic, 100% grass-fed and grass-finished beef. GAP4 certified, fully traceable herd logs, dry-aged prime cuts 30+ days. Ships nationwide with free shipping on orders over $199 for OR/WA/CA/ID/NV. Processed at Mark's Meat Co., Canby, OR. Added Oregon state hub at `/oregon/` - first Oregon ranch on directory. Added new deal: Oreganic Crockpot Comfort Box at $199 (regular $229) - 18+ lb box with roasts, short ribs, and shanks. Re-verified all 3 existing deals still live: Long Hill 15 lb ground at $180, Hufeisen Last Harvest Family Box at $199, Mossyrock WAGYU BBQ BOX at $395 (updated verified_at to 2026-09-19). Oregon hub now wired into home page hub links and navigation. Good Life Beef still parked pending website verification. Total site count: 37 ranches, 4 active deals, 3 markets, 19 butchers, 59 pages.
- 📅 **Sep 20, 2026:** Added **Yocha Dehe Ranch** (Capay Valley / Brooks, CA) - Yocha Dehe Wintun Nation ranch raising premium Angus beef on 20,000 acres of tribal lands in California's Capay Valley. 800 head of cattle raised on open pastures with sustainable grazing practices; finished with oats, barley, and corn for 45-60 days. Beef available exclusively through Séka Hills Beef Club (quarterly pickup-only packages at Capay Valley Tasting Room in Brooks). Contact Club@sekahills.com for club inquiries or info@yochadehe.gov for general ranch questions. Marketed under Séka Hills brand alongside olive oil, wine, and honey. California hub now shows 16 ranches (up from 15). Re-verified all 4 active deals. Total site count: 38 ranches, 4 active deals, 3 markets, 19 butchers, 59 pages.
- 📅 **Sep 20, 2026 PT nightly ship:** Added **Washington state hub** at `/washington/` featuring Mossyrock Wagyu (Mossyrock, WA) - 100% Fullblood Japanese Black Wagyu raised in the Klickitat Valley between Mt. Rainier and Mt. St. Helens. Washington hub now wired into home page hub links and navigation, mirroring Oregon/Colorado pattern. Re-verified all 4 active deals still live: Long Hill 15 lb ground at $180, Hufeisen Last Harvest Family Box at $199, Mossyrock WAGYU BBQ BOX at $395, Oreganic Crockpot Comfort Box at $199 (updated verified_at to 2026-09-20). No new ranches found tonight that met honesty criteria. Good Life Beef still parked pending website verification. Total site count: 38 ranches, 4 active deals, 3 markets, 19 butchers, 60 pages.
- 📅 **Sep 21, 2026 PT follow-up ship:** Added **Mariposa Ranch** (Mariposa, CA) - Seth & Mica Nitschke family ranchers in Central California (Mariposa County) raising 100% grass-fed and grass-finished beef since 2006. Cattle grown and finished entirely on pasture with no hormones, no antibiotics, no grains, and no herbicides/pesticides/fertilizers. Ships frozen nationwide with free shipping on orders over $150 in CA, NV, AZ. Offers subscription boxes, retail cuts (steaks, ground, roasts), organ meats, bones, and whole/half/quarter cow. Originally founded as Open Space Meats in 2006, rebranded to Mariposa Ranch in 2017 for transparency. Phone: 209-771-0399; Email: service@mariposaranch.com; Ranch location: 3132 Spengler Way, Mariposa, CA 95380. California hub now shows 17 ranches (up from 16). Re-verified all 4 active deals still live. Research notes: 1902 Ranch (Whidbey Island, WA) reviewed but all products currently sold out; Kauboi Ranch (Redmond, OR) and Lone Crow Ranch (Eltopia, WA) reviewed as candidates. Good Life Beef still parked. Total site count: 39 ranches, 4 active deals, 3 markets, 19 butchers, 61 pages.
- 📅 **Sep 21, 2026 PT nightly ship:** Added **Lone Crow Ranch** (Eltopia, WA) - first-generation vertically integrated ranch (Cody & Jen Hoseth) raising Wagyu and Angus with own USDA butcher shop in Connell. 1,000 head of cattle, pasture-raised with grain-finished and grass-finished options; no added hormones; diet formulated by certified animal nutritionist with locally sourced non-GMO feed (wheat, apples, potatoes). Ships to WA, OR, ID, CA; delivery in Spokane, Tri-Cities, Seattle areas. Phone: 360-509-3835; Email: orders@lonecrowranch.com. Gap: Wagyu genetics percentage not specified on public site. Washington hub now shows 2 ranches (up from 1). Wagyu hub shows 19 ranches (up from 18). Re-verified all 4 active deals still live: Long Hill 15 lb ground at $180, Hufeisen Last Harvest Family Box at $199, Mossyrock WAGYU BBQ BOX at $395, Oreganic Crockpot Comfort Box at $199 (updated verified_at to 2026-09-21). Good Life Beef still parked. Total site count: 40 ranches, 4 active deals, 3 markets, 19 butchers, 63 pages.

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
- [x] Add Oregon state hub page (SHIPPED!)
- [x] Add heritage breeds hub page (SHIPPED!)
- [ ] Add more state hub pages (as more ranches are added)
- [ ] Expand to more ranches (verified genetics only)
- [ ] Add search/filter functionality (JavaScript)
- [ ] Weekly/monthly deal verification cron
- [ ] Consider RSS feed for new listings and deals

## Ranch Outreach Contact Sheet

**File:** `data/ranch-contacts.json`  
**Status:** Complete  
**Coverage:** 36 ranches (all current listings)  
**Harvestable Emails:** 27 of 36 (75%)

### Purpose
Contact sheet for Featured Ranch outbound drip campaign. Contains verified business contact emails suitable for B2B outreach.

### Email Quality
- ✅ 27 ranches have public business emails (info@, sales@, hello@, ranch-specific)
- ✅ All emails verified from public website contact pages, footers, or about pages
- ⚠️ 9 ranches have no public email (contact forms only or phone-only)
- ✅ Zero invented emails - nulls are honest nulls

### Missing Emails (9 ranches)
- Long Hill Wagyu (TX) - contact form only
- Hawks Hill Ranch (WY) - no public email
- Slickhorn Ranch (Northern Rockies) - no public email
- Chapel Hill Farm (VA) - no public email
- Certified Piedmontese (NE) - contact form only
- Mahanaim Farms (UT) - no contact info (local pickup only)
- Cross Creek Ranch (CO) - contact form only
- Nyland Herefords (CA) - no public email
- Hufeisen-Ranch (WY) - no public email
- Ells Cattle Ranch (CA) - minimal website, no contact info

### Notes
- Personal emails (Gmail/Yahoo) used only when no business email exists (e.g., smaller family operations)
- Phone numbers included when publicly available
- All data verified 2026-09-19

## Maintenance

**Data Sources:**
- `data/listings.json` - Ranch listings
- `data/ranch-contacts.json` - Ranch contact sheet for outreach (NEW!)
- `data/deals.json` - Current deals
- `data/markets.json` - Farmers markets
- `data/butchers.json` - Butcher shops
- `data/featured.json` - Featured Ranch placements (paid)
- `data/stripe.json` - Stripe payment link configuration

**Template Engine:** `build.py` (Python)  
**Styling:** `css/site.css`

To add a ranch, see `ADDING_A_PAGE.md`.  
To add a deal, see `ADDING_A_DEAL.md`.  
For Featured Ranch setup, see `FEATURED.md` (or `/featured/` page).
