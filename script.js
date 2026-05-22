// ==========================================
// Isaac & Elijah's Car Wash — script.js
// ==========================================

(function () {
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

  // Trigger animation after a brief delay so the fill animates in
  requestAnimationFrame(() => {
    setTimeout(() => {
      fillEl.style.width = pct + '%';
    }, 200);
  });

  // Friendly progress message
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

  // Footer year
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
