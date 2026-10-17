#!/usr/bin/env python3
"""
Report which listings' summaries were fixed.
Compare old broken logic (split on first period) vs new logic.
"""

import json
import re

with open('data/listings.json', 'r') as f:
    data = json.load(f)
    listings = data['listings']

def old_logic(listing):
    """Old broken logic that just split on first period"""
    description = listing.get('description', '')
    return description.split('.')[0] + '.' if description else ''

def new_logic(listing):
    """New fixed logic"""
    description = listing.get('description', '')
    genetics = listing.get('genetics', '')
    
    def get_sentences(text, count=2, max_chars=200):
        if not text:
            return ''
        sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
        result_sentences = []
        total_len = 0
        for i, sent in enumerate(sentences[:count]):
            sent_len = len(sent)
            if i == 0 and sent_len > max_chars:
                return sent[:max_chars-3] + '...'
            if result_sentences and total_len + sent_len + 1 > max_chars:
                break
            result_sentences.append(sent)
            total_len += sent_len + 1
        return ' '.join(result_sentences).strip()
    
    if description:
        summary = get_sentences(description, 2, 200)
        if len(summary) >= 30:
            return summary
    if genetics:
        summary = get_sentences(genetics, 1, 150)
        if len(summary) >= 20:
            return summary
        if len(genetics) <= 150:
            return genetics
        return genetics[:147] + '...'
    return description or genetics or ''

# Compare old vs new
changed = []
for listing in listings:
    old = old_logic(listing)
    new = new_logic(listing)
    
    if old != new:
        changed.append({
            'name': listing['name'],
            'slug': listing['slug'],
            'old_len': len(old),
            'new_len': len(new),
            'old': old,
            'new': new
        })

print(f"📝 Summary Changes Report")
print(f"=" * 70)
print(f"\n{len(changed)} listings had their summaries fixed:\n")

# Sort by severity (shortest old summaries first)
changed.sort(key=lambda x: x['old_len'])

for item in changed:
    print(f"✏️  {item['name']}")
    print(f"   Old ({item['old_len']} chars): {item['old'][:80]}{'...' if len(item['old']) > 80 else ''}")
    print(f"   New ({item['new_len']} chars): {item['new'][:80]}{'...' if len(item['new']) > 80 else ''}")
    print()

print(f"\n{'='*70}")
print(f"Total: {len(changed)} summaries improved")
print(f"Unchanged: {len(listings) - len(changed)} summaries were already good")
