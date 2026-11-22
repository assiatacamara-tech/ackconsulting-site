(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  // Menus déroulants (Prestations, À propos)
  $$("[data-dropdown]").forEach(function (box) {
    var btn = $("[data-dropdown-toggle]", box), panel = $("[data-dropdown-panel]", box);
    if (!btn || !panel) return;
    btn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = panel.classList.toggle("hidden") === false;
      btn.setAttribute("aria-expanded", open);
      var ico = $("svg", btn); if (ico) ico.classList.toggle("rotate-180", open);
    });
  });
  document.addEventListener("mousedown", function (e) {
    $$("header nav [data-dropdown]").forEach(function (box) {
      if (!box.contains(e.target)) {
        var p = $("[data-dropdown-panel]", box), b = $("[data-dropdown-toggle]", box);
        if (p && !p.classList.contains("hidden") && box.closest(".lg\\:flex")) {
          p.classList.add("hidden"); b.setAttribute("aria-expanded", "false");
          var ico = $("svg", b); if (ico) ico.classList.remove("rotate-180");
        }
      }
    });
  });

  // Menu mobile
  var mt = $("[data-mobile-toggle]"), mm = $("[data-mobile-menu]"), fab = $("[data-floating-contact]");
  if (mt && mm) mt.addEventListener("click", function () {
    var open = mm.classList.toggle("hidden") === false;
    mt.setAttribute("aria-expanded", open);
    $("[data-icon-open]", mt).classList.toggle("hidden", open);
    $("[data-icon-close]", mt).classList.toggle("hidden", !open);
    if (fab) fab.classList.toggle("hidden", open);
  });

  // Fenêtre « Nous contacter »
  var modal = $("[data-contact-modal]");
  function openModal() { if (!modal) return; modal.classList.remove("hidden"); document.body.style.overflow = "hidden"; if (fab) fab.classList.add("hidden"); }
  function closeModal() { if (!modal) return; modal.classList.add("hidden"); document.body.style.overflow = ""; if (fab) fab.classList.remove("hidden"); }
  $$("[data-open-contact]").forEach(function (b) { b.addEventListener("click", openModal); });
  $$("[data-close-contact]").forEach(function (b) { b.addEventListener("click", closeModal); });
  if (modal) modal.addEventListener("mousedown", function (e) { if (e.target === modal) closeModal(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeModal(); });

  // Questions fréquentes
  $$("[data-faq]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var ans = btn.nextElementSibling;
      if (!ans || !ans.classList.contains("faq-answer")) return;
      var open = ans.classList.toggle("hidden") === false;
      btn.setAttribute("aria-expanded", open);
      var ico = $("svg", btn); if (ico) ico.classList.toggle("rotate-180", open);
    });
  });

  // Formulaires : enregistrés par Netlify, puis confirmation à l'écran
  $$("form[data-netlify]").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var id = form.getAttribute("name");
      var btn = $("button[type=submit]", form);
      var err = form.parentNode.querySelector('[data-error="' + id + '"]');
      if (btn) { btn.disabled = true; btn.dataset.label = btn.textContent; btn.textContent = "..."; }
      if (err) err.classList.add("hidden");
      var data = new URLSearchParams(new FormData(form)).toString();
      fetch("/", { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: data })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          form.classList.add("hidden");
          var ok = form.parentNode.querySelector('[data-success="' + id + '"]');
          if (ok) ok.classList.remove("hidden");
          if (window.dataLayer) window.dataLayer.push({ event: "form_submit", form: id });
        })
        .catch(function () {
          if (err) err.classList.remove("hidden");
          if (btn) { btn.disabled = false; btn.textContent = btn.dataset.label; }
        });
    });
  });
})();
