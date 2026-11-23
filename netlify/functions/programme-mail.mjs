// Envoi du programme de formation par e-mail (formulaire « programme »).
// Le lien du PDF n'est jamais affiché sur le site : il part uniquement à l'adresse saisie.
// L'e-mail est envoyé depuis la boîte Google d'ACK Consulting par un script Google Apps Script (voir docs/envoi-programme.gs).

// Adresse du script et jeton : variables d'environnement Netlify PROGRAMME_MAIL_URL et PROGRAMME_MAIL_TOKEN.
const MAIL_URL = process.env.PROGRAMME_MAIL_URL || "";
const MAIL_TOKEN = process.env.PROGRAMME_MAIL_TOKEN || "";

export const PROGRAMMES = {
  "Catalogue des formations ACK Consulting": "https://www.ackconsulting.fr/catalogue-formations",
  "Prospection commerciale B2B": "https://drive.google.com/file/d/1dD046PBvZosJxOlDj5FbGZ-Tp9xi6awP/view",
  "Closer efficacement une demande entrante": "https://drive.google.com/file/d/1OY2M5INOeTxkpYSc_HPgQydtFwhp76cY/view",
  "IA & Performance Commerciale": "https://drive.google.com/file/d/1QfgVzZ2sdmt8_jFK3dsfILM5h7wRskj3/view",
  "Manager une équipe commerciale sédentaire": "https://drive.google.com/file/d/1gr5u8ksdITX6dYjyvH3DETl84JgvDMRj/view",
  "Structurer et piloter une organisation commerciale orientée performance": "https://drive.google.com/file/d/1sWfL5eVq2_h6uggOHifYKRoEtrghJbjb/view",
  "Prise de parole en public (e-learning mentoré)": "https://drive.google.com/file/d/1E2i1WQtCzWyxpMmVjzx2sIqleDMeUD0F/view",
  "Prise de parole en public : la journée (présentiel ou classe virtuelle)": "https://drive.google.com/file/d/1k5KS0SRk5QPxD02UfcORvxTM91eC1MAZ/view",
  "Gestion des conflits (e-learning mentoré)": "https://drive.google.com/file/d/1Cd2x1kNNsm3uT5XrMBmSPMsfUBlSRfNe/view",
  "Gestion des conflits : la journée (présentiel ou classe virtuelle)": "https://drive.google.com/file/d/1irBMOWB-YRO9CbQM2It0FoaJzcf7W4Dd/view",
  "Gestion du stress": "https://drive.google.com/file/d/1s4yPy5f-tMxz25A12eL_otC2drCS_4mv/view"
};

export async function envoyerProgramme(data) {
  const d = data || {};
  const un = (v) => String(Array.isArray(v) ? v[0] || "" : v || "").trim();
  const titre = PROGRAMMES[un(d.programme_choisi)] ? un(d.programme_choisi) : un(d.formation);
  const lien = PROGRAMMES[titre];
  const email = un(d.email);
  if (!lien) throw new Error(`programme inconnu : ${titre}`);
  if (!email) throw new Error("e-mail manquant");
  if (!MAIL_URL || !MAIL_TOKEN) throw new Error("envoi par e-mail non configuré");
  const res = await fetch(MAIL_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token: MAIL_TOKEN, email, prenom: un(d.prenom), titre, lien }),
  });
  const txt = await res.text();
  if (!res.ok || !txt.includes("ok")) throw new Error(`envoi refusé : ${res.status} ${txt.slice(0, 120)}`);
  return true;
}
