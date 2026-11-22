// Toutes les 15 minutes : renvoie à Zoho les demandes qui n'ont pas pu être transmises.
import { getStore } from "@netlify/blobs";
import { sendToZoho } from "./zoho.mjs";

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
};

export const config = { schedule: "*/15 * * * *" };
