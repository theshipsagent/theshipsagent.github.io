#!/usr/bin/env python3
"""
Build final bibliography from user-edited categories
"""

import csv
import re
from collections import defaultdict
from pathlib import Path

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
    user_csv_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\bibliography_with_categories_user_edits_0120261150.csv')
    original_csv_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\03_resume\zotero_bibliography.csv')
    output_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\bibliography_final.html')

    print(f"Reading user-edited categories from: {user_csv_path}")

    # Read user CSV to get row numbers and their assigned categories
    row_categories = {}
    with open(user_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_num = int(row['Row'])
            category = row['Category'].strip()
            row_categories[row_num] = category

    print(f"User selected {len(row_categories)} entries")

    # Get unique categories and their counts
    from collections import Counter
    category_counts = Counter(row_categories.values())
    print(f"\nCategories found:")
    for cat, count in sorted(category_counts.items()):
        print(f"  {cat}: {count}")

    # Read original CSV and get full data for selected rows
    print(f"\nReading original Zotero data...")
    entries_by_category = defaultdict(list)

    with open(original_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader, 1):
            if idx in row_categories:
                category = row_categories[idx]

                entry_data = {
                    'Title': row.get('Title', ''),
                    'Author': row.get('Author', ''),
                    'Year': row.get('Year', ''),
                    'Publisher': row.get('Publisher', ''),
                    'Edition': row.get('Edition', ''),
                    'sort_key': (extract_author_last_name(row.get('Author', '')),
                                extract_year(row.get('Year', '')))
                }

                entries_by_category[category].append(entry_data)

    # Sort entries within each category
    for category in entries_by_category:
        entries_by_category[category].sort(key=lambda x: x['sort_key'])

    # Create section order (alphabetically for now, we'll customize after seeing categories)
    sorted_categories = sorted(entries_by_category.keys())

    # Create section IDs from category names
    def make_section_id(category_name):
        return 'bib-' + re.sub(r'[^a-z0-9]+', '-', category_name.lower()).strip('-')

    sections_html = []
    toc_data = []
    total_entries = 0

    for idx, category_title in enumerate(sorted_categories, 1):
        entries = entries_by_category[category_title]
        count = len(entries)
        total_entries += count

        section_id = make_section_id(category_title)

        entries_html = '\n'.join(format_entry(entry) for entry in entries)

        section_html = f'''  <div id="{section_id}" class="bib-section">
    <div class="bib-section-header" onclick="toggleSection(this)">
      <h3>{idx}. {category_title.upper()} <span class="entry-count">({count} works)</span></h3>
      <span class="expand-icon">▼</span>
    </div>
    <div class="bib-section-content">
{entries_html}
    </div>
  </div>'''

        sections_html.append(section_html)
        toc_data.append((section_id, f"{idx}. {category_title.upper()}", count))
        print(f"  {idx}. {category_title}: {count} entries")

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

    print(f"\n✓ Generated final bibliography HTML: {output_path}")
    print(f"✓ Total entries: {total_entries}")
    print(f"✓ Total categories: {len(sorted_categories)}")

if __name__ == '__main__':
    main()
