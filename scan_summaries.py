#!/usr/bin/env python3
"""
Scan all listings for problematic summaries and identify what needs fixing.
"""

import json
import re

with open('data/listings.json', 'r') as f:
    data = json.load(f)
    listings = data['listings']

def extract_summary_sentences(text, target_sentences=2):
    """Extract 1-2 sentences from text, handling abbreviations"""
    if not text:
        return ''
    
    # Replace common abbreviations to avoid splitting on them
    text = text.replace('T.O.', 'TO').replace('U.S.', 'US').replace('U.K.', 'UK')
    text = text.replace('Dr.', 'Dr').replace('Mr.', 'Mr').replace('Mrs.', 'Mrs')
    text = text.replace('Inc.', 'Inc').replace('Co.', 'Co').replace('Ltd.', 'Ltd')
    
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Take first 1-2 sentences
    result = ' '.join(sentences[:target_sentences])
    
    # Restore abbreviations
    result = result.replace('TO', 'T.O.').replace(' US', ' U.S.').replace(' UK', ' U.K.')
    result = result.replace(' Dr', ' Dr.').replace(' Mr', ' Mr.').replace(' Mrs', ' Mrs.')
    result = result.replace(' Inc', ' Inc.').replace(' Co', ' Co.').replace(' Ltd', ' Ltd.')
    
    return result

def get_card_summary(listing):
    """Get the summary that would appear on the card"""
    description = listing.get('description', '')
    genetics = listing.get('genetics', '')
    
    # Try description first
    if description:
        summary = extract_summary_sentences(description, 2)
        if len(summary) >= 30:  # Minimum viable summary length
            return summary, 'description'
    
    # Fall back to genetics
    if genetics:
        summary = extract_summary_sentences(genetics, 2)
        if len(summary) >= 30:
            return summary, 'genetics'
        # If genetics is too short, use it all
        return genetics, 'genetics'
    
    # Last resort: use what we have
    return description or genetics or 'No description available', 'fallback'

# Scan all listings
problematic = []
for listing in listings:
    summary, source = get_card_summary(listing)
    
    # Check for issues
    issues = []
    if len(summary) < 20:
        issues.append('too_short')
    if summary.endswith(' ') or summary.endswith('-'):
        issues.append('cut_mid_word')
    if not summary or summary == 'No description available':
        issues.append('empty')
    if summary.endswith('.') and len(summary) < 30:
        issues.append('likely_truncated')
    
    if issues:
        problematic.append({
            'name': listing['name'],
            'slug': listing['slug'],
            'summary': summary,
            'source': source,
            'length': len(summary),
            'issues': issues
        })

print(f"Found {len(problematic)} listings with problematic summaries:\n")
for item in problematic:
    print(f"❌ {item['name']} ({item['slug']})")
    print(f"   Summary ({item['length']} chars): \"{item['summary']}\"")
    print(f"   Source: {item['source']}")
    print(f"   Issues: {', '.join(item['issues'])}")
    print()

if not problematic:
    print("✅ All summaries look good!")
