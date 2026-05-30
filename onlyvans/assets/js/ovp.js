/* ============================================================================
   OnlyVans Panama — shared behavior (ovp.js)
   Plain JavaScript, no libraries. Loaded by every page.
   Handles only the mobile nav; everything else is CSS or static markup.
   ========================================================================== */

(function () {
  'use strict';

  // --- Brand logo (real OnlyVans Panamá wordmark) --------------------------
  // The real white script wordmark, extracted from Claas's brand sheet. Built
  // ONCE here with safe DOM methods and injected into every .navbar-brand (nav +
  // footer) so there's a single source of truth across all pages. The plain text
  // "OnlyVans Panama" in the HTML is the fallback if JS is off.
  document.querySelectorAll('.navbar-brand').forEach(function (b) {
    while (b.firstChild) b.removeChild(b.firstChild);
    var img = document.createElement('img');
    img.className = 'brand-logo';
    img.src = 'assets/img/logo-white.png';
    img.alt = 'OnlyVans Panamá';
    b.appendChild(img);
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

  // --- Splash slideshow: crossfade through several drone clips -------------
  // Two stacked <video> layers (#splashA / #splashB). One is visible; we load
  // the next clip into the hidden layer, fade it in (CSS opacity transition),
  // then swap. Honors prefers-reduced-motion by staying on the first clip.
  var splashRoot = document.getElementById('splash');
  if (splashRoot) {
    var PLAYLIST = [
      'assets/video/splash-river.mp4',
      'assets/video/splash-surf.mp4',
      'assets/video/splash-waterfall.mp4'
    ];
    var layers = [document.getElementById('splashA'), document.getElementById('splashB')];
    var reduceMotion = window.matchMedia &&
      window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (layers[0] && layers[1] && PLAYLIST.length > 1 && !reduceMotion) {
      var clipIdx = 0;     // playlist index currently shown
      var activeLayer = 0; // which of the two layers is visible
      var HOLD_MS = 7000;  // time each clip is shown before crossfading

      setInterval(function () {
        var nextIdx  = (clipIdx + 1) % PLAYLIST.length;
        var incoming = layers[activeLayer ^ 1];
        var outgoing = layers[activeLayer];

        incoming.src = PLAYLIST[nextIdx];
        incoming.load();
        var playPromise = incoming.play();
        if (playPromise && playPromise.catch) playPromise.catch(function () {});

        incoming.classList.add('is-active');   // fade in
        outgoing.classList.remove('is-active'); // fade out

        activeLayer ^= 1;
        clipIdx = nextIdx;
      }, HOLD_MS);
    }
  }

  // --- Splash "Enter" → reveal the content below (index page only) ---------
  // The landing opens as a full-screen drone splash; the Enter button OR the
  // Enter key smooth-scrolls down to the first content section. Guarded so it
  // only fires on the splash page and only while still near the top.
  var splash  = document.getElementById('splash');
  var content = document.getElementById('content');
  function enterSite() { if (content) content.scrollIntoView({ behavior: 'smooth' }); }
  var enterBtn = document.getElementById('enterBtn');
  if (enterBtn) enterBtn.addEventListener('click', enterSite);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && splash && window.scrollY < window.innerHeight * 0.6) {
      enterSite();
    }
  });
})();
