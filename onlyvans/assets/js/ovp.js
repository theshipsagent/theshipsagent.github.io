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
      'assets/video/splash-van-transit.mp4',
      'assets/video/splash-coast.mp4',
      'assets/video/splash-van-tree.mp4',
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

  // --- Splash "Enter" → navigate INTO the site (index gate only) -----------
  // The landing is a pure entry gate: a full-screen drone splash with no scroll
  // content below it. The Enter button OR the Enter key takes you into the site,
  // landing on the mission page. Guarded by #splash so it only fires on the gate.
  var splash      = document.getElementById('splash');
  var ENTER_TARGET = 'about.html';
  function enterSite() { window.location.href = ENTER_TARGET; }
  var enterBtn = document.getElementById('enterBtn');
  if (enterBtn) enterBtn.addEventListener('click', enterSite);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' && splash) enterSite();
  });

  // --- i18n: trilingual EN / ES / DE toggle --------------------------------
  // Source-string translation: pages are authored in English; we walk text
  // nodes and swap their text via a dictionary keyed by the English source
  // (window.OVP_I18N, defined in assets/js/i18n.js and loaded before this).
  // Strings absent from the dict pass through unchanged — so brand names, van
  // names, emails and model numbers stay safe by default. The toggle UI is
  // INJECTED here (same pattern as the logo) so no page markup changes.
  var I18N  = window.OVP_I18N || {};
  var LANGS = ['en', 'es', 'de'];
  var LSKEY = 'ovp-lang';
  function tableFor(lang) { return (lang === 'en' ? I18N.en : I18N[lang]) || {}; }

  // Cache every translatable text node + its original (English) value, once.
  var i18nNodes = [];
  if (document.body) {
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        if (!n.nodeValue || !n.nodeValue.trim()) return NodeFilter.FILTER_REJECT;
        for (var p = n.parentNode; p && p !== document.body; p = p.parentNode) {
          var tag = p.nodeName.toLowerCase();
          if (tag === 'script' || tag === 'style' || tag === 'svg') return NodeFilter.FILTER_REJECT;
          if (p.classList && p.classList.contains('lang-toggle')) return NodeFilter.FILTER_REJECT;
          if (p.hasAttribute && p.hasAttribute('data-no-i18n')) return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    var tn;
    while ((tn = walker.nextNode())) i18nNodes.push({ node: tn, en: tn.nodeValue });
  }
  // Placeholders + <title> live outside the body-text-node set.
  var i18nPh = [];
  document.querySelectorAll('[placeholder]').forEach(function (el) {
    i18nPh.push({ el: el, en: el.getAttribute('placeholder') });
  });
  var titleEN = document.title;

  function swap(text, lang) {
    var t = tableFor(lang), key = text.trim();
    if (t[key] == null) return text;                 // not translated → leave as-is
    return text.match(/^\s*/)[0] + t[key] + text.match(/\s*$/)[0]; // keep surrounding space
  }

  function applyLang(lang) {
    if (LANGS.indexOf(lang) < 0) lang = 'en';
    i18nNodes.forEach(function (o) { o.node.nodeValue = swap(o.en, lang); });
    i18nPh.forEach(function (o) { o.el.setAttribute('placeholder', swap(o.en, lang)); });
    var tt = tableFor(lang);
    document.title = tt[titleEN.trim()] != null ? tt[titleEN.trim()] : titleEN;
    document.documentElement.setAttribute('lang', lang);
    try { localStorage.setItem(LSKEY, lang); } catch (e) {}
    document.querySelectorAll('.lang-btn').forEach(function (b) {
      var on = b.getAttribute('data-lang') === lang;
      b.classList.toggle('active', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }

  // Build an EN · ES · DE toggle (one for the navbar, one for the mobile menu).
  function buildToggle() {
    var wrap = document.createElement('div');
    wrap.className = 'lang-toggle';
    wrap.setAttribute('role', 'group');
    wrap.setAttribute('aria-label', 'Language');
    LANGS.forEach(function (l, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'lang-btn';
      b.setAttribute('data-lang', l);
      b.textContent = l.toUpperCase();
      b.addEventListener('click', function () { applyLang(l); });
      wrap.appendChild(b);
      if (i < LANGS.length - 1) {
        var sep = document.createElement('span');
        sep.className = 'lang-sep';
        sep.setAttribute('aria-hidden', 'true');
        sep.textContent = '·';
        wrap.appendChild(sep);
      }
    });
    return wrap;
  }

  var navLinks = document.querySelector('.navbar-links');
  if (navLinks) {
    var socials = navLinks.querySelector('.social-icons');
    navLinks.insertBefore(buildToggle(), socials || null);
  }
  if (menu) {
    var mTog = buildToggle();
    mTog.classList.add('lang-toggle-mobile');
    menu.appendChild(mTog);
  }

  // Initial language: saved choice → browser language → English.
  var initialLang = 'en';
  try {
    var savedLang = localStorage.getItem(LSKEY);
    if (savedLang && LANGS.indexOf(savedLang) >= 0) {
      initialLang = savedLang;
    } else {
      var navLang = (navigator.language || 'en').slice(0, 2).toLowerCase();
      if (LANGS.indexOf(navLang) >= 0) initialLang = navLang;
    }
  } catch (e) {}
  applyLang(initialLang);

  // --- Scroll-reveal: fade/rise elements in as they enter the viewport ------
  // Progressive enhancement: elements start with .reveal (hidden via CSS); we
  // add .in-view when they scroll into frame, then stop observing. If the API
  // is missing or the user prefers reduced motion, everything is shown at once.
  var revealEls = document.querySelectorAll('.reveal');
  var reduceReveal = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (revealEls.length && 'IntersectionObserver' in window && !reduceReveal) {
    var revealIO = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in-view'); obs.unobserve(e.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    revealEls.forEach(function (el) { revealIO.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('in-view'); });
  }
})();
