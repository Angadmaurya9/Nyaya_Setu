/**
 * NyayaSetu — Main JavaScript (app/static/js/main.js)
 * =====================================================
 * Vanilla JS only — no external libraries or frameworks.
 *
 * Features:
 *   1. Dark / Light theme toggle (persisted in localStorage)
 *   2. Mobile hamburger navigation
 *   3. Flash message auto-dismiss
 *   4. Active navigation highlighting (based on URL)
 *   5. Smooth scroll for anchor links
 */

(function () {
  "use strict";

  /* ──────────────────────────────────────────────────────────
     1. Theme Toggle
     ────────────────────────────────────────────────────────── */
  const HTML_ROOT     = document.getElementById("html-root");
  const THEME_TOGGLE  = document.getElementById("theme-toggle");
  const STORAGE_KEY   = "nyayasetu-theme";

  /**
   * Apply the given theme ('light' | 'dark') to the document.
   * Saves the preference to localStorage so it persists across visits.
   */
  function applyTheme(theme) {
    HTML_ROOT.setAttribute("data-theme", theme);
    localStorage.setItem(STORAGE_KEY, theme);
    // Update button aria-label for accessibility
    if (THEME_TOGGLE) {
      THEME_TOGGLE.setAttribute(
        "aria-label",
        theme === "dark" ? "Switch to light mode" : "Switch to dark mode"
      );
      THEME_TOGGLE.setAttribute(
        "title",
        theme === "dark" ? "Switch to light mode" : "Switch to dark mode"
      );
    }
  }

  /**
   * Load the saved theme from localStorage, defaulting to 'light'.
   * Also respects the user's OS preference (prefers-color-scheme) as
   * a fallback when no explicit choice has been saved.
   */
  function loadTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      applyTheme(saved);
    } else if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      applyTheme("dark");
    } else {
      applyTheme("light");
    }
  }

  if (THEME_TOGGLE) {
    THEME_TOGGLE.addEventListener("click", function () {
      const current = HTML_ROOT.getAttribute("data-theme") || "light";
      applyTheme(current === "dark" ? "light" : "dark");
    });
  }

  // Load theme immediately to prevent flash of wrong theme
  loadTheme();


  /* ──────────────────────────────────────────────────────────
     2. Mobile Hamburger Navigation
     ────────────────────────────────────────────────────────── */
  const NAV_TOGGLE = document.getElementById("nav-toggle");
  const NAV_MENU   = document.getElementById("nav-menu");

  if (NAV_TOGGLE && NAV_MENU) {
    NAV_TOGGLE.addEventListener("click", function () {
      const isOpen = NAV_MENU.classList.toggle("is-open");
      NAV_TOGGLE.setAttribute("aria-expanded", isOpen.toString());
    });

    // Close nav when a link inside it is clicked (single-page-like UX)
    NAV_MENU.querySelectorAll(".navbar__link").forEach(function (link) {
      link.addEventListener("click", function () {
        NAV_MENU.classList.remove("is-open");
        NAV_TOGGLE.setAttribute("aria-expanded", "false");
      });
    });

    // Close nav when clicking outside of it
    document.addEventListener("click", function (e) {
      if (!NAV_TOGGLE.contains(e.target) && !NAV_MENU.contains(e.target)) {
        NAV_MENU.classList.remove("is-open");
        NAV_TOGGLE.setAttribute("aria-expanded", "false");
      }
    });
  }


  /* ──────────────────────────────────────────────────────────
     3. Flash Message Auto-Dismiss
     ────────────────────────────────────────────────────────── */
  /**
   * Auto-dismiss flash messages after 6 seconds.
   * User can also close them manually via the × button in the template.
   */
  document.querySelectorAll(".flash").forEach(function (flashEl) {
    setTimeout(function () {
      flashEl.style.transition = "opacity 0.4s ease, max-height 0.4s ease";
      flashEl.style.opacity    = "0";
      flashEl.style.maxHeight  = "0";
      flashEl.style.overflow   = "hidden";
      setTimeout(function () { flashEl.remove(); }, 450);
    }, 6000);
  });


  /* ──────────────────────────────────────────────────────────
     4. Smooth Scroll (polyfill for older browsers)
     ────────────────────────────────────────────────────────── */
  /**
   * For browsers that don't support CSS scroll-behavior: smooth,
   * intercept anchor clicks and scroll smoothly.
   */
  if (!("scrollBehavior" in document.documentElement.style)) {
    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
      anchor.addEventListener("click", function (e) {
        const target = document.querySelector(this.getAttribute("href"));
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      });
    });
  }


  /* ──────────────────────────────────────────────────────────
     5. Keyboard accessibility — close nav on Escape
     ────────────────────────────────────────────────────────── */
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && NAV_MENU && NAV_MENU.classList.contains("is-open")) {
      NAV_MENU.classList.remove("is-open");
      NAV_TOGGLE.setAttribute("aria-expanded", "false");
      NAV_TOGGLE.focus();
    }
  });

}()); // end IIFE
