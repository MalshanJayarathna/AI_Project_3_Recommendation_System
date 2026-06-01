/* ============================================================
   script.js — DecodeLabs AI Course Recommendation System
   Handles: particles, API calls, result rendering, catalogue
   ============================================================ */

// ── Utility: Category CSS class mapping ───────────────────────
const CATEGORY_CLASS = {
  "Machine Learning":   "cat-ml",
  "Deep Learning":      "cat-dl",
  "NLP":                "cat-nlp",
  "Natural Language Processing": "cat-nlp",
  "Computer Vision":    "cat-cv",
  "Data Science":       "cat-ds",
  "Programming":        "cat-prog",
  "Cloud Computing":    "cat-cloud",
  "Statistics":         "cat-ml",
  "Big Data":           "cat-cloud",
  "Automation":         "cat-cv",
  "MLOps":              "cat-ds",
  "Reinforcement Learning": "cat-dl",
  "Generative AI":      "cat-nlp",
  "AI Ethics":          "cat-default",
  "Databases":          "cat-prog",
};

const CATEGORY_EMOJI = {
  "Machine Learning":   "🤖",
  "Deep Learning":      "🧠",
  "NLP":                "💬",
  "Natural Language Processing": "💬",
  "Computer Vision":    "👁️",
  "Data Science":       "📊",
  "Programming":        "🐍",
  "Cloud Computing":    "☁️",
  "Statistics":         "📐",
  "Big Data":           "🗄️",
  "Automation":         "⚙️",
  "MLOps":              "🔧",
  "Reinforcement Learning": "🎮",
  "Generative AI":      "✨",
  "AI Ethics":          "⚖️",
  "Databases":          "🗃️",
};

// ── Generate Particles ─────────────────────────────────────────
function createParticles() {
  const container = document.getElementById("particles");
  if (!container) return;
  const colors = ["#7c6ff7", "#a78bfa", "#06b6d4", "#ec4899"];
  for (let i = 0; i < 40; i++) {
    const p = document.createElement("div");
    p.className = "particle";
    p.style.left      = Math.random() * 100 + "%";
    p.style.top       = Math.random() * 100 + "%";
    p.style.setProperty("--dur",   (4 + Math.random() * 8) + "s");
    p.style.setProperty("--delay", -(Math.random() * 10) + "s");
    p.style.background = colors[Math.floor(Math.random() * colors.length)];
    p.style.width  = (1 + Math.random() * 3) + "px";
    p.style.height = p.style.width;
    container.appendChild(p);
  }
}

// ── Navbar scroll effect ──────────────────────────────────────
function initNavbarScroll() {
  const navbar = document.querySelector(".navbar");
  window.addEventListener("scroll", () => {
    if (window.scrollY > 40) {
      navbar.style.background = "rgba(6,6,18,0.92)";
    } else {
      navbar.style.background = "rgba(6,6,18,0.7)";
    }
  }, { passive: true });
}

// ── Intersection Observer for fade-in animations ──────────────
function initScrollAnimations() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = "1";
          entry.target.style.transform = "translateY(0)";
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  document.querySelectorAll(".step-card, .section-header").forEach(el => {
    el.style.opacity = "0";
    el.style.transform = "translateY(24px)";
    el.style.transition = "opacity 0.55s ease, transform 0.55s ease";
    observer.observe(el);
  });
}

// ── Get category CSS class ─────────────────────────────────────
function getCatClass(category) {
  return CATEGORY_CLASS[category] || "cat-default";
}
function getCatEmoji(category) {
  return CATEGORY_EMOJI[category] || "📚";
}

// ── Score → bar width (cap at 100%) ───────────────────────────
function scoreToWidth(score) {
  return Math.min(score * 300, 100).toFixed(1) + "%";
}

// ── Score color label ──────────────────────────────────────────
function scoreLabel(score) {
  if (score >= 0.5) return "Excellent Match";
  if (score >= 0.3) return "Strong Match";
  if (score >= 0.15) return "Good Match";
  if (score >= 0.05) return "Moderate Match";
  return "Weak Match";
}

// ── Render a single result card ────────────────────────────────
function renderResultCard(item, delay) {
  const catClass = getCatClass(item.category);
  const catEmoji = getCatEmoji(item.category);
  const barW     = scoreToWidth(item.similarity_score);
  const rankClass = item.rank <= 3 ? `rank-${item.rank}` : "";

  const card = document.createElement("div");
  card.className = "result-card";
  card.style.animationDelay = delay + "ms";

  card.innerHTML = `
    <div class="rank-badge ${rankClass}">#${item.rank}</div>
    <div class="card-body">
      <div class="card-title">${escapeHTML(item.title)}</div>
      <span class="card-category ${catClass}">
        ${catEmoji} ${escapeHTML(item.category)}
      </span>
      <p class="card-desc">${escapeHTML(item.description)}</p>
    </div>
    <div class="card-score-panel">
      <span class="score-value">${item.similarity_score.toFixed(4)}</span>
      <span class="score-label">${scoreLabel(item.similarity_score)}</span>
      <div class="score-bar-wrap">
        <div class="score-bar-fill" style="width: 0%" data-target="${barW}"></div>
      </div>
    </div>
  `;

  return card;
}

// ── Animate score bars after cards are inserted ────────────────
function animateScoreBars() {
  document.querySelectorAll(".score-bar-fill").forEach(bar => {
    const target = bar.dataset.target;
    requestAnimationFrame(() => {
      setTimeout(() => { bar.style.width = target; }, 100);
    });
  });
}

// ── Fetch recommendations from Flask API ──────────────────────
async function fetchRecommendations(query) {
  const loadingEl  = document.getElementById("loading-state");
  const errorEl    = document.getElementById("error-state");
  const resultsEl  = document.getElementById("results-section");
  const gridEl     = document.getElementById("results-grid");

  // Reset UI
  loadingEl.hidden  = false;
  errorEl.hidden    = true;
  resultsEl.hidden  = true;
  gridEl.innerHTML  = "";

  try {
    const res = await fetch("/recommend", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ interests: query }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || "Server error. Please try again.");
    }

    loadingEl.hidden = true;

    // Update header
    document.getElementById("results-query").textContent = `"${data.query}"`;
    document.getElementById("results-meta").textContent =
      `${data.recommendations.length} courses matched`;

    // Render cards
    data.recommendations.forEach((item, i) => {
      const card = renderResultCard(item, i * 80);
      gridEl.appendChild(card);
    });

    resultsEl.hidden = false;

    // Animate bars after paint
    requestAnimationFrame(() => {
      setTimeout(animateScoreBars, 200);
    });

    // Smooth scroll to results
    setTimeout(() => {
      resultsEl.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100);

  } catch (err) {
    loadingEl.hidden = true;
    document.getElementById("error-message").textContent = err.message;
    errorEl.hidden = false;
  }
}

// ── Load and render all courses in catalogue ──────────────────
async function loadCatalogue() {
  const grid = document.getElementById("catalogue-grid");
  try {
    const res  = await fetch("/courses");
    const data = await res.json();

    grid.innerHTML = "";
    data.courses.forEach((course, i) => {
      const catClass = getCatClass(course.category);
      const catEmoji = getCatEmoji(course.category);

      const card = document.createElement("div");
      card.className = "catalogue-card";
      card.style.animationDelay = (i * 40) + "ms";

      card.innerHTML = `
        <div class="cat-card-header">
          <div class="cat-card-title">${escapeHTML(course.title)}</div>
          <span class="card-category ${catClass}" style="white-space:nowrap">
            ${catEmoji} ${escapeHTML(course.category)}
          </span>
        </div>
        <p class="cat-card-desc">${escapeHTML(course.description)}</p>
      `;

      grid.appendChild(card);
    });
  } catch {
    grid.innerHTML = `<p class="catalogue-loading">Failed to load courses.</p>`;
  }
}

// ── XSS safety ────────────────────────────────────────────────
function escapeHTML(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ── Event Listeners ────────────────────────────────────────────
function initEvents() {
  const input   = document.getElementById("interests-input");
  const btn     = document.getElementById("search-btn");
  const chips   = document.querySelectorAll(".chip");

  // Search button click
  btn.addEventListener("click", () => {
    const q = input.value.trim();
    if (q) fetchRecommendations(q);
  });

  // Enter key
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const q = input.value.trim();
      if (q) fetchRecommendations(q);
    }
  });

  // Suggestion chips
  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      const q = chip.dataset.query;
      input.value = q;
      fetchRecommendations(q);
      document.getElementById("recommender").scrollIntoView({ behavior: "smooth" });
    });
  });
}

// ── Init ───────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  createParticles();
  initNavbarScroll();
  initScrollAnimations();
  initEvents();
  loadCatalogue();
});
