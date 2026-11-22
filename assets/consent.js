(function () {
  "use strict";
  var GA_ID = "G-ZB9N47BPGX";
  var KEY = "ack_consentement_cookies";
  var DUREE = 1000 * 60 * 60 * 24 * 182; // le choix est redemandé au bout de 6 mois

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  function lire() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY));
      if (v && v.date && Date.now() - v.date < DUREE) return v.choix;
    } catch (e) {}
    return null;
  }
  function enregistrer(choix) {
    try { localStorage.setItem(KEY, JSON.stringify({ choix: choix, date: Date.now() })); } catch (e) {}
  }

  var charge = false;
  function chargerGA() {
    if (charge) return;
    charge = true;
    gtag("consent", "default", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "granted" });
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
    gtag("js", new Date());
    gtag("config", GA_ID);
    // Chaque demande envoyée par un formulaire est comptée comme un prospect (« generate_lead »)
    document.querySelectorAll("[data-success]").forEach(function (ok) {
      new MutationObserver(function () {
        if (!ok.classList.contains("hidden")) gtag("event", "generate_lead", { form_name: ok.getAttribute("data-success"), page_path: location.pathname });
      }).observe(ok, { attributes: true, attributeFilter: ["class"] });
    });
  }

  function supprimerCookiesGA() {
    document.cookie.split(";").forEach(function (c) {
      var nom = c.split("=")[0].trim();
      if (/^(_ga|_gid|_gat)/.test(nom)) {
        ["", "; domain=" + location.hostname, "; domain=." + location.hostname.replace(/^www\./, "")].forEach(function (d) {
          document.cookie = nom + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/" + d;
        });
      }
    });
  }

  var banner = document.querySelector("[data-cookie-banner]");
  function montrer() { if (banner) banner.classList.remove("hidden"); }
  function cacher() { if (banner) banner.classList.add("hidden"); }

  function choisir(choix) {
    enregistrer(choix);
    cacher();
    if (choix === "accepte") {
      chargerGA();
    } else {
      supprimerCookiesGA();
      if (charge) location.reload();
    }
  }

  document.querySelectorAll("[data-cookie-accept]").forEach(function (b) { b.addEventListener("click", function () { choisir("accepte"); }); });
  document.querySelectorAll("[data-cookie-refuse]").forEach(function (b) { b.addEventListener("click", function () { choisir("refuse"); }); });
  document.querySelectorAll("[data-cookie-settings]").forEach(function (b) { b.addEventListener("click", montrer); });

  var choix = lire();
  if (choix === "accepte") chargerGA();
  else if (choix !== "refuse") montrer();
})();
