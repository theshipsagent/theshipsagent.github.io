#!/usr/bin/env python3
"""
Create CSV with assigned categories for user review
"""

import csv
import re
from pathlib import Path

def extract_year(year_field):
    if not year_field:
        return ''
    match = re.search(r'\d{4}', year_field)
    return match.group(0) if match else ''

def clean_title(title):
    title = re.sub(r'\s*\[.*?PDF.*?\].*$', '', title)
    title = re.sub(r'\s*›\s*Marine Tracker.*$', '', title)
    title = re.sub(r'\s*-\s*[A-Z][a-z]+\s+[A-Z][a-z]+.*?\[\d{4},\s*PDF\].*$', '', title)
    return title.strip()

def clean_author(author):
    author = re.sub(r';\s*Internet Archive', '', author)
    return author.strip()

def smart_categorize(title, author, publisher, collection):
    title_lower = title.lower()
    collection_lower = collection.lower() if collection else ''

    # CHARTERING
    chartering_keywords = [
        'charter', 'laytime', 'demurrage', 'fixture', 'freight', 'voyage charter',
        'time charter', 'bareboat', 'charter party', 'gencon', 'nype', 'baltime'
    ]
    if any(kw in title_lower for kw in chartering_keywords) or 'chartering' in collection_lower:
        return 'I. CHARTERING'

    # MARITIME LAW
    law_keywords = [
        'law', 'legal', 'regulation', 'convention', 'admiralty', 'maritime law',
        'liability', 'jurisdiction', 'arrest', 'lien', 'salvage', 'collision',
        'hague', 'hamburg', 'rotterdam', 'marpol', 'solas', 'isps', 'ism code'
    ]
    if any(kw in title_lower for kw in law_keywords):
        return 'II. MARITIME LAW'

    # PORT OPERATIONS
    port_keywords = [
        'port', 'terminal', 'stevedore', 'berth', 'wharf', 'harbor', 'harbour',
        'tugboat', 'tug', 'towboat', 'channel', 'dredging', 'shiphandling'
    ]
    if any(kw in title_lower for kw in port_keywords) or 'ports' in collection_lower:
        return 'III. PORT OPERATIONS'

    # CARGO OPERATIONS
    cargo_keywords = [
        'cargo', 'stowage', 'loading', 'discharge', 'grain', 'coal', 'ore',
        'steel', 'bulk cargo', 'container', 'breakbulk', 'heavy lift',
        'dangerous goods', 'hazmat', 'lng', 'petroleum', 'chemical', 'cement'
    ]
    if any(kw in title_lower for kw in cargo_keywords) or 'cargo' in collection_lower:
        return 'IV. CARGO OPERATIONS'

    # SUPPLY CHAIN
    supply_chain_keywords = [
        'supply chain', 'logistics', 'distribution', 'warehousing', 'inventory',
        'multimodal', 'intermodal', 'rail', 'truck', 'barge', 'transportation'
    ]
    if any(kw in title_lower for kw in supply_chain_keywords) or 'supplychain' in collection_lower or 'logistics' in collection_lower:
        return 'V. SUPPLY CHAIN'

    # TRADE DOCUMENTATION
    trade_doc_keywords = [
        'bill of lading', 'letter of credit', 'incoterms', 'export', 'import',
        'customs', 'trade documentation', 'shipping documents'
    ]
    if any(kw in title_lower for kw in trade_doc_keywords) or 'customs' in collection_lower:
        return 'VI. TRADE DOCUMENTATION'

    # CLAIMS & INSURANCE
    claims_keywords = [
        'insurance', 'claim', 'p&i', 'protection and indemnity', 'hull insurance',
        'cargo insurance', 'average', 'general average', 'marine insurance'
    ]
    if any(kw in title_lower for kw in claims_keywords):
        return 'VII. CLAIMS & INSURANCE'

    # HISTORICAL
    historical_keywords = [
        'history', 'historical', 'evolution', 'development of', 'origins'
    ]
    if any(kw in title_lower for kw in historical_keywords) or 'history' in collection_lower:
        return 'VIII. HISTORICAL'

    # Default
    if 'shipping' in collection_lower:
        return 'IV. CARGO OPERATIONS'
    elif 'transport' in collection_lower or 'econometrics' in collection_lower:
        return 'V. SUPPLY CHAIN'
    elif 'missriver' in collection_lower:
        return 'III. PORT OPERATIONS'
    else:
        return 'V. SUPPLY CHAIN'

def main():
    user_csv_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\bibliography_summary_user_edit.csv')
    original_csv_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\03_resume\zotero_bibliography.csv')
    output_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\bibliography_with_categories.csv')

    # Get rows to keep
    rows_to_keep = set()
    with open(user_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows_to_keep.add(int(row['Row']))

    # Read original and assign categories
    entries = []
    with open(original_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, 1):
            if idx in rows_to_keep:
                title = clean_title(row.get('Title', ''))
                author = clean_author(row.get('Author', ''))
                year = extract_year(row.get('Year', ''))
                publisher = row.get('Publisher', '').strip()[:40]
                collection = row.get('Collection', '').strip()

                category = smart_categorize(title, author, publisher, collection)

                entries.append({
                    'Row': idx,
                    'Title': title[:80],
                    'Author': author[:40],
                    'Year': year,
                    'Publisher': publisher,
                    'Collection': collection,
                    'Category': category
                })

    # Write output
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Row', 'Title', 'Author', 'Year', 'Publisher', 'Collection', 'Category'])
        writer.writeheader()
        writer.writerows(entries)

    print(f"Created CSV with categories: {output_path}")
    print(f"Total entries: {len(entries)}")
    print(f"\nCategory breakdown:")
    from collections import Counter
    cat_counts = Counter(e['Category'] for e in entries)
    for cat, count in sorted(cat_counts.items()):
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    main()
