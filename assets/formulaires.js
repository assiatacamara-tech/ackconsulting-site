(function () {
  var P = window.ACK_PROGRAMMES || {};
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
    var lien = document.querySelector("[data-prog-lien]");
    var titre = document.querySelector("[data-prog-titre]");
    var dv = document.querySelector("[data-prog-devis]");
    if (k && P[k][1]) {
      if (lien) lien.href = P[k][1];
      if (titre) titre.textContent = P[k][0];
      if (dv) dv.href = "/demande-de-devis?formation=" + k;
    }
  }
  if (prog && prog[1]) {
    choix.value = prog[0];
    var h = document.querySelector("[data-prog-hero]");
    if (h) h.textContent = prog[0] + " : objectifs, contenu, durée, tarif et modalités d'évaluation.";
  }
  choix.addEventListener("change", majProgramme);
  majProgramme();
})();
