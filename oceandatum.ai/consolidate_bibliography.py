#!/usr/bin/env python3
"""
Consolidate bibliography into 8 major categories with smart categorization logic
"""

import csv
import re
from collections import defaultdict
from pathlib import Path

# New consolidated category mapping
CATEGORY_MAP = {
    'bib-chartering': 'I. CHARTERING',
    'bib-maritime-law': 'II. MARITIME LAW',
    'bib-port-operations': 'III. PORT OPERATIONS',
    'bib-cargo-operations': 'IV. CARGO OPERATIONS',
    'bib-supply-chain': 'V. SUPPLY CHAIN',
    'bib-trade-documentation': 'VI. TRADE DOCUMENTATION',
    'bib-claims-insurance': 'VII. CLAIMS & INSURANCE',
    'bib-historical': 'VIII. HISTORICAL',
}

def extract_year(year_field):
    """Extract year from date field"""
    if not year_field:
        return ''
    match = re.search(r'\d{4}', year_field)
    return match.group(0) if match else ''

def extract_author_last_name(author_field):
    """Extract last name for sorting"""
    if not author_field:
        return 'ZZZ'
    first_author = author_field.split(';')[0].strip()
    if ',' in first_author:
        return first_author.split(',')[0].strip()
    parts = first_author.split()
    return parts[-1] if parts else 'ZZZ'

def clean_title(title):
    """Clean up title formatting"""
    title = re.sub(r'\s*\[.*?PDF.*?\].*$', '', title)
    title = re.sub(r'\s*›\s*Marine Tracker.*$', '', title)
    title = re.sub(r'\s*-\s*[A-Z][a-z]+\s+[A-Z][a-z]+.*?\[\d{4},\s*PDF\].*$', '', title)
    title = title.strip()
    return title

def clean_author(author):
    """Clean up author formatting"""
    author = re.sub(r';\s*Internet Archive', '', author)
    author = author.strip()
    return author

def smart_categorize(title, author, publisher, collection):
    """
    Use intelligent logic to categorize entries into consolidated categories
    """
    title_lower = title.lower()
    collection_lower = collection.lower() if collection else ''
    publisher_lower = publisher.lower() if publisher else ''

    categories = []

    # CHARTERING - charter parties, fixtures, time charter, voyage charter
    chartering_keywords = [
        'charter', 'laytime', 'demurrage', 'fixture', 'freight', 'voyage charter',
        'time charter', 'bareboat', 'trip charter', 'charter party', 'gencon',
        'nype', 'baltime', 'shelltime', 'chartering', 'dry cargo', 'tanker charter'
    ]
    if any(kw in title_lower for kw in chartering_keywords) or 'chartering' in collection_lower:
        categories.append('I. CHARTERING')

    # MARITIME LAW - legal, regulation, conventions, admiralty
    law_keywords = [
        'law', 'legal', 'regulation', 'convention', 'admiralty', 'maritime law',
        'liability', 'jurisdiction', 'arrest', 'lien', 'salvage', 'collision',
        'hague', 'hamburg', 'rotterdam', 'york-antwerp', 'marpol', 'solas',
        'isps', 'ism code', 'imdg', 'ballast water', 'treaty', 'legislation'
    ]
    if any(kw in title_lower for kw in law_keywords):
        categories.append('II. MARITIME LAW')

    # PORT OPERATIONS - terminals, stevedoring, port management
    port_keywords = [
        'port', 'terminal', 'stevedore', 'berth', 'wharf', 'harbor', 'harbour',
        'quay', 'dock', 'mooring', 'pilotage', 'tugboat', 'tug', 'towboat',
        'channel', 'dredging', 'port management', 'container terminal',
        'bulk terminal', 'shiphandling', 'ship handling'
    ]
    if any(kw in title_lower for kw in port_keywords) or 'ports' in collection_lower:
        categories.append('III. PORT OPERATIONS')

    # CARGO OPERATIONS - stowage, handling, stevedoring, specific commodities
    cargo_keywords = [
        'cargo', 'stowage', 'loading', 'discharge', 'stevedoring', 'grain',
        'coal', 'ore', 'steel', 'bulk cargo', 'container', 'breakbulk',
        'heavy lift', 'project cargo', 'dangerous goods', 'hazmat',
        'refrigerated', 'reefer', 'liquid cargo', 'gas carrier', 'lng',
        'petroleum', 'chemical', 'cement', 'fertilizer'
    ]
    if any(kw in title_lower for kw in cargo_keywords) or 'cargo' in collection_lower:
        categories.append('IV. CARGO OPERATIONS')

    # SUPPLY CHAIN - logistics, distribution, warehousing
    supply_chain_keywords = [
        'supply chain', 'logistics', 'distribution', 'warehousing', 'inventory',
        'procurement', 'multimodal', 'intermodal', 'rail', 'truck', 'barge',
        'transportation', 'freight forwarding', '3pl', '4pl', 'distribution center'
    ]
    if any(kw in title_lower for kw in supply_chain_keywords) or 'supplychain' in collection_lower or 'logistics' in collection_lower:
        categories.append('V. SUPPLY CHAIN')

    # TRADE DOCUMENTATION - bills of lading, letters of credit, export/import
    trade_doc_keywords = [
        'bill of lading', 'b/l', 'letter of credit', 'l/c', 'documentary credit',
        'incoterms', 'export', 'import', 'customs', 'trade documentation',
        'shipping documents', 'certificate of origin', 'commercial invoice',
        'packing list', 'trade finance', 'ucp 600', 'isbp'
    ]
    if any(kw in title_lower for kw in trade_doc_keywords) or 'customs' in collection_lower:
        categories.append('VI. TRADE DOCUMENTATION')

    # CLAIMS & INSURANCE - P&I, hull, cargo claims, average
    claims_keywords = [
        'insurance', 'claim', 'p&i', 'protection and indemnity', 'hull insurance',
        'cargo insurance', 'average', 'general average', 'particular average',
        'york-antwerp', 'marine insurance', 'underwriting', 'lloyd',
        'institute cargo clauses', 'total loss', 'constructive total loss'
    ]
    if any(kw in title_lower for kw in claims_keywords):
        categories.append('VII. CLAIMS & INSURANCE')

    # HISTORICAL - history, historical accounts
    historical_keywords = [
        'history', 'historical', 'evolution', 'development of', 'origins',
        'transcontinental', 'maritime history', 'shipping history'
    ]
    if any(kw in title_lower for kw in historical_keywords) or 'history' in collection_lower:
        categories.append('VIII. HISTORICAL')

    # If no categories found, try to make best guess from collection field
    if not categories:
        if 'shipping' in collection_lower:
            categories.append('IV. CARGO OPERATIONS')
        elif 'transport' in collection_lower or 'econometrics' in collection_lower:
            categories.append('V. SUPPLY CHAIN')
        elif 'missriver' in collection_lower:
            categories.append('III. PORT OPERATIONS')
        else:
            # Default to most relevant based on publisher/content
            if 'maritime' in publisher_lower or 'nautical' in publisher_lower:
                categories.append('IV. CARGO OPERATIONS')
            else:
                categories.append('V. SUPPLY CHAIN')

    return categories

def format_entry(entry):
    """Format a bibliography entry as HTML"""
    title = clean_title(entry.get('Title', 'Untitled').strip())
    author = clean_author(entry.get('Author', '').strip())
    year = extract_year(entry.get('Year', ''))
    publisher = entry.get('Publisher', '').strip()
    edition = entry.get('Edition', '').strip()

    meta_parts = []
    if author:
        meta_parts.append(author)
    if year:
        meta_parts.append(f"({year})")
    if publisher:
        meta_parts.append(publisher)
    if edition:
        meta_parts.append(edition)

    meta = ' '.join(meta_parts) if meta_parts else 'No metadata'

    return f'''      <div class="bib-entry">
        <div class="bib-title">{title}</div>
        <div class="bib-meta">{meta}</div>
      </div>'''

def main():
    user_csv_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\bibliography_summary_user_edit.csv')
    original_csv_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\03_resume\zotero_bibliography.csv')
    output_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\bibliography_consolidated.html')

    print(f"Reading user-edited selection...")
    rows_to_keep = set()
    with open(user_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_num = int(row['Row'])
            rows_to_keep.add(row_num)

    print(f"Selected {len(rows_to_keep)} entries")

    # Read original CSV and categorize
    print(f"Reading and categorizing entries...")
    entries_by_category = defaultdict(list)

    with open(original_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader, 1):
            if idx in rows_to_keep:
                title = row.get('Title', '')
                author = row.get('Author', '')
                publisher = row.get('Publisher', '')
                collection = row.get('Collection', '')

                categories = smart_categorize(title, author, publisher, collection)

                entry_data = {
                    'Title': title,
                    'Author': author,
                    'Year': row.get('Year', ''),
                    'Publisher': publisher,
                    'Edition': row.get('Edition', ''),
                    'sort_key': (extract_author_last_name(author), extract_year(row.get('Year', '')))
                }

                for category in categories:
                    entries_by_category[category].append(entry_data)

    # Sort entries within each category
    for category in entries_by_category:
        entries_by_category[category].sort(key=lambda x: x['sort_key'])

    # Generate HTML sections
    sections_html = []
    toc_data = []
    total_entries = 0

    for section_id, section_title in CATEGORY_MAP.items():
        if section_title in entries_by_category:
            entries = entries_by_category[section_title]
            count = len(entries)
            total_entries += count

            entries_html = '\n'.join(format_entry(entry) for entry in entries)
            section_html = f'''  <div id="{section_id}" class="bib-section">
    <div class="bib-section-header" onclick="toggleSection(this)">
      <h3>{section_title} <span class="entry-count">({count} works)</span></h3>
      <span class="expand-icon">▼</span>
    </div>
    <div class="bib-section-content">
{entries_html}
    </div>
  </div>'''
            sections_html.append(section_html)
            toc_data.append((section_id, section_title, count))
            print(f"  {section_title}: {count} entries")

    # Generate TOC
    toc_items = [f'      <li><a href="#{sid}">{title} ({count})</a></li>'
                 for sid, title, count in toc_data]
    toc_html = '''  <nav class="bib-toc">
    <h2>Contents</h2>
    <ul>
''' + '\n'.join(toc_items) + '''
    </ul>
  </nav>'''

    # Build complete HTML with updated intro text
    html = f'''<div id="bibliography" class="tab-content">
  <div class="content-header">
    <img src="images/wsd_logo.png" alt="W.S.D. Logo" class="cv-logo">
    <h1>WILLIAM S. DAVIS III</h1>
    <div class="subtitle">Professional Bibliography</div>
  </div>

  <p>Throughout my career, continuous learning has been central to professional development. Over 30 years, I've built a comprehensive professional library of hundreds of curated works spanning chartering, maritime law, port operations, cargo handling, supply chain management, and international trade.</p>

  <p>This collection represents systematic study across the full spectrum of maritime commerce, from foundational legal texts to operational best practices. The bibliography demonstrates both breadth of knowledge and depth of focus in key commercial and operational areas.</p>

  <!-- Controls -->
  <div class="bib-controls">
    <button onclick="expandAllSections()">Expand All</button>
    <button onclick="collapseAllSections()">Collapse All</button>
  </div>

{toc_html}

{chr(10).join(sections_html)}

  <p style="margin-top: 2rem; font-style: italic; color: rgba(255,255,255,0.7);">
    This bibliography demonstrates commitment to continuous professional development and deep domain expertise across maritime commerce, operations, and business management.
  </p>
</div>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\nGenerated consolidated HTML: {output_path}")
    print(f"Total entries: {total_entries} (from {len(rows_to_keep)} unique works)")
    print(f"\nConsolidated into 8 categories:")
    for _, title in CATEGORY_MAP.items():
        if title in entries_by_category:
            print(f"  ✓ {title}")

if __name__ == '__main__':
    main()
