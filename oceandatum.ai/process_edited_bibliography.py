#!/usr/bin/env python3
"""
Process user-edited bibliography CSV and cross-reference with original Zotero data
to get complete, correctly formatted entries
"""

import csv
import re
from collections import defaultdict
from pathlib import Path

# Category mapping based on Collection taxonomy
CATEGORY_MAPPING = {
    'KeyTexts': 'I. FOUNDATIONAL REFERENCES',
    'Shipping': 'II. MARITIME SHIPPING & OPERATIONS',
    'Shipping > Chartering': 'II-B. Chartering & Charter Parties',
    'Shipping > Operations': 'II-A. General Shipping Operations',
    'Cargo': 'III. CARGO & COMMODITY HANDLING',
    'Cargo > SteelMetals': 'III-A. Steel & Metals',
    'Cargo > OilGas': 'III-B. Oil & Gas',
    'Cargo > Grain': 'III-C. Grain & Agricultural',
    'Cargo > Cement': 'III-D. Cement & Bulk Materials',
    'Logistics': 'IV. LOGISTICS & SUPPLY CHAIN',
    'Logistics > SupplyChain': 'IV-A. Supply Chain Management',
    'Logistics > Ports': 'IV-B. Port Operations',
    'Logistics > Rail': 'IV-C. Rail Transport',
    'Logistics > Barge': 'IV-D. Barge & Inland Waterways',
    'Transport Econometrics': 'V. TRANSPORT ECONOMICS & ANALYTICS',
    'MissRiver': 'VI. REGIONAL SPECIALIZATION: MISSISSIPPI RIVER',
    'History': 'VII. MARITIME HISTORY',
    'Customs': 'VIII. CUSTOMS & REGULATORY',
}

def extract_year(year_field):
    """Extract year from date field like '1982-00-00 1982' or '2015-00-00 2015'"""
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
    # Remove file extensions and unwanted suffixes
    title = re.sub(r'\s*\[.*?PDF.*?\].*$', '', title)
    title = re.sub(r'\s*›\s*Marine Tracker.*$', '', title)
    title = re.sub(r'\s*-\s*[A-Z][a-z]+\s+[A-Z][a-z]+.*?\[\d{4},\s*PDF\].*$', '', title)
    title = title.strip()
    return title

def clean_author(author):
    """Clean up author formatting"""
    # Remove 'Internet Archive' and similar artifacts
    author = re.sub(r';\s*Internet Archive', '', author)
    author = author.strip()
    return author

def categorize_entry(collection_field):
    """Categorize entry based on Collection tags"""
    if not collection_field:
        return ['IX. GENERAL REFERENCE']

    collections = [c.strip() for c in collection_field.split(';')]
    categories = set()

    for collection in collections:
        if collection in CATEGORY_MAPPING:
            categories.add(CATEGORY_MAPPING[collection])
        elif ' > ' in collection:
            if collection in CATEGORY_MAPPING:
                categories.add(CATEGORY_MAPPING[collection])
            else:
                parent = collection.split(' > ')[0]
                if parent in CATEGORY_MAPPING:
                    categories.add(CATEGORY_MAPPING[parent])
        elif 'Shipping' in collection:
            categories.add('II. MARITIME SHIPPING & OPERATIONS')
        elif 'Cargo' in collection:
            categories.add('III. CARGO & COMMODITY HANDLING')
        elif 'Logistics' in collection:
            categories.add('IV. LOGISTICS & SUPPLY CHAIN')
        elif 'Transport' in collection or 'Econometrics' in collection:
            categories.add('V. TRANSPORT ECONOMICS & ANALYTICS')
        elif 'History' in collection:
            categories.add('VII. MARITIME HISTORY')
        elif 'Customs' in collection or 'Regulatory' in collection:
            categories.add('VIII. CUSTOMS & REGULATORY')

    return list(categories) if categories else ['IX. GENERAL REFERENCE']

def format_entry(entry):
    """Format a bibliography entry as HTML"""
    title = clean_title(entry.get('Title', 'Untitled').strip())
    author = clean_author(entry.get('Author', '').strip())
    year = extract_year(entry.get('Year', ''))
    publisher = entry.get('Publisher', '').strip()
    edition = entry.get('Edition', '').strip()

    # Build metadata string
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
    # Read user-edited CSV to get row numbers to keep
    user_csv_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\bibliography_summary_user_edit.csv')
    original_csv_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\03_resume\zotero_bibliography.csv')
    output_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\bibliography_generated_clean.html')

    print(f"Reading user-edited selection from: {user_csv_path}")
    rows_to_keep = set()
    with open(user_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_num = int(row['Row'])
            rows_to_keep.add(row_num)

    print(f"User selected {len(rows_to_keep)} entries to keep")

    # Read original CSV and keep only selected rows
    print(f"Reading original Zotero CSV: {original_csv_path}")
    entries_by_category = defaultdict(list)

    with open(original_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader, 1):
            if idx in rows_to_keep:
                categories = categorize_entry(row.get('Collection', ''))

                for category in categories:
                    entries_by_category[category].append({
                        'Title': row.get('Title', ''),
                        'Author': row.get('Author', ''),
                        'Year': row.get('Year', ''),
                        'Publisher': row.get('Publisher', ''),
                        'Edition': row.get('Edition', ''),
                        'sort_key': (extract_author_last_name(row.get('Author', '')),
                                    extract_year(row.get('Year', '')))
                    })

    # Sort entries within each category
    for category in entries_by_category:
        entries_by_category[category].sort(key=lambda x: x['sort_key'])

    # Generate sections
    section_order = [
        ('bib-keytexts', 'I. FOUNDATIONAL REFERENCES'),
        ('bib-shipping', 'II. MARITIME SHIPPING & OPERATIONS'),
        ('bib-shipping-chartering', 'II-B. Chartering & Charter Parties'),
        ('bib-cargo', 'III. CARGO & COMMODITY HANDLING'),
        ('bib-cargo-steel', 'III-A. Steel & Metals'),
        ('bib-cargo-oilgas', 'III-B. Oil & Gas'),
        ('bib-cargo-grain', 'III-C. Grain & Agricultural'),
        ('bib-cargo-cement', 'III-D. Cement & Bulk Materials'),
        ('bib-logistics', 'IV. LOGISTICS & SUPPLY CHAIN'),
        ('bib-logistics-supplychain', 'IV-A. Supply Chain Management'),
        ('bib-logistics-ports', 'IV-B. Port Operations'),
        ('bib-logistics-rail', 'IV-C. Rail Transport'),
        ('bib-logistics-barge', 'IV-D. Barge & Inland Waterways'),
        ('bib-econometrics', 'V. TRANSPORT ECONOMICS & ANALYTICS'),
        ('bib-missriver', 'VI. REGIONAL SPECIALIZATION: MISSISSIPPI RIVER'),
        ('bib-history', 'VII. MARITIME HISTORY'),
        ('bib-customs', 'VIII. CUSTOMS & REGULATORY'),
        ('bib-general', 'IX. GENERAL REFERENCE'),
    ]

    sections_html = []
    toc_data = []
    total_entries = 0

    for section_id, section_title in section_order:
        if section_title in entries_by_category:
            entries = entries_by_category[section_title]
            count = len(entries)
            total_entries += count

            # Generate section HTML
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

    # Build complete HTML
    html = f'''<div id="bibliography" class="tab-content">
  <div class="content-header">
    <img src="images/wsd_logo.png" alt="W.S.D. Logo" class="cv-logo">
    <h1>WILLIAM S. DAVIS III</h1>
    <div class="subtitle">Professional Bibliography</div>
  </div>

  <p>Throughout my career, continuous learning has been central to professional development. Over 30 years, I've built a comprehensive professional library of {total_entries} curated works spanning ship agency, chartering, maritime law, port operations, supply chain management, and commodity markets.</p>

  <p>This collection represents systematic study across the full spectrum of maritime commerce, from foundational texts to specialized regional expertise. The bibliography demonstrates both breadth of knowledge and depth of focus in key operational areas.</p>

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

    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\nGenerated clean HTML written to: {output_path}")
    print(f"Total entries processed: {total_entries}")
    print(f"\nCleaning applied:")
    print("  - Removed PDF markers and file extensions from titles")
    print("  - Removed 'Marine Tracker' and similar artifacts")
    print("  - Cleaned author fields (removed 'Internet Archive', etc.)")
    print("  - Used complete, untruncated data from original Zotero export")

if __name__ == '__main__':
    main()
