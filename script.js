// ==========================================
// Isaac & Elijah's Car Wash — script.js
// ==========================================

(function () {
  // ---------- Progress bar ----------
  const main = document.querySelector('main');
  const raised = Number(main.dataset.raised) || 0;
  const goal = Number(main.dataset.goal) || 1000;
  const pct = Math.min(100, Math.round((raised / goal) * 100));

  const raisedEl = document.getElementById('raisedValue');
  const goalEl = document.getElementById('goalValue');
  const fillEl = document.getElementById('progressFill');
  const noteEl = document.getElementById('progressNote');

  const fmt = (n) => '$' + n.toLocaleString('en-US');

  raisedEl.textContent = fmt(raised);
  goalEl.textContent = fmt(goal);

  requestAnimationFrame(() => {
    setTimeout(() => { fillEl.style.width = pct + '%'; }, 200);
  });

  if (pct === 0) {
    noteEl.textContent = "Every wash gets us closer.";
  } else if (pct < 25) {
    noteEl.textContent = `${pct}% of the way there — thanks for helping us start!`;
  } else if (pct < 75) {
    noteEl.textContent = `${pct}% to our goal — we're picking up speed!`;
  } else if (pct < 100) {
    noteEl.textContent = `${pct}% — so close! Every wash counts now.`;
  } else {
    noteEl.textContent = `🎉 We hit our goal! Thank you, Queen Creek Villages!`;
  }

  // ---------- Footer year ----------
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ---------- Carousel + Lightbox ----------
  const track = document.getElementById('carouselTrack');
  const cards = Array.from(track.querySelectorAll('.carousel-card'));
  const dotsContainer = document.getElementById('carouselDots');
  const prevBtn = document.querySelector('.carousel-nav-prev');
  const nextBtn = document.querySelector('.carousel-nav-next');

  // Build dots
  cards.forEach((_, idx) => {
    const dot = document.createElement('button');
    dot.className = 'dot' + (idx === 0 ? ' active' : '');
    dot.type = 'button';
    dot.setAttribute('aria-label', `Go to photo ${idx + 1}`);
    dot.addEventListener('click', () => scrollToCard(idx));
    dotsContainer.appendChild(dot);
  });
  const dots = Array.from(dotsContainer.querySelectorAll('.dot'));

  function scrollToCard(idx) {
    const card = cards[idx];
    if (!card) return;
    const trackRect = track.getBoundingClientRect();
    const cardRect = card.getBoundingClientRect();
    const offset = cardRect.left - trackRect.left + track.scrollLeft - (trackRect.width - cardRect.width) / 2;
    track.scrollTo({ left: offset, behavior: 'smooth' });
  }

  function currentIndex() {
    const trackRect = track.getBoundingClientRect();
    const center = trackRect.left + trackRect.width / 2;
    let best = 0, bestDist = Infinity;
    cards.forEach((c, i) => {
      const r = c.getBoundingClientRect();
      const d = Math.abs((r.left + r.width / 2) - center);
      if (d < bestDist) { bestDist = d; best = i; }
    });
    return best;
  }

  function updateDots() {
    const i = currentIndex();
    dots.forEach((d, idx) => d.classList.toggle('active', idx === i));
  }

  let scrollTimeout;
  track.addEventListener('scroll', () => {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(updateDots, 60);
  }, { passive: true });

  prevBtn.addEventListener('click', () => {
    scrollToCard(Math.max(0, currentIndex() - 1));
  });
  nextBtn.addEventListener('click', () => {
    scrollToCard(Math.min(cards.length - 1, currentIndex() + 1));
  });

  // ---------- Lightbox ----------
  const lightbox = document.getElementById('lightbox');
  const lightboxImg = document.getElementById('lightboxImg');
  const lightboxCounter = document.getElementById('lightboxCounter');
  const lbClose = lightbox.querySelector('.lightbox-close');
  const lbPrev = lightbox.querySelector('.lightbox-prev');
  const lbNext = lightbox.querySelector('.lightbox-next');
  let lbIndex = 0;

  function showInLightbox(idx) {
    lbIndex = (idx + cards.length) % cards.length;
    const card = cards[lbIndex];
    lightboxImg.src = card.dataset.img;
    lightboxImg.alt = card.dataset.alt || '';
    lightboxCounter.textContent = `${lbIndex + 1} / ${cards.length}`;
    // Re-trigger pop animation
    lightboxImg.style.animation = 'none';
    lightboxImg.offsetHeight;
    lightboxImg.style.animation = '';
  }

  function openLightbox(idx) {
    showInLightbox(idx);
    if (typeof lightbox.showModal === 'function') {
      lightbox.showModal();
    } else {
      lightbox.setAttribute('open', '');
    }
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox() {
    if (typeof lightbox.close === 'function') {
      lightbox.close();
    } else {
      lightbox.removeAttribute('open');
    }
    document.body.style.overflow = '';
  }

  cards.forEach((card, idx) => {
    card.addEventListener('click', (e) => {
      e.preventDefault();
      openLightbox(idx);
    });
  });

  lbClose.addEventListener('click', closeLightbox);
  lbPrev.addEventListener('click', () => showInLightbox(lbIndex - 1));
  lbNext.addEventListener('click', () => showInLightbox(lbIndex + 1));

  // Click backdrop to close
  lightbox.addEventListener('click', (e) => {
    if (e.target === lightbox) closeLightbox();
  });

  // Keyboard
  document.addEventListener('keydown', (e) => {
    if (!lightbox.hasAttribute('open') && !lightbox.open) return;
    if (e.key === 'ArrowLeft') { e.preventDefault(); showInLightbox(lbIndex - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); showInLightbox(lbIndex + 1); }
    if (e.key === 'Escape') { closeLightbox(); }
  });

  // Touch swipe in lightbox
  let touchStartX = 0;
  let touchStartY = 0;
  lightbox.addEventListener('touchstart', (e) => {
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
  }, { passive: true });

  lightbox.addEventListener('touchend', (e) => {
    const dx = e.changedTouches[0].clientX - touchStartX;
    const dy = e.changedTouches[0].clientY - touchStartY;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) {
      if (dx > 0) showInLightbox(lbIndex - 1);
      else showInLightbox(lbIndex + 1);
    }
  }, { passive: true });

  // Native dialog close event (covers Esc handled by browser)
  lightbox.addEventListener('close', () => {
    document.body.style.overflow = '';
  });
})();
