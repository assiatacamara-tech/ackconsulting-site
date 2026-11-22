(function () {
  "use strict";
  // Vidéo YouTube chargée seulement au clic : page plus rapide, aucun échange avec YouTube avant la lecture
  document.querySelectorAll("[data-video]").forEach(function (cadre) {
    var bouton = cadre.querySelector("button");
    if (!bouton) return;
    bouton.addEventListener("click", function () {
      var f = document.createElement("iframe");
      f.src = "https://www.youtube-nocookie.com/embed/" + cadre.getAttribute("data-video") + "?rel=0&autoplay=1";
      f.title = bouton.getAttribute("aria-label").replace("Lire la vidéo : ", "");
      f.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      f.referrerPolicy = "strict-origin-when-cross-origin";
      f.allowFullscreen = true;
      cadre.innerHTML = "";
      cadre.appendChild(f);
    });
  });
})();
