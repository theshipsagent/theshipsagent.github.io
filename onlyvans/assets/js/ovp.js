/* ============================================================================
   OnlyVans Panama — shared behavior (ovp.js)
   Plain JavaScript, no libraries. Loaded by every page.
   Handles only the mobile nav; everything else is CSS or static markup.
   ========================================================================== */

(function () {
  'use strict';

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
