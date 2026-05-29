/* ============================================================================
   OnlyVans Panama — shared behavior (ovp.js)
   Plain JavaScript, no libraries. Loaded by every page.
   Handles only the mobile nav; everything else is CSS or static markup.
   ========================================================================== */

(function () {
  'use strict';

  // --- Brand logo (placeholder "close-likeness" mark) ----------------------
  // Camper-van glyph + wordmark. Defined ONCE here and injected into every
  // .navbar-brand (nav + footer) so there's a single source of truth. The text
  // "OnlyVans Panama" stays in the HTML as a fallback if JS is off.
  // Swap this whole SVG for Claas's real logo once we can read it from IG.
  var VAN_SVG = '<svg class="brand-van" viewBox="0 0 104 60" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">' +
    '<path d="M8 46 V22 a6 6 0 0 1 6-6 h44 c4 0 7 1.5 10 4.5 L88 32 a6 6 0 0 1 2 4.3 V46 a3 3 0 0 1-3 3 H11 a3 3 0 0 1-3-3 Z" fill="#fff8f0"/>' +
    '<path d="M14 16 h44 c4 0 7 1.5 10 4.5 l2 1.9 H14 V18 a2 2 0 0 1 0-2 Z" fill="#ff6b35"/>' +
    '<rect x="14" y="22" width="17" height="11" rx="2.5" fill="#00b4a6"/>' +
    '<rect x="35" y="22" width="17" height="11" rx="2.5" fill="#00b4a6"/>' +
    '<path d="M58 22 h4 c3 0 5 1 7 3 l5 5 h-16 a2 2 0 0 1-2-2 V24 a2 2 0 0 1 2-2 Z" fill="#00b4a6"/>' +
    '<rect x="8" y="45" width="82" height="4" rx="2" fill="#ffb347"/>' +
    '<circle cx="30" cy="50" r="9" fill="#15202b"/><circle cx="30" cy="50" r="3.4" fill="#fff8f0"/>' +
    '<circle cx="72" cy="50" r="9" fill="#15202b"/><circle cx="72" cy="50" r="3.4" fill="#fff8f0"/></svg>';
  document.querySelectorAll('.navbar-brand').forEach(function (b) {
    b.insertAdjacentHTML('afterbegin', VAN_SVG);
  });

  // --- Mobile hamburger menu (mirrors oceandatum's proven pattern) ---------
  var btn      = document.getElementById('hamburgerBtn');
  var menu     = document.getElementById('mobileMenu');
  var backdrop = document.getElementById('menuBackdrop');

  function openMenu()  { if (menu)     menu.classList.add('open');
                         if (backdrop) backdrop.classList.add('open'); }
  function closeMenu() { if (menu)     menu.classList.remove('open');
                         if (backdrop) backdrop.classList.remove('open'); }

  if (btn)      btn.addEventListener('click', openMenu);
  if (backdrop) backdrop.addEventListener('click', closeMenu);

  // Close after tapping any menu link (so the destination is visible) and on
  // the explicit close button.
  if (menu) {
    menu.querySelectorAll('a, .close').forEach(function (el) {
      el.addEventListener('click', closeMenu);
    });
  }

  // Esc closes the menu — a small accessibility nicety.
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') closeMenu();
  });

  // --- Hero crossfade: drone video <-> van photo ---------------------------
  // The video loops underneath; we fade the still photo in and out on top so
  // the hero alternates "aerial beach" and "the van" every few seconds.
  var heroStill = document.querySelector('.hero-media .hero-still');
  if (heroStill) {
    var showingStill = false;
    setInterval(function () {
      showingStill = !showingStill;
      heroStill.classList.toggle('show', showingStill);
    }, 6000);
  }

  // --- Mock "Book" / "Add to cart" buttons ---------------------------------
  // These are demo placeholders: in the real site each opens the embedded
  // FareHarbor/Stripe/Printful widget. Here they just explain that.
  document.querySelectorAll('[data-mock]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      alert(el.getAttribute('data-mock'));
    });
  });
})();
