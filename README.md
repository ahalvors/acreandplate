# Acre & Plate

**Ranch-direct beef for people who care where dinner came from—local pasture, named herds, honest sourcing.**

Static directory site listing ranches selling beef with traceable bloodlines direct to consumers.

🔗 **[View Site](https://acreandplate.com)**

---

## What This Is

A curated directory of 20 U.S. ranches selling:
- **Fullblood Wagyu** (registered Japanese bloodlines, DNA-verified)
- **Akaushi** (Japanese Brown Wagyu)
- **Heritage breeds** (Randall Lineback, Dexter, Piedmontese)

All direct-to-consumer. No retail "Wagyu" marketing. Every ranch has a public website with verifiable breed claims.

**What's New:**
- **Featured Ranch monetization:** Paid monthly placement for ranches (Standard $99/mo, Premium $199/mo)
- **Seasonal deals section:** Tracking verified sale, clearance, and overstock pricing across ranches
- **UTM tracking:** All outbound ranch links include tracking parameters for attribution

## Architecture

Static HTML site generated from `data/listings.json`:

```
data/listings.json     # Source of truth: 20 ranch listings
data/deals.json        # Current deals: 14 verified deals
data/featured.json     # Featured Ranch placements (paid)
data/stripe.json       # Stripe payment link config
build.py              # Python generator: data → HTML pages
css/site.css          # Styling
index.html            # Home page (generated)
listings/             # All ranch pages (generated)
deals/                # Deals hub (generated)
featured/             # Featured Ranch pages (generated)
wagyu/                # Hub pages (generated)
akaushi/              # Hub pages (generated)
texas/                # Hub pages (generated)
guides/               # Guide pages (generated)
about/                # About page (generated)
```

**Build:** `python3 build.py`  
**Output:** 30 static HTML pages

## Repository Structure

```
├── data/
│   ├── listings.json          # 20 ranch listings (source of truth)
│   ├── deals.json             # 14 current deals (verified pricing)
│   ├── featured.json          # Featured Ranch placements (paid)
│   └── stripe.json            # Stripe payment link config
├── css/
│   └── site.css              # Site styles
├── build.py                  # Static site generator
├── netlify.toml              # Netlify build config
├── README.md                 # This file
├── STATUS.md                 # Build status, counts, known gaps
├── ADDING_A_PAGE.md          # Guide for adding ranches
├── ADDING_A_DEAL.md          # Guide for adding deals
└── [generated files]         # index.html, listings/, deals/, etc.
```

## Local Development

### Build the site
```bash
python3 build.py
```

This generates all 28 pages in the root directory.

### View locally
```bash
python3 -m http.server 8000
open http://localhost:8000
```

## Deployment

**Platform:** Netlify  
**Build command:** `python3 build.py`  
**Publish directory:** `/` (root)

Every push to `main` triggers a build and deploy via `netlify.toml`.

## Adding Content

### Adding a Ranch
See **[ADDING_A_PAGE.md](ADDING_A_PAGE.md)** for full instructions.

Quick version:
1. Verify ranch has public website with genetics claims
2. Add entry to `data/listings.json`
3. Run `python3 build.py`
4. Commit and push

### Adding a Deal
See **[ADDING_A_DEAL.md](ADDING_A_DEAL.md)** for full instructions.

Quick version:
1. Verify deal on ranch website (sale/clearance/overstock)
2. Add entry to `data/deals.json`
3. Run `python3 build.py`
4. Commit and push

### Featured Ranch (Monetization)
Ranches can purchase premium placement on the site:
- **Standard** ($99/mo): Featured on home + listings with badge
- **Premium** ($199/mo): Home + listings + deals hub spotlight

**Setup:**
1. Update `data/stripe.json` with real Stripe Payment Link URLs
2. Ranch owners subscribe via `/featured/` page
3. Add placement to `data/featured.json` with listing_id, tier, dates
4. Rebuild and deploy

All ranch links include UTM tracking for attribution.

## Data Quality

All 20 ranches verified from public websites as of September 2026.

**We record:**
- Breed and bloodline claims (exact wording from ranch sites)
- Location, products, shipping
- Contact info (phone, website)

**We don't include:**
- Real-time pricing or inventory
- Breeding stock / live cattle
- Retail products without ranch attribution

See [STATUS.md](STATUS.md) for known gaps and limitations.

## Site Statistics

- 20 ranches
- 14 active deals (verified Sept 5, 2026)
- 0 featured placements (feature ready, awaiting first subscribers)
- 13 Wagyu, 5 Akaushi, 3 heritage breeds
- 30 total pages (home, listings, deals, featured, hubs, guides)
- Mobile-first, warm ranch/editorial design
- UTM tracking on all outbound ranch links

## Technology

- **Generator:** Python 3
- **Templating:** Python string formatting (build.py)
- **Styling:** Vanilla CSS (css/site.css)
- **JavaScript:** None (currently)
- **Deployment:** Netlify

No framework. No build toolchain. Just Python + HTML + CSS.

## Maintenance

**Owner:** BeefBot  
**Project:** Acre & Plate
**Repository:** github.com/ahalvors/acreandplate  
**Status:** See [STATUS.md](STATUS.md)

To update ranch info:
1. Edit `data/listings.json`
2. Run `python3 build.py`
3. Commit changes
4. Push to `main`

Netlify auto-deploys.

## License

Data: Public information compiled from ranch websites  
Code: MIT License (build.py, site structure)

## Contact

Acre & Plate is a directory site. We don't sell beef.  
Contact ranches directly via links in each listing.

For directory questions or ranch additions: Open an issue on GitHub.

---

**Last Updated:** September 7, 2026  
**Ranches:** 20 | **Deals:** 14 | **Featured:** 0 | **Pages:** 30 | **Build:** ✅ Passing
