(function () {
  "use strict";
  var GTM_ID = "GTM-T45DPCWZ";
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
  function chargerGTM() {
    if (charge) return;
    charge = true;
    gtag("consent", "default", { ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied", analytics_storage: "granted" });
    window.dataLayer.push({ "gtm.start": new Date().getTime(), event: "gtm.js" });
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtm.js?id=" + GTM_ID;
    document.head.appendChild(s);
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
      chargerGTM();
    } else {
      supprimerCookiesGA();
      if (charge) location.reload();
    }
  }

  document.querySelectorAll("[data-cookie-accept]").forEach(function (b) { b.addEventListener("click", function () { choisir("accepte"); }); });
  document.querySelectorAll("[data-cookie-refuse]").forEach(function (b) { b.addEventListener("click", function () { choisir("refuse"); }); });
  document.querySelectorAll("[data-cookie-settings]").forEach(function (b) { b.addEventListener("click", montrer); });

  var choix = lire();
  if (choix === "accepte") chargerGTM();
  else if (choix !== "refuse") montrer();
})();
