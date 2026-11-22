(function () {
  "use strict";
  // Clics sur « Réserver un appel » (Calendly) comptés comme conversion, uniquement si la mesure d'audience est acceptée
  function accepte() {
    try {
      var v = JSON.parse(localStorage.getItem("ack_consentement_cookies"));
      return v && v.choix === "accepte";
    } catch (e) { return false; }
  }
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href*="calendly.com"]');
    if (!a || !accepte() || typeof window.gtag !== "function") return;
    window.gtag("event", "reservation_appel", { page_path: location.pathname, link_text: (a.textContent || "").trim().slice(0, 60) });
  });
})();
