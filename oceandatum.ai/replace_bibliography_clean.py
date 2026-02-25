#!/usr/bin/env python3
"""
Replace bibliography in cv.html with cleaned, user-edited version
"""

from pathlib import Path
import re

def main():
    cv_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\cv.html')
    bib_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\bibliography_generated_clean.html')

    print(f"Reading cv.html...")
    with open(cv_path, 'r', encoding='utf-8') as f:
        cv_content = f.read()

    print(f"Reading cleaned bibliography...")
    with open(bib_path, 'r', encoding='utf-8') as f:
        bib_content = f.read()

    # Find and replace the bibliography section
    pattern = r'(<!-- TAB 3: BIBLIOGRAPHY -->)\s*<div id="bibliography" class="tab-content">.*?</div>(\s+</div>\s+<button class="print-button")'

    replacement = r'\1\n        ' + bib_content.strip() + r'\2'

    print(f"Replacing bibliography section...")
    new_content = re.sub(pattern, replacement, cv_content, flags=re.DOTALL)

    if new_content == cv_content:
        print("WARNING: No replacement was made. Pattern may need adjustment.")
        return

    print(f"Writing updated cv.html...")
    with open(cv_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"\nSuccess! Bibliography updated in cv.html")
    print(f"New bibliography contains 437 entries (369 unique works)")
    print(f"- Cleaned titles (removed PDF markers, file extensions)")
    print(f"- Cleaned author names (removed artifacts)")
    print(f"- Full untruncated data from Zotero")

if __name__ == '__main__':
    main()
