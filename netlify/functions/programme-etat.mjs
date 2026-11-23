// Indique seulement si l'envoi des programmes est configuré (aucune valeur n'est affichée).
export default async () => {
  const url = process.env.PROGRAMME_MAIL_URL || "";
  const jeton = process.env.PROGRAMME_MAIL_TOKEN || "";
  return Response.json({
    adresse_renseignee: url.length > 0,
    adresse_script_google: url.startsWith("https://script.google.com/"),
    jeton_renseigne: jeton.length > 0,
    contexte: process.env.CONTEXT || "inconnu",
  });
};
