#!/usr/bin/env python3
"""
Create a summary CSV of bibliography entries for review
"""

import csv
from pathlib import Path
import re

def extract_year(year_field):
    """Extract year from date field"""
    if not year_field:
        return ''
    match = re.search(r'\d{4}', year_field)
    return match.group(0) if match else ''

def main():
    csv_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\03_resume\zotero_bibliography.csv')
    output_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\bibliography_summary.csv')

    entries = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, 1):
            entries.append({
                'Row': idx,
                'Title': row.get('Title', '').strip()[:80],  # Truncate long titles
                'Author': row.get('Author', '').strip()[:40],  # Truncate long author lists
                'Year': extract_year(row.get('Year', '')),
                'Publisher': row.get('Publisher', '').strip()[:30],
                'Collection': row.get('Collection', '').strip()
            })

    # Write summary CSV
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Row', 'Title', 'Author', 'Year', 'Publisher', 'Collection'])
        writer.writeheader()
        writer.writerows(entries)

    print(f"Created summary CSV with {len(entries)} entries")
    print(f"Output: {output_path}")

if __name__ == '__main__':
    main()
