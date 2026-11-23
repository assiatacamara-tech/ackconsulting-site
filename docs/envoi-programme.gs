// Envoi des programmes de formation demandés sur ackconsulting.fr
// À coller dans un projet Google Apps Script, puis Déployer > Application web
// (Exécuter en tant que : moi · Accès : tout le monde).

const JETON = "À_REMPLACER_PAR_LE_JETON";

function doPost(e) {
  let d;
  try { d = JSON.parse(e.postData.contents); } catch (err) { return reponse("erreur : données illisibles"); }
  if (d.token !== JETON) return reponse("erreur : accès refusé");
  const email = String(d.email || "").trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return reponse("erreur : e-mail invalide");
  const lien = String(d.lien || "");
  if (lien.indexOf("https://drive.google.com/") !== 0) return reponse("erreur : lien invalide");
  const titre = String(d.titre || "").slice(0, 200);
  const prenom = String(d.prenom || "").slice(0, 80);
  const bonjour = prenom ? "Bonjour " + prenom + "," : "Bonjour,";
  const devis = "https://www.ackconsulting.fr/demande-de-devis";
  const rdv = "https://calendly.com/assiata-camara-ackconsulting/30min";
  const sujet = "Votre programme de formation : " + titre;
  const texte = bonjour + "\n\nMerci pour votre intérêt pour nos formations. Voici le programme détaillé de la formation « " + titre + " » :\n" + lien +
    "\n\nVous y trouverez les objectifs, le contenu module par module, la durée, le tarif et les modalités d'évaluation." +
    "\n\nVous souhaitez l'adapter à votre équipe ou recevoir un devis ? Répondez simplement à cet e-mail, demandez votre devis en ligne (" + devis + ") ou réservez 30 minutes pour en parler (" + rdv + ")." +
    "\n\nBelle journée,\n\nAssiata Camara Konaté\nFondatrice, ACK Consulting\n07 80 71 20 36 · ackconsulting.fr\nOrganisme de formation certifié Qualiopi";
  const html = '<div style="font-family:Arial,sans-serif;font-size:15px;line-height:1.5;color:#1a1a1a;max-width:600px">' +
    '<p>' + esc(bonjour) + '</p><p>Merci pour votre intérêt pour nos formations. Voici le programme détaillé de la formation <b>« ' + esc(titre) + ' »</b> :</p>' +
    '<p style="margin:24px 0"><a href="' + esc(lien) + '" style="background:#1e8482;color:#ffffff;padding:12px 22px;border-radius:10px;text-decoration:none;font-weight:bold">Télécharger le programme (PDF)</a></p>' +
    '<p>Vous y trouverez les objectifs, le contenu module par module, la durée, le tarif et les modalités d\'évaluation.</p>' +
    '<p>Vous souhaitez l\'adapter à votre équipe ou recevoir un devis ? Répondez simplement à cet e-mail, <a href="' + devis + '" style="color:#055388">demandez votre devis en ligne</a> ou <a href="' + rdv + '" style="color:#055388">réservez 30 minutes pour en parler</a>.</p>' +
    '<p>Belle journée,</p><p style="margin-top:24px"><b style="color:#055388">Assiata Camara Konaté</b><br>Fondatrice, ACK Consulting<br>07 80 71 20 36 · <a href="https://www.ackconsulting.fr" style="color:#055388">ackconsulting.fr</a><br><span style="color:#1e8482">Organisme de formation certifié Qualiopi</span></p></div>';
  GmailApp.sendEmail(email, sujet, texte, { htmlBody: html, name: "Assiata Camara Konaté · ACK Consulting" });
  return reponse("ok");
}

function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
function reponse(t) { return ContentService.createTextOutput(t); }
