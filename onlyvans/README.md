# OnlyVans Panama — sample site (mockup)

Demonstrative sample pages for **OnlyVans Panama S.A.** (Claas), showing what a modern,
custom-built site would look and feel like. This is a **mockup to look at and react to** —
**not** the live site, and not yet wired to any real service.

It follows **Approach 2** from the build guide: a fast, fully custom front end with the "money"
features (payments, bookings, merch) supplied by best-in-class services embedded into the page.
Here those services are shown as clearly-labeled **placeholders** so the look is real without
needing any accounts, keys, or backend.

## How to view

Just open `index.html` in a browser (double-click it). It's plain HTML/CSS/JS — no install, no
build step.

Optionally, serve it locally so links behave exactly like a real site:

```bash
cd ~/dev/onlyvans-panama
python3 -m http.server 8000
# then open http://localhost:8000
```

> **Self-contained:** all photos are bundled locally in `assets/img/`, so the demo works
> offline. (The two webfonts load from Google Fonts when online and fall back to system fonts
> otherwise — cosmetic only.)

## Pages

| Page | What it shows |
|------|---------------|
| `index.html` | Home — hero, brand story, featured trips, Instagram strip, reviews, deposit CTA |
| `tours.html` | The trip list — photo cards with price, duration, and a Book button |
| `book.html` | Availability calendar + deposit checkout (both **mock**) and the service "seam" explained |
| `shop.html` | Print-on-demand merch grid (**mock**) |

## What's real vs. placeholder

| Real in this mockup | Placeholder (wired up later) |
|---|---|
| The full look, layout, fonts, colors, responsiveness | Tour names, descriptions & **pricing** (need Claas's real list) |
| Mobile nav (hamburger at 768px), hover effects | **Photos** — local stock stand-ins for Claas's real Instagram shots |
| Page structure & navigation between pages | **Booking calendar** → FareHarbor / Rezdy / Bokun widget |
| | **Payments / deposit** → Stripe / PayPal / Yappy |
| | **Instagram feed** → live `@onlyvanspanama` embed |
| | **Merch store** → Printful / Printify |

Every placeholder is marked on the page with a dashed **"seam"** box naming the service that
fills it.

## Structure

```
index.html  tours.html  book.html  shop.html
assets/
  css/ovp.css   # shared design system — ALL styling lives here (edit once, every page updates)
  js/ovp.js     # shared behavior — mobile menu + mock-button handler
```

The design is driven by CSS variables at the top of `assets/css/ovp.css` (`--sunset`, `--ocean-teal`,
etc.) and the fonts (Bricolage Grotesque + Outfit). Change the brand there and the whole site
follows. Keeping shared code in one file from day one avoids the duplicate-navbar maintenance trap.

## Next steps (from the build guide)

1. Pull real tour content + pricing and real photos from Instagram (`@onlyvanspanama`).
2. Confirm which payment processor accepts payouts to the Panama S.A. (Stripe vs. PayPal / Yappy).
3. Open a free trial of a tour-booking platform (FareHarbor or Rezdy) and embed the widget.
4. When ready, repoint `onlyvanspanama.com` DNS from One.com to the new host —
   **leave the One.com email untouched.**

---

*Mockup prepared 2026-05-29. Reference build: oceandatum.ai. Full reasoning in the
"OnlyVans Panama — Website Build Guide".*
