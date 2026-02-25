#!/usr/bin/env python3
"""
Harmonize Port Sulphur pages navbar to exactly match index.html
"""

from pathlib import Path
import re

BASE_DIR = Path(__file__).parent
ROOT_DIR = BASE_DIR.parent.parent
INDEX_FILE = ROOT_DIR / "index.html"
REPORT_FILE = BASE_DIR / "port-sulphur-report.html"
MIDSTREAM_FILE = BASE_DIR.parent / "port-sulphur-midstream.html"

def extract_navbar_css(index_content):
    """Extract exact navbar CSS from index.html"""
    # Find navbar CSS section
    start = index_content.find(".navbar {")
    if start == -1:
        return None

    # Find end (look for next major section or closing style tag)
    end = index_content.find("@media (max-width: 768px) {", start)
    if end == -1:
        end = index_content.find("</style>", start)

    # Get the full mobile media query too
    mobile_end = index_content.find("}", end)
    if mobile_end != -1:
        # Find the closing brace of media query
        brace_count = 1
        pos = end + len("@media (max-width: 768px) {")
        while brace_count > 0 and pos < len(index_content):
            if index_content[pos] == '{':
                brace_count += 1
            elif index_content[pos] == '}':
                brace_count -= 1
            pos += 1
        end = pos

    return index_content[start:end]

def create_navbar_html_for_report():
    """Create navbar HTML for port-sulphur-report.html"""
    return """    <nav class="navbar">
        <span class="navbar-brand">An <a href="../../index.html">oceandatum.ai</a> company</span>

        <!-- Hamburger button (mobile only) -->
        <button class="hamburger-button" id="hamburgerBtn" aria-label="Menu">
            ☰
        </button>

        <!-- Desktop navigation -->
        <div class="navbar-right">
            <div class="social-icons">
                <a href="https://www.linkedin.com/company/oceandatum-ai" target="_blank" class="social-icon" title="LinkedIn">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                </a>
                <a href="https://twitter.com/oceandatum_ai" target="_blank" class="social-icon" title="Twitter">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                    </svg>
                </a>
                <a href="https://www.instagram.com/oceandatum.ai" target="_blank" class="social-icon" title="Instagram">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                    </svg>
                </a>
            </div>
            <div class="dropdown">
                <a class="navbar-link">About</a>
                <div class="dropdown-content">
                    <a href="../../cv.html">CV/Bio</a>
                </div>
            </div>
            <div class="dropdown">
                <a class="navbar-link">Projects</a>
                <div class="dropdown-content">
                    <a href="../tampa-cement.html">Tampa Cement Terminal</a>
                    <a href="port-sulphur-report.html">Port Sulphur Terminal</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Mobile menu (hidden by default) -->
    <div class="mobile-menu" id="mobileMenu">
        <div class="mobile-menu-section">
            <div class="mobile-menu-item">
                <a href="../../cv.html">CV/Bio</a>
            </div>
            <div class="mobile-menu-item">
                <a href="../tampa-cement.html">Tampa Cement Terminal</a>
            </div>
            <div class="mobile-menu-item">
                <a href="port-sulphur-report.html">Port Sulphur Terminal</a>
            </div>
        </div>
        <div class="mobile-menu-social">
            <a href="https://www.linkedin.com/company/oceandatum-ai" target="_blank" class="social-icon" title="LinkedIn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                </svg>
            </a>
            <a href="https://twitter.com/oceandatum_ai" target="_blank" class="social-icon" title="Twitter">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
            </a>
            <a href="https://www.instagram.com/oceandatum.ai" target="_blank" class="social-icon" title="Instagram">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
            </a>
        </div>
    </div>"""

def create_navbar_html_for_midstream():
    """Create navbar HTML for port-sulphur-midstream.html (independent)"""
    return """    <nav class="navbar">
        <span class="navbar-brand">An <a href="../index.html">oceandatum.ai</a> company</span>

        <!-- Hamburger button (mobile only) -->
        <button class="hamburger-button" id="hamburgerBtn" aria-label="Menu">
            ☰
        </button>

        <!-- Desktop navigation -->
        <div class="navbar-right">
            <div class="social-icons">
                <a href="https://www.linkedin.com/company/oceandatum-ai" target="_blank" class="social-icon" title="LinkedIn">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                </a>
                <a href="https://twitter.com/oceandatum_ai" target="_blank" class="social-icon" title="Twitter">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                    </svg>
                </a>
                <a href="https://www.instagram.com/oceandatum.ai" target="_blank" class="social-icon" title="Instagram">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                    </svg>
                </a>
            </div>
            <div class="dropdown">
                <a class="navbar-link">About</a>
                <div class="dropdown-content">
                    <a href="../cv.html">CV/Bio</a>
                </div>
            </div>
            <div class="dropdown">
                <a class="navbar-link">Projects</a>
                <div class="dropdown-content">
                    <a href="tampa-cement.html">Tampa Cement Terminal</a>
                    <a href="port-sulphur-midstream.html">Port Sulphur Midstream</a>
                </div>
            </div>
        </div>
    </nav>

    <!-- Mobile menu (hidden by default) -->
    <div class="mobile-menu" id="mobileMenu">
        <div class="mobile-menu-section">
            <div class="mobile-menu-item">
                <a href="../cv.html">CV/Bio</a>
            </div>
            <div class="mobile-menu-item">
                <a href="tampa-cement.html">Tampa Cement Terminal</a>
            </div>
            <div class="mobile-menu-item">
                <a href="port-sulphur-midstream.html">Port Sulphur Midstream</a>
            </div>
        </div>
        <div class="mobile-menu-social">
            <a href="https://www.linkedin.com/company/oceandatum-ai" target="_blank" class="social-icon" title="LinkedIn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                </svg>
            </a>
            <a href="https://twitter.com/oceandatum_ai" target="_blank" class="social-icon" title="Twitter">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
                </svg>
            </a>
            <a href="https://www.instagram.com/oceandatum.ai" target="_blank" class="social-icon" title="Instagram">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
                </svg>
            </a>
        </div>
    </div>"""

def get_navbar_js():
    """Get navbar JavaScript"""
    return """
    <script>
        // Mobile menu toggle
        const hamburgerBtn = document.getElementById('hamburgerBtn');
        const mobileMenu = document.getElementById('mobileMenu');

        if (hamburgerBtn && mobileMenu) {
            hamburgerBtn.addEventListener('click', function(e) {
                e.stopPropagation();
                mobileMenu.classList.toggle('active');
            });

            // Close mobile menu when clicking outside
            document.addEventListener('click', function(event) {
                if (mobileMenu.classList.contains('active') &&
                    !mobileMenu.contains(event.target) &&
                    !hamburgerBtn.contains(event.target)) {
                    mobileMenu.classList.remove('active');
                }
            });

            // Close mobile menu when clicking a link
            const menuLinks = mobileMenu.querySelectorAll('a');
            menuLinks.forEach(link => {
                link.addEventListener('click', () => {
                    mobileMenu.classList.remove('active');
                });
            });
        }

        // Dropdown handling for touch devices
        const dropdowns = document.querySelectorAll('.dropdown');
        dropdowns.forEach(dropdown => {
            const link = dropdown.querySelector('.navbar-link');
            if (link) {
                link.addEventListener('click', function(e) {
                    if (window.innerWidth <= 768) {
                        e.preventDefault();
                        dropdown.classList.toggle('active');
                    }
                });
            }
        });
    </script>"""

def update_page(filepath, navbar_html):
    """Update a page with exact navbar from index.html"""
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Read index.html to get exact CSS
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_content = f.read()

    # Extract navbar CSS from index.html
    navbar_css = extract_navbar_css(index_content)
    if not navbar_css:
        print("Could not extract navbar CSS from index.html")
        return False

    # Find and replace CSS
    css_start = content.find(".navbar {")
    if css_start != -1:
        # Find end of navbar CSS (look for next major section)
        css_end = content.find("/* Content */", css_start)
        if css_end == -1:
            css_end = content.find(".content {", css_start)
        if css_end != -1:
            content = content[:css_start] + navbar_css + "\n\n        " + content[css_end:]

    # Find and replace navbar HTML
    nav_start = content.find("<nav class=\"navbar\">")
    if nav_start != -1:
        # Find end of mobile menu div
        mobile_menu_end = content.find("</div>", content.find("mobile-menu", nav_start))
        if mobile_menu_end != -1:
            # Find the actual closing div for mobile-menu
            div_count = 1
            pos = content.find("<div class=\"mobile-menu\"", nav_start)
            pos = content.find(">", pos) + 1
            while div_count > 0 and pos < len(content):
                if content[pos:pos+4] == '<div':
                    div_count += 1
                elif content[pos:pos+6] == '</div>':
                    div_count -= 1
                    if div_count == 0:
                        pos += 6
                        break
                pos += 1
            mobile_menu_end = pos

        # Replace navbar HTML
        content = content[:nav_start] + navbar_html + "\n\n" + content[mobile_menu_end:]

    # Add/update JavaScript
    if "hamburgerBtn" not in content or "Mobile menu toggle" not in content:
        body_close = content.rfind("</body>")
        if body_close != -1:
            # Remove old mobile menu script if exists
            old_script_start = content.rfind("<script>", 0, body_close)
            if old_script_start != -1 and "toggleMobileMenu" in content[old_script_start:body_close]:
                old_script_end = content.find("</script>", old_script_start) + 9
                content = content[:old_script_start] + content[old_script_end:]
                body_close = content.rfind("</body>")

            content = content[:body_close] + get_navbar_js() + "\n" + content[body_close:]

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated: {filepath.name}")
    return True

def main():
    print("Harmonizing Port Sulphur pages with exact index.html navbar...")
    print()

    # Update report page (NO midstream link)
    print("Updating Port Sulphur Terminal Report...")
    update_page(REPORT_FILE, create_navbar_html_for_report())

    # Update midstream page (independent, NO report link)
    print("Updating Port Sulphur Midstream (independent)...")
    update_page(MIDSTREAM_FILE, create_navbar_html_for_midstream())

    print()
    print("Navbar harmonization complete!")
    print("- Both pages now match index.html exactly")
    print("- Port Sulphur report: Does NOT link to midstream")
    print("- Midstream page: Independent, does NOT link to report")
    print("- Same fonts, spacing, and appearance as main site")

if __name__ == "__main__":
    main()
