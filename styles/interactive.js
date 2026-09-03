(function () {
  var doc;
  try {
    doc = window.parent.document;
  } catch (e) {
    return;
  }
  if (!doc || doc.getElementById("aurora-interactive")) return;

  var reduceMotion = false;
  try {
    reduceMotion = window.parent.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch (e) {}

  // ---- Cursor spotlight on glass cards ----
  var CARD_SELECTOR = [
    ".timeline-card",
    ".skill-card",
    ".edu-card",
    ".stat-card",
    ".mini-card",
    ".pillar-card",
    ".testimonial-card",
    ".coursework-card",
    ".telemetry-card",
    ".workbench-card",
    "[data-testid='stVerticalBlockBorderWrapper']"
  ].join(",");

  function initSpotlight() {
    var cards = doc.querySelectorAll(CARD_SELECTOR);
    cards.forEach(function (card) {
      if (!card.classList.contains("spotlight-host")) {
        card.classList.add("spotlight-host");
      }
    });
  }

  doc.addEventListener("pointermove", function (e) {
    if (!(e.target && e.target.closest)) return;
    var card = e.target.closest(CARD_SELECTOR);
    if (!card) return;
    var rect = card.getBoundingClientRect();
    card.style.setProperty("--mx", ((e.clientX - rect.left) / rect.width) * 100 + "%");
    card.style.setProperty("--my", ((e.clientY - rect.top) / rect.height) * 100 + "%");
  }, { passive: true });

  // ---- Scroll reveal ----
  function initReveal() {
    if (reduceMotion || !("IntersectionObserver" in window.parent)) return;
    var targets = doc.querySelectorAll(
      ".timeline-item, .stat-card, .mini-card, .pillar-card, .skill-card, .edu-card, .testimonial-card, .coursework-card, .telemetry-card, .workbench-card"
    );
    var observer = new window.parent.IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("reveal-in");
            entry.target.classList.remove("reveal-init");
            observer.unobserve(entry.target);
          }
        });
      },
      { root: null, rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
    );
    targets.forEach(function (el, i) {
      if (el.dataset.revealBound) return;
      el.dataset.revealBound = "1";
      el.classList.add("reveal-init");
      el.style.animationDelay = Math.min(i % 6, 5) * 60 + "ms";
      observer.observe(el);
    });
  }

  function boot() {
    initSpotlight();
    initReveal();
  }

  if (doc.readyState === "complete" || doc.readyState === "interactive") {
    setTimeout(boot, 120);
  } else {
    window.parent.addEventListener("DOMContentLoaded", boot);
  }

  // Streamlit re-renders sections on nav change: rebind shortly after.
  setTimeout(boot, 700);
  setTimeout(boot, 1800);

  var marker = doc.createElement("div");
  marker.id = "aurora-interactive";
  marker.style.display = "none";
  doc.body.appendChild(marker);
})();
