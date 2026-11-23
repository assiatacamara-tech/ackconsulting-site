// Toutes les 15 minutes : renvoie à Zoho les demandes qui n'ont pas pu être transmises.
import { getStore } from "@netlify/blobs";
import { sendToZoho } from "./zoho.mjs";
import { envoyerProgramme } from "./programme-mail.mjs";

export default async () => {
  const store = getStore("zoho-en-attente");
  const { blobs } = await store.list();
  for (const { key } of blobs) {
    const item = await store.get(key, { type: "json" });
    if (!item) continue;
    try {
      await sendToZoho(item.formName, item.data);
      await store.delete(key);
      console.log(`Demande ${key} transmise à Zoho après ${item.essais} essai(s)`);
    } catch (err) {
      item.essais += 1;
      await store.setJSON(key, item);
      console.error(`Demande ${key} toujours en attente (${item.essais} essais) : ${err.message}`);
    }
  }
  // Programmes de formation non envoyés par e-mail : nouvel essai (abandon après 24 h)
  const prog = getStore("programme-en-attente");
  const liste = (await prog.list()).blobs;
  for (const { key } of liste) {
    const item = await prog.get(key, { type: "json" });
    if (!item) continue;
    try {
      await envoyerProgramme(item.data);
      await prog.delete(key);
      console.log(`Programme ${key} envoyé après ${item.essais} essai(s)`);
    } catch (err) {
      item.essais += 1;
      if (item.essais > 96) { await prog.delete(key); console.error(`Programme ${key} abandonné : ${err.message}`); continue; }
      await prog.setJSON(key, item);
      console.error(`Programme ${key} toujours en attente (${item.essais} essais) : ${err.message}`);
    }
  }
};

export const config = { schedule: "*/15 * * * *" };
