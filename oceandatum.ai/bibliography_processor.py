#!/usr/bin/env python3
"""
Bibliography Processor for oceandatum.ai CV/Bio page
Processes Zotero CSV export and generates HTML for bibliography section
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
    # Match 4-digit year
    match = re.search(r'\d{4}', year_field)
    return match.group(0) if match else ''

def extract_author_last_name(author_field):
    """Extract last name for sorting. Handles 'Last, First' and 'First Last' formats"""
    if not author_field:
        return 'ZZZ'  # Sort entries without authors last

    # Split by semicolon for multiple authors
    first_author = author_field.split(';')[0].strip()

    # If contains comma, it's "Last, First" format
    if ',' in first_author:
        return first_author.split(',')[0].strip()

    # Otherwise, assume last word is last name
    parts = first_author.split()
    return parts[-1] if parts else 'ZZZ'

def categorize_entry(collection_field):
    """Categorize entry based on Collection tags"""
    if not collection_field:
        return ['IX. GENERAL REFERENCE']

    collections = [c.strip() for c in collection_field.split(';')]
    categories = set()

    for collection in collections:
        # Check for exact matches first
        if collection in CATEGORY_MAPPING:
            categories.add(CATEGORY_MAPPING[collection])
        # Check for subcategory matches
        elif ' > ' in collection:
            if collection in CATEGORY_MAPPING:
                categories.add(CATEGORY_MAPPING[collection])
            else:
                # Get parent category
                parent = collection.split(' > ')[0]
                if parent in CATEGORY_MAPPING:
                    categories.add(CATEGORY_MAPPING[parent])
        # Default categorization based on keywords
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
    title = entry.get('Title', 'Untitled').strip()
    author = entry.get('Author', '').strip()
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

def process_csv(csv_path):
    """Process CSV and organize entries by category"""
    entries_by_category = defaultdict(list)

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            categories = categorize_entry(row.get('Collection', ''))

            # Add entry to each category it belongs to
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

    return entries_by_category

def generate_section_html(section_id, section_title, entries):
    """Generate HTML for a bibliography section"""
    entry_count = len(entries)
    entries_html = '\n'.join(format_entry(entry) for entry in entries)

    return f'''  <div id="{section_id}" class="bib-section">
    <div class="bib-section-header" onclick="toggleSection(this)">
      <h3>{section_title} <span class="entry-count">({entry_count} works)</span></h3>
      <span class="expand-icon">▼</span>
    </div>
    <div class="bib-section-content">
{entries_html}
    </div>
  </div>'''

def generate_toc(sections):
    """Generate table of contents"""
    toc_items = []
    for section_id, section_title, count in sections:
        toc_items.append(f'      <li><a href="#{section_id}">{section_title} ({count})</a></li>')

    return '''  <nav class="bib-toc">
    <h2>Contents</h2>
    <ul>
''' + '\n'.join(toc_items) + '''
    </ul>
  </nav>'''

def main():
    csv_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\03_resume\zotero_bibliography.csv')
    output_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\bibliography_generated.html')

    print(f"Processing bibliography from: {csv_path}")
    entries_by_category = process_csv(csv_path)

    # Define section order
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

    # Generate sections
    sections_html = []
    toc_data = []
    total_entries = 0

    for section_id, section_title in section_order:
        if section_title in entries_by_category:
            entries = entries_by_category[section_title]
            count = len(entries)
            total_entries += count
            sections_html.append(generate_section_html(section_id, section_title, entries))
            toc_data.append((section_id, section_title, count))
            print(f"  {section_title}: {count} entries")

    # Generate TOC
    toc_html = generate_toc(toc_data)

    # Build complete HTML
    html = f'''<div id="bibliography" class="tab-content">
  <div class="content-header">
    <img src="images/wsd_logo.png" alt="W.S.D. Logo" class="cv-logo">
    <h1>WILLIAM S. DAVIS III</h1>
    <div class="subtitle">Professional Bibliography</div>
  </div>

  <p>Throughout my career, continuous learning has been central to professional development. Over 30 years, I've built a comprehensive professional library of {total_entries} works spanning ship agency, chartering, maritime law, port operations, supply chain management, and commodity markets.</p>

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

    print(f"\nGenerated HTML written to: {output_path}")
    print(f"Total entries processed: {total_entries}")
    print("\nNext steps:")
    print("1. Review the generated HTML")
    print("2. Add CSS styles to cv.html")
    print("3. Add JavaScript functions to cv.html")
    print("4. Replace placeholder content in cv.html with generated HTML")

if __name__ == '__main__':
    main()
