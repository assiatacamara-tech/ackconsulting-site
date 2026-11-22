# Registre des décisions — site ackconsulting.fr

Chaque décision validée par Assiata est notée ici. Les agents relisent ce fichier avant de travailler.

## Migration Sintra → Netlify (novembre 2026)
- Le site est recopié à l'identique depuis Sintra (textes, adresses, images) : on recopie, on ne réécrit pas.
- Les adresses des pages ne changent pas, pour ne rien perdre sur Google.
- Le site Sintra reste en ligne tant que la nouvelle version n'est pas validée et que les DNS ne sont pas basculés.
- Communications du site : au « nous » (préférence d'Assiata). Les textes actuels au « je » sont recopiés tels quels pour l'instant ; leur passage au « nous » sera une décision séparée.

## Corrections faites pendant la migration
- Menu : « A propos » devient « À propos » (accent).
- Les adresses e-mail des pages légales et des fiches formation, masquées par l'ancien hébergeur, sont écrites en clair (liens mailto).
- Le modèle Excel de plan d'action commercial (articles de blog) est hébergé sur le site, et non plus chez Sintra.
- L'image de partage sur les réseaux sociaux est hébergée sur www.ackconsulting.fr.
- Les réponses des FAQ sont présentes dans le code de la page (avant : chargées au clic seulement), ce qui permet à Google de les lire.
- Fenêtre « Nous contacter » : formulaire en version claire (titres et texte saisi en foncé sur fond blanc), comme sur Sintra. Une vérification bloque désormais tout texte blanc dans cette fenêtre.
- Formulaire web Zoho mis à jour par Assiata le 22/11/2026 (champ Description ajouté, Canal d'acquisition et Statut masqués aux visiteurs) : nouveau code installé sur /contact et dans l'envoi automatique.
- RGPD (demandé par Assiata le 22/11/2026) : chaque formulaire du site comporte une case de consentement obligatoire, non pré-cochée, avec lien vers la politique de confidentialité. Newsletter : consentement spécifique à la newsletter avec mention de la désinscription. Le consentement et la date de réception sont notés dans la Description Zoho. Une vérification bloque toute mise en ligne d'un formulaire sans consentement.
- Les demandes indiquent la page réelle d'où elles sont envoyées (y compris depuis la fenêtre « Nous contacter »).
- Blocs modifiés puis reverrouillés avec l'accord d'Assiata (22/11/2026) : formulaire de contact, pieds de page (case de consentement), script du site (page réelle).
- Formulaires (décidé le 22/11/2026) : chaque demande est enregistrée par Netlify, puis envoyée dans Zoho (Prospects) via le formulaire web « Leads-ack-consulting-formulaire site ». En cas d'échec, nouvel essai automatique toutes les 15 minutes. Le détail complet de la demande est dans le champ Description.
- Canal d'acquisition : chaque réponse à « Comment nous avez-vous connu ? » correspond à un choix Zoho (Recherche google, IA, Malt ajoutés par Assiata le 22/11/2026) ; sans réponse : « Site web — formulaire de contact ».
- Candidatures formateurs : bouton vers le formulaire Tally (inchangé). Candidatures partenaires (/devenir-partenaire) : Zoho Prospects, marquées « Candidature partenaire ».
- Pages légales (validées par Assiata le 22/11/2026) : hébergeur Netlify et nom de domaine IONOS dans les mentions légales ; base légale, destinataires et sous-traitants, droits complétés (limitation, retrait du consentement, CNIL) dans la politique de confidentialité ; mention Google Analytics conservée (installation prévue, décision d'Assiata) ; date de mise à jour affichée.
- Mesure d'audience (22/11/2026) : Google Analytics 4 G-ZB9N47BPGX installé directement (sans Tag Manager, Assiata ayant deux conteneurs GTM-T45DPCWZ et GTM-K83JHSR6 non configurés), chargé uniquement après « Tout accepter » ; chaque demande envoyée est comptée comme « generate_lead » (rien n'est chargé avant ni après refus). Bandeau avec « Tout refuser » et « Tout accepter » de même poids, choix redemandé tous les 6 mois, modifiable depuis la politique de confidentialité. En attente de validation du bandeau par Assiata.

- Page d'accueil (proposition du 22/11/2026, en prévisualisation, à valider) : accroche A « Vos ventes dépendent encore de vous ? Nous les structurons et les pilotons à votre place, à temps partagé. » ; H1, titre et description Google inchangés ; cas concrets validés par Assiata ; vidéo chargée au clic juste après le haut de page ; FAQ dirigeants avec données structurées ; couleurs de la charte (#055388, #1E8482, #48D4D1, #E6F9F8) ; section fondatrice mise à jour (elle n'est plus directrice commerciale salariée) ; photos allégées (1,2 Mo → 20-40 Ko).

## Points en attente de décision
- Formulaire « Télécharger le PDF » (/diagnostic) : chez Sintra, le Diagnostic Express était envoyé automatiquement par e-mail. À recréer (Zoho).
