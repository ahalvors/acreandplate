#!/usr/bin/env python3
"""
Acre & Plate - Static Site Generator
Generates all pages from data/listings.json and data/deals.json
"""

import json
import html as html_tools
import re
import os
from pathlib import Path
from typing import List, Dict, Any

# Load listings data
with open('data/listings.json', 'r') as f:
    data = json.load(f)
    listings = data['listings']

# Load deals data
with open('data/deals.json', 'r') as f:
    deals_data = json.load(f)
    deals = deals_data['deals']

# Load featured data
with open('data/featured.json', 'r') as f:
    featured_data = json.load(f)
    featured_placements = featured_data['featured']

# Load Stripe configuration
with open('data/stripe.json', 'r') as f:
    stripe_config = json.load(f)

# Load markets data
with open('data/markets.json', 'r') as f:
    markets_data = json.load(f)
    markets = markets_data['markets']

# Load butchers data
with open('data/butchers.json', 'r') as f:
    butchers_data = json.load(f)
    butchers = butchers_data['butchers']

# Load news data
with open('data/news.json', 'r') as f:
    news_data = json.load(f)
    news_items = news_data['news']

def ensure_dir(path: str):
    """Create directory if it doesn't exist"""
    Path(path).mkdir(parents=True, exist_ok=True)

def write_page(path: str, content: str):
    """Write HTML content to file"""
    ensure_dir(os.path.dirname(path))
    route = '/' + path.removesuffix('index.html')
    section = '/listings/' if route.startswith('/listings/') else None
    if route != '/' and re.search(r'class="listings-section"', content):
        section = '/listings/'
    for prefix in ('/deals/', '/markets/', '/beyond-beef/', '/news/', '/guides/', '/about/'):
        if route.startswith(prefix):
            section = '/guides/wagyu-vs-akaushi/' if prefix == '/guides/' else prefix
    if section:
        content = content.replace(f'<li><a href="{section}">', f'<li><a href="{section}" aria-current="page">', 1)
    content = content.replace('__PAGE_URL__', 'https://acreandplate.com' + route)
    with open(path, 'w') as f:
        f.write(content)
    print(f"✓ {path}")

DEFAULT_OG_IMAGE = 'https://acreandplate.com/assets/og-news-default.png'

def default_social_tags(title: str, meta_description: str, existing: str = "") -> str:
    """Site-wide Open Graph + Twitter card defaults; skips anything a page already sets.
    __PAGE_URL__ is filled in by write_page() with the page's canonical URL."""
    import html as _html
    def attr(v):
        return _html.escape(_html.unescape(v), quote=True)
    full_title = attr(f"{title} | Acre & Plate")
    desc = attr(meta_description)
    tags = []
    if 'rel="canonical"' not in existing:
        tags.append('<link rel="canonical" href="__PAGE_URL__">')
    if 'property="og:title"' not in existing:
        tags += [
            '<meta property="og:type" content="website">',
            '<meta property="og:site_name" content="Acre &amp; Plate">',
            f'<meta property="og:title" content="{full_title}">',
            f'<meta property="og:description" content="{desc}">',
            '<meta property="og:url" content="__PAGE_URL__">',
            f'<meta property="og:image" content="{DEFAULT_OG_IMAGE}">',
            '<meta property="og:image:width" content="1200">',
            '<meta property="og:image:height" content="630">',
            '<meta property="og:image:alt" content="Acre &amp; Plate: ranch-direct beef from named herds">',
        ]
    if 'name="twitter:card"' not in existing:
        tags += [
            '<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:title" content="{full_title}">',
            f'<meta name="twitter:description" content="{desc}">',
            f'<meta name="twitter:image" content="{DEFAULT_OG_IMAGE}">',
        ]
    return ("\n    " + "\n    ".join(tags)) if tags else ""

def base_template(title: str, content: str, meta_description: str = "", og_tags: str = "") -> str:
    """Base HTML template for all pages"""
    if not meta_description:
        meta_description = "Find local, sustainable, ranch-direct beef—Fullblood Wagyu, Akaushi, Japanese Black, and rare heritage breeds from ranches you can trace."
    og_tags = og_tags + default_social_tags(title, meta_description, og_tags)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Acre & Plate</title>
    <meta name="description" content="{meta_description}">
    {og_tags}
    <link rel="icon" type="image/png" href="/assets/brand/rocking-ap-mark.png">
    <link rel="stylesheet" href="/css/site.css">
</head>
<body>
    <a class="skip-link" href="#main-content">Skip to content</a>
    <header>
        <nav class="container">
            <div class="logo">
                <a href="/" aria-label="Acre & Plate home">
                    <span class="brand-star" aria-hidden="true">✦</span>
                    <span><strong>Acre & Plate</strong><small>Ranch direct · Rooted in good ground</small></span>
                </a>
            </div>
            <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu" onclick="var h=this.closest('header'),o=h.classList.toggle('nav-open');this.setAttribute('aria-expanded',o);this.setAttribute('aria-label',o?'Close menu':'Open menu')"><span></span><span></span><span></span></button>
            <ul class="nav-links" id="site-nav">
                <li><a href="/listings/">Browse</a></li>
                <li><a href="/deals/">Deals</a></li>
                <li><a href="/markets/">Markets</a></li>
                <li><a href="/beyond-beef/">Beyond Beef</a></li>
                <li><a href="/news/">News</a></li>
                <li><a href="https://acreandplate.printful.me/" target="_blank" rel="noopener noreferrer">Shop</a></li>
                <li><a href="/guides/wagyu-vs-akaushi/">Guide</a></li>
                <li><a href="/about/">About</a></li>
            </ul>
        </nav>
    </header>
    
    <main id="main-content">
        {content}
    </main>
    
    <footer>
        <div class="container">
            <p class="tagline">Ranch-direct beef for people who care where dinner came from—local pasture, named herds, honest sourcing.</p>
            <p class="disclaimer">Acre & Plate connects you with ranches raising cattle with traceable genetics. We do not sell beef. Contact ranches directly. Claims verified from public ranch websites as of {get_build_date()}.</p>
            <p class="links">
                <a href="/about/">About This Directory</a> · 
                <a href="/listings/">All Ranches</a> · 
                <a href="/beyond-beef/">Beyond Beef</a> · {footer_prime_rib()}
                <a href="https://acreandplate.printful.me/" target="_blank" rel="noopener noreferrer">Shop</a> · 
                <a href="mailto:hello@acreandplate.com">Contact</a> · 
                <a href="https://www.instagram.com/acreandplate/" target="_blank" rel="noopener">Instagram</a> · 
                <a href="/privacy/">Privacy</a> · 
                <a href="/terms/">Terms</a>
            </p>
        </div>
    </footer>
    <script src="/assets/filter.js" defer></script>
</body>
</html>"""

def footer_prime_rib() -> str:
    """Footer link to the holiday price board, shown only in season and only if its data loads."""
    return '<a href="/prime-rib-price/">Prime Rib Prices</a> · ' if (prime_rib_season_active() and prime_rib_cached()) else ''

def get_build_date() -> str:
    """Get current date for footer"""
    from datetime import datetime
    return datetime.now().strftime("%B %Y")

def breed_chip(breed: str) -> str:
    """Generate breed chip HTML"""
    breed_map = {
        'wagyu': 'Wagyu',
        'akaushi': 'Akaushi',
        'heritage': 'Heritage',
        'randall-lineback': 'Randall Lineback',
        'dexter': 'Dexter',
        'piedmontese': 'Piedmontese'
    }
    return f'<span class="breed-chip breed-{breed}">{breed_map.get(breed, breed)}</span>'

def add_utm_params(url: str, listing_id: str = None) -> str:
    """Add UTM parameters to ranch URLs"""
    separator = '&' if '?' in url else '?'
    utm = f"{separator}utm_source=acreandplate&utm_medium=referral&utm_campaign=directory"
    if listing_id:
        utm += f"&utm_content={listing_id}"
    return url + utm

def get_active_featured_placements() -> List[Dict[str, Any]]:
    """Get currently active featured placements with their listings"""
    from datetime import datetime
    
    active = []
    now = datetime.now().isoformat()
    
    for placement in featured_placements:
        # Check if placement is active (within date range if specified)
        is_active = True
        
        if placement.get('starts_at'):
            is_active = is_active and now >= placement['starts_at']
        
        if placement.get('ends_at'):
            is_active = is_active and now <= placement['ends_at']
        
        if is_active:
            # Find the corresponding listing
            listing = next((l for l in listings if l['slug'] == placement['listing_id']), None)
            if listing:
                active.append({
                    'placement': placement,
                    'listing': listing
                })
    
    return active

def get_best_deals_by_cut() -> Dict[str, Dict[str, Any]]:
    """Get the best deal for each cut type"""
    best_by_cut = {}
    
    for deal in deals:
        cut = deal['cut']
        
        # Calculate discount percentage
        discount_pct = 0
        if deal.get('regular_price') and deal['regular_price'] > 0:
            discount_pct = ((deal['regular_price'] - deal['sale_price']) / deal['regular_price']) * 100
        
        # If we don't have this cut yet, or this deal is better, save it
        if cut not in best_by_cut:
            best_by_cut[cut] = {'deal': deal, 'discount_pct': discount_pct}
        else:
            # Compare by absolute price (lower is better)
            if deal['sale_price'] < best_by_cut[cut]['deal']['sale_price']:
                best_by_cut[cut] = {'deal': deal, 'discount_pct': discount_pct}
    
    return best_by_cut

def deal_card(deal: Dict[str, Any]) -> str:
    """Generate deal card HTML"""
    # Calculate discount percentage
    discount_pct = 0
    discount_html = ''
    price_html = f'<span class="sale-price">${deal["sale_price"]:.2f}</span>'
    
    if deal.get('regular_price') and deal['regular_price'] > 0:
        discount_pct = ((deal['regular_price'] - deal['sale_price']) / deal['regular_price']) * 100
        discount_html = f'<span class="discount-badge">-{discount_pct:.0f}%</span>'
        price_html = f'<span class="regular-price">${deal["regular_price"]:.2f}</span> <span class="sale-price">${deal["sale_price"]:.2f}</span>'
    
    # Get listing link if available
    listing_link_html = ''
    if deal.get('listing_id'):
        listing_link_html = f'<a href="/listings/{deal["listing_id"]}/" class="btn-secondary">View Ranch</a>'
    
    gaps_html = ''
    if deal.get('gaps'):
        gaps_html = f'<p class="note">{deal["gaps"]}</p>'
    
    verified_date = deal.get('verified_at', '')
    
    # Add UTM parameters to product URL
    product_url = add_utm_params(deal['product_url'], deal.get('listing_id'))
    
    return f"""<article class="deal-card">
        <div class="deal-header">
            <span class="season-badge">{deal['season_label']}</span>
            {discount_html}
        </div>
        <h3><a href="{product_url}" target="_blank" rel="noopener">{deal['product_name']}</a></h3>
        <div class="ranch-name">{deal['ranch_name']}</div>
        <div class="cut-type">{deal['cut'].replace('-', ' ').title()}</div>
        <div class="deal-price">
            {price_html}
            <span class="unit">/ {deal['unit']}</span>
        </div>
        <p class="deal-reason">{deal['reason']}</p>
        {gaps_html}
        <div class="deal-verified">Verified {verified_date}</div>
        <div class="actions">
            {listing_link_html}
            <a href="{product_url}" target="_blank" rel="noopener" class="btn-primary">View Deal →</a>
        </div>
    </article>"""

def filter_metadata(listing):
    """Use current source text; do not import stale claims from the old preview."""
    item = dict(listing)
    text = ' '.join(str(listing.get(k, '')) for k in ('genetics', 'description', 'note')).lower()
    shipping = listing.get('shipping', '').lower()
    grass = bool(re.search(r'grass[- ]finished|grass[- ]fed (?:&|and) finished', text))
    grain = bool(re.search(r'(?<!no )grain[- ]finish|fermented grain finish', text))
    if grass and grain: item['finish'] = 'grass-or-grain'
    elif grain: item['finish'] = 'grain-finished'
    elif grass: item['finish'] = 'grass-finished'
    # Explicit destination wording takes priority over local delivery mentions.
    if re.search(r'continental|contiguous|lower.?48|48 contiguous', shipping): item['ships_scope'] = 'lower-48'
    elif re.search(r'(?<!not )nationwide|all 50|throughout us|domestic usa', shipping): item['ships_scope'] = 'nationwide'
    elif 'pickup only' in shipping or 'no shipping' in shipping or 'in-person pickup' in shipping or 'butcher pickup at' in shipping: item['ships_scope'] = 'none'
    elif re.search(r'local delivery|regional|ships to wa|elsewhere in ca|across all of ohio|delivery to select|delivery between|florida only|delivery to nashville', shipping): item['ships_scope'] = 'regional'
    elif 'ship' in shipping: item['ships_scope'] = 'available'
    if 'pickup' in shipping and 'no pickup' not in shipping: item['pickup'] = True
    certs = []
    if 'audubon' in text and ('certified' in text or 'certification' in text): certs.append('Audubon Bird Friendly')
    if re.search(r'certified (?:grassfed )?by (?:the )?american grassfed|american grassfed association certified|certified grassfed by american grassfed', text): certs.append('AGA Certified Grassfed')
    if 'non-gmo verified' in text: certs.append('Non-GMO Verified')
    item['certs'] = certs
    item['pet_products'] = any(re.search(r'pet|dog food|dog treat', product.lower()) for product in listing.get('products', []))
    return item

def filter_bar(listings: List[Dict[str, Any]]) -> str:
    """Generate filter bar HTML for a list of listings"""
    import html
    
    listings = [filter_metadata(l) for l in listings]

    # Collect unique values from this page's listings
    finish_opts = {}
    ships_opts = {}
    pickup_count = 0
    cert_opts = {}
    pet_count = 0
    
    for listing in listings:
        finish = listing.get('finish')
        if finish:
            finish_opts[finish] = finish_opts.get(finish, 0) + 1
        
        ships = listing.get('ships_scope')
        if ships:
            ships_opts[ships] = ships_opts.get(ships, 0) + 1
        
        if listing.get('pickup'):
            pickup_count += 1
        
        certs = listing.get('certs', [])
        for cert in certs:
            cert_opts[cert] = cert_opts.get(cert, 0) + 1
        
        # Check for pet products
        if listing.get('pet_products'):
            pet_count += 1
        else:
            # Also check products array
            products_text = ' '.join(listing.get('products', [])).lower()
            if ('pet' in products_text or 'dog food' in products_text or 'dog treat' in products_text) and 'hot dog' not in products_text:
                pet_count += 1
    
    # Build filter groups
    filters_html = []
    
    # Free-text search
    filters_html.append('''
        <div class="filter-group">
            <label class="filter-label" for="filter-search">Search ranches</label>
            <input type="search" id="filter-search" class="filter-search" placeholder="Ranch name, town, state, or breed…">
        </div>
    ''')
    
    # Finish filter (only if there are options)
    if finish_opts:
        finish_labels = {
            'grass-finished': 'Grass-finished',
            'mostly-grass-fed': 'Mostly grass-fed',
            'grain-finished': 'Grain-finished',
            'grass-or-grain': 'Grass or grain'
        }
        chips = []
        for val in sorted(finish_opts.keys()):
            label = finish_labels.get(val, val.replace('-', ' ').title())
            count = finish_opts[val]
            chips.append(f'<button class="filter-chip" data-filter="finish" data-value="{html.escape(val)}">{html.escape(label)} <span class="count">({count})</span></button>')
        
        filters_html.append(f'''
            <div class="filter-group">
                <label class="filter-label">Finish</label>
                <div class="filter-chips">{"".join(chips)}</div>
            </div>
        ''')
    
    # Shipping filter
    if ships_opts:
        ships_labels = {
            'nationwide': 'Ships nationwide',
            'lower-48': 'Ships lower 48',
            'regional': 'Regional delivery / shipping',
            'none': 'No shipping', 'available': 'Shipping available; area unspecified'
        }
        chips = []
        for val in ['nationwide', 'lower-48', 'regional', 'available', 'none']:
            if val in ships_opts:
                label = ships_labels[val]
                count = ships_opts[val]
                chips.append(f'<button class="filter-chip" data-filter="ships" data-value="{html.escape(val)}">{html.escape(label)} <span class="count">({count})</span></button>')
        
        filters_html.append(f'''
            <div class="filter-group">
                <label class="filter-label">Shipping</label>
                <div class="filter-chips">{"".join(chips)}</div>
            </div>
        ''')
    
    # Pickup filter
    if pickup_count > 0:
        filters_html.append(f'''
            <div class="filter-group">
                <label class="filter-label">Pickup</label>
                <div class="filter-chips">
                    <button class="filter-chip" data-filter="pickup" data-value="true">Local/ranch pickup <span class="count">({pickup_count})</span></button>
                </div>
            </div>
        ''')
    
    # Certifications filter
    if cert_opts:
        chips = []
        for cert in sorted(cert_opts.keys()):
            count = cert_opts[cert]
            # Shorten long cert names
            short_cert = cert.replace('AGA Certified Grassfed', 'AGA Grassfed').replace('USDA Organic', 'Organic')
            chips.append(f'<button class="filter-chip" data-filter="cert" data-value="{html.escape(cert)}">{html.escape(short_cert)} <span class="count">({count})</span></button>')
        
        filters_html.append(f'''
            <div class="filter-group">
                <label class="filter-label">Certifications</label>
                <div class="filter-chips">{"".join(chips)}</div>
            </div>
        ''')
    
    # Pet products filter
    if pet_count > 0:
        filters_html.append(f'''
            <div class="filter-group">
                <label class="filter-label">Products</label>
                <div class="filter-chips">
                    <button class="filter-chip" data-filter="pet" data-value="true">Pet food & treats <span class="count">({pet_count})</span></button>
                </div>
            </div>
        ''')
    
    total_count = len(listings)
    
    states = sorted({state for l in listings for state in l['state'].split('/') if state})
    breeds = sorted({breed for l in listings for breed in l.get('breeds', [])})
    state_options = ''.join(f'<option value="{html.escape(v)}">{html.escape(v)}</option>' for v in states)
    breed_options = ''.join(f'<option value="{html.escape(v)}">{html.escape(v.replace("-", " ").title())}</option>' for v in breeds)
    return f'''
    <div class="filter-bar" hidden>
        <div class="filter-basics">
            {filters_html[0]}
            <div class="filter-group"><label for="filter-state" class="filter-label">State</label><select id="filter-state"><option value="">All states</option>{state_options}</select></div>
            <div class="filter-group"><label for="filter-breed" class="filter-label">Breed</label><select id="filter-breed"><option value="">All breeds</option>{breed_options}</select></div>
        </div>
        <details class="filter-more"><summary>More filters: finish, shipping & pickup</summary><div class="filter-panel">{"".join(filters_html[1:])}</div><p class="filter-help">Filters use details recorded in each ranch listing. Unspecified details are not treated as a match; confirm current options with the ranch.</p></details>
        <div class="filter-summary"><span class="filter-count" role="status" aria-live="polite">Showing <strong id="shown-count">{total_count}</strong> of <strong id="total-count">{total_count}</strong> ranches</span><button type="button" class="filter-clear" hidden>Clear filters</button></div>
        <div class="filter-empty" hidden><p>No ranches match your filters. <button type="button" class="filter-clear-inline">Clear filters</button> to see all listings.</p></div>
    </div>
    '''

def listing_card(listing: Dict[str, Any], show_full: bool = False, featured_badge: bool = False) -> str:
    """Generate listing card HTML"""
    breeds_html = ''.join([breed_chip(b) for b in listing['breeds']])
    
    products_text = ', '.join(listing['products'][:3])
    if len(listing['products']) > 3:
        products_text += '…'
    
    shipping_class = ''
    shipping_text = listing['shipping']
    if 'pickup' in shipping_text.lower() or 'florida only' in shipping_text.lower():
        shipping_class = ' limited'
    
    note_html = ''
    if 'note' in listing:
        note_html = f'<p class="note">{listing["note"]}</p>'
    
    featured_html = ''
    if featured_badge:
        featured_html = '<div class="featured-badge">Featured Partner</div>'
    
    ranch_url = add_utm_params(listing['url'], listing['slug'])
    
    metadata = filter_metadata(listing)
    attrs = {'name': listing['name'].lower(), 'city': listing['city'].lower(), 'state': listing['state'], 'breeds': ' '.join(listing.get('breeds', [])), 'search': ' '.join([listing['name'], listing['city'], listing['state'], listing.get('genetics', ''), *listing.get('breeds', [])]).lower()}
    for key, field in [('finish','finish'), ('ships','ships_scope')]:
        attrs[key] = metadata.get(field, '')
    attrs['pickup'] = 'true' if metadata.get('pickup') else ''
    attrs['pet'] = 'true' if metadata.get('pet_products') else ''
    attrs['certs'] = '|'.join(metadata.get('certs', []))
    data_attrs = ' '.join(f'data-{key}="{html_tools.escape(value, quote=True)}"' for key, value in attrs.items())
    return f"""<article class="listing-card" {data_attrs}>
        {featured_html}
        <h3><a href="/listings/{listing['slug']}/">{listing['name']}</a></h3>
        <div class="location">{listing['city']}, {listing['state']}</div>
        <div class="breeds">{breeds_html}</div>
        <p class="genetics">{listing['genetics']}</p>
        <p class="products"><strong>Products:</strong> {products_text}</p>
        <p class="shipping{shipping_class}"><strong>Shipping:</strong> {shipping_text}</p>
        {note_html}
        <div class="actions">
            <a href="/listings/{listing['slug']}/" class="btn-secondary">View Details</a>
            <a href="{ranch_url}" target="_blank" rel="noopener" class="btn-primary">Visit Ranch →</a>
        </div>
    </article>"""

def build_index():
    """Build home page"""
    # Get active featured placements (paid)
    active_featured = get_active_featured_placements()
    premium_featured = [f for f in active_featured if f['placement']['tier'] == 'premium']
    standard_featured = [f for f in active_featured if f['placement']['tier'] == 'standard']
    
    # Build featured ranch section if there are any active
    featured_ranch_html = ''
    if active_featured:
        featured_cards = []
        # Show premium first, then standard
        for featured in premium_featured + standard_featured:
            featured_cards.append(listing_card(featured['listing'], featured_badge=True))
        
        featured_ranch_html = f"""
    <section class="featured-ranch-section">
        <div class="container">
            <h2>Featured Ranch Partners</h2>
            <p class="section-intro">Featured ranch placements—ranches committed to traceable bloodlines and transparent sourcing. <a href="/featured/">Learn about Featured Ranch placement</a></p>
            <div class="listings-grid">
                {''.join(featured_cards[:4])}
            </div>
        </div>
    </section>
    """
    
    # Original featured ranches (editorial picks)
    featured = [l for l in listings if l.get('featured', False)]
    
    featured_html = '\n'.join([listing_card(l) for l in featured[:3]])
    
    # Get best deals by cut for seasonal deals section
    best_by_cut = get_best_deals_by_cut()
    top_deals = sorted(best_by_cut.items(), key=lambda x: x[1]['discount_pct'], reverse=True)[:3]
    
    deals_html = ''
    if top_deals:
        deals_cards = '\n'.join([deal_card(item[1]['deal']) for item in top_deals])
        deals_html = f"""
    <section class="seasonal-deals">
        <div class="container">
            <p class="eyebrow">Straight from the ranch</p>
            <h2>Good beef. A better buy.</h2>
            <p class="deals-subtitle">Seasonal deals & overstock</p>
            <p class="section-intro">The best current deals across ranches—sale, clearance, and overstock inventory verified from ranch websites.</p>
            <div class="deals-grid">
                {deals_cards}
            </div>
            <div class="view-all">
                <a href="/deals/" class="btn-primary">View All {len(deals)} Deals</a>
            </div>
            <p class="deals-disclaimer">⚠️ Prices verified {deals[0].get('verified_at', '')} — confirm current availability and pricing on ranch websites before ordering.</p>
        </div>
    </section>
    """
    
    content = f"""
    {prime_rib_home_banner()}
    <section class="heritage-hero">
        <div class="container hero-layout">
            <div class="heritage-copy">
                <p class="eyebrow">From the pasture. For your table.</p>
                <h1>Good food.<br><em>Good ground.</em></h1>
                <p class="hero-deck">Know the ranch behind your beef.</p>
                <p class="hero-description">Find exceptional ranch-direct beef from named herds with traceable genetics—from open pasture to your plate.</p>
                <div class="hero-actions">
                    <a href="/listings/" class="btn-primary">Find your ranch <span aria-hidden="true">↗</span></a>
                    <a href="/guides/cattle-breeds/" class="text-link">Get to know your beef →</a>
                </div>
            </div>
            <div class="ranch-emblem" aria-label="Acre and Plate ranch emblem">
                <p class="emblem-top">Pasture to plate.</p>
                <img src="/assets/brand/rocking-ap-mark.png" width="1224" height="1285" alt="Engraved cattle head above the Acre & Plate rocking AP brand" fetchpriority="high">
                <p class="emblem-bottom">Named herds. Honest sourcing.</p>
                <span class="emblem-star" aria-hidden="true">✦</span>
            </div>
        </div>
        <div class="container hero-ledger">
            <span><strong>{len(listings)}</strong> ranches to discover</span>
            <span><strong>Real roots.</strong> Traceable bloodlines</span>
            <span><strong>Ranch direct.</strong> From their land to your table</span>
        </div>
    </section>

    <section class="ranch-finder" aria-labelledby="finder-title">
        <div class="container">
            <div class="section-heading"><div><p class="eyebrow">01 / The ranch directory</p><h2 id="finder-title">Find your kind of good.</h2></div><a href="/listings/" class="text-link">Explore all {len(listings)} ranches ↗</a></div>
            <div class="breed-paths">
                <a href="/wagyu/"><span class="path-number">01</span><h3>Wagyu</h3><p>Discover registered and DNA-verified Japanese bloodlines.</p><span class="path-bottom">{len([l for l in listings if 'wagyu' in l['breeds']])} ranches <b aria-hidden="true">↗</b></span></a>
                <a href="/akaushi/"><span class="path-number">02</span><h3>Akaushi</h3><p>Explore Japanese Brown cattle with traceable heritage.</p><span class="path-bottom">{len([l for l in listings if 'akaushi' in l['breeds']])} ranches <b aria-hidden="true">↗</b></span></a>
                <a href="/heritage/"><span class="path-number">03</span><h3>Heritage breeds</h3><p>Meet distinctive breeds and the ranches keeping them thriving.</p><span class="path-bottom">{len([l for l in listings if 'heritage' in l.get('breeds', [])])} ranches <b aria-hidden="true">↗</b></span></a>
            </div>
            <details class="state-directory"><summary>Looking closer to home? <span>Browse by state +</span></summary><div class="hub-links">
                <a href="/alabama/" class="hub-link">Alabama <span class="count">({len([l for l in listings if l.get('state') == 'AL'])})</span></a>
                <a href="/alaska/" class="hub-link">Alaska <span class="count">({len([l for l in listings if l.get('state') == 'AK'])})</span></a>
                <a href="/arizona/" class="hub-link">Arizona <span class="count">({len([l for l in listings if l.get('state') == 'AZ'])})</span></a>
                <a href="/arkansas/" class="hub-link">Arkansas <span class="count">({len([l for l in listings if l.get('state') == 'AR'])})</span></a>
                <a href="/illinois/" class="hub-link">Illinois <span class="count">({len([l for l in listings if l.get('state') == 'IL'])})</span></a>
                <a href="/indiana/" class="hub-link">Indiana <span class="count">({len([l for l in listings if l.get('state') == 'IN'])})</span></a>
                <a href="/iowa/" class="hub-link">Iowa <span class="count">({len([l for l in listings if l.get('state') == 'IA'])})</span></a>
                <a href="/kansas/" class="hub-link">Kansas <span class="count">({len([l for l in listings if l.get('state') == 'KS'])})</span></a>
                <a href="/kentucky/" class="hub-link">Kentucky <span class="count">({len([l for l in listings if l.get('state') == 'KY'])})</span></a>
                <a href="/louisiana/" class="hub-link">Louisiana <span class="count">({len([l for l in listings if l.get('state') == 'LA'])})</span></a>
                <a href="/maine/" class="hub-link">Maine <span class="count">({len([l for l in listings if l.get('state') == 'ME'])})</span></a>
                <a href="/maryland/" class="hub-link">Maryland <span class="count">({len([l for l in listings if l.get('state') == 'MD'])})</span></a>
                <a href="/massachusetts/" class="hub-link">Massachusetts <span class="count">({len([l for l in listings if l.get('state') == 'MA'])})</span></a>
                <a href="/michigan/" class="hub-link">Michigan <span class="count">({len([l for l in listings if l.get('state') == 'MI'])})</span></a>
                <a href="/minnesota/" class="hub-link">Minnesota <span class="count">({len([l for l in listings if l.get('state') == 'MN'])})</span></a>
                <a href="/mississippi/" class="hub-link">Mississippi <span class="count">({len([l for l in listings if l.get('state') == 'MS'])})</span></a>
                <a href="/missouri/" class="hub-link">Missouri <span class="count">({len([l for l in listings if l.get('state') == 'MO'])})</span></a>
                <a href="/nebraska/" class="hub-link">Nebraska <span class="count">({len([l for l in listings if l.get('state') == 'NE'])})</span></a>
                <a href="/nevada/" class="hub-link">Nevada <span class="count">({len([l for l in listings if l.get('state') == 'NV'])})</span></a>
                <a href="/new-hampshire/" class="hub-link">New Hampshire <span class="count">({len([l for l in listings if l.get('state') == 'NH'])})</span></a>
                <a href="/new-jersey/" class="hub-link">New Jersey <span class="count">({len([l for l in listings if l.get('state') == 'NJ'])})</span></a>
                <a href="/new-mexico/" class="hub-link">New Mexico <span class="count">({len([l for l in listings if l.get('state') == 'NM'])})</span></a>
                <a href="/new-york/" class="hub-link">New York <span class="count">({len([l for l in listings if l.get('state') == 'NY'])})</span></a>
                <a href="/north-carolina/" class="hub-link">North Carolina <span class="count">({len([l for l in listings if l.get('state') == 'NC'])})</span></a>
                <a href="/north-dakota/" class="hub-link">North Dakota <span class="count">({len([l for l in listings if l.get('state') == 'ND'])})</span></a>
                <a href="/ohio/" class="hub-link">Ohio <span class="count">({len([l for l in listings if l.get('state') == 'OH'])})</span></a>
                <a href="/texas/" class="hub-link">Texas <span class="count">({len([l for l in listings if l['state'] == 'TX'])})</span></a>
                <a href="/california/" class="hub-link">California <span class="count">({len([l for l in listings if l['state'] == 'CA' or 'CA' in l.get('state', '')])})</span></a>
                <a href="/colorado/" class="hub-link">Colorado <span class="count">({len([l for l in listings if l['state'] == 'CO'])})</span></a>
                <a href="/connecticut/" class="hub-link">Connecticut <span class="count">({len([l for l in listings if l.get('state') == 'CT'])})</span></a>
                <a href="/delaware/" class="hub-link">Delaware <span class="count">({len([l for l in listings if l.get('state') == 'DE'])})</span></a>
                <a href="/florida/" class="hub-link">Florida <span class="count">({len([l for l in listings if l['state'] == 'FL'])})</span></a>
                <a href="/georgia/" class="hub-link">Georgia <span class="count">({len([l for l in listings if l.get('state') == 'GA'])})</span></a>
                <a href="/hawaii/" class="hub-link">Hawaii <span class="count">({len([l for l in listings if l.get('state') == 'HI'])})</span></a>
                <a href="/idaho/" class="hub-link">Idaho <span class="count">({len([l for l in listings if 'ID' in l.get('state', '')])})</span></a>
                <a href="/montana/" class="hub-link">Montana <span class="count">({len([l for l in listings if l.get('state') == 'MT'])})</span></a>
                <a href="/oklahoma/" class="hub-link">Oklahoma <span class="count">({len([l for l in listings if l.get('state') == 'OK'])})</span></a>
                <a href="/oregon/" class="hub-link">Oregon <span class="count">({len([l for l in listings if l['state'] == 'OR'])})</span></a>
                <a href="/pennsylvania/" class="hub-link">Pennsylvania <span class="count">({len([l for l in listings if l.get('state') == 'PA'])})</span></a>
                <a href="/rhode-island/" class="hub-link">Rhode Island <span class="count">({len([l for l in listings if l.get('state') == 'RI'])})</span></a>
                <a href="/south-carolina/" class="hub-link">South Carolina <span class="count">({len([l for l in listings if l.get('state') == 'SC'])})</span></a>
                <a href="/south-dakota/" class="hub-link">South Dakota <span class="count">({len([l for l in listings if l.get('state') == 'SD'])})</span></a>
                <a href="/tennessee/" class="hub-link">Tennessee <span class="count">({len([l for l in listings if l.get('state') == 'TN'])})</span></a>
                <a href="/utah/" class="hub-link">Utah <span class="count">({len([l for l in listings if l.get('state') == 'UT'])})</span></a>
                <a href="/vermont/" class="hub-link">Vermont <span class="count">({len([l for l in listings if l.get('state') == 'VT'])})</span></a>
                <a href="/virginia/" class="hub-link">Virginia <span class="count">({len([l for l in listings if l.get('state') == 'VA'])})</span></a>
                <a href="/washington/" class="hub-link">Washington <span class="count">({len([l for l in listings if l['state'] == 'WA'])})</span></a>
                <a href="/west-virginia/" class="hub-link">West Virginia <span class="count">({len([l for l in listings if l.get('state') == 'WV'])})</span></a>
                <a href="/wyoming/" class="hub-link">Wyoming <span class="count">({len([l for l in listings if 'WY' in l.get('state', '')])})</span></a>
            </div></details>
        </div>
    </section>

    {featured_ranch_html}

    <section class="featured heritage-featured">
        <div class="container">
            <div class="section-heading"><div><p class="eyebrow">Meet the people behind the pasture</p><h2>A few good places to start.</h2></div><span class="section-note">Featured ranches<br>Selected from the directory</span></div>
            <div class="listings-grid">{featured_html}</div>
            <div class="view-all"><a href="/listings/" class="text-link">View all {len(listings)} ranches →</a></div>
        </div>
    </section>

    {deals_html}

    <section class="markets-teaser heritage-markets">
        <div class="container market-layout">
            <div><p class="eyebrow">02 / Around your table</p><h2>Good food.<br>Closer to home.</h2><p class="section-intro">Find farmers markets where local ranchers sell beef from named herds, plus butcher shops where Bay Area residents buy quality beef.</p><a href="/markets/" class="btn-primary">Markets & butchers ↗</a></div>
            <div class="markets-preview">
                {''.join([f'<a class="market-preview-item" href="/markets/"><span class="market-index">0{i + 1}</span><div><strong>{m["name"]}</strong><span>{m["city"]}, {m["state"]} — {m["schedule"].split(",")[0]}</span></div><b aria-hidden="true">↗</b></a>' for i, m in enumerate(markets[:3])])}
            </div>
        </div>
    </section>

    <section class="how-it-works heritage-how">
        <div class="container"><p class="eyebrow">A shorter path from pasture to plate</p><h2>Know more. Eat well.</h2>
            <div class="steps">
                <div class="step"><div class="step-number">01</div><h3>Find your ranch.</h3><p>Explore ranches with named, traceable herds—Fullblood Wagyu, Akaushi, heritage breeds.</p></div>
                <div class="step"><div class="step-number">02</div><h3>Know your source.</h3><p>Each ranch lists their cattle's bloodlines, breed registrations, or DNA verification. Real sourcing, not marketing.</p></div>
                <div class="step"><div class="step-number">03</div><h3>Order direct.</h3><p>Contact ranches directly. Most ship nationwide, some offer local pickup.</p></div>
            </div>
        </div>
    </section>

    <section class="field-notes">
        <div class="container"><div class="section-heading"><div><p class="eyebrow">03 / The field guide</p><h2>A little knowledge goes a long way.</h2></div></div>
            <div class="guide-paths"><a href="/guides/cattle-breeds/"><span class="eyebrow">Start with the herd</span><h3>Get to know the breeds.</h3><p>A closer look at the cattle behind your beef.</p><span class="text-link">Read the breeds guide →</span></a><a href="/guides/wagyu-vs-akaushi/"><span class="eyebrow">Know the difference</span><h3>Wagyu & Akaushi, explained.</h3><p>Understand the bloodlines before you buy.</p><span class="text-link">Explore the guide →</span></a><a href="/news/"><span class="eyebrow">From the field</span><h3>The latest from ranch country.</h3><p>Follow the news, updates, and stories.</p><span class="text-link">Read the latest →</span></a></div>
        </div>
    </section>

    <section class="heritage-shop">
        <div class="container shop-layout">
            <figure><img src="/assets/brand/heritage-ranchwear.webp" width="1536" height="1024" loading="lazy" alt="Acre & Plate heritage apparel concepts: cream ranch illustration sweatshirt and washed sage Western lettering sweatshirt"><figcaption>From the Acre & Plate design collection · Styles available in the shop may vary.</figcaption></figure>
            <div class="shop-copy"><p class="eyebrow">04 / Wear your roots</p><h2>Good ground.<br>Good company.</h2><p>For the people who care where dinner came from. Take a little of that pasture-to-plate spirit with you.</p><a href="https://acreandplate.printful.me/" target="_blank" rel="noopener noreferrer" class="btn-primary">Visit the Acre & Plate shop ↗</a><span class="shop-signoff">Pasture to plate.</span></div>
        </div>
    </section>
    """

    html = base_template("Home", "\n".join(line.rstrip() for line in content.splitlines()))
    write_page('index.html', html)

def build_listings_index():
    """Build all listings page"""
    all_cards = '\n'.join([listing_card(l) for l in listings])
    
    content = f"""
    <section class="page-header">
        <div class="container">
            <h1>All Ranches</h1>
            <p>{len(listings)} ranches with named herds, registered cattle, or DNA-verified bloodlines</p>
        </div>
    </section>
    
    {prime_rib_callout('general')}
    <section class="listings-section">
        <div class="container">
            {filter_bar(listings)}
            <div class="listings-grid">
                {all_cards}
            </div>
        </div>
    </section>
    """
    
    html = base_template("All Ranches", content, "Complete directory of ranch-direct beef with traceable bloodlines and named herds.")
    write_page('listings/index.html', html)

def build_listing_detail(listing: Dict[str, Any]):
    """Build individual listing page"""
    breeds_html = ''.join([breed_chip(b) for b in listing['breeds']])
    
    products_list = '</li><li>'.join(listing['products'])
    
    phone_html = ''
    if 'phone' in listing:
        phone_html = f'<p><strong>Phone:</strong> {listing["phone"]}</p>'

    instagram_html = ''
    if listing.get('instagram'):
        instagram_html = (
            '\n                    '
            f'<p><strong>Instagram:</strong> '
            f'<a href="{listing["instagram"]}" target="_blank" rel="noopener">Instagram</a></p>'
        )
    
    note_html = ''
    if 'note' in listing:
        note_html = f'<div class="note-box"><strong>Note:</strong> {listing["note"]}</div>'
    
    content = f"""
    <section class="page-header">
        <div class="container">
            <div class="breadcrumb">
                <a href="/">Home</a> / <a href="/listings/">All Ranches</a> / {listing['name']}
            </div>
            <h1>{listing['name']}</h1>
            <div class="location">{listing['city']}, {listing['state']}</div>
            <div class="breeds">{breeds_html}</div>
        </div>
    </section>
    
    <section class="listing-detail">
        <div class="container">
            <div class="detail-main">
                <h2>Genetics</h2>
                <p class="genetics-detail">{listing['genetics']}</p>
                
                <h2>About</h2>
                <p>{listing.get('description', '')}</p>
                
                {note_html}
                
                <h2>Products Available</h2>
                <ul class="products-list">
                    <li>{products_list}</li>
                </ul>
                
                {prime_rib_callout('ranch', slug=listing['slug'])}
                
                <h2>Shipping</h2>
                <p>{listing['shipping']}</p>
                
                <div class="contact-info">
                    <h2>Contact</h2>
                    <p><strong>Website:</strong> <a href="{listing['url']}" target="_blank" rel="noopener">{listing['url']}</a></p>
                    {phone_html}{instagram_html}
                </div>
                
                <div class="cta">
                    <a href="{add_utm_params(listing['url'], listing['slug'])}" target="_blank" rel="noopener" class="btn-primary">Visit Ranch Website →</a>
                </div>
            </div>
            
            <aside class="detail-sidebar">
                <div class="quick-facts">
                    <h3>Quick Facts</h3>
                    <dl>
                        <dt>Location</dt>
                        <dd>{listing['city']}, {listing['state']}</dd>
                        <dt>Breeds</dt>
                        <dd>{', '.join(listing['breeds'])}</dd>
                        <dt>Shipping</dt>
                        <dd>{listing['shipping']}</dd>
                    </dl>
                </div>
            </aside>
        </div>
    </section>
    """
    
    meta = f"{listing['name']} - {listing['genetics']} in {listing['city']}, {listing['state']}"
    html = base_template(listing['name'], content, meta)
    write_page(f"listings/{listing['slug']}/index.html", html)

def build_hub_page(title: str, slug: str, filter_fn, intro: str):
    """Build hub pages (Wagyu, Akaushi, Texas)"""
    filtered = [l for l in listings if filter_fn(l)]
    cards_html = '\n'.join([listing_card(l) for l in filtered])
    
    content = f"""
    <section class="page-header">
        <div class="container">
            <h1>{title}</h1>
            <p>{intro}</p>
            <p class="count">{len(filtered)} ranches</p>
        </div>
    </section>
    
    {prime_rib_callout('hub', hub_slugs=[l['slug'] for l in filtered])}
    <section class="listings-section">
        <div class="container">
            {filter_bar(filtered)}
            <div class="listings-grid">
                {cards_html}
            </div>
        </div>
    </section>
    """
    
    html = base_template(title, content, intro)
    write_page(f'{slug}/index.html', html)

def build_guide():
    """Build Wagyu vs Akaushi guide"""
    content = """
    <section class="page-header">
        <div class="container">
            <h1>Wagyu vs Akaushi: What's the Difference?</h1>
        </div>
    </section>
    
    <section class="guide-content">
        <div class="container">
            <article class="guide">
                <h2>The Quick Answer</h2>
                <p>Akaushi is a specific breed of Wagyu. "Wagyu" means Japanese cattle and includes four breeds: Japanese Black (Kuroge), Brown (Akaushi), Polled, and Shorthorn. In the U.S., "Wagyu" usually refers to Japanese Black, while Akaushi is specifically the Japanese Brown breed.</p>
                
                <h2>Wagyu (Usually Japanese Black)</h2>
                <ul>
                    <li><strong>Genetics:</strong> Most common Wagyu breed, known for intense marbling</li>
                    <li><strong>Flavor:</strong> Rich, buttery, highly marbled</li>
                    <li><strong>Availability:</strong> More ranches raising Fullblood Wagyu in the U.S.</li>
                    <li><strong>Verification:</strong> Look for DNA-tested, registered, or traceable bloodlines</li>
                </ul>
                
                <h2>Akaushi (Japanese Brown Wagyu)</h2>
                <ul>
                    <li><strong>Genetics:</strong> Rarer breed, originally from Kumamoto Prefecture</li>
                    <li><strong>Flavor:</strong> Balanced marbling, slightly less fat than Japanese Black</li>
                    <li><strong>Health:</strong> Higher in monounsaturated fats and oleic acid</li>
                    <li><strong>Certification:</strong> HeartBrand Beef holds the "Certified Akaushi Beef®" trademark</li>
                </ul>
                
                <h2>What to Look For</h2>
                <p><strong>Fullblood vs. Crossbred:</strong> "Fullblood" or "100%" means pure Japanese bloodlines. "American Wagyu" or "F1" typically means crossed with Angus. Both can be excellent—depends on your preference.</p>
                
                <p><strong>Verification:</strong> Ranches on Acre & Plate claim DNA testing, registration with breed associations (American Wagyu Association, American Akaushi Association), or traceable herds. Check ranch websites for details.</p>
                
                <p><strong>Not Grocery Store "Wagyu":</strong> Acre & Plate focuses on ranch-direct beef with traceable sourcing—not retail products using "Wagyu-style" marketing without proof.</p>
                
                <div class="cta">
                    <a href="/wagyu/" class="btn-primary">Browse Wagyu Ranches</a>
                    <a href="/akaushi/" class="btn-primary">Browse Akaushi Ranches</a>
                    <a href="/guides/cattle-breeds/" class="btn-secondary">Cattle Breeds Overview</a>
                </div>
                __PR_GUIDE_NOTE__
            </article>
        </div>
    </section>
    """
    
    _note = prime_rib_callout('general')
    _note = re.sub(r'</?section[^>]*>|</?div[^>]*>', '', _note) if _note else ''
    content = content.replace('__PR_GUIDE_NOTE__', _note)
    html = base_template("Wagyu vs Akaushi Guide", content, "Understand the difference between Wagyu and Akaushi beef, and what to look for when buying ranch-direct.")
    write_page('guides/wagyu-vs-akaushi/index.html', html)

# ---------------------------------------------------------------------------
# Prime rib price board (holiday page + reusable ticker)
# Data: data/prime_rib.json, written by scripts/update_prime_rib.py. Every figure carries its source and as-of date.
# ---------------------------------------------------------------------------
PRIME_RIB_JSON = 'data/prime_rib.json'
PRIME_RIB_URL = '/prime-rib-price/'


def load_prime_rib():
    """Return the prime rib dataset, or None if it is missing/unusable (page and banner are then skipped)."""
    try:
        with open(PRIME_RIB_JSON, 'r') as f:
            d = json.load(f)
    except (OSError, ValueError):
        return None
    retail = d.get('retail') or {}
    nat = [r for r in retail.get('national', []) if r['cut'] == 'Bone-In' and r['tier'] == 'Regular'
           and r['env'] == 'Conventional' and r['cond'] == 'Fresh' and r.get('cw')]
    if not nat:
        return None
    d['_headline'] = nat[0]
    return d


def _money(v, nd=2):
    return f"${v:,.{nd}f}"


def _fmt_date(iso: str) -> str:
    from datetime import date as _d
    try:
        dt = _d.fromisoformat(iso)
    except (TypeError, ValueError):
        return iso or ''
    return f"{dt.strftime('%b')} {dt.day}, {dt.year}"


def _fmt_md(iso: str) -> str:
    from datetime import date as _d
    dt = _d.fromisoformat(iso)
    return f"{dt.month}/{dt.day}"


def prime_rib_season_active() -> bool:
    """Holiday-roast season (Nov 15 - Dec 31): the homepage ticker and cross-links show only inside this window."""
    from datetime import date as _d
    t = _d.today()
    return (t.month == 11 and t.day >= 15) or t.month == 12


def _ranch_rows(pr):
    """One row per listed-ranch product that is in stock AND states its weight (so $/lb is not guessed)."""
    rows = []
    for r in pr.get('ranches', []):
        vs = [v for v in r.get('variants', []) if v.get('available') and v.get('per_lb_low') is not None]
        if not r.get('available') or not vs:
            continue
        per_lo = min(v['per_lb_low'] for v in vs)
        per_hi = max(v['per_lb_high'] for v in vs)
        lbs = [x for v in vs for x in (v.get('lb_low'), v.get('lb_high')) if x]
        rows.append({'r': r, 'per_lo': per_lo, 'per_hi': per_hi,
                     'lb_lo': min(lbs) if lbs else None, 'lb_hi': max(lbs) if lbs else None,
                     'p_lo': min(v['price'] for v in vs), 'p_hi': max(v['price'] for v in vs),
                     'approx': any(v.get('approx') for v in vs), 'stale': r.get('stale', False)})
    rows.sort(key=lambda x: (x['per_lo'], x['r']['name']))
    return rows


def _per_lb_text(lo, hi):
    return _money(lo) if abs(hi - lo) < 0.005 else f"{_money(lo)}–{_money(hi)}"


def prime_rib_ticker_items(pr, compact=False):
    """Ticker entries as (label, value, source/as-of). All values come straight from the dataset."""
    retail = pr['retail']
    h = pr['_headline']['cw']['avg']
    items = []
    items.append(('Bone-in rib roast · retail ad average', f"{_money(h)}/lb",
                  f"USDA, ads {_fmt_md(retail['ad_period']['start'])}–{_fmt_md(retail['ad_period']['end'])}" if retail.get('ad_period') else f"USDA, {_fmt_date(retail['report_date'])}"))
    bl = next((r for r in retail['national'] if r['cut'] == 'Boneless' and r['tier'] == 'Regular' and r['env'] == 'Conventional' and r['cond'] == 'Fresh' and r.get('cw')), None)
    if bl:
        items.append(('Boneless rib roast · retail ad average', f"{_money(bl['cw']['avg'])}/lb", f"USDA, {_fmt_date(retail['report_date'])}"))
    py = pr['_headline'].get('py')
    if py:
        items.append(('Same item a year ago', f"{_money(py['avg'])}/lb", 'USDA'))
    w = pr.get('wholesale', {})
    d = w.get('daily')
    if d and d.get('ribeye_lipon_bonein_choice'):
        items.append(('Wholesale Choice bone-in rib', f"{_money(d['ribeye_lipon_bonein_choice']['avg_cwt'] / 100)}/lb", f"USDA, {_fmt_date(d['report_date'])}"))
    p = w.get('prime')
    if p and p.get('ribeye_lipon_bonein_prime'):
        items.append(('Wholesale Prime bone-in rib', f"{_money(p['ribeye_lipon_bonein_prime']['avg_cwt'] / 100)}/lb", f"USDA, week of {_fmt_date(p['report_date'])}"))
    rows = _ranch_rows(pr)
    if rows:
        lo = min(x['per_lo'] for x in rows)
        items.append((f"Ranch-direct, {len(rows)} listed offers", f"from {_money(lo)}/lb", f"checked {_fmt_date(max(x['r']['checked'] for x in rows))}"))
    return items


def prime_rib_ticker(pr, compact=False, label_id='prime-rib-ticker'):
    """Scrolling strip. Reduced-motion visitors get a static, scrollable row instead."""
    import html as _h
    items = prime_rib_ticker_items(pr, compact)
    def one(hidden):
        cells = ''.join(
            f'<li><span class="pr-t-label">{_h.escape(l)}</span> <strong>{_h.escape(v)}</strong> <span class="pr-t-src">{_h.escape(s)}</span></li>'
            for l, v, s in items)
        attr = ' aria-hidden="true"' if hidden else ''
        return f'<ul class="pr-ticker-list"{attr}>{cells}</ul>'
    return f"""<div class="pr-ticker{' pr-ticker-compact' if compact else ''}" role="region" aria-label="Prime rib price ticker">
        <a class="pr-ticker-tag" href="{PRIME_RIB_URL}"><span aria-hidden="true">✦</span> Prime rib watch</a>
        <div class="pr-ticker-viewport"><div class="pr-ticker-track">{one(False)}{one(True)}</div></div>
        <a class="pr-ticker-more" href="{PRIME_RIB_URL}">Full price board →</a>
    </div>"""


def prime_rib_home_banner():
    pr = load_prime_rib()
    if not pr or not prime_rib_season_active():
        return ''
    return f'<section class="pr-home-banner" aria-label="Holiday prime rib prices">{prime_rib_ticker(pr, compact=True)}</section>'


def _snow_html(n=26):
    flakes = []
    for i in range(n):
        left = (i * 37) % 100
        size = 4 + (i * 5) % 7
        delay = -((i * 1.7) % 14)
        dur = 11 + (i * 3) % 9
        drift = ((i * 13) % 40) - 20
        flakes.append(f'<i style="left:{left}%;--s:{size}px;--d:{dur}s;--dl:{delay:.1f}s;--x:{drift}px"></i>')
    return '<div class="pr-snow" aria-hidden="true">' + ''.join(flakes) + '</div>'


_PR_CACHE = {}


def prime_rib_cached():
    if 'd' not in _PR_CACHE:
        _PR_CACHE['d'] = load_prime_rib()
    return _PR_CACHE['d']


def prime_rib_ranch_slugs():
    """Slugs of listed ranches with an in-stock rib roast that states its weight (from data/prime_rib.json)."""
    pr = prime_rib_cached()
    return {x['r']['slug'] for x in _ranch_rows(pr)} if pr else set()


def prime_rib_callout(kind='general', slug=None, hub_slugs=None):
    """Small cross-link to the price board. Always built from data/prime_rib.json; season-gated except on ranch pages."""
    import html as _h
    pr = prime_rib_cached()
    if not pr:
        return ''
    h = pr['_headline']['cw']['avg']
    rd = pr['retail']['report_date']
    if kind == 'ranch':
        rows = [x for x in _ranch_rows(pr) if x['r']['slug'] == slug]
        if not rows:
            return ''
        parts = []
        for x in rows:
            nm = _h.escape(x['r']['product'])
            parts.append(f"<li><a href=\"{_h.escape(x['r']['url'])}?utm_source=acreandplate&amp;utm_medium=referral&amp;utm_campaign=directory&amp;utm_content={slug}\" target=\"_blank\" rel=\"noopener\">{nm}</a>: <strong>{_per_lb_text(x['per_lo'], x['per_hi'])}/lb</strong>{' (approx.)' if x['approx'] else ''}, checked {_fmt_date(x['r']['checked'])}</li>")
        return (f'<div class="pr-callout pr-callout-ranch"><h2>Holiday rib roast</h2><ul>{"".join(parts)}</ul>'
                f'<p>Grocery ads averaged <strong>{_money(h)}/lb</strong> for bone-in rib roasts in USDA\'s report dated {_fmt_date(rd)}. '
                f'<a href="{PRIME_RIB_URL}">See the full prime rib price board →</a></p></div>')
    if not prime_rib_season_active():
        return ''
    if kind == 'hub':
        n = len(set(hub_slugs or []) & prime_rib_ranch_slugs())
        if not n:
            return ''
        text = (f'<strong>{n} ranch{"es" if n != 1 else ""} on this page {"have" if n != 1 else "has"} a rib roast in stock right now.</strong> '
                f'Compare their price per pound with grocery ads ({_money(h)}/lb average, USDA).')
    elif kind == 'deals':
        text = (f'<strong>Holiday roast shopping?</strong> Bone-in rib roasts are averaging <strong>{_money(h)}/lb</strong> in grocery ads '
                f'(USDA, report dated {_fmt_date(rd)}). See how that compares with wholesale and ranch-direct prices.')
    else:
        text = (f'<strong>Prime Rib Watch:</strong> grocery ads for bone-in rib roasts average <strong>{_money(h)}/lb</strong> '
                f'(USDA, report dated {_fmt_date(rd)}).')
    return (f'<section class="pr-callout-wrap"><div class="container"><p class="pr-callout"><span aria-hidden="true">✦</span> {text} '
            f'<a href="{PRIME_RIB_URL}">Prime rib price board →</a></p></div></section>')


def build_prime_rib_page():
    """Holiday-themed prime rib market price board."""
    import html as _h
    from datetime import date as _d
    pr = load_prime_rib()
    if not pr:
        print("! prime rib data missing, skipped /prime-rib-price/")
        return
    E = _h.escape
    retail = pr['retail']
    head = pr['_headline']
    cw, pw, py = head['cw'], head.get('pw'), head.get('py')
    reg = [r for r in retail['regional'] if r['cut'] == 'Bone-In' and r['tier'] == 'Regular' and r['env'] == 'Conventional' and r['cond'] == 'Fresh']
    low = min(r['low'] for r in reg)
    high = max(r['high'] for r in reg)
    report_iso = retail['report_date']
    age_days = (_d.today() - _d.fromisoformat(report_iso)).days
    ad = retail.get('ad_period')
    period_txt = f"ads running {_fmt_date(ad['start'])} – {_fmt_date(ad['end'])}" if ad else f"report dated {_fmt_date(report_iso)}"
    stale_html = ''
    if age_days > 10:
        stale_html = f'<p class="note pr-stale">The USDA retail report behind this page is {age_days} days old. A newer one may be out; check the source links below.</p>'

    # --- change vs last week / last year (USDA's own columns)
    def delta(prev):
        if not prev:
            return ''
        diff = cw['avg'] - prev['avg']
        sign = '+' if diff >= 0 else '−'
        return f"{sign}{_money(abs(diff))}"
    chips = []
    if py:
        chips.append(f'<li><span>A year ago</span><strong>{_money(py["avg"])}/lb</strong><em>{delta(py)} · {py["stores"]:,} stores</em></li>')
    if pw:
        chips.append(f'<li><span>Last week</span><strong>{_money(pw["avg"])}/lb</strong><em>{delta(pw)} · only {pw["stores"]:,} stores advertised it</em></li>')
    chips.append(f'<li><span>This week</span><strong>{_money(cw["avg"])}/lb</strong><em>{cw["stores"]:,} stores advertised it</em></li>')
    chips_html = ''.join(chips)

    # --- by-grade store-weighted average (computed from USDA's regional rows)
    grade_order = ['Choice', 'Prime', 'Select', 'Ungraded/Other', 'Branded - Choice', 'Branded - Prime']
    grade_label = {'Choice': 'USDA Choice', 'Prime': 'USDA Prime', 'Select': 'USDA Select', 'Ungraded/Other': 'No grade stated',
                   'Branded - Choice': 'Branded Choice', 'Branded - Prime': 'Branded Prime'}
    grade_avgs = {}
    for g in grade_order:
        rs = [r for r in reg if r['grade'] == g]
        st = sum(r['stores'] for r in rs)
        if st:
            grade_avgs[g] = (sum(r['avg'] * r['stores'] for r in rs) / st, st, min(r['low'] for r in rs), max(r['high'] for r in rs))
    grade_cards = ''.join(
        f'<li><span>{grade_label[g]}</span><strong>{_money(a)}/lb</strong><em>{_money(lo)}–{_money(hi)} · {st:,} stores</em></li>'
        for g, (a, st, lo, hi) in grade_avgs.items())

    # --- region x grade matrix
    regions = []
    for r in reg:
        if r['region'] not in regions:
            regions.append(r['region'])
    region_note = {'Northeast': 'CT DE MA MD ME NH NJ NY PA RI VT', 'Southeast': 'AL FL GA MS NC SC TN VA WV',
                   'Midwest': 'IA IL IN KY MI MN ND NE OH SD WI', 'South Central': 'AR CO KS LA MO NM OK TX',
                   'Southwest': 'AZ CA NV UT', 'Northwest': 'ID MT OR WA WY', 'Alaska': 'AK', 'Hawaii': 'HI'}
    cols = [g for g in grade_order if g in grade_avgs]
    head_row = '<th scope="col">Region</th>' + ''.join(f'<th scope="col">{grade_label[g]}</th>' for g in cols)
    body_rows = ''
    for rg in regions:
        tds = ''
        for g in cols:
            m = next((r for r in reg if r['region'] == rg and r['grade'] == g), None)
            tds += (f'<td><strong>{_money(m["avg"])}</strong><small>{_money(m["low"])}–{_money(m["high"])} · {m["stores"]:,}</small></td>' if m else '<td class="pr-none">—</td>')
        body_rows += f'<tr><th scope="row">{E(rg)}<small>{region_note.get(rg, "")}</small></th>{tds}</tr>'

    # --- other retail items
    other = []
    for r in retail['national']:
        if not r.get('cw') or (r['env'] != 'Conventional' or r['cond'] != 'Fresh'):
            continue
        if (r['cut'], r['tier']) == ('Bone-In', 'Regular'):
            continue
        other.append(r)
    other_rows = ''.join(
        f"<tr><th scope=\"row\">{r['cut']} rib roast, {'value-priced' if r['tier'] == 'Value' else 'regular'}</th><td><strong>{_money(r['cw']['avg'])}/lb</strong></td><td>{r['cw']['stores']:,}</td>"
        f"<td>{_money(r['pw']['avg']) + '/lb' if r.get('pw') else '—'}</td><td>{_money(r['py']['avg']) + '/lb' if r.get('py') else '—'}</td></tr>"
        for r in other)
    dinner = retail.get('prime_rib_dinner')
    dinner_html = ''
    if dinner:
        dinner_html = (f'<p class="pr-fine">Not cooking? USDA also tracked fully cooked prime rib dinners (serves {dinner["servings"]}): '
                       f'average {_money(dinner["avg"])}, advertised from {_money(dinner["low"])} to {_money(dinner["high"])}'
                       + (f', at {dinner["pct_stores"]}% of surveyed stores' if dinner.get('pct_stores') else '') + '.</p>')

    # --- wholesale
    wh = pr.get('wholesale', {})
    wcards = ''
    d = wh.get('daily')
    if d:
        c = d['ribeye_lipon_bonein_choice']
        wcards += (f'<li><span>Choice bone-in rib (IMPS 109E), 0–21 day delivery</span><strong>{_money(c["avg_cwt"] / 100)}/lb</strong>'
                   f'<em>{_money(c["low_cwt"] / 100)}–{_money(c["high_cwt"] / 100)} · {c["trades"]} trades · {c["pounds"]:,} lb · {_fmt_date(d["report_date"])} {d.get("session") or ""}</em></li>')
        wcards += (f'<li><span>Primal rib value, Choice / Select</span><strong>{_money(d["primal_rib_choice_cwt"] / 100)} / {_money(d["primal_rib_select_cwt"] / 100)} per lb</strong>'
                   f'<em>Whole rib primal, USDA cutout · {_fmt_date(d["report_date"])}</em></li>')
    p = wh.get('prime')
    if p:
        c = p['ribeye_lipon_bonein_prime']
        wcards += (f'<li><span>Prime bone-in rib (IMPS 109E), weekly</span><strong>{_money(c["avg_cwt"] / 100)}/lb</strong>'
                   f'<em>{_money(c["low_cwt"] / 100)}–{_money(c["high_cwt"] / 100)} · {c["trades"]} trades · week reported {_fmt_date(p["report_date"])}</em></li>')

    # --- ranch-direct
    rrows = _ranch_rows(pr)
    listed = {l['slug'] for l in listings}
    ranch_html = ''
    for x in rrows:
        r = x['r']
        name = E(r['name'])
        name_html = f'<a href="/listings/{r["slug"]}/">{name}</a>' if r['slug'] in listed else name
        size = ''
        if x['lb_lo']:
            size = (f"{x['lb_lo']:g} lb" if x['lb_lo'] == x['lb_hi'] else f"{x['lb_lo']:g}–{x['lb_hi']:g} lb")
            if x['approx']:
                size = '≈ ' + size
        price = _money(x['p_lo']) if abs(x['p_hi'] - x['p_lo']) < 0.005 else f"{_money(x['p_lo'])}–{_money(x['p_hi'])}"
        if r.get('price_note') and x['p_lo'] <= 100 and not size:
            price = 'deposit ' + price
        note = f'<small>{E(r["price_note"])}</small>' if r.get('price_note') else ''
        ranch_html += (f'<tr><th scope="row">{name_html}<small>{E(r.get("state") or "")}</small></th>'
                       f'<td><a href="{E(r["url"])}?utm_source=acreandplate&amp;utm_medium=referral&amp;utm_campaign=prime-rib-board&amp;utm_content={r["slug"]}" target="_blank" rel="noopener">{E(r["product"])}</a>{note}</td>'
                       f'<td>{size or "—"}</td><td><strong>{_per_lb_text(x["per_lo"], x["per_hi"])}</strong>{"<small>approx.</small>" if x["approx"] else ""}</td>'
                       f'<td>{price}</td><td>{_fmt_date(r["checked"])}{"<small>stale: last check failed</small>" if x["stale"] else ""}</td></tr>')
    ranch_checked = max((x['r']['checked'] for x in rrows), default=None)
    if rrows:
        cheapest = min(rrows, key=lambda x: x['per_lo'])
        n_ranches = len({x['r']['slug'] for x in rrows})
    ranch_intro = ''
    if rrows:
        ranch_intro = (f'<p class="section-intro">{n_ranches} listed ranches have a rib roast in stock right now with a stated weight, from '
                       f'{_money(cheapest["per_lo"])}/lb at {E(cheapest["r"]["name"])} up to {_money(max(x["per_hi"] for x in rrows))}/lb. '
                       f'These are named-herd, ranch-raised roasts, mostly frozen and shipped, so shipping is extra and the comparison with grocery ads is loose.</p>')

    # --- sources
    srcs = [
        (retail['source'], retail['url'], f"Report dated {_fmt_date(report_iso)}; {period_txt}", 'Retail advertised prices (the headline numbers)'),
    ]
    if d:
        srcs.append((d['source'], d['url'], f"{_fmt_date(d['report_date'])} ({d.get('session') or ''})", 'Wholesale Choice rib price and primal rib value'))
    if p:
        srcs.append((p['source'], p['url'], f"Week reported {_fmt_date(p['report_date'])}", 'Wholesale Prime rib price'))
    if rrows:
        srcs.append(('Ranch websites (product pages linked in the table)', '/listings/', f"Checked {_fmt_date(ranch_checked)}", 'Ranch-direct prices; $/lb only where the ranch states the weight'))
    def ext(u):
        return '' if u.startswith('/') else ' target="_blank" rel="noopener"'
    src_rows = ''.join(
        f'<tr><th scope="row"><a href="{E(u)}"{ext(u)}>{E(n)}</a></th><td>{E(a)}</td><td>{E(w)}</td></tr>' for n, u, a, w in srcs)

    # --- buying guide: portions x price (plain arithmetic on the sourced numbers above)
    import statistics as _st
    guide_html = ''
    faq = []
    price_cols = [('Grocery ad average', cw['avg'], f"USDA, report dated {_fmt_date(report_iso)}")]
    if 'Prime' in grade_avgs:
        price_cols.append(('Grocery USDA Prime ad average', grade_avgs['Prime'][0], 'USDA regional rows, store-weighted'))
    if rrows:
        price_cols.append(('Ranch-direct, lowest listed', min(x['per_lo'] for x in rrows), f"ranch sites, checked {_fmt_date(ranch_checked)}"))
        price_cols.append(('Ranch-direct, middle of listed offers', _st.median([x['per_lo'] for x in rrows]), f"ranch sites, checked {_fmt_date(ranch_checked)}"))
    th = ''.join(f'<th scope="col">{E(n)}<small>{_money(p)}/lb</small></th>' for n, p, _ in price_cols)
    trs = ''
    for g in (4, 6, 8, 10, 12):
        tds = ''.join(f'<td><strong>{_money(g * p, 0)}</strong></td>' for _, p, _ in price_cols)
        trs += f'<tr><th scope="row">{g} guests<small>about {g} lb bone-in</small></th>{tds}</tr>'
    guide_html = f"""
    <section class="pr-guide" id="how-much-prime-rib">
        <div class="container">
            <p class="pr-eyebrow pr-eyebrow-dark">Plan the table</p>
            <h2 class="pr-h2">How much prime rib per person, and what it costs</h2>
            <p class="section-intro">A common rule of thumb is about 1 lb of bone-in roast per person (roughly one rib for every two guests), or about ½ to ¾ lb per person for boneless. Multiply by the price per pound below. This is simple arithmetic on the prices above, before shipping, tax and trimming, not a quote.</p>
            <div class="pr-table-wrap"><table class="pr-table"><thead><tr><th scope="col">Table size</th>{th}</tr></thead><tbody>{trs}</tbody></table></div>
            <p class="pr-fine">Ranch-direct roasts are often grass-fed, Akaushi or Wagyu and ship frozen, so they are a different product from a commodity grocery roast. Prices shown are the sourced per-pound figures above; the "lowest" and "middle" ranch figures use the low end of each in-stock offer's per-lb range.</p>
        </div>
    </section>
    """
    lowest = min((x['per_lo'] for x in rrows), default=None)
    faq = [
        ("How much does prime rib cost per pound right now?",
         f"In USDA's weekly grocery feature report dated {_fmt_date(report_iso)} ({period_txt}), bone-in rib roasts advertised at grocery stores averaged {_money(cw['avg'])} per pound, with advertised prices from {_money(low)} to {_money(high)}. "
         + (f"Ranch-direct prime rib from ranches in the Acre & Plate directory starts at {_money(lowest)} per pound." if lowest else "")),
        ("What is the difference between prime rib, standing rib roast and rib roast?",
         "They are the same bone-in beef rib roast, cut from the rib primal. 'Standing rib roast' describes it roasted standing on its ribs. 'Prime rib' names the cut and is not the same as the USDA Prime quality grade; a prime rib can be USDA Choice, Prime or Select, or ungraded."),
        ("How much prime rib do I need per person?",
         "A common rule of thumb is about 1 pound of bone-in roast per person, roughly one rib for every two guests, or about half to three-quarters of a pound per person for boneless."),
        ("Is the wholesale price what I will pay?",
         "No. The USDA boxed beef figures are packer prices for an uncut rib, FOB plant. Stores trim, cut and package the roast and set their own prices, and grocery ads are promotional."),
        ("Why is ranch-direct prime rib priced higher than grocery ads?",
         "Grocery ads are promotional prices, mostly on commodity beef. Ranch-direct roasts are often grass-fed, Akaushi or Wagyu, are sold by the ranch rather than a chain, and usually ship frozen with shipping extra. Check each ranch's page for the exact weight and final price."),
    ]
    faq_html = '<section class="pr-faq"><div class="container"><h2 class="pr-h2">Prime rib price FAQ</h2>' + ''.join(
        f'<details class="pr-q"><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in faq) + '</div></section>'

    # --- structured data (everything from the sourced dataset)
    import json as _json
    page_url = 'https://acreandplate.com' + PRIME_RIB_URL
    og_img = 'https://acreandplate.com/social/prime-rib/prime-rib-og-1200x630.png'
    updated = pr['generated_at'][:10]
    sources_ld = [retail['url']] + [w['url'] for w in (wh.get('daily'), wh.get('prime')) if w]
    ld = [
        {"@context": "https://schema.org", "@type": "WebPage", "@id": page_url, "url": page_url,
         "name": f"Prime Rib Price Per Pound Today: {_money(cw['avg'])}/lb average (USDA)",
         "description": f"Current prime rib (standing rib roast) price per pound from USDA grocery ad data, wholesale cutout and ranch-direct prices.",
         "datePublished": "2026-11-26", "dateModified": updated, "inLanguage": "en-US",
         "isPartOf": {"@type": "WebSite", "name": "Acre & Plate", "url": "https://acreandplate.com/"},
         "primaryImageOfPage": {"@type": "ImageObject", "url": og_img, "width": 1200, "height": 630},
         "breadcrumb": {"@id": page_url + "#breadcrumb"}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "@id": page_url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://acreandplate.com/"},
            {"@type": "ListItem", "position": 2, "name": "Deals", "item": "https://acreandplate.com/deals/"},
            {"@type": "ListItem", "position": 3, "name": "Prime rib price board", "item": page_url}]},
        {"@context": "https://schema.org", "@type": "Dataset", "name": "Prime rib (bone-in rib roast) price per pound, United States",
         "description": f"Average advertised grocery price for bone-in rib roasts ({_money(cw['avg'])}/lb, USDA report dated {report_iso}), USDA wholesale boxed beef rib prices, and ranch-direct prices from ranches listed on Acre & Plate.",
         "url": page_url, "dateModified": updated, "creator": {"@type": "Organization", "name": "Acre & Plate", "url": "https://acreandplate.com/"},
         "isBasedOn": sources_ld, "measurementTechnique": "Compiled from USDA AMS Market News reports and ranch product pages; each figure is shown with its source and as-of date.",
         "variableMeasured": [{"@type": "PropertyValue", "name": "Bone-in rib roast, average advertised grocery price", "value": cw['avg'], "unitText": "USD per lb"}],
         "temporalCoverage": f"{ad['start']}/{ad['end']}" if ad else report_iso, "spatialCoverage": "United States"},
        {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]
    ld_html = ''.join(f'<script type="application/ld+json">{_json.dumps(x, ensure_ascii=False).replace("</", "<\\/")}</script>\n    ' for x in ld)
    title_txt = f"Prime Rib Price Per Pound Today: {_money(cw['avg'])}/lb Avg"
    meta_txt = (f"Prime rib price per pound: {_money(cw['avg'])}/lb average in grocery ads (USDA, {_fmt_date(report_iso)}), "
                f"plus wholesale" + (f" and ranch-direct from {_money(lowest)}/lb." if lowest else "."))
    og = (f'<link rel="canonical" href="{page_url}">\n    <meta property="og:type" content="article">\n    <meta property="og:site_name" content="Acre &amp; Plate">\n'
          f'    <meta property="og:title" content="{E(title_txt)} | Acre &amp; Plate">\n    <meta property="og:description" content="{E(meta_txt)}">\n'
          f'    <meta property="og:url" content="{page_url}">\n    <meta property="og:image" content="{og_img}">\n    <meta property="og:image:width" content="1200">\n    <meta property="og:image:height" content="630">\n'
          f'    <meta property="og:image:alt" content="Prime Rib Watch: bone-in rib roast averages {_money(cw["avg"])} per pound in grocery ads, USDA">\n'
          f'    <meta name="twitter:card" content="summary_large_image">\n    <meta name="twitter:title" content="{E(title_txt)} | Acre &amp; Plate">\n'
          f'    <meta name="twitter:description" content="{E(meta_txt)}">\n    <meta name="twitter:image" content="{og_img}">\n'
          f'    <meta name="robots" content="index, follow, max-image-preview:large">\n    ' + ld_html)

    week_note = ''
    if pw and pw['stores'] < cw['stores']:
        week_note = (f"Last week's {_money(pw['avg'])} came from far fewer advertising stores ({pw['stores']:,} vs {cw['stores']:,}), "
                     "so part of the week-over-week jump reflects which stores were running ads, not only price changes.")
    ticker = prime_rib_ticker(pr)
    usda_note = retail.get('usda_note')
    content = f"""
    <section class="page-header pr-hero">
        {_snow_html()}
        <div class="pr-garland" aria-hidden="true"></div>
        <div class="container pr-hero-inner">
            <p class="breadcrumb"><a href="/">Home</a> / <a href="/deals/">Deals</a> / Prime rib price board</p>
            <p class="pr-eyebrow"><span aria-hidden="true">✦</span> Holiday roast season <span aria-hidden="true">✦</span></p>
            <h1>What a prime rib roast costs right now.</h1>
            <p class="pr-deck">Standing rib roast, bone-in rib roast, prime rib: same holiday centerpiece, three names. Here is the current market price per pound, straight from USDA reports and ranch shops, with the source and date on every number.</p>
        </div>
        <div class="pr-ribbon" aria-hidden="true"><span></span></div>
    </section>
    {ticker}
    <section class="pr-board">
        <div class="container">
            {stale_html}
            <div class="pr-headline">
                <div class="pr-headline-main">
                    <p class="pr-kicker">National retail ad average · bone-in rib roast</p>
                    <p class="pr-big" aria-label="{_money(cw['avg'])} per pound">{_money(cw['avg'])}<small>/lb</small></p>
                    <p class="pr-range">Advertised from <strong>{_money(low)}</strong> to <strong>{_money(high)}</strong> per lb across all grades, brands and regions</p>
                    <p class="pr-src">Source: <a href="{E(retail['url'])}" target="_blank" rel="noopener">USDA AMS Market News, Weekly Grocery Store Beef Feature Activity</a> · report dated {_fmt_date(report_iso)} · {period_txt}.</p>
                </div>
                <ul class="pr-chips" aria-label="Comparison to last week and last year">{chips_html}</ul>
            </div>
            <p class="pr-fine">This is the average advertised price for conventional, fresh, regular-priced bone-in ribeye (rib) roasts at grocery stores USDA surveys, weighted by the number of stores running the ad. {E(usda_note) if usda_note else ''} {week_note}</p>

            <h2 class="pr-h2">By grade</h2>
            <p class="section-intro">Store-weighted averages calculated by Acre &amp; Plate from USDA's regional rows (bone-in, regular-priced, conventional, fresh). Range is the lowest and highest advertised price.</p>
            <ul class="pr-cards">{grade_cards}</ul>

            <h2 class="pr-h2">By region</h2>
            <p class="section-intro">Average advertised price per lb, with the low–high range and number of stores below each figure. A dash means USDA recorded no ads in that group.</p>
            <div class="pr-table-wrap"><table class="pr-table"><thead><tr>{head_row}</tr></thead><tbody>{body_rows}</tbody></table></div>

            <h2 class="pr-h2">Other rib roasts at the grocery store</h2>
            <div class="pr-table-wrap"><table class="pr-table pr-table-narrow"><thead><tr><th scope="col">Item</th><th scope="col">This week</th><th scope="col">Stores</th><th scope="col">Last week</th><th scope="col">Last year</th></tr></thead><tbody>{other_rows}</tbody></table></div>
            {dinner_html}
        </div>
    </section>

    <section class="pr-wholesale">
        <div class="container">
            <p class="pr-eyebrow pr-eyebrow-dark">Wholesale reference</p>
            <h2 class="pr-h2">What the rib costs before it reaches the case</h2>
            <p class="section-intro"><strong>Wholesale, not retail.</strong> These are negotiated packer prices, FOB plant, for an uncut bone-in rib (lip-on ribeye). They are not what you pay at a counter, and the store still trims, cuts and packages the roast. Advertised grocery prices are promotional, which is why they can sit below the wholesale box price.</p>
            <ul class="pr-cards">{wcards}</ul>
        </div>
    </section>

    <section class="pr-ranches">
        <div class="container">
            <p class="pr-eyebrow pr-eyebrow-dark">Ranch-direct</p>
            <h2 class="pr-h2">Prime rib from ranches in our directory</h2>
            {ranch_intro}
            <div class="pr-table-wrap"><table class="pr-table pr-table-ranch"><thead><tr><th scope="col">Ranch</th><th scope="col">Roast (ranch's product page)</th><th scope="col">Size</th><th scope="col">Price / lb</th><th scope="col">Price</th><th scope="col">Checked</th></tr></thead><tbody>{ranch_html}</tbody></table></div>
            <p class="pr-fine">Only in-stock roasts where the ranch states the weight or a per-pound price are shown. Many are pre-orders with ship weeks in December; shipping and final weights vary, so confirm on the ranch's page before you order. Grass-fed, Akaushi and Wagyu roasts are not the same product as a commodity Choice roast. <a href="/listings/">Browse every ranch →</a> · <a href="/deals/">Current deals →</a></p>
        </div>
    </section>

    {guide_html}
    {faq_html}

    <section class="pr-sources">
        <div class="container">
            <h2 class="pr-h2">Sources and as-of dates</h2>
            <div class="pr-table-wrap"><table class="pr-table pr-table-narrow"><thead><tr><th scope="col">Source</th><th scope="col">As of</th><th scope="col">Used for</th></tr></thead><tbody>{src_rows}</tbody></table></div>
            <p class="pr-fine">Each number above is read from the source and date shown here; run <code>scripts/update_prime_rib.py</code> to re-read them. They are reports, not offers: store ads, wholesale trades and ranch prices change, so always confirm at the seller. Acre &amp; Plate does not sell beef. Page data updated {_fmt_date(pr['generated_at'][:10])}.</p>
        </div>
    </section>
    """
    html = base_template(title_txt, content, meta_txt, og)
    write_page('prime-rib-price/index.html', html)


def build_deals_page():
    """Build deals hub page"""
    # Get active featured placements (premium tier gets spotlight on deals page)
    active_featured = get_active_featured_placements()
    premium_featured = [f for f in active_featured if f['placement']['tier'] == 'premium']
    
    featured_ranch_html = ''
    if premium_featured:
        featured_cards = [listing_card(f['listing'], featured_badge=True) for f in premium_featured[:2]]
        featured_ranch_html = f"""
        <div class="featured-ranch-spotlight">
            <h2>Featured Ranch Spotlight</h2>
            <p class="spotlight-intro">Ultra ranch partners committed to traceable bloodlines and transparent sourcing.</p>
            <div class="listings-grid">
                {''.join(featured_cards)}
            </div>
        </div>
        """
    
    # Group deals by cut
    deals_by_cut = {}
    for deal in deals:
        cut = deal['cut']
        if cut not in deals_by_cut:
            deals_by_cut[cut] = []
        deals_by_cut[cut].append(deal)
    
    # Sort cuts alphabetically
    sorted_cuts = sorted(deals_by_cut.keys())
    
    # Generate all deal cards
    all_deals_html = '\n'.join([deal_card(deal) for deal in deals])
    
    # Generate by-cut sections
    by_cut_html = ''
    for cut in sorted_cuts:
        cut_deals = deals_by_cut[cut]
        cut_cards_html = '\n'.join([deal_card(deal) for deal in cut_deals])
        cut_title = cut.replace('-', ' ').title()
        by_cut_html += f"""
        <div class="deals-by-cut">
            <h3 class="cut-heading">{cut_title} ({len(cut_deals)})</h3>
            <div class="deals-grid">
                {cut_cards_html}
            </div>
        </div>
        """
    
    content = f"""
    <section class="page-header">
        <div class="container">
            <h1>Seasonal Deals & Overstock</h1>
            <p>Current sale, clearance, and overstock deals from verified ranches</p>
            <p class="count">{len(deals)} active deals</p>
        </div>
    </section>
    
    {prime_rib_callout('deals')}
    <section class="deals-section">
        <div class="container">
            {featured_ranch_html}
            
            <div class="deals-intro">
                <h2>How This Works</h2>
                <p>Acre & Plate scouts ranch websites for sale, clearance, and overstock inventory. When a ranch marks down ribeyes, ground beef, or other cuts, we verify the deal and list it here. <strong>Always confirm pricing and availability on the ranch website before ordering</strong>—deals change frequently.</p>
                <p class="deals-disclaimer">⚠️ Prices last verified {deals[0].get('verified_at', '')}. Deals subject to ranch inventory and may sell out or expire.</p>
            </div>
            
            <h2>All Current Deals</h2>
            <div class="deals-grid">
                {all_deals_html}
            </div>
            
            <h2 class="section-divider">Deals by Cut</h2>
            {by_cut_html}
        </div>
    </section>
    """
    
    meta = f"Current seasonal deals and overstock on Wagyu, Akaushi, and heritage beef from ranch-direct sources. {len(deals)} active deals."
    html = base_template("Seasonal Deals & Overstock", content, meta)
    write_page('deals/index.html', html)

def build_featured():
    """Build Featured Ranch landing page"""
    # Determine CTA based on Stripe config
    standard_cta = ''
    premium_cta = ''
    
    if stripe_config['standard_payment_link'] == 'REPLACE_ME':
        standard_cta = '<a href="mailto:info@acreandplate.com?subject=Featured Ranch - Standard" class="btn-primary">Contact Us (Checkout Coming Soon)</a>'
        premium_cta = '<a href="mailto:info@acreandplate.com?subject=Featured Ranch - Ultra" class="btn-primary">Contact Us (Checkout Coming Soon)</a>'
    else:
        standard_cta = f'<a href="{stripe_config["standard_payment_link"]}" class="btn-primary">Get Featured - Standard</a>'
        premium_cta = f'<a href="{stripe_config["premium_payment_link"]}" class="btn-primary">Get Featured - Ultra</a>'
    
    content = f"""
    <section class="hero">
        <div class="container">
            <h1>Featured Ranch Placement</h1>
            <p class="tagline">Showcase your ranch to customers actively searching for traceable, ranch-direct beef. Get featured placement on Acre & Plate.</p>
        </div>
    </section>
    
    <section class="featured-info">
        <div class="container">
            <div class="featured-intro">
                <h2>What is Featured Ranch?</h2>
                <p>Featured Ranch gives your ranch premium visibility on Acre & Plate's directory. We connect you with customers who care about traceable bloodlines, named herds, and honest sourcing—people who are ready to buy ranch-direct beef.</p>
                
                <p><strong>Your listing already appears in the directory for free.</strong> Featured Ranch placement adds premium visibility to drive more traffic to your ranch website.</p>
                
                <p style="margin-top: 1rem; font-size: 0.9rem; color: #666;"><a href="/featured/one-pager.pdf" style="color: #666; text-decoration: underline;">Download one-pager (PDF)</a></p>
            </div>
            
            <div class="pricing-tiers">
                <div class="tier tier-standard">
                    <div class="tier-header">
                        <h3>Standard</h3>
                        <div class="price">{stripe_config['standard_price_display']}</div>
                    </div>
                    <div class="tier-features">
                        <h4>What's Included:</h4>
                        <ul>
                            <li>✓ Featured placement on home page</li>
                            <li>✓ Highlighted in all listings browse</li>
                            <li>✓ "Featured Partner" badge on your listing</li>
                            <li>✓ Priority placement in search results</li>
                            <li>✓ Monthly traffic reports</li>
                            <li>✓ <strong>Your logo, on our apron:</strong> one co-branded apron in the Acre &amp; Plate shop, a $5 cut of every sale, and member pricing on crew and farm-store orders (ask us for a quote)</li>
                        </ul>
                    </div>
                    <div class="tier-cta">
                        {standard_cta}
                    </div>
                </div>
                
                <div class="tier tier-premium">
                    <div class="tier-header">
                        <div class="popular-badge">Most Visible</div>
                        <h3>Ultra</h3>
                        <div class="price">{stripe_config['premium_price_display']}</div>
                    </div>
                    <div class="tier-features">
                        <h4>Everything in Standard, plus:</h4>
                        <ul>
                            <li>✓ Top placement on home page</li>
                            <li>✓ Featured in Seasonal Deals hub</li>
                            <li>✓ Spotlight section when deals are active</li>
                            <li>✓ Social media mentions (when available)</li>
                            <li>✓ Priority support for listing updates</li>
                            <li>✓ <strong>Your logo, on our apron:</strong> up to 2 apron colors, a $10 cut of every sale, a free sample apron, and crew orders at our cost</li>
                        </ul>
                    </div>
                    <div class="tier-cta">
                        {premium_cta}
                    </div>
                </div>
            </div>
            
            <div class="featured-faq">
                <h2>How It Works</h2>
                
                <div class="faq-item">
                    <h3>Who should get featured?</h3>
                    <p>Ranches raising cattle with traceable bloodlines—Fullblood Wagyu, Akaushi, Japanese Black, heritage breeds. If you're already listed on Acre & Plate, Featured Ranch gives you premium visibility.</p>
                </div>
                
                <div class="faq-item">
                    <h3>What's the commitment?</h3>
                    <p>Monthly subscription. Cancel anytime. Your free directory listing stays active regardless of Featured Ranch status.</p>
                </div>
                
                <div class="faq-item">
                    <h3>How do I track results?</h3>
                    <p>We provide monthly traffic reports showing visits to your listing and clicks to your ranch website. All outbound links include UTM tracking so you can see Acre & Plate referrals in your own analytics.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Your logo, on our apron</h3>
                    <img src="/assets/featured/apron-cobrand-sample.png" alt="Sample co-branded Acre &amp; Plate apron in forest green with a placeholder ranch logo on the chest and a small Acre &amp; Plate mark below it" width="600" height="600" loading="lazy" style="display:block; max-width:320px; width:100%; height:auto; margin:0 auto 1rem;">
                    <p>Featured Ranches get a co-branded Acre &amp; Plate apron with their own logo on the chest, in heavy cotton twill in our forest green. We list it in the <a href="https://acreandplate.printful.me/" target="_blank" rel="noopener noreferrer">Acre &amp; Plate shop</a> so your customers can buy it, and you earn a cut of every sale. You can also order a batch for your crew or farm store at member pricing.</p>
                    <ul>
                        <li><strong>Standard:</strong> one apron listing in Dark Green, $5 to you per $50 sale, and member pricing on crew and farm-store orders (ask us for a quote).</li>
                        <li><strong>Ultra:</strong> up to 2 apron colors, $10 to you per sale, one free sample apron, and crew orders at our cost.</li>
                    </ul>
                    <p>No setup fee. We only print your logo with your written permission. Your share of sales is paid monthly, and amounts under $25 roll over to the next month. If you leave Featured Ranch, we take your apron listing down within 7 days. Sample shown uses a placeholder logo; shop orders ship within the US.</p>
                </div>
                
                <div class="faq-item">
                    <h3>What if my ranch isn't listed yet?</h3>
                    <p>Visit our <a href="/about/">About page</a> for instructions on adding your ranch to the directory, or email us at <a href="mailto:ranches@acreandplate.com">ranches@acreandplate.com</a>. Featured Ranch placement is available once your listing is live.</p>
                </div>
                
                <div class="faq-item">
                    <h3>Questions about Featured Ranch?</h3>
                    <p>Contact us at <a href="mailto:ranches@acreandplate.com">ranches@acreandplate.com</a> for questions about featured placement, listing updates, or custom packages.</p>
                </div>
            </div>
            
            <div class="featured-cta-footer">
                <h2>Ready to get featured?</h2>
                <p>Choose your tier and start driving more customers to your ranch.</p>
                <div class="cta-buttons">
                    {standard_cta}
                    {premium_cta}
                </div>
                <p style="margin-top: 1.5rem; text-align: center;">Questions? Email <a href="mailto:ranches@acreandplate.com">ranches@acreandplate.com</a></p>
            </div>
        </div>
    </section>
    """
    
    html = base_template("Featured Ranch Placement", content, "Get premium placement for your ranch on Acre & Plate. Featured Ranch drives traffic to ranches raising traceable Wagyu, Akaushi, and heritage beef.")
    write_page('featured/index.html', html)

def build_list_your_ranch():
    """Build Free vs Premium Profile vs Featured Ranch comparison page (DRAFT: Premium Profile is waitlist-only)"""
    n_ranches = len(listings)
    waitlist = 'mailto:ranches@acreandplate.com?subject=Premium%20Profile%20waitlist&body=Ranch%20name%3A%0AListing%20URL%3A%0A'
    featured_cta = '<a href="/featured/" class="btn-primary">See Featured Ranch</a>'
    content = f"""
    <section class="hero">
        <div class="container">
            <h1>List Your Ranch</h1>
            <p class="tagline">Free, verified listings for ranches that sell beef direct. No commission, ever. You keep 100% of every sale.</p>
        </div>
    </section>

    <section class="featured-info">
        <div class="container">
            <div class="featured-intro">
                <h2>Free stays free</h2>
                <p>Acre &amp; Plate lists {n_ranches} verified ranches across all 50 states. Every listing is free and verified by hand. We never touch the meat or the money: buyers click through and buy from you on your own site, by phone, or at your farm.</p>
                <p>If you want more visibility, there are optional paid upgrades. Your free listing stays live whether or not you use them.</p>
            </div>

            <div class="pricing-tiers">
                <div class="tier tier-standard">
                    <div class="tier-header">
                        <h3>Free Listing</h3>
                        <div class="price">$0 forever</div>
                    </div>
                    <div class="tier-features">
                        <h4>What's included:</h4>
                        <ul>
                            <li>✓ Verified listing in the directory</li>
                            <li>✓ Your ranch on your state page and breed pages</li>
                            <li>✓ Direct links to your website, phone, and email</li>
                            <li>✓ No commission and no transaction fees</li>
                            <li>✓ Free updates when your shipping or prices change</li>
                        </ul>
                    </div>
                    <div class="tier-cta">
                        <a href="mailto:ranches@acreandplate.com?subject=List%20my%20ranch" class="btn-primary">Ask to Be Listed</a>
                    </div>
                </div>

                <div class="tier tier-premium">
                    <div class="tier-header">
                        <div class="popular-badge">Coming Soon</div>
                        <h3>Premium Profile</h3>
                        <div class="price">$199/yr</div>
                    </div>
                    <div class="tier-features">
                        <h4>Everything in Free, plus:</h4>
                        <ul>
                            <li>✓ A ranch video on your listing</li>
                            <li>✓ Your herd names and where they came from</li>
                            <li>✓ Your grazing practices, in your words</li>
                            <li>✓ A downloadable cut sheet (PDF)</li>
                            <li>✓ Your booking or ordering calendar, embedded</li>
                            <li>✓ More photos</li>
                            <li>✓ One Story Post about your ranch, shared to our newsletter and Instagram</li>
                        </ul>
                    </div>
                    <div class="tier-cta">
                        <a href="{waitlist}" class="btn-primary">Join the Waitlist</a>
                    </div>
                </div>

                <div class="tier tier-standard">
                    <div class="tier-header">
                        <h3>Featured Ranch</h3>
                        <div class="price">from {stripe_config['standard_price_display']}</div>
                    </div>
                    <div class="tier-features">
                        <h4>Top placement:</h4>
                        <ul>
                            <li>✓ Featured on the home page and in listings browse</li>
                            <li>✓ "Featured Partner" badge</li>
                            <li>✓ Monthly traffic reports</li>
                            <li>✓ Your logo on a co-branded Acre &amp; Plate apron, with a cut of every sale</li>
                            <li>✓ Standard {stripe_config['standard_price_display']} or Ultra {stripe_config['premium_price_display']}, cancel anytime</li>
                        </ul>
                    </div>
                    <div class="tier-cta">
                        {featured_cta}
                    </div>
                </div>
            </div>

            <div class="featured-faq">
                <h2>Questions</h2>
                <div class="faq-item">
                    <h3>Do you take a cut of my beef sales?</h3>
                    <p>No. Not on any tier. Buyers pay you directly, and you keep 100% of every sale.</p>
                </div>
                <div class="faq-item">
                    <h3>What does "verified" mean?</h3>
                    <p>We check that you raise the cattle and sell beef direct to buyers, and we confirm your contact details and how you sell before your listing goes live. We recheck listings on a regular cycle.</p>
                </div>
                <div class="faq-item">
                    <h3>When does Premium Profile launch?</h3>
                    <p>We're opening it to a small group of listed ranches first. Join the waitlist and we'll email you before it opens. Nothing is charged to join the waitlist.</p>
                </div>
                <div class="faq-item">
                    <h3>Can I combine Premium Profile and Featured Ranch?</h3>
                    <p>Yes. Premium Profile makes your listing richer. Featured Ranch puts it in front of more buyers. They work on their own or together.</p>
                </div>
                <div class="faq-item">
                    <h3>Questions?</h3>
                    <p>Email <a href="mailto:ranches@acreandplate.com">ranches@acreandplate.com</a>.</p>
                </div>
            </div>
        </div>
    </section>
    """
    html = base_template("List Your Ranch: Free vs Premium Profile", content, "List your ranch on Acre & Plate for free. Verified listings, no commission, you keep 100% of every sale. Optional Premium Profile and Featured Ranch upgrades.")
    write_page('list-your-ranch/index.html', html)

def build_beyond_beef():
    """Build Beyond Beef hub: verified pasture-raised non-beef farms (kept out of ranch counts and state hubs)"""
    with open('data/beyond-beef.json') as f:
        farms = json.load(f)['farms']
    e = html_tools.escape
    cards = []
    for farm in farms:
        items = ''.join(f'<li>{e(p)}</li>' for p in farm['products'])
        note = f'<p class="note">{e(farm["note"])}</p>' if farm.get('note') else ''
        contact_bits = []
        if farm.get('operator'):
            contact_bits.append(e(farm['operator']))
        if farm.get('phone'):
            contact_bits.append(f'<a href="tel:{farm["phone"]}">{e(farm["phone"])}</a>')
        if farm.get('email'):
            contact_bits.append(f'<a href="mailto:{farm["email"]}">{e(farm["email"])}</a>')
        contact = ' · '.join(contact_bits)
        cards.append(f"""<article class="listing-card" id="{farm['slug']}">
        <h3>{e(farm['name'])}</h3>
        <div class="location">{e(farm['city'])}, {e(farm['state'])}</div>
        <div class="breeds">{''.join(f'<span class="breed-chip">{e(c)}</span>' for c in farm['categories'])}</div>
        <p class="genetics">{e(farm['summary'])}</p>
        <p class="products"><strong>Products:</strong></p><ul>{items}</ul>
        <p class="shipping limited"><strong>How to buy:</strong> {e(farm['access'])}</p>
        <p><strong>Contact:</strong> {contact}</p>
        {note}
        <p class="note">Verified from the farm's website on {e(farm['verified'])}.</p>
        <div class="actions"><a href="{add_utm_params(farm['url'], farm['slug'])}" target="_blank" rel="noopener" class="btn-primary">Visit Farm →</a></div>
    </article>""")
    content = f"""
    <section class="hero">
        <div class="container">
            <h1>Beyond Beef</h1>
            <p class="tagline">Verified pasture-raised farms selling chicken, eggs, dairy, and pork direct. Same rules as our ranches: checked by hand, free to list, no commission.</p>
        </div>
    </section>
    <section class="listings-section">
        <div class="container">
            <p class="section-intro">{len(farms)} verified farm{'s' if len(farms) != 1 else ''} so far. These farms are listed separately from our beef ranch directory. Know a farm we should check? Email <a href="mailto:ranches@acreandplate.com">ranches@acreandplate.com</a>.</p>
            <div class="listings-grid">
                {''.join(cards)}
            </div>
        </div>
    </section>
    """
    html = base_template("Beyond Beef: Pasture-Raised Chicken, Eggs, Dairy & Pork Direct From Farms", content, "Verified pasture-raised farms selling chicken, eggs, dairy, and pork direct. No commission.")
    write_page('beyond-beef/index.html', html)

def build_featured_thanks():
    """Build Featured Ranch thank you page"""
    content = """
    <section class="hero">
        <div class="container">
            <h1>Thank You!</h1>
            <p class="tagline">Your Featured Ranch placement is being set up. We'll be in touch within 24 hours to confirm your listing details and start date.</p>
        </div>
    </section>
    
    <section class="thanks-content">
        <div class="container">
            <div class="thanks-box">
                <h2>What Happens Next?</h2>
                
                <div class="next-steps">
                    <div class="step">
                        <div class="step-number">1</div>
                        <h3>Confirmation Email</h3>
                        <p>You'll receive a confirmation email with your subscription details within a few minutes.</p>
                    </div>
                    
                    <div class="step">
                        <div class="step-number">2</div>
                        <h3>Setup & Launch</h3>
                        <p>We'll activate your featured placement within 24 hours. Your listing will appear in featured sections across the site.</p>
                    </div>
                    
                    <div class="step">
                        <div class="step-number">3</div>
                        <h3>Monthly Reports</h3>
                        <p>You'll receive monthly traffic reports showing visits and clicks to your ranch website.</p>
                    </div>
                </div>
                
                <div class="contact-box">
                    <h3>Questions?</h3>
                    <p>Contact us at <a href="mailto:ranches@acreandplate.com">ranches@acreandplate.com</a> to check your listing status or update your information.</p>
                </div>
                
                <div class="cta">
                    <a href="/" class="btn-primary">Return to Home</a>
                    <a href="/listings/" class="btn-secondary">Browse All Ranches</a>
                </div>
            </div>
        </div>
    </section>
    """
    
    html = base_template("Thank You - Featured Ranch", content)
    write_page('featured/thanks/index.html', html)

def market_card(market: Dict[str, Any]) -> str:
    """Generate market card HTML"""
    # Build beef vendors section
    vendors_html = ''
    if market.get('beef_vendors') and len(market['beef_vendors']) > 0:
        vendors_list = []
        for vendor in market['beef_vendors']:
            vendor_text = vendor['name']
            if vendor.get('origin'):
                vendor_text += f" ({vendor['origin']})"
            if vendor.get('note'):
                vendor_text += f" — {vendor['note']}"
            vendors_list.append(f'<li>{vendor_text}</li>')
        vendors_html = f'<div class="market-vendors"><strong>Beef Vendors:</strong><ul>{"".join(vendors_list)}</ul></div>'
    
    # Build note section
    note_html = ''
    if market.get('note'):
        note_html = f'<p class="note">{market["note"]}</p>'
    
    # Build operator section
    operator_html = ''
    if market.get('operator'):
        operator_html = f'<p class="market-operator"><strong>Operated by:</strong> {market["operator"]}</p>'
    
    return f"""<article class="market-card">
        <h3><a href="{market['url']}" target="_blank" rel="noopener">{market['name']}</a></h3>
        <div class="location">{market['city']}, {market['state']}</div>
        <div class="market-schedule"><strong>Schedule:</strong> {market['schedule']}</div>
        <div class="market-location"><strong>Location:</strong> {market['location']}</div>
        {operator_html}
        {vendors_html}
        {note_html}
        <div class="market-verified">Verified {market['verified_at']}</div>
        <div class="actions">
            <a href="{market['url']}" target="_blank" rel="noopener" class="btn-primary">Visit Market Site →</a>
        </div>
    </article>"""

def butcher_card(butcher: Dict[str, Any]) -> str:
    """Generate butcher card HTML"""
    # Build note section
    note_html = ''
    if butcher.get('note'):
        note_html = f'<p class="butcher-note">{butcher["note"]}</p>'
    
    # Build gaps section
    gaps_html = ''
    if butcher.get('gaps'):
        gaps_html = f'<p class="note">{butcher["gaps"]}</p>'
    
    # Build specialties section
    specialties_html = ''
    if butcher.get('specialties') and len(butcher['specialties']) > 0:
        specialties_list = '</li><li>'.join(butcher['specialties'])
        specialties_html = f'<div class="butcher-specialties"><strong>Specialties:</strong><ul><li>{specialties_list}</li></ul></div>'
    
    return f"""<article class="butcher-card">
        <h3><a href="{butcher['url']}" target="_blank" rel="noopener">{butcher['name']}</a></h3>
        <div class="location">{butcher['city']}, {butcher['county']} County</div>
        {note_html}
        {specialties_html}
        {gaps_html}
        <div class="butcher-verified">Verified {butcher['verified_at']}</div>
        <div class="actions">
            <a href="{butcher['url']}" target="_blank" rel="noopener" class="btn-primary">Visit Website →</a>
        </div>
    </article>"""

def strip_html(html_text: str) -> str:
    """Strip HTML tags and return plain text"""
    import re
    # Remove HTML tags
    text = re.sub('<[^<]+?>', '', html_text)
    # Replace common entities
    text = text.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    # Clean up whitespace
    text = ' '.join(text.split())
    return text

def truncate_text(text: str, max_length: int = 155) -> str:
    """Truncate text to max_length, breaking at word boundaries"""
    if len(text) <= max_length:
        return text
    truncated = text[:max_length].rsplit(' ', 1)[0]
    return truncated + '…'

def news_card(item: Dict[str, Any], link_headline: bool = False) -> str:
    """Generate news card HTML"""
    # Parse ISO timestamp and format date for display
    from datetime import datetime
    
    dt = datetime.fromisoformat(item['published_at'])
    formatted_date = dt.strftime("%B %d, %Y")
    
    # Build optional image section
    image_html = ''
    if item.get('image'):
        image_html = f'<div class="news-image"><img src="{item["image"]}" alt=""></div>'
    
    # Get icon (emoji or path)
    icon = item.get('icon', '📰')
    
    # Optionally link headline to story page
    headline_html = item['headline']
    if link_headline:
        headline_html = f'<a href="/news/{item["id"]}/">{item["headline"]}</a>'
    
    # Build absolute URL for this news item
    item_url = f"https://acreandplate.com/news/{item['id']}/"
    
    return f"""<article class="news-card" id="{item['id']}">

        <div class="news-header">
            <span class="news-icon">{icon}</span>
            <h3>{headline_html}</h3>
        </div>
        <div class="news-body">
            {item['body']}
        </div>
        {image_html}
        <div class="news-meta">
            <time datetime="{item['published_at']}">{formatted_date}</time>
        </div>
        <div class="news-actions">
            <button class="news-action-btn favorite-btn" 
                    data-news-id="{item['id']}" 
                    aria-label="Favorite this news item" 
                    aria-pressed="false">
                <svg class="heart-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                <span class="btn-label">Favorite</span>
            </button>
            <button class="news-action-btn share-btn" 
                    data-news-id="{item['id']}"
                    data-news-url="{item_url}"
                    data-news-title="{item['headline']}"
                    aria-label="Share this news item">
                <svg class="share-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="18" cy="5" r="3"></circle>
                    <circle cx="6" cy="12" r="3"></circle>
                    <circle cx="18" cy="19" r="3"></circle>
                    <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                    <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
                </svg>
                <span class="btn-label">Share</span>
            </button>
        </div>
    </article>"""

def build_news_page():
    """Build news hub page with time-grouped feed"""
    from datetime import datetime, timezone, timedelta
    
    # Sort news by published date (newest first)
    sorted_news = sorted(news_items, key=lambda x: x['published_at'], reverse=True)
    
    # Group news by day-part labels (like "Monday afternoon")
    # Use Pacific timezone (UTC-7 or UTC-8)
    pacific_offset = timedelta(hours=-7)  # PDT
    grouped_news = []
    current_label = None
    
    for item in sorted_news:
        dt = datetime.fromisoformat(item['published_at'])
        
        # Generate day-part label
        day_name = dt.strftime("%A")
        hour = dt.hour
        
        if 5 <= hour < 12:
            time_part = "morning"
        elif 12 <= hour < 17:
            time_part = "afternoon"
        elif 17 <= hour < 21:
            time_part = "evening"
        else:
            time_part = "night"
        
        label = f"{day_name} {time_part}"
        
        if label != current_label:
            grouped_news.append({'type': 'label', 'text': label})
            current_label = label
        
        grouped_news.append({'type': 'item', 'data': item})
    
    # Generate HTML for grouped news (with linked headlines)
    news_html = ''
    for entry in grouped_news:
        if entry['type'] == 'label':
            news_html += f'<h2 class="day-label">{entry["text"]}</h2>\n'
        else:
            news_html += news_card(entry['data'], link_headline=True) + '\n'
    
    content = f"""
    <section class="page-header">
        <div class="container">
            <h1>Cattle News</h1>
            <p>Updates from the ranch-direct beef directory</p>
            <p class="count">{len(news_items)} updates</p>
        </div>
    </section>
    
    <section class="news-section">
        <div class="container">
            <div class="news-feed">
                {news_html}
            </div>
        </div>
    </section>
    
    <script src="/assets/news.js"></script>
    """
    
    meta = f"Latest news and updates from Acre & Plate—new ranches, markets, deals, and directory features."
    html = base_template("Cattle News", content, meta)
    write_page('news/index.html', html)

def build_news_story(item: Dict[str, Any]):
    """Build individual news story page with Open Graph tags"""
    from datetime import datetime
    
    # Parse date for display
    dt = datetime.fromisoformat(item['published_at'])
    formatted_date = dt.strftime("%B %d, %Y")
    
    # Create plain text excerpt for og:description
    plain_body = strip_html(item['body'])
    og_description = truncate_text(plain_body, 155)
    
    # Determine og:image
    og_image_url = item.get('image') or item.get('og_image') or 'https://acreandplate.com/assets/og-news-default.png'
    if og_image_url.startswith('/'):
        og_image_url = f"https://acreandplate.com{og_image_url}"
    
    # Build canonical URL
    canonical_url = f"https://acreandplate.com/news/{item['id']}/"
    
    # Build Open Graph tags
    og_tags = f"""<link rel="canonical" href="{canonical_url}">
    <meta property="og:title" content="{item['headline']}">
    <meta property="og:description" content="{og_description}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:type" content="article">
    <meta property="og:image" content="{og_image_url}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{item['headline']}">
    <meta name="twitter:description" content="{og_description}">
    <meta name="twitter:image" content="{og_image_url}">"""
    
    # Build optional image section
    image_html = ''
    if item.get('image'):
        image_html = f'<div class="news-image"><img src="{item["image"]}" alt=""></div>'
    
    # Get icon
    icon = item.get('icon', '📰')
    
    # Build action buttons (matching main's structure)
    story_url = f"https://acreandplate.com/news/{item['id']}/"
    actions_html = f'''<div class="news-actions">
            <button class="news-action-btn favorite-btn" 
                    data-news-id="{item['id']}" 
                    aria-label="Favorite this news item" 
                    aria-pressed="false">
                <svg class="heart-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                <span class="btn-label">Favorite</span>
            </button>
            <button class="news-action-btn share-btn" 
                    data-news-id="{item['id']}"
                    data-news-url="{story_url}"
                    data-news-title="{item['headline']}"
                    aria-label="Share this news item">
                <svg class="share-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="18" cy="5" r="3"></circle>
                    <circle cx="6" cy="12" r="3"></circle>
                    <circle cx="18" cy="19" r="3"></circle>
                    <line x1="8.59" y1="13.51" x2="15.42" y2="17.49"></line>
                    <line x1="15.41" y1="6.51" x2="8.59" y2="10.49"></line>
                </svg>
                <span class="btn-label">Share</span>
            </button>
        </div>'''
    
    content = f"""
    <section class="page-header">
        <div class="container">
            <div class="breadcrumb">
                <a href="/">Home</a> / <a href="/news/">News</a> / {item['headline']}
            </div>
            <h1><span class="news-icon">{icon}</span> {item['headline']}</h1>
            <p><time datetime="{item['published_at']}">{formatted_date}</time></p>
        </div>
    </section>
    
    <section class="news-story">
        <div class="container">
            <article class="news-card news-card-full" data-id="{item['id']}">
                <div class="news-body">
                    {item['body']}
                </div>
                {image_html}
                {actions_html}
            </article>
            <div class="news-story-footer">
                <a href="/news/" class="btn-secondary">← Back to All News</a>
            </div>
        </div>
    </section>
    <script src="/assets/news.js"></script>
    """
    
    html = base_template(item['headline'], content, og_description, og_tags)
    write_page(f"news/{item['id']}/index.html", html)

def build_markets_page():
    """Build markets hub page with farmers markets and butcher shops"""
    # Group markets by city for organization
    markets_by_city = {}
    for market in markets:
        city = market['city']
        if city not in markets_by_city:
            markets_by_city[city] = []
        markets_by_city[city].append(market)
    
    # Generate all market cards
    all_markets_html = '\n'.join([market_card(market) for market in markets])
    
    # Group butchers by county
    butchers_by_county = {}
    for butcher in butchers:
        county = butcher['county']
        if county not in butchers_by_county:
            butchers_by_county[county] = []
        butchers_by_county[county].append(butcher)
    
    # Sort counties alphabetically
    sorted_counties = sorted(butchers_by_county.keys())
    
    # Generate butcher sections by county
    butchers_by_county_html = ''
    for county in sorted_counties:
        county_butchers = butchers_by_county[county]
        county_cards_html = '\n'.join([butcher_card(butcher) for butcher in county_butchers])
        butchers_by_county_html += f"""
        <div class="butchers-by-county">
            <h3 class="county-heading">{county} County ({len(county_butchers)})</h3>
            <div class="butchers-grid">
                {county_cards_html}
            </div>
        </div>
        """
    
    content = f"""
    <section class="page-header">
        <div class="container">
            <h1>Local Activity</h1>
            <p>Farmers markets and butcher shops where locals buy ranch-direct beef</p>
            <p class="count">{len(markets)} farmers markets · {len(butchers)} butcher shops</p>
        </div>
    </section>
    
    <section class="markets-section">
        <div class="container">
            <div class="markets-intro">
                <h2>Farmers Markets</h2>
                <p>Local farmers markets give ranchers a place to sell beef directly to the community. The markets listed here are verified from public sources and feature vendors offering ranch-direct beef with traceable genetics.</p>
                <p><strong>Important:</strong> Vendor lineups change frequently. Always confirm current beef vendors at the market or on the market's website before visiting. Acre & Plate does not operate these markets—we simply list verified public information.</p>
            </div>
            
            <h3 class="section-divider">All Markets</h3>
            <div class="markets-grid">
                {all_markets_html}
            </div>
            
            <div class="markets-disclaimer">
                <p><strong>National Scope:</strong> While we're starting with Bay Area markets, we're expanding nationwide. Know a farmers market where local ranchers sell traceable beef? <a href="mailto:hello@acreandplate.com">Let us know</a>.</p>
            </div>
        </div>
    </section>
    
    <section class="butchers-section">
        <div class="container">
            <div class="butchers-intro">
                <h2>Butcher Shops</h2>
                <p>Local butcher shops where Bay Area residents buy quality beef. These butcher shops are verified from public sources. We don't sell beef—butchers are where locals buy it.</p>
                <p><strong>Note:</strong> Acre & Plate does not verify sourcing claims or grass-fed designations for butcher shops. Contact shops directly for details about their meat sources and practices.</p>
            </div>
            
            <h3 class="section-divider">Butchers by County</h3>
            {butchers_by_county_html}
        </div>
    </section>
    """
    
    meta = f"Find local farmers markets and butcher shops in the Bay Area. {len(markets)} farmers markets and {len(butchers)} butcher shops verified."
    html = base_template("Local Activity - Farmers Markets & Butcher Shops", content, meta)
    write_page('markets/index.html', html)

def build_about():
    """Build about page"""
    content = """
    <section class="page-header">
        <div class="container">
            <h1>About This Directory</h1>
        </div>
    </section>
    
    <section class="about-content">
        <div class="container">
            <article class="about">
                <h2>What Acre & Plate Is</h2>
                <p>A curated directory of ranches selling beef direct to consumers—ranches that name their herds, register their cattle, or verify bloodlines. Find Fullblood Wagyu, Akaushi, Japanese Black, and rare heritage breeds like Randall Lineback, Dexter, and Piedmontese.</p>
                
                <p>Not grocery store "Wagyu" marketing. Not breeding stock. Local, sustainable, ranch-direct beef you can trace.</p>
                
                <h2>Methodology</h2>
                <p>Each ranch listing is verified from the ranch's own public website. We record:</p>
                <ul>
                    <li>Breed and bloodline claims (DNA-tested, registered, traceable herds)</li>
                    <li>Available products (steaks, ground, shares)</li>
                    <li>Shipping info (nationwide, regional, pickup only)</li>
                    <li>Direct contact information</li>
                </ul>
                
                <p>We note gaps where information is thin or shipping is limited. We prefer omitting details over inventing them.</p>
                
                <h2>What We Don't Include</h2>
                <ul>
                    <li>Breeding stock / live cattle sales</li>
                    <li>Retail products without ranch attribution</li>
                    <li>"Wagyu-style" products without traceable sourcing</li>
                    <li>Restaurants (unless they're the ranch's direct retail channel)</li>
                </ul>
                
                <h2>Who Built This</h2>
                <p>Acre & Plate is an independent directory connecting consumers with ranches raising cattle with traceable genetics. Data is verified from ranch websites and updated periodically. If you're a ranch owner and need to update your listing, please email us at <a href="mailto:ranches@acreandplate.com">ranches@acreandplate.com</a>.</p>
                
                <h2>How to Use Acre & Plate</h2>
                <ol>
                    <li><strong>Browse</strong> by breed, state, or all listings</li>
                    <li><strong>Check breed claims</strong> on each ranch's detail page</li>
                    <li><strong>Visit ranch websites</strong> to verify current availability and pricing</li>
                    <li><strong>Order direct</strong> from the ranch</li>
                </ol>
                
                <p class="disclaimer"><strong>Disclaimer:</strong> We don't sell beef. We don't receive commissions. We list publicly available information. Contact ranches directly for orders. Verify claims independently if needed.</p>
                
                <h2>Contact</h2>
                <p>Have questions or feedback? Reach out to us at <a href="mailto:hello@acreandplate.com">hello@acreandplate.com</a></p>
                
                <div class="cta">
                    <a href="/listings/" class="btn-primary">Browse All Ranches</a>
                </div>
            </article>
        </div>
    </section>
    """
    
    html = base_template("About", content, "How Acre & Plate works and what makes it different from grocery store 'Wagyu' marketing.")
    write_page('about/index.html', html)

def legal_page(slug: str, title: str, description: str, sections) -> None:
    """Plain legal page (privacy / terms) in the site's about-page layout"""
    body = "\n".join(
        f"                <h2>{h}</h2>\n" + "\n".join(f"                <p>{p}</p>" for p in ps)
        for h, ps in sections)
    content = f"""
    <section class="page-header">
        <div class="container">
            <h1>{title}</h1>
        </div>
    </section>
    
    <section class="about-content">
        <div class="container">
            <article class="about">
                <p class="disclaimer">Last updated November 24, 2026</p>
{body}
            </article>
        </div>
    </section>
    """
    write_page(f'{slug}/index.html', base_template(title, content, description))

def build_legal_pages():
    """Build /privacy/ and /terms/"""
    hello = '<a href="mailto:hello@acreandplate.com">hello@acreandplate.com</a>'
    legal_page('privacy', 'Privacy Policy', "How Acre & Plate handles information when you browse the directory, email us, or buy a Featured Ranch placement.", [
        ("Who we are", [f"Acre &amp; Plate (acreandplate.com) is an independent directory of ranches that sell beef direct to consumers. Questions about this policy can be sent to {hello}."]),
        ("Browsing the site", ["This site does not use analytics or advertising cookies. Like most websites, our host, Netlify, processes standard technical request data such as IP address, browser type, and the pages requested in order to serve and secure the site.",
                               "Links to ranch websites include tracking parameters (such as utm_source=acreandplate) so ranches can see that a visit came from Acre &amp; Plate. These parameters do not contain personal information about you."]),
        ("When you contact us", ["If you email us, for example to update a ranch listing or ask a question, we receive your email address and whatever you include in your message. We use it to reply and to keep the directory accurate. We do not sell your personal information."]),
        ("Featured Ranch purchases", ['Featured Ranch placements are paid through Stripe. Stripe collects the payment details needed to complete the purchase and shares the order details with us; we do not see or store full card numbers. See <a href="https://stripe.com/privacy" rel="noopener">Stripe&#8217;s privacy policy</a>.']),
        ("Shop and other sites", ["Our merchandise shop at acreandplate.printful.me is run on Printful, and ranch websites we link to are run by the ranches. Their own privacy policies apply when you visit them."]),
        ("Retention and your rights", [f"We keep emails and purchase records only as long as we need them for the purposes above or as required by law. You can ask what information we hold about you, or ask us to correct or delete it, by emailing {hello}."]),
        ("Children", ["This site is not directed to children under 13, and we do not knowingly collect their personal information."]),
        ("Changes", ["We may update this policy. The date at the top shows when it last changed."]),
    ])
    legal_page('terms', 'Terms of Use', "The terms that apply when you use the Acre & Plate ranch directory.", [
        ("Agreement", [f"By using acreandplate.com you agree to these terms. Questions can be sent to {hello}."]),
        ("A directory, not a store", ["Acre &amp; Plate does not sell beef. Any purchase you make from a ranch is between you and that ranch, under the ranch&#8217;s own terms, prices, and shipping policies."]),
        ("Accuracy", ["Listings, breed claims, prices, and deals are gathered from ranches&#8217; public websites and may be incomplete or out of date. Please confirm current details, availability, and pricing with the ranch before you order."]),
        ("Featured placements", ["Some listings are paid Featured Ranch placements and are labeled as featured. A featured placement is not an endorsement or a guarantee of any ranch&#8217;s products."]),
        ("Use of the site", ["Please do not misuse the site, including by attempting to disrupt it, scraping it at a rate that degrades service, or republishing the directory as your own. You are welcome to share links."]),
        ("Third-party sites", ["We link to ranch websites and other services we do not control and are not responsible for their content or practices."]),
        ("No warranty; limitation of liability", ["The site is provided &#8220;as is&#8221; without warranties of any kind. To the fullest extent permitted by law, Acre &amp; Plate is not liable for any indirect or consequential damages arising from your use of the site or from dealings with any ranch."]),
        ("Changes", ["We may update these terms. The date at the top shows when they last changed."]),
    ])

def prune_orphaned_listings():
    """Remove orphaned listing directories not in listings.json"""
    import os
    import shutil
    
    # Get all current listing slugs from data
    current_slugs = {listing['slug'] for listing in listings}
    
    # Get all directories in listings/
    listings_dir = Path('listings')
    if not listings_dir.exists():
        return
    
    orphaned = []
    for item in listings_dir.iterdir():
        if not item.is_dir():
            continue
        
        dir_name = item.name
        
        # Check if this directory is orphaned (not in current listings)
        if dir_name not in current_slugs:
            # Verify it only contains an index.html (our generated file)
            contents = list(item.iterdir())
            if len(contents) == 1 and contents[0].name == 'index.html':
                print(f"🗑️  Pruning orphaned listing: {dir_name}")
                shutil.rmtree(item)
                orphaned.append(dir_name)
            else:
                print(f"⚠️  Skipping {dir_name} (contains unexpected files)")
    
    if orphaned:
        print(f"\n✓ Pruned {len(orphaned)} orphaned listing(s): {', '.join(orphaned)}")
    else:
        print("\n✓ No orphaned listings found")

SITE_URL = 'https://acreandplate.com'
# Generated pages that should not be in sitemap.xml (post-checkout thank-you page)
SITEMAP_EXCLUDE = {'featured/thanks/index.html'}

def build_sitemap():
    """Write sitemap.xml listing every public */index.html page on the site"""
    from xml.sax.saxutils import escape
    news_dates = {}
    for item in news_items:
        day = (item.get('published_at') or '')[:10]
        if day and day <= get_build_date_iso():
            news_dates[f"news/{item['id']}/index.html"] = day
    pages = []
    for root, dirs, files in os.walk('.'):
        dirs[:] = sorted(d for d in dirs if not d.startswith(('.', '_')) and d != 'node_modules')
        if 'index.html' not in files:
            continue
        rel = os.path.relpath(os.path.join(root, 'index.html'), '.').replace(os.sep, '/')
        if rel in SITEMAP_EXCLUDE:
            continue
        with open(rel, 'r', encoding='utf-8', errors='ignore') as f:
            head = f.read(4000).lower()
        if 'noindex' in head:
            continue
        pages.append(rel)
    pages.sort(key=lambda r: (r != 'index.html', r))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for rel in pages:
        path = '/' if rel == 'index.html' else '/' + rel[:-len('index.html')]
        lines.append('  <url>')
        lines.append(f'    <loc>{escape(SITE_URL + path)}</loc>')
        if rel in news_dates:
            lines.append(f'    <lastmod>{news_dates[rel]}</lastmod>')
        lines.append('  </url>')
    lines.append('</urlset>')
    with open('sitemap.xml', 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"✓ sitemap.xml ({len(pages)} URLs)")

def get_build_date_iso() -> str:
    """Today's date (YYYY-MM-DD), used to skip future lastmod values"""
    from datetime import date
    return date.today().isoformat()

def main():
    """Build all pages"""
    print("Building Acre & Plate...\n")
    
    # Prune orphaned listing directories before building
    prune_orphaned_listings()
    print()
    
    # Home page
    build_index()
    
    # All listings index
    build_listings_index()
    
    # Individual listing pages
    for listing in listings:
        build_listing_detail(listing)
    
    # Hub pages
    build_hub_page(
        "Wagyu Ranches",
        "wagyu",
        lambda l: 'wagyu' in l['breeds'],
        "Fullblood Wagyu ranches with registered or DNA-verified Japanese bloodlines. Most are Japanese Black (Kuroge), the breed known for intense marbling."
    )
    
    build_hub_page(
        "Akaushi Ranches",
        "akaushi",
        lambda l: 'akaushi' in l['breeds'],
        "Akaushi (Japanese Brown) ranches with traceable bloodlines. Akaushi is a rarer Wagyu breed known for balanced marbling and high monounsaturated fats."
    )
    
    build_hub_page(
        "Texas Ranches",
        "texas",
        lambda l: l['state'] == 'TX',
        "Texas ranches raising Wagyu, Akaushi, and other traceable-bloodline beef. Ranch-direct shipping available."
    )
    
    build_hub_page(
        "California Ranches",
        "california",
        lambda l: l['state'] == 'CA' or 'CA' in l.get('state', ''),
        "California ranches with pasture-raised beef and regenerative grazing practices. Local pickup and shipping available."
    )
    
    build_hub_page(
        "Colorado Ranches",
        "colorado",
        lambda l: l['state'] == 'CO',
        "Colorado ranches raising Wagyu and other traceable-bloodline beef in the Rocky Mountains. Ranch-direct shipping available."
    )
    
    build_hub_page(
        "Florida Ranches",
        "florida",
        lambda l: l['state'] == 'FL',
        "Florida ranches raising Wagyu with DNA-tested or grass-finished herds. Local pickup and Florida-only shipping available where applicable."
    )
    
    build_hub_page(
        "Georgia Ranches",
        "georgia",
        lambda l: l.get('state') == 'GA',
        "Georgia family farms raising grass-fed and grass-finished beef, from regenerative land management and on-farm USDA processing in Bluffton to local delivery around Gainesville in north Georgia."
    )
    
    build_hub_page(
        "Wyoming Ranches",
        "wyoming",
        lambda l: 'WY' in l.get('state', ''),
        "Wyoming ranches raising Fullblood Wagyu in the Greater Yellowstone area and beyond. Ranch-direct shipping available."
    )
    
    build_hub_page(
        "Oregon Ranches",
        "oregon",
        lambda l: l['state'] == 'OR',
        "Oregon ranches raising USDA Certified Organic, grass-fed and grass-finished beef with traceable herds. Ranch-direct shipping available."
    )
    
    build_hub_page(
        "Washington Ranches",
        "washington",
        lambda l: l['state'] == 'WA',
        "Washington ranches raising 100% Fullblood Wagyu in the Pacific Northwest. Ranch-direct beef from the Klickitat Valley."
    )
    
    build_hub_page(
        "Wisconsin Ranches",
        "wisconsin",
        lambda l: l['state'] == 'WI',
        "Wisconsin grass-fed beef, from a farmer-owned cooperative of 230+ family farms to a first-generation family farm in Mondovi with daily rotational grazing, on-farm Burger Nights, and Midwest shipping."
    )
    
    build_hub_page(
        "Heritage Breeds",
        "heritage",
        lambda l: 'heritage' in l.get('breeds', []),
        "Heritage breed cattle including critically endangered Randall Lineback and rare Dexter breeds. Centuries-old genetics raised with regenerative practices."
    )
    
    build_hub_page(
        "Hawaii Ranches",
        "hawaii",
        lambda l: l.get('state') == 'HI',
        "Hawaii ranches raising 100% grass-fed and grass-finished beef on island pasture, with farm pickup and frozen shipping between the islands."
    )
    
    build_hub_page(
        "Idaho Ranches",
        "idaho",
        lambda l: 'ID' in l.get('state', ''),
        "Idaho ranches raising certified organic, grass-fed and grass-finished beef. Ranch-direct shipping available."
    )
    
    build_hub_page(
        "Montana Ranches",
        "montana",
        lambda l: l.get('state') == 'MT',
        "Montana ranches raising pasture-raised, ranch-direct beef with nationwide shipping."
    )
    
    build_hub_page(
        "Arizona Ranches",
        "arizona",
        lambda l: l.get('state') == 'AZ',
        "Arizona ranches raising 100% grass-fed and grass-finished beef on open range land with nationwide shipping."
    )
    
    build_hub_page(
        "Iowa Ranches",
        "iowa",
        lambda l: l.get('state') == 'IA',
        "Iowa family farms raising 100% grass-fed and grass-finished beef, from a fifth-generation regenerative farm in Clarion shipping nationwide to a Red Angus herd in Carroll shipping across 28 states."
    )
    
    build_hub_page(
        "Illinois Ranches",
        "illinois",
        lambda l: l.get('state') == 'IL',
        "Illinois ranches and family farms raising 100% grass-fed and grass-finished beef, from a regenerative Southern Illinois ranch with nationwide shipping to an organic-pasture Angus herd delivering across the Chicago area."
    )
    
    build_hub_page(
        "Kansas Ranches",
        "kansas",
        lambda l: l.get('state') == 'KS',
        "Kansas ranches raising 100% grass-fed and grass-finished beef with regenerative practices and nationwide shipping."
    )
    
    build_hub_page(
        "Michigan Ranches",
        "michigan",
        lambda l: l.get('state') == 'MI',
        "Michigan family farms selling beef direct, from Full-blood Wagyu beef shares with local delivery near Laingsburg to grass-fed, grass-finished cuts and bundles from a Millington farm in the Thumb that ships frozen across much of the U.S."
    )
    
    build_hub_page(
        "Minnesota Ranches",
        "minnesota",
        lambda l: l.get('state') == 'MN',
        "Minnesota beef, from American Wagyu dry-aged at a family butcher shop in Conger to 100% grass-fed beef from a fourth-generation family farm in Elgin with weekly home delivery. Both ship to the lower 48."
    )
    
    build_hub_page(
        "Missouri Ranches",
        "missouri",
        lambda l: l.get('state') == 'MO',
        "Missouri ranches selling beef direct, from a Fullblood Wagyu farm in Kaiser with a unique feeding program and nationwide shipping to a Rocheport family farm raising 100% grass-fed, grass-finished beef for farm pickup."
    )
    
    build_hub_page(
        "Oklahoma Ranches",
        "oklahoma",
        lambda l: l.get('state') == 'OK',
        "Oklahoma ranches raising premium Black Angus beef, born and raised on family ranches with nationwide shipping."
    )
    
    build_hub_page(
        "Rhode Island Ranches",
        "rhode-island",
        lambda l: l.get('state') == 'RI',
        "Rhode Island farms selling 100% grass-fed, grass-finished beef direct from the farm store, with curbside pickup and local delivery."
    )
    
    build_hub_page(
        "Connecticut Ranches",
        "connecticut",
        lambda l: l.get('state') == 'CT',
        "Connecticut farms selling 100% grass-fed, grass-finished beef direct, with on-farm pickup by appointment and delivery routes across southern New England."
    )
    
    build_hub_page(
        "Delaware Ranches",
        "delaware",
        lambda l: l.get('state') == 'DE',
        "Delaware family farms selling grass-fed, grain-finished beef raised without antibiotics or added hormones, by the cut or by the share, with pickup at the farm in Harrington."
    )
    
    build_hub_page(
        "New Hampshire Ranches",
        "new-hampshire",
        lambda l: l.get('state') == 'NH',
        "New Hampshire farms raising 100% grass-fed, grass-finished Scottish Highland beef and bison, with a year-round farm store in Warner and frozen shipping across the continental U.S."
    )
    
    build_hub_page(
        "New Jersey Ranches",
        "new-jersey",
        lambda l: l.get('state') == 'NJ',
        "New Jersey farms raising 100% grass-fed, grass-finished Black Angus beef, dry-aged 14 days, with a Warren County farm store and weekly frozen shipping across the East Coast."
    )
    
    build_hub_page(
        "New York Ranches",
        "new-york",
        lambda l: l.get('state') == 'NY',
        "New York family farms raising pasture-raised beef, from an all-natural Angus ranch in the Butternut Valley that ships nationwide to a 100% grass-fed Hudson Valley farm in Valatie with an on-farm store and bulk beef for pickup."
    )
    
    build_hub_page(
        "North Carolina Ranches",
        "north-carolina",
        lambda l: l.get('state') == 'NC',
        "Two North Carolina ranches selling beef direct: pasture-raised Hereford and Angus, dry-aged on a fifth-generation farm in Vilas and shipped frozen nationwide, and grass-fed, grass-finished beef from a family ranch in Tobaccoville, sold by the share with free North Carolina delivery and a shipped quarter to the lower 48."
    )
    
    build_hub_page(
        "North Dakota Ranches",
        "north-dakota",
        lambda l: l.get('state') == 'ND',
        "Two North Dakota ranches selling beef direct: regenerative, 100% grass-fed and grass-finished beef born on the ranch, with home delivery to the lower 48 and Bismarck-area pickup, and home-raised, grass-finished beef from a family ranch near Ashley sold through its own online store."
    )
    
    build_hub_page(
        "Tennessee Ranches",
        "tennessee",
        lambda l: l.get('state') == 'TN',
        "Tennessee ranches raising American Wagyu beef with free-range, hormone-free practices and nationwide shipping."
    )
    
    build_hub_page(
        "Utah Ranches",
        "utah",
        lambda l: l.get('state') == 'UT',
        "Utah ranches raising locally raised beef with family farm traditions and ranch-direct delivery."
    )
    
    build_hub_page(
        "Pennsylvania Ranches",
        "pennsylvania",
        lambda l: l.get('state') == 'PA',
        "Pennsylvania family farms raising grass-fed, grass-finished beef, from a Scottish Highland herd in St. Marys that ships nationwide to a regenerative Bucks County farm in Sellersville with an on-farm store and Berger Box subscriptions shipped across the Northeast."
    )
    
    build_hub_page(
        "South Dakota Ranches",
        "south-dakota",
        lambda l: l.get('state') == 'SD',
        "Two South Dakota ranches selling beef direct: heritage breed Belted Galloway cattle grassfed and grass-finished on tallgrass prairie in Estelline, sold for pickup at the farm and in Brookings, Sioux Falls, and Watertown, and 100% grass-finished beef from a family farm near Platte that ships frozen across the lower 48."
    )
    
    build_hub_page(
        "Ohio Ranches",
        "ohio",
        lambda l: l.get('state') == 'OH',
        "Ohio ranches and family farms raising 100% grass-fed beef, from regenerative grass-finished herds in Holmes County to Highland cattle in Union County, with home delivery across Ohio."
    )
    
    build_hub_page(
        "Indiana Ranches",
        "indiana",
        lambda l: l.get('state') == 'IN',
        "Indiana family farms raising 100% grass-fed and grass-finished beef, from an American Grassfed Association certified South Poll and Corriente herd in Greenfield to an Angus-based Middletown herd whose dry-aged beef ships frozen across the lower 48 with free farm pickup."
    )
    
    build_hub_page(
        "Kentucky Ranches",
        "kentucky",
        lambda l: l.get('state') == 'KY',
        "Kentucky family farms raising 100% grass-fed and grass-finished beef, from registered Heritage Dexter cattle in Edmonton to a biodynamic closed herd in Crestwood, with regional delivery and East Coast shipping."
    )
    
    build_hub_page(
        "Louisiana Ranches",
        "louisiana",
        lambda l: l.get('state') == 'LA',
        "Louisiana farms selling grass-fed, pasture-finished, dry-aged beef direct from the farm, ordered online and picked up at the farm or a local pickup spot."
    )
    
    build_hub_page(
        "Mississippi Ranches",
        "mississippi",
        lambda l: l.get('state') == 'MS',
        "Two Mississippi ranches selling beef direct: 100% grass-fed and grass-finished beef from a fifth-generation family farm in Como, with on-farm USDA processing and nationwide frozen shipping, and 100% grass-finished beef from Etta Hills Farm in Etta, on pasture from birth through the last day, with farm pickup, free local delivery near Etta, and continental frozen shipping the site still marks as coming soon."
    )
    
    build_hub_page(
        "Nevada Ranches",
        "nevada",
        lambda l: l.get('state') == 'NV',
        "Nevada ranches selling beef direct from registered Black Angus herds raised on irrigated Great Basin pasture, with Fallon pickup, regional delivery and frozen UPS shipping across the West."
    )
    
    build_hub_page(
        "Maryland Ranches",
        "maryland",
        lambda l: l.get('state') == 'MD',
        "Two Maryland farms selling Black Angus beef direct: dry-aged beef with farm stores near Baltimore and Frederick and frozen shipping nationwide, and 100% grass-fed beef from a family farm near Buckeystown, sold by the share for pickup in Adamstown and Potomac."
    )
    
    build_hub_page(
        "West Virginia Ranches",
        "west-virginia",
        lambda l: l.get('state') == 'WV',
        "West Virginia farms selling 100% grass-fed, grass-finished beef direct from the farm, from an on-farm store in Romney with frozen shipping to the lower 48, to monthly pickup and delivery around Fairmont and Morgantown."
    )
    
    build_hub_page(
        "South Carolina Ranches",
        "south-carolina",
        lambda l: l.get('state') == 'SC',
        "South Carolina beef sold direct from the farm, from AWA-certified Full Blood Wagyu in Landrum to 100% grass-fed, grass-finished beef from Watson Farms in Chester, shipped frozen across the lower 48."
    )
    
    build_hub_page(
        "Vermont Ranches",
        "vermont",
        lambda l: l.get('state') == 'VT',
        "Vermont beef sold direct from the farm, from Wagyu raised in Springfield to 100% grass-fed beef bred, born and raised at North Hollow Farm in Rochester, with an on-farm store on Route 100."
    )
    
    build_hub_page(
        "Virginia Ranches",
        "virginia",
        lambda l: l.get('state') == 'VA',
        "Virginia beef sold direct from the farm, from critically endangered Randall Lineback cattle in Berryville to 100% grass-fed beef from the Salatin family's Polyface Farm in the Shenandoah Valley, shipped frozen by UPS."
    )
    
    build_hub_page(
        "Nebraska Ranches",
        "nebraska",
        lambda l: l.get('state') == 'NE',
        "Nebraska beef sold direct, from Piedmontese raised on Midwest family ranches to DNA-tested, dry-aged beef from a fifth-generation West Point family shipped frozen to all 50 states."
    )
    
    build_hub_page(
        "New Mexico Ranches",
        "new-mexico",
        lambda l: l.get('state') == 'NM',
        "New Mexico beef sold direct from the ranch, from 100% Fullblood Wagyu with DNA-certified Japanese lineage shipped nationwide to grassfed and grass-finished beef from Sol Ranch in Wagon Mound with local delivery across New Mexico and Trinidad, CO."
    )
    
    build_hub_page(
        "Arkansas Ranches",
        "arkansas",
        lambda l: l.get('state') == 'AR',
        "Arkansas ranches selling beef direct, from registered Akaushi near Hot Springs shipped frozen nationwide to 100% grass-finished beef from a fourth-generation Fayetteville family farm with local delivery and pickup."
    )
    
    build_hub_page(
        "Alaska Ranches",
        "alaska",
        lambda l: l.get('state') == 'AK',
        "Alaska ranches raising beef born and finished on Interior pasture, sold as farm shares and boxes delivered to Fairbanks, North Pole, Palmer and Anchorage."
    )
    
    build_hub_page(
        "Alabama Ranches",
        "alabama",
        lambda l: l.get('state') == 'AL',
        "Two Alabama ranches selling beef direct: dry-aged, grass-fed grain-finished beef from Diamond D Ranch in Ramer, with free Saturday pickup at the Montgomery Curb Market and frozen shipping to the contiguous U.S., and 100% grass-fed, grass-finished beef from Purely Pastured Farm in Foley, with farm pickup by appointment in Baldwin County, home delivery within 22 miles for Subscribe & Save customers, and no shipping."
    )
    
    build_hub_page(
        "Maine Ranches",
        "maine",
        lambda l: l.get('state') == 'ME',
        "Maine farms selling 100% grass-fed, grass-finished beef by the cut, raised on organic pasture near Brunswick, with online ordering for farm and farmers' market pickup."
    )
    
    build_hub_page(
        "Massachusetts Ranches",
        "massachusetts",
        lambda l: l.get('state') == 'MA',
        "Massachusetts farms selling grass-fed beef direct, from Angus cuts on conserved central Massachusetts farmland with frozen shipping around New England, New York and New Jersey, to certified grassfed Hereford beef on the South Coast with delivery around Boston and Providence."
    )
    
    # Guide
    build_guide()
    
    # Featured Ranch pages
    build_featured()
    build_featured_thanks()
    build_beyond_beef()
    build_list_your_ranch()
    
    # About
    build_about()
    build_legal_pages()
    
    # Deals page
    build_deals_page()

    # Holiday prime rib price board
    build_prime_rib_page()
    
    # Markets page
    build_markets_page()
    
    # News page
    build_news_page()
    
    # Individual news story pages
    for item in news_items:
        build_news_story(item)
    
    print(f"\n✓ Built {len(listings)} listing pages")
    print("✓ Built hub pages (wagyu, akaushi, heritage, alabama, alaska, arizona, arkansas, connecticut, delaware, indiana, iowa, kansas, kentucky, louisiana, maine, maryland, massachusetts, michigan, minnesota, mississippi, missouri, nebraska, nevada, new-hampshire, new-jersey, new-mexico, new-york, north-carolina, north-dakota, ohio, oklahoma, pennsylvania, rhode-island, south-carolina, south-dakota, tennessee, texas, utah, vermont, virginia, california, colorado, florida, georgia, hawaii, idaho, montana, oregon, washington, west-virginia, wisconsin, wyoming)")
    print("✓ Built guide and about pages")
    print(f"✓ Built deals page with {len(deals)} deals")
    print("✓ Built prime rib price board")
    print(f"✓ Built markets page with {len(markets)} farmers markets and {len(butchers)} butcher shops")
    print(f"✓ Built news page with {len(news_items)} updates")
    print(f"✓ Built {len(news_items)} individual news story pages")
    print("✓ Built featured ranch pages")
    # Sitemap (after all pages are written)
    build_sitemap()
    print(f"\n✨ Site build complete! Total pages: {len(listings) + len(news_items) + 18}")

if __name__ == '__main__':
    main()
