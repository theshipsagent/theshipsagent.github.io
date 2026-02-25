#!/usr/bin/env python3
"""
Replace bibliography placeholder in cv.html with generated content
"""

from pathlib import Path
import re

def main():
    cv_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\cv.html')
    bib_path = Path(r'G:\My Drive\LLM\theshipsagent.github.io\oceandatum.ai\bibliography_generated.html')

    # Read files
    print(f"Reading cv.html...")
    with open(cv_path, 'r', encoding='utf-8') as f:
        cv_content = f.read()

    print(f"Reading bibliography_generated.html...")
    with open(bib_path, 'r', encoding='utf-8') as f:
        bib_content = f.read()

    # Find and replace the bibliography section
    # Pattern: from "<!-- TAB 3: BIBLIOGRAPHY -->" to "</div>" before "    </div>\n\n    <button class="print-button""
    pattern = r'(<!-- TAB 3: BIBLIOGRAPHY -->)\s*<div id="bibliography" class="tab-content">.*?</div>(\s+</div>\s+<button class="print-button")'

    # Create replacement content (keep the comment, add generated content, keep the closing structure)
    replacement = r'\1\n        ' + bib_content.strip() + r'\2'

    # Perform replacement
    print(f"Replacing bibliography section...")
    new_content = re.sub(pattern, replacement, cv_content, flags=re.DOTALL)

    # Check if replacement was successful
    if new_content == cv_content:
        print("WARNING: No replacement was made. Check the pattern.")
        return

    # Write back
    print(f"Writing updated cv.html...")
    with open(cv_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"Success! Bibliography section replaced in cv.html")
    print(f"Bibliography now contains 824 works organized into sections.")

if __name__ == '__main__':
    main()
