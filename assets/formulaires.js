(function () {
  var P = window.ACK_PROGRAMMES || {};
  var params = new URLSearchParams(window.location.search);
  if (params.get("envoye") === "1") {
    var f = document.querySelector('form[action*="envoye=1"]');
    if (f) {
      f.classList.add("hidden");
      var ok = f.parentNode.querySelector('[data-success="' + f.getAttribute("name") + '"]');
      if (ok) ok.classList.remove("hidden");
    }
    var t = document.querySelector("[data-prog-titre]");
    if (t) t.textContent = "demandé";
    return;
  }
  var cle = new URLSearchParams(window.location.search).get("formation") || "";
  var prog = P[cle];
  var parNom = {};
  Object.keys(P).forEach(function (k) { parNom[P[k][0]] = k; });

  var devis = document.querySelector('select[name="formation"]');
  if (devis && prog) devis.value = prog[0];

  var choix = document.querySelector('select[name="programme_choisi"]');
  if (!choix) return;
  var cache = document.querySelector('input[name="formation"]');
  function majProgramme() {
    var k = parNom[choix.value];
    if (cache) cache.value = choix.value;
    var titre = document.querySelector("[data-prog-titre]");
    var dv = document.querySelector("[data-prog-devis]");
    if (k) {
      if (titre) titre.textContent = P[k][0];
      if (dv) dv.href = "/demande-de-devis?formation=" + k;
    }
  }
  if (prog) {
    choix.value = prog[0];
    var h = document.querySelector("[data-prog-hero]");
    if (h) h.textContent = prog[0] + " : objectifs, contenu, durée, tarif et modalités d'évaluation, envoyé à votre adresse e-mail.";
  }
  choix.addEventListener("change", majProgramme);
  majProgramme();
})();
