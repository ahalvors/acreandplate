#!/usr/bin/env python3
"""
Apply badge fields to listings.json
"""

import json
import re

with open('data/listings.json', 'r') as f:
    data = json.load(f)
    listings = data['listings']

def derive_finish(listing):
    """Derive finish type from genetics field"""
    genetics = listing.get('genetics', '').lower()
    description = listing.get('description', '').lower()
    note = listing.get('note', '').lower()
    text = f"{genetics} {description} {note}"
    
    # Grass or grain (ask) - check this FIRST before individual checks
    if 'both grass-finished and grain-finished are offered' in text:
        return 'grass-or-grain'
    if 'grass-finished and grain-finished are offered' in text:
        return 'grass-or-grain'
    
    # Mostly grass-fed (mixed diet) - check this BEFORE grass-finished
    if 'mostly grass-fed' in text:
        return 'mostly-grass-fed'
    if 'finishing ration' in text and 'grass' in text:
        return 'mostly-grass-fed'
    if 'grass-fed, grain-finished' in text or 'grass-raised, grain-finished' in text:
        return 'mostly-grass-fed'
    
    # Check for explicit negation of grass-finished
    if 'not 100% grass-fed or grass-finished' in text or 'not grass-finished' in text:
        # Has grass but not finished, likely mixed
        if 'grass' in text:
            return 'mostly-grass-fed'
        return None
    
    # Grass-finished (strong indicators)
    if 'grassfed and grass-finished' in text or '100% grass-fed and grass-finished' in text:
        return 'grass-finished'
    if 'grass-fed and grass-finished' in text:
        return 'grass-finished'
    if re.search(r'\bgrass-finished\b', text) or re.search(r'\bgrass finished\b', text):
        # Only if not contradicted
        if 'grain' not in text or 'grain-finished' not in text:
            return 'grass-finished'
    
    # Grain-finished
    if 'grain-finished' in text or 'grain finished' in text:
        # Check if it's mixed (grass-raised, grain-finished)
        if 'grass-raised' in text or 'grass-fed' in text or 'pasture' in text:
            return 'mostly-grass-fed'
        return 'grain-finished'
    
    return None

def derive_ships_scope(listing):
    """Derive shipping scope from shipping field"""
    shipping = listing.get('shipping', '').lower()
    
    if 'ships nationwide' in shipping or 'nationwide' in shipping:
        # Check for actual nationwide (not limited)
        if 'alaska' in shipping or 'hawaii' in shipping or '50 states' in shipping:
            return 'nationwide'
        # Check for lower 48
        if '48' in shipping or 'contiguous' in shipping or 'continental' in shipping:
            return 'lower-48'
        return 'nationwide'  # Default if unclear
    
    if 'lower 48' in shipping or '48 states' in shipping or 'contiguous' in shipping or 'continental us' in shipping:
        return 'lower-48'
    
    # Regional indicators
    if 'pickup only' in shipping:
        return 'none'
    if any(state in shipping for state in ['florida only', 'california', 'texas', 'regional', 'local']):
        return 'regional'
    if 'ships' not in shipping and 'pickup' in shipping:
        return 'none'
    
    # Conservative: if shipping mentions specific states/regions
    if any(word in shipping for word in ['delivery', 'zip', 'area']):
        return 'regional'
    
    return None

def derive_pickup(listing):
    """Derive pickup availability from shipping field"""
    shipping = listing.get('shipping', '').lower()
    note = listing.get('note', '').lower()
    text = f"{shipping} {note}"
    
    if 'pickup only' in text:
        return 'Pickup only'
    if 'on-farm pickup' in text or 'farm pickup' in text:
        return 'On-farm pickup'
    if 'local pickup' in text:
        return 'Local pickup'
    if 'ranch pickup' in text:
        return 'Ranch pickup'
    if 'pickup' in shipping:
        return True  # Generic pickup available
    
    return None

def derive_certs(listing):
    """Derive certifications from genetics/description/note"""
    genetics = listing.get('genetics', '')
    description = listing.get('description', '')
    note = listing.get('note', '')
    text = f"{genetics} {description} {note}"
    
    certs = []
    
    # Check for specific certifications
    if 'AGA Certified Grassfed' in text or 'American Grassfed Association' in text:
        if 'certified' in text.lower() or 'certification' in text.lower():
            certs.append('AGA Certified Grassfed')
    
    if 'USDA Certified Organic' in text or ('USDA' in text and 'organic' in text.lower() and 'certified' in text.lower()):
        certs.append('USDA Organic')
    
    if 'Audubon Certified' in text:
        certs.append('Audubon Bird Friendly')
    
    if 'Non-GMO verified' in text or 'Non-GMO Verified' in text:
        certs.append('Non-GMO Verified')
    
    return certs if certs else None

# Apply fields to all listings
badge_summary = []
for listing in listings:
    finish = derive_finish(listing)
    ships_scope = derive_ships_scope(listing)
    pickup = derive_pickup(listing)
    certs = derive_certs(listing)
    
    # Add fields to listing (only if they have values)
    if finish:
        listing['finish'] = finish
    if ships_scope:
        listing['ships_scope'] = ships_scope
    if pickup:
        listing['pickup'] = pickup
    if certs:
        listing['certs'] = certs
    
    badge_summary.append({
        'slug': listing['slug'],
        'name': listing['name'],
        'finish': finish,
        'ships_scope': ships_scope,
        'pickup': pickup,
        'certs': certs
    })

# Write updated listings.json
with open('data/listings.json', 'w') as f:
    json.dump(data, f, indent=2)
    
print(f"✓ Updated {len(listings)} listings in data/listings.json")

# Save badge summary for PR description
with open('badge_summary.json', 'w') as f:
    json.dump(badge_summary, f, indent=2)
    
print(f"✓ Saved badge summary to badge_summary.json")

# Print summary stats
print(f"\n=== BADGE SUMMARY ===")
print(f"With finish: {len([r for r in badge_summary if r['finish']])}")
print(f"With ships_scope: {len([r for r in badge_summary if r['ships_scope']])}")
print(f"With pickup: {len([r for r in badge_summary if r['pickup']])}")
print(f"With certs: {len([r for r in badge_summary if r['certs']])}")
print(f"With no badges: {len([r for r in badge_summary if not r['finish'] and not r['ships_scope'] and not r['pickup'] and not r['certs']])}")

# Print listings with no badges for review
no_badges = [r for r in badge_summary if not r['finish'] and not r['ships_scope'] and not r['pickup'] and not r['certs']]
if no_badges:
    print(f"\n=== LISTINGS WITH NO BADGES ({len(no_badges)}) ===")
    for r in no_badges:
        print(f"  - {r['name']} ({r['slug']})")
