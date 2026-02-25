#!/usr/bin/env python3
"""
Update Port Sulphur report pages to match oceandatum.ai navbar
"""

from pathlib import Path

BASE_DIR = Path(__file__).parent

# Files to update
REPORT_FILE = BASE_DIR / "port-sulphur-report.html"
MIDSTREAM_FILE = BASE_DIR.parent / "port-sulphur-midstream.html"

# New navbar HTML that matches oceandatum.ai
NAVBAR_HTML = """    <!-- Navbar -->
    <nav class="navbar">
        <div class="navbar-brand">
            <a href="../../index.html">oceandatum.ai</a>
        </div>
        <div class="navbar-right">
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
                    <a href="../port-sulphur-midstream.html">Port Sulphur Midstream</a>
                </div>
            </div>
        </div>
        <button class="hamburger-button" onclick="toggleMobileMenu()">☰</button>
    </nav>

    <!-- Mobile Menu -->
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
            <div class="mobile-menu-item">
                <a href="../port-sulphur-midstream.html">Port Sulphur Midstream</a>
            </div>
        </div>
    </div>"""

# Navbar for midstream page (different paths)
NAVBAR_HTML_MIDSTREAM = """    <!-- Navbar -->
    <nav class="navbar">
        <div class="navbar-brand">
            <a href="../index.html">oceandatum.ai</a>
        </div>
        <div class="navbar-right">
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
                    <a href="port-sulphur-report/port-sulphur-report.html">Port Sulphur Terminal</a>
                    <a href="port-sulphur-midstream.html">Port Sulphur Midstream</a>
                </div>
            </div>
        </div>
        <button class="hamburger-button" onclick="toggleMobileMenu()">☰</button>
    </nav>

    <!-- Mobile Menu -->
    <div class="mobile-menu" id="mobileMenu">
        <div class="mobile-menu-section">
            <div class="mobile-menu-item">
                <a href="../cv.html">CV/Bio</a>
            </div>
            <div class="mobile-menu-item">
                <a href="tampa-cement.html">Tampa Cement Terminal</a>
            </div>
            <div class="mobile-menu-item">
                <a href="port-sulphur-report/port-sulphur-report.html">Port Sulphur Terminal</a>
            </div>
            <div class="mobile-menu-item">
                <a href="port-sulphur-midstream.html">Port Sulphur Midstream</a>
            </div>
        </div>
    </div>"""

# Updated navbar CSS to match oceandatum.ai
NAVBAR_CSS = """        /* Navigation */
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: rgba(0,0,0,0.4);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border-bottom: 1px solid rgba(255,255,255,0.15);
            padding: 0.8rem 2rem;
            z-index: 1000;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .navbar-brand {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.85rem;
            font-weight: 300;
            font-style: italic;
            color: rgba(255,255,255,0.7);
            text-decoration: none;
            letter-spacing: 0.03em;
        }

        .navbar-brand a {
            color: rgba(255,255,255,0.9);
            font-weight: 600;
            font-style: normal;
            text-decoration: none;
            transition: all 0.3s ease;
        }

        .navbar-brand a:hover {
            color: #64ffb4;
        }

        .navbar-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .navbar-link {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 0.9rem;
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            letter-spacing: 0.05em;
            cursor: pointer;
            transition: all 0.3s ease;
            padding: 0.5rem 1rem;
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 6px;
        }

        .navbar-link:hover {
            color: #64ffb4;
            border-color: rgba(100,255,180,0.4);
            background: rgba(100,255,180,0.05);
        }

        .dropdown {
            position: relative;
            display: inline-block;
        }

        .dropdown > .navbar-link {
            cursor: pointer;
            user-select: none;
        }

        .dropdown > .navbar-link::after {
            content: " ▼";
            font-size: 0.7em;
            opacity: 0.6;
            margin-left: 0.3rem;
        }

        .dropdown-content {
            display: none;
            position: absolute;
            top: 100%;
            right: 0;
            background: rgba(0,0,0,0.9);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 6px;
            min-width: 200px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.5);
            z-index: 1001;
            margin-top: 0.5rem;
        }

        .dropdown:hover .dropdown-content,
        .dropdown.active .dropdown-content {
            display: block !important;
        }

        .dropdown-content a {
            color: rgba(255,255,255,0.8);
            padding: 0.75rem 1rem;
            text-decoration: none;
            display: block;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }

        .dropdown-content a:hover {
            background: rgba(100,255,180,0.1);
            color: #64ffb4;
        }

        /* Hamburger Menu */
        .hamburger-button {
            display: none;
            background: none;
            border: 2px solid rgba(255,255,255,0.3);
            color: white;
            font-size: 1.5rem;
            width: 40px;
            height: 40px;
            cursor: pointer;
            border-radius: 6px;
            transition: all 0.3s ease;
            flex-shrink: 0;
        }

        .hamburger-button:hover {
            border-color: #64ffb4;
            color: #64ffb4;
            background: rgba(100,255,180,0.05);
        }

        .mobile-menu {
            display: none;
            position: fixed;
            top: 60px;
            left: 0;
            right: 0;
            background: rgba(0,0,0,0.98);
            border-top: 1px solid rgba(100,255,180,0.3);
            border-bottom: 1px solid rgba(100,255,180,0.3);
            z-index: 1000;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }

        .mobile-menu.active {
            display: block;
            max-height: 500px;
        }

        .mobile-menu-section {
            padding: 10px 0;
        }

        .mobile-menu-item {
            display: block;
        }

        .mobile-menu-item a {
            display: block;
            padding: 15px 20px;
            color: rgba(255,255,255,0.9);
            text-decoration: none;
            transition: all 0.3s ease;
            border-left: 3px solid transparent;
        }

        .mobile-menu-item a:hover {
            background: rgba(100,255,180,0.1);
            border-left-color: #64ffb4;
            color: #64ffb4;
        }

        @media (max-width: 768px) {
            .navbar-right {
                display: none;
            }

            .hamburger-button {
                display: flex;
                align-items: center;
                justify-content: center;
            }
        }"""

# Mobile menu JavaScript
MOBILE_MENU_JS = """
    <!-- Mobile Menu Script -->
    <script>
        function toggleMobileMenu() {
            const menu = document.getElementById('mobileMenu');
            if (menu) {
                menu.classList.toggle('active');
            }
        }

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            const menu = document.getElementById('mobileMenu');
            const hamburger = document.querySelector('.hamburger-button');

            if (menu && menu.classList.contains('active') &&
                !menu.contains(event.target) &&
                !hamburger.contains(event.target)) {
                menu.classList.remove('active');
            }
        });
    </script>"""

def update_file(filepath, navbar_html):
    """Update navbar in a file"""
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and replace old navbar CSS
    old_navbar_css_start = content.find("/* Navigation */")
    if old_navbar_css_start == -1:
        old_navbar_css_start = content.find(".navbar {")

    old_navbar_css_end = content.find("/* Content */", old_navbar_css_start)

    if old_navbar_css_start != -1 and old_navbar_css_end != -1:
        # Replace CSS
        content = content[:old_navbar_css_start] + NAVBAR_CSS + "\n\n        " + content[old_navbar_css_end:]

    # Find and replace old navbar HTML
    old_navbar_start = content.find("<nav class=\"navbar\">")
    if old_navbar_start != -1:
        # Find the end of the navbar (look for closing nav tag and any following div)
        old_navbar_end = content.find("</nav>", old_navbar_start)
        if old_navbar_end != -1:
            old_navbar_end = content.find(">", old_navbar_end) + 1
            # Check if there's a following content div to preserve spacing
            next_tag_start = content.find("<", old_navbar_end)
            content = content[:old_navbar_start] + navbar_html + "\n\n" + content[next_tag_start:]

    # Add mobile menu script before </body> if not present
    if "toggleMobileMenu" not in content:
        body_close = content.rfind("</body>")
        if body_close != -1:
            content = content[:body_close] + MOBILE_MENU_JS + "\n" + content[body_close:]

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Updated: {filepath}")
    return True

def main():
    print("Updating Port Sulphur pages navbar...")

    # Update report file
    if REPORT_FILE.exists():
        update_file(REPORT_FILE, NAVBAR_HTML)

    # Update midstream file
    if MIDSTREAM_FILE.exists():
        update_file(MIDSTREAM_FILE, NAVBAR_HTML_MIDSTREAM)

    print("\nNavbar updates complete!")
    print("Both pages now match oceandatum.ai navbar style with dropdowns")

if __name__ == "__main__":
    main()
