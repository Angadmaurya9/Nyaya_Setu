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


  /* ──────────────────────────────────────────────────────────
     6. RTI AI Question Generator (Phase 2 Frontend Integration)
     ────────────────────────────────────────────────────────── */
  const rtiForm           = document.getElementById("rti-form");
  const btnGenerate       = document.getElementById("btn-generate-questions");
  const aiDesc            = document.getElementById("ai_description");
  const aiCharCounter     = document.getElementById("ai-char-counter");
  const aiSpinner         = document.getElementById("ai-spinner");
  const aiBtnText         = document.getElementById("ai-btn-text");
  const aiErrorBox        = document.getElementById("ai-error-box");
  const aiErrorText       = document.getElementById("ai-error-text");
  const aiSuccessBox      = document.getElementById("ai-success-box");
  const aiSuccessText     = document.getElementById("ai-success-text");

  const subjectInput      = document.getElementById("subject");
  const infoRequested     = document.getElementById("info_requested");
  const btnAddQuery       = document.getElementById("btn-add-query");
  const btnRemoveLast     = document.getElementById("btn-remove-last-query");

  if (btnGenerate && aiDesc && subjectInput && infoRequested) {
    const pageLang = (rtiForm && rtiForm.getAttribute("data-lang")) ||
                     document.documentElement.lang ||
                     "en";

    // 1. Live character counter
    if (aiCharCounter) {
      aiDesc.addEventListener("input", function () {
        const len = this.value.length;
        aiCharCounter.textContent = len + " / 1000";
        if (len > 900) {
          aiCharCounter.classList.add("char-counter--warning");
        } else {
          aiCharCounter.classList.remove("char-counter--warning");
        }
        if (len > 1000) {
          aiCharCounter.classList.add("char-counter--error");
        } else {
          aiCharCounter.classList.remove("char-counter--error");
        }
      });
    }

    function showAiError(msg) {
      if (aiErrorBox && aiErrorText) {
        aiErrorText.textContent = msg;
        aiErrorBox.style.display = "flex";
      }
      if (aiSuccessBox) {
        aiSuccessBox.style.display = "none";
      }
    }

    function showAiSuccess(msg) {
      if (aiSuccessBox && aiSuccessText) {
        aiSuccessText.textContent = msg;
        aiSuccessBox.style.display = "flex";
      }
      if (aiErrorBox) {
        aiErrorBox.style.display = "none";
      }
    }

    function clearAiFeedback() {
      if (aiErrorBox) aiErrorBox.style.display = "none";
      if (aiSuccessBox) aiSuccessBox.style.display = "none";
    }

    // 2. Generate button click handler
    btnGenerate.addEventListener("click", async function () {
      clearAiFeedback();
      const rawText = aiDesc.value.trim();

      // Client-side length validation
      if (rawText.length < 10) {
        showAiError(
          pageLang === "hi"
            ? "कृपया अपनी समस्या का विवरण कम से कम 10 अक्षरों में दर्ज करें।"
            : "Please describe your issue or the information needed in at least 10 characters."
        );
        aiDesc.focus();
        return;
      }

      if (rawText.length > 1000) {
        showAiError(
          pageLang === "hi"
            ? "विवरण 1000 अक्षरों से अधिक नहीं हो सकता।"
            : "Description cannot exceed 1000 characters."
        );
        aiDesc.focus();
        return;
      }

      // Check for accidental overwrite of existing user input
      const existingSubject = subjectInput.value.trim();
      const existingQueries = infoRequested.value.trim();
      if (existingSubject.length > 0 || existingQueries.length > 0) {
        const confirmMsg = pageLang === "hi"
          ? "विषय या प्रश्नों में पहले से सामग्री दर्ज है। क्या आप इसे AI द्वारा सुझाए गए प्रश्नों से बदलना चाहते हैं?"
          : "You already have content entered in the Subject or Questions fields. Do you want to replace it with the AI suggestions?";
        if (!window.confirm(confirmMsg)) {
          return; // User declined overwrite
        }
      }

      // Set loading state & prevent duplicate submission
      btnGenerate.disabled = true;
      btnGenerate.setAttribute("aria-busy", "true");
      if (aiSpinner) aiSpinner.style.display = "inline-block";
      const defaultBtnLabel = aiBtnText ? aiBtnText.textContent : "Generate RTI Questions";
      if (aiBtnText) {
        aiBtnText.textContent = pageLang === "hi"
          ? "प्रश्न तैयार किए जा रहे हैं..."
          : "Generating questions...";
      }

      try {
        const response = await fetch("/rti/suggest-questions", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Accept": "application/json"
          },
          body: JSON.stringify({
            description: rawText,
            lang: pageLang
          })
        });

        const data = await response.json().catch(function () { return null; });

        if (!response.ok) {
          const errMsg = (data && data.error)
            ? data.error
            : (pageLang === "hi"
                ? "AI सेवा वर्तमान में अनुपलब्ध है। कृपया मैन्युअल रूप से विवरण भरें या बाद में प्रयास करें।"
                : "AI service is currently unavailable. Please enter details manually or try again later.");
          showAiError(errMsg);
          return;
        }

        if (data && data.success && data.data) {
          // Populate Subject
          if (data.data.subject) {
            subjectInput.value = data.data.subject;
          }

          // Populate Questions (one per line with standard numbering)
          if (Array.isArray(data.data.questions) && data.data.questions.length > 0) {
            const formatted = data.data.questions.map(function (q, idx) {
              const clean = q.replace(/^\s*(?:\d+[\.\)]|\-|\*)\s*/, "").trim();
              return (idx + 1) + ". " + clean;
            }).join("\n");
            infoRequested.value = formatted;
          }

          showAiSuccess(
            pageLang === "hi"
              ? "✅ आरटीआई विषय और प्रश्न नीचे भर दिए गए हैं। कृपया समीक्षा करें और आवश्यकतानुसार संपादन करें।"
              : "✅ RTI subject and questions generated below. Please review and edit as needed before generating the preview."
          );

          // Smooth scroll to Subject field so user sees populated results
          subjectInput.scrollIntoView({ behavior: "smooth", block: "center" });
          subjectInput.focus();
        } else {
          showAiError(
            pageLang === "hi"
              ? "अमान्य AI प्रतिक्रिया प्राप्त हुई। कृपया पुनः प्रयास करें।"
              : "Received an invalid response from AI. Please try again."
          );
        }
      } catch (networkErr) {
        showAiError(
          pageLang === "hi"
            ? "नेटवर्क त्रुटि: सर्वर से संपर्क नहीं हो सका। कृपया अपना कनेक्शन जांचें।"
            : "Network error: Could not reach the server. Please check your connection."
        );
      } finally {
        btnGenerate.disabled = false;
        btnGenerate.removeAttribute("aria-busy");
        if (aiSpinner) aiSpinner.style.display = "none";
        if (aiBtnText) aiBtnText.textContent = defaultBtnLabel;
      }
    });

    // 3. Add Query button
    if (btnAddQuery) {
      btnAddQuery.addEventListener("click", function () {
        const val = infoRequested.value.trimEnd();
        const lines = val ? val.split("\n").filter(function (l) { return l.trim().length > 0; }) : [];
        const nextNum = lines.length + 1;
        infoRequested.value = (val ? val + "\n" : "") + nextNum + ". ";
        infoRequested.focus();
        infoRequested.setSelectionRange(infoRequested.value.length, infoRequested.value.length);
      });
    }

    // 4. Remove Last Query button
    if (btnRemoveLast) {
      btnRemoveLast.addEventListener("click", function () {
        const val = infoRequested.value.trimEnd();
        if (!val) return;
        const lines = val.split("\n");
        if (lines.length > 0) {
          lines.pop();
          infoRequested.value = lines.join("\n");
          infoRequested.focus();
        }
      });
    }
  }

}()); // end IIFE

