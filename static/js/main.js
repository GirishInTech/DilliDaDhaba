/**
 * Dilli Da Dhaba — main.js
 * Lightweight vanilla JS helpers (Alpine handles interactivity).
 */

/* ---------------------------------------------------------------------------
   1. Intersection Observer — animate elements as they enter viewport
--------------------------------------------------------------------------- */
(function () {
  const ANIMATED_CLASS = 'animate-fade-up';
  const TRIGGER_CLASS = '[data-animate]';

  if (!('IntersectionObserver' in window)) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add(ANIMATED_CLASS);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1 }
  );

  document
    .querySelectorAll(TRIGGER_CLASS)
    .forEach((el) => observer.observe(el));
})();

/* ---------------------------------------------------------------------------
   2. Active nav highlight (already handled via Django template, but kept
      here as fallback for JS-navigate situations)
--------------------------------------------------------------------------- */
(function () {
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach((link) => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('nav-link--active');
    }
  });
})();

/* ---------------------------------------------------------------------------
   3. Smooth-scroll for anchor links on the same page
--------------------------------------------------------------------------- */
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
