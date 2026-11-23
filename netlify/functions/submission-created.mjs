// Déclenchée automatiquement par Netlify à chaque demande validée (hors spam).
// La demande est déjà enregistrée dans Netlify ; on l'envoie à Zoho.
// En cas d'échec, elle est mise de côté et renvoyée toutes les 15 minutes (zoho-retry.mjs).
import { getStore } from "@netlify/blobs";
import { sendToZoho } from "./zoho.mjs";
import { envoyerProgramme } from "./programme-mail.mjs";

export default async (req) => {
  const { payload } = await req.json();
  const formName = payload.form_name;
  const data = { ...payload.data, page: payload.data?.page || "" };
  try {
    await sendToZoho(formName, data);
    console.log(`Demande ${payload.id} (${formName}) envoyée à Zoho`);
  } catch (err) {
    console.error(`Zoho indisponible pour ${payload.id} : ${err.message}. Nouvel essai dans 15 minutes.`);
    await getStore("zoho-en-attente").setJSON(payload.id, { formName, data, essais: 1, depuis: new Date().toISOString() });
  }
  if (formName === "programme") {
    try {
      await envoyerProgramme(data);
      console.log(`Programme envoyé par e-mail pour ${payload.id}`);
    } catch (err) {
      console.error(`Programme non envoyé pour ${payload.id} : ${err.message}. Nouvel essai dans 15 minutes.`);
      await getStore("programme-en-attente").setJSON(payload.id, { data, essais: 1, depuis: new Date().toISOString() });
    }
  }
  return new Response("ok");
};
