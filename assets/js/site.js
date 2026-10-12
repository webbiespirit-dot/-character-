(() => {
  'use strict';

  const d = document;
  const root = d.documentElement;
  const $ = (s, c = d) => c.querySelector(s);
  const $$ = (s, c = d) => [...c.querySelectorAll(s)];
  const MEDIA = window.WS_MEDIA || {};
  const EMAIL = 'webbiespirit@gmail.com';
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saveData = !!(navigator.connection && navigator.connection.saveData);
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  };

  /* ---------- words ---------- */
  const T = {
    en: {
      title: 'Web design in Cyprus · Free website preview | webbiespirit',
      description: 'webbiespirit is a web design studio in Cyprus. We design a free concept preview of your new website first, so you see it before you decide anything.',
      skip: 'Skip to content',
      videoLabel: 'Welcome video: our presenter introduces webbiespirit.',
      soundOn: 'Sound on',
      soundOff: 'Sound off',
      replay: 'Replay',
      pause: 'Pause',
      play: 'Play',
      captions: 'Captions',
      h1: 'Test the water first.',
      lead: 'We design a free concept preview of your new website, so you see it before you decide anything.',
      cta: 'Say hello',
      howLink: 'How it works',
      howTitle: 'How the free preview works',
      step1: 'Tell us about your business.',
      step2: 'We design a preview of your new site, free.',
      step3: 'You see it, then you decide.',
      illus: 'Illustration',
      whereTitle: 'Based in Cyprus. Working with businesses anywhere.',
      helloTitle: 'Write to us.',
      helloLead: "Tell us about your business, and we'll design your free preview.",
      copy: 'Copy email',
      copied: 'Copied',
      copyFail: 'Press and hold the address to copy it.',
      printAlt: 'Our presenter as a cyanotype print: a smiling woman with long wavy hair, in shades of Prussian blue.',
      printCap: 'Our presenter, as a sun-print.',
      mailSubject: 'Free concept preview',
      mailBody: 'Hi webbiespirit,\n\nMy business: \nWebsite (if any): \n',
    },
    el: {
      title: 'Κατασκευή ιστοσελίδων στην Κύπρο · Δωρεάν μακέτα | webbiespirit',
      description: 'Στο webbiespirit σχεδιάζουμε ιστοσελίδες με έδρα την Κύπρο. Σου φτιάχνουμε πρώτα δωρεάν μια μακέτα της νέας σου ιστοσελίδας, για να τη δεις πριν αποφασίσεις οτιδήποτε.',
      skip: 'Μετάβαση στο περιεχόμενο',
      videoLabel: 'Βίντεο καλωσορίσματος: η παρουσιάστριά μας σου συστήνει το webbiespirit.',
      soundOn: 'Άνοιξε τον ήχο',
      soundOff: 'Κλείσε τον ήχο',
      replay: 'Δες το ξανά',
      pause: 'Παύση',
      play: 'Αναπαραγωγή',
      captions: 'Υπότιτλοι',
      h1: 'Δοκίμασε πρώτα τα νερά.',
      lead: 'Σου σχεδιάζουμε δωρεάν μια μακέτα της νέας σου ιστοσελίδας, για να τη δεις πριν αποφασίσεις οτιδήποτε.',
      cta: 'Πες μας γεια',
      howLink: 'Πώς λειτουργεί',
      howTitle: 'Πώς λειτουργεί η δωρεάν μακέτα',
      step1: 'Πες μας για την επιχείρησή σου.',
      step2: 'Σχεδιάζουμε δωρεάν μια μακέτα της νέας σου ιστοσελίδας.',
      step3: 'Τη βλέπεις και μετά αποφασίζεις.',
      illus: 'Εικονογράφηση',
      whereTitle: 'Με έδρα την Κύπρο. Δουλεύουμε με επιχειρήσεις όπου κι αν βρίσκονται.',
      helloTitle: 'Γράψε μας.',
      helloLead: 'Πες μας για την επιχείρησή σου και θα σχεδιάσουμε τη δωρεάν μακέτα σου.',
      copy: 'Αντιγραφή email',
      copied: 'Αντιγράφηκε',
      copyFail: 'Πάτησε παρατεταμένα τη διεύθυνση για να την αντιγράψεις.',
      printAlt: 'Η παρουσιάστριά μας σε κυανοτυπία: μια χαμογελαστή γυναίκα με μακριά κυματιστά μαλλιά, σε αποχρώσεις του μπλε της Πρωσίας.',
      printCap: 'Η παρουσιάστριά μας σε κυανοτυπία.',
      mailSubject: 'Δωρεάν μακέτα ιστοσελίδας',
      mailBody: 'Γεια σας,\n\nΗ επιχείρησή μου: \nΙστοσελίδα (αν υπάρχει): \n',
    },
  };

  const pickLang = () => {
    const q = new URLSearchParams(location.search).get('lang');
    if (q === 'en' || q === 'el') return q;
    const saved = store.get('ws-lang');
    if (saved === 'en' || saved === 'el') return saved;
    return /^el\b/i.test(navigator.language || '') ? 'el' : 'en';
  };
  let lang = pickLang();

  // Where the visitor came from (?utm_source=instagram, ?ref=dm, or Instagram's in-app browser),
  // kept for the visit and added to the email subject so each enquiry shows its channel.
  const source = (() => {
    const p = new URLSearchParams(location.search);
    const clean = (v) => (v || '').toLowerCase().replace(/[^a-z0-9_-]/g, '').slice(0, 24);
    let s = clean(p.get('utm_source') || p.get('ref'));
    try {
      if (s) sessionStorage.setItem('ws-src', s);
      else s = sessionStorage.getItem('ws-src') || '';
    } catch (e) { /* private mode */ }
    if (!s && /Instagram/i.test(navigator.userAgent)) s = 'instagram';
    return s;
  })();

  const mailto = (l) => {
    const subject = T[l].mailSubject + (source ? ` · ${source}` : '');
    return `mailto:${EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(T[l].mailBody)}`;
  };

  const applyWords = (l) => {
    const t = T[l];
    root.lang = l;
    d.title = t.title;
    const desc = $('meta[name="description"]');
    if (desc) desc.setAttribute('content', t.description);
    const canon = $('link[rel="canonical"]');
    if (canon) canon.href = l === 'el' ? 'https://webbiespirit.com/?lang=el' : 'https://webbiespirit.com/';
    $$('[data-i18n]').forEach((el) => {
      const v = t[el.dataset.i18n];
      if (v != null) el.textContent = v;
    });
    $$('[data-i18n-aria-label]').forEach((el) => {
      const v = t[el.dataset.i18nAriaLabel];
      if (v != null) el.setAttribute('aria-label', v);
    });
    $$('[data-i18n-alt]').forEach((el) => {
      const v = t[el.dataset.i18nAlt];
      if (v != null) el.setAttribute('alt', v);
    });
    $$('[data-mailto]').forEach((a) => { a.href = mailto(l); });
    $$('.lang__btn').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.lang === l)));
  };

  /* ---------- presenter video ---------- */
  const video = $('#presenter');
  const print = $('#print');
  const ctrl = $('#ctrl');
  const cap = $('#cap');
  const capLine = $('#capLine');
  const btnSound = $('#btnSound');
  const btnSoundLabel = $('#btnSoundLabel');
  const btnPlay = $('#btnPlay');
  const btnCC = $('#btnCC');
  let heard = false;      // the visitor turned sound on at least once
  let captionsOn = store.get('ws-cc') !== 'off';
  let userPaused = false;
  let inView = true;
  let videoLoaded = false;

  const useIcon = (btn, id) => { const u = $('use', btn); if (u) u.setAttribute('href', id); };

  const pickSize = () => {
    // 1080p only when the print is drawn large on a dense screen and data is not being saved.
    const h = print ? print.getBoundingClientRect().height : 0;
    return !saveData && h * (window.devicePixelRatio || 1) > 1400 ? 'v1080' : 'v720';
  };

  let cueTrack = null;
  const renderCue = () => {
    const cues = cueTrack && cueTrack.activeCues;
    capLine.textContent = cues && cues.length ? [...cues].map((c) => c.text).join('\n') : '';
  };

  // The page draws captions itself, so the track stays 'hidden': its cues load and fire
  // cuechange, but the browser never paints its own copy on top. No `default` attribute,
  // because a default track gets switched back to 'showing' by the browser.
  const setTrack = (l) => {
    $$('track', video).forEach((t) => t.remove());
    const tr = d.createElement('track');
    tr.kind = 'captions';
    tr.srclang = l;
    tr.label = l === 'el' ? 'Ελληνικά' : 'English';
    tr.src = `assets/captions/${l}.vtt`;
    video.appendChild(tr);
    cueTrack = tr.track;
    cueTrack.mode = 'hidden';
    cueTrack.addEventListener('cuechange', renderCue);
    tr.addEventListener('load', () => { if (cueTrack === tr.track) { cueTrack.mode = 'hidden'; renderCue(); } });
  };

  const syncButtons = () => {
    const t = T[lang];
    const ended = heard && video.ended;
    if (ended) {
      useIcon(btnSound, '#i-replay');
      btnSoundLabel.textContent = t.replay;
      btnSound.setAttribute('aria-pressed', 'false');
    } else if (video.muted) {
      useIcon(btnSound, '#i-sound-off');
      btnSoundLabel.textContent = t.soundOn;
      btnSound.setAttribute('aria-pressed', 'false');
    } else {
      useIcon(btnSound, '#i-sound-on');
      btnSoundLabel.textContent = t.soundOff;
      btnSound.setAttribute('aria-pressed', 'true');
    }
    const playing = !video.paused && !video.ended;
    useIcon(btnPlay, playing ? '#i-pause' : '#i-play');
    btnPlay.setAttribute('aria-label', playing ? t.pause : t.play);
    btnCC.setAttribute('aria-pressed', String(captionsOn));
    btnCC.setAttribute('aria-label', t.captions);
    if (captionsOn) cap.removeAttribute('data-off'); else cap.setAttribute('data-off', '');
  };

  const tryPlay = () => {
    const p = video.play();
    if (p && p.catch) p.catch(() => syncButtons());
  };

  const loadVideo = (l) => {
    const src = MEDIA[l] || MEDIA.en;
    if (!src) return;
    const wasPlaying = !video.paused && !video.ended;
    video.poster = src.poster;
    video.preload = saveData ? 'none' : 'metadata';
    video.src = src[pickSize()] || src.v720;
    setTrack(l);
    capLine.textContent = '';
    // A new language always starts from the greeting.
    if (wasPlaying || (!reduceMotion && !saveData && !userPaused && inView)) tryPlay();
    syncButtons();
  };

  if (video) {
    // Script is running: drop the native controls and use the print's own.
    video.removeAttribute('controls');
    $$('source', video).forEach((s) => s.remove());
    ctrl.hidden = false;
    video.muted = true;
    video.loop = true;

    btnSound.addEventListener('click', () => {
      if (heard && video.ended) {
        video.currentTime = 0;
        tryPlay();
      } else if (video.muted) {
        // First time with sound: start from the greeting so nothing is missed.
        if (!heard) video.currentTime = 0;
        heard = true;
        video.muted = false;
        video.loop = false;
        userPaused = false;
        tryPlay();
      } else {
        video.muted = true;
      }
      syncButtons();
    });
    btnPlay.addEventListener('click', () => {
      if (video.paused || video.ended) { userPaused = false; tryPlay(); }
      else { userPaused = true; video.pause(); }
      syncButtons();
    });
    btnCC.addEventListener('click', () => {
      captionsOn = !captionsOn;
      store.set('ws-cc', captionsOn ? 'on' : 'off');
      syncButtons();
    });
    ['play', 'pause', 'ended', 'volumechange'].forEach((e) => video.addEventListener(e, syncButtons));

    // Keep the battery: a muted loop pauses itself off screen and resumes when it comes back.
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(([e]) => {
        inView = e.isIntersecting;
        if (!video.muted) return;
        if (!inView) video.pause();
        else if (!userPaused && !reduceMotion && !saveData) tryPlay();
      }, { threshold: 0.2 }).observe(print);
    }
  }

  /* ---------- language switch ---------- */
  const setLang = (l, user) => {
    if (!T[l]) return;
    const changed = l !== lang;
    lang = l;
    applyWords(l);
    // Always run the loader once: it picks 720p or 1080p and installs the hidden caption track.
    if (video && (changed || !videoLoaded)) { videoLoaded = true; loadVideo(l); }
    if (user) {
      store.set('ws-lang', l);
      const u = new URL(location.href);
      u.searchParams.set('lang', l);
      history.replaceState(null, '', u);
    }
  };
  $$('.lang__btn').forEach((b) => b.addEventListener('click', () => setLang(b.dataset.lang, true)));

  /* ---------- develop: bands expose as they come into view ----------
     Where CSS can tie the olive print's exposure to scroll position, it does, so leave it out here. */
  const scrollExpose = !!(window.CSS && CSS.supports && CSS.supports('animation-timeline: view()'));
  const latent = $$('[data-develop]').filter((el) => !(scrollExpose && el.classList.contains('where__print')));
  if (!reduceMotion && 'IntersectionObserver' in window) {
    latent.forEach((el) => el.classList.add('is-latent'));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        const sibs = [...e.target.parentElement.children].filter((n) => n.hasAttribute('data-develop'));
        const i = Math.max(0, sibs.indexOf(e.target));
        setTimeout(() => e.target.classList.remove('is-latent'), 180 + i * 260);
      });
    }, { threshold: 0.35, rootMargin: '0px 0px -8% 0px' });
    latent.forEach((el) => io.observe(el));
  }

  /* ---------- olive sun-print loop ---------- */
  const olive = $('#olive');
  if (olive && MEDIA.olive) {
    olive.poster = MEDIA.olive.poster;
    if (!reduceMotion && !saveData && 'IntersectionObserver' in window) {
      new IntersectionObserver(([e]) => {
        if (e.isIntersecting) {
          if (!olive.src) olive.src = MEDIA.olive.loop;
          const p = olive.play();
          if (p && p.catch) p.catch(() => {});
        } else {
          olive.pause();
        }
      }, { threshold: 0.25 }).observe(olive);
    }
  }

  /* ---------- copy the address ---------- */
  const btnCopy = $('#btnCopy');
  const copyLabel = $('#btnCopyLabel');
  const copyStatus = $('#copyStatus');
  if (btnCopy) {
    btnCopy.addEventListener('click', () => {
      const done = (ok) => {
        const msg = ok ? T[lang].copied : T[lang].copyFail;
        copyLabel.textContent = msg;
        copyStatus.textContent = msg;
        clearTimeout(btnCopy._t);
        btnCopy._t = setTimeout(() => { copyLabel.textContent = T[lang].copy; copyStatus.textContent = ''; }, 2200);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(EMAIL).then(() => done(true), () => done(false));
      } else {
        done(false);
      }
    });
  }

  /* ---------- phone dock: shown while neither in-page action is on screen ---------- */
  const dock = $('#dock');
  const dockLink = dock && $('a', dock);
  const watch = [$('#heroActions .btn--sun'), $('#helloActions .btn--sun')].filter(Boolean);
  if (dock && 'IntersectionObserver' in window && watch.length) {
    const seen = new Map();
    const update = () => {
      const show = ![...seen.values()].some(Boolean);
      dock.classList.toggle('is-on', show);
      dock.setAttribute('aria-hidden', String(!show));
      if (dockLink) dockLink.tabIndex = show ? 0 : -1;
    };
    // An in-page action only counts as reachable when it is fully on screen;
    // a button cut off by the bottom edge is not under the thumb.
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => seen.set(e.target, e.intersectionRatio > 0.98));
      update();
    }, { threshold: [0, 0.99, 1] });
    watch.forEach((el) => io.observe(el));
  }

  setLang(lang, false);
})();
