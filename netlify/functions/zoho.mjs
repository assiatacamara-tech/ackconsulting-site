// Envoi d'une demande du site vers Zoho CRM (formulaire web « Leads-ack-consulting-formulaire site »).
// Utilisé par submission-created.mjs (à chaque envoi) et zoho-retry.mjs (nouvel essai toutes les 15 minutes).

const ZOHO_URL = "https://crm.zoho.eu/crm/WebToLeadForm";
const ZOHO_KEYS = {
  xnQsjsdp: "b4911a6114a03db70d63f91e89332121c1b701c4cbe37be3b33868a106c53f15",
  xmIwtLD: "eea7fbef2559487b8eb251b561aeb518285424981f6297a62258cc569dd2c243ebeb37a18c8fe92c3f204860f54c3527",
  actionType: "TGVhZHM=",
  returnURL: "https://www.ackconsulting.fr/",
};

const FORM_LABELS = {
  contact: "Formulaire de contact",
  newsletter: "Inscription à la newsletter",
  diagnostic: "Demande de diagnostic gratuit",
  "diagnostic-pdf": "Téléchargement du Diagnostic Express (PDF)",
  "qualification-formation": "Demande de qualification formation",
  "sales-squad": "ACK Sales Squad — projet de force commerciale",
  partenaire: "Candidature partenaire",
};

// « Comment nous avez-vous connu ? » → choix existants du champ Zoho « Canal d'acquisition »
const CANAL = {
  LinkedIn: "LinkedIn",
  "Recherche Google": "Recherche google",
  "Recommandation ou bouche-à-oreille": "Recommandation / Bouche-à-oreille",
  "Événement ou salon": "Réseau professionnel / Événement",
  Malt: "Malt",
  "ACK Sales Match": "ACK Sales Match",
  IA: "IA",
  Autre: "Autre",
};

const FIELD_LABELS = {
  name: "Nom", prenom: "Prénom", nom: "Nom", email: "E-mail", "email-lm": "E-mail", phone: "Téléphone", tel: "Téléphone",
  company: "Société", entreprise: "Société", website: "Site web", sector: "Secteur", services: "Services proposés",
  target: "Cible", message: "Message", enjeu: "Enjeu", profil: "Profil", taille: "Taille de l'équipe commerciale",
  objectif: "Objectif", delai: "Délai", commerciaux: "Nombre de commerciaux envisagés", how_heard: "Comment nous avez-vous connu ?",
  page: "Page du site",
};

export function toZohoFields(formName, data) {
  const d = data || {};
  const email = (d.email || d["email-lm"] || "").trim();
  let first = (d.prenom || "").trim();
  let last = (d.nom || "").trim();
  if (!last && d.name) {
    const parts = d.name.trim().split(/\s+/);
    if (parts.length > 1) { first = parts.shift(); last = parts.join(" "); } else { last = parts[0]; }
  }
  if (!last) last = email ? email.split("@")[0] : "Inconnu";
  const company = (d.company || d.entreprise || "").trim() || "Non renseignée";

  const lines = [`[SITE WEB] ${FORM_LABELS[formName] || formName}`];
  for (const [k, v] of Object.entries(d)) {
    if (!v || ["form-name", "bot-field", "ip", "user_agent", "referrer"].includes(k)) continue;
    lines.push(`${FIELD_LABELS[k] || k} : ${Array.isArray(v) ? v.join(", ") : v}`);
  }

  const fields = {
    ...ZOHO_KEYS,
    Company: company,
    "First Name": first,
    "Last Name": last,
    Email: email,
    Phone: (d.phone || d.tel || "").trim(),
    Description: lines.join("\n"),
  };
  fields.LEADCF3 = CANAL[d.how_heard] || "Site web — formulaire de contact";
  if (formName === "qualification-formation") fields.LEADCF5 = "Me former ou former un membre de mon équipe";
  return fields;
}

export async function sendToZoho(formName, data) {
  const body = new URLSearchParams(toZohoFields(formName, data));
  const res = await fetch(ZOHO_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body,
    redirect: "manual",
  });
  // Zoho répond par une redirection vers returnURL quand la fiche est créée
  const ok = res.status >= 200 && res.status < 400;
  if (!ok) throw new Error(`Zoho a répondu ${res.status}`);
  return res.status;
}
