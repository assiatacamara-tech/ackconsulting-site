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
- Mesure d'audience (22/11/2026) : Google Analytics 4 G-ZB9N47BPGX installé directement (sans Tag Manager, Assiata ayant deux conteneurs GTM-T45DPCWZ et GTM-K83JHSR6 non configurés), chargé uniquement après « Tout accepter » ; chaque demande envoyée est comptée comme « generate_lead » (rien n'est chargé avant ni après refus). Bandeau avec « Tout refuser » et « Tout accepter » de même poids, choix redemandé tous les 6 mois, modifiable depuis la politique de confidentialité. Validé par Assiata le 22/11/2026.

- Page d'accueil (validée par Assiata le 22/11/2026, photo affichée aussi sur mobile) : accroche A « Vos ventes dépendent encore de vous ? Nous les structurons et les pilotons à votre place, à temps partagé. » ; H1, titre et description Google inchangés ; cas concrets validés par Assiata ; vidéo chargée au clic juste après le haut de page ; FAQ dirigeants avec données structurées ; couleurs de la charte (#055388, #1E8482, #48D4D1, #E6F9F8) ; section fondatrice mise à jour (elle n'est plus directrice commerciale salariée) ; photos allégées (1,2 Mo → 20-40 Ko).

## Points en attente de décision
- Formulaire « Télécharger le PDF » (/diagnostic) : chez Sintra, le Diagnostic Express était envoyé automatiquement par e-mail. À recréer (Zoho).

## 22/11/2026 — Bascule DNS vers Netlify
- IONOS : renvoi IONOS de ackconsulting.fr désactivé (A 217.160.0.166, AAAA, TXT _dep_ws_mutex) ; A @ = 75.2.60.5 ; CNAME www = ackconsulting.netlify.app (avant : custom-sites.sintra.ai). MX, SPF, DKIM, DMARC, formation (Teachizy) inchangés.
- Netlify : domaine ajouté (ackconsulting.fr + www). Domaine principal à passer sur www dès que le certificat HTTPS est émis (les balises canonical et le sitemap utilisent www).
- Reste chez IONOS : TXT _cf-custom-hostname.www (ancien Sintra), à supprimer après validation.
- 22/11/2026 : certificat HTTPS émis, www passé en domaine principal Netlify. Offre Netlify Personal souscrite par Assiata (9 $/mois) ; badge « Powered by Netlify » désactivé. Page 404 ajoutée (noindex). Sitemap https://www.ackconsulting.fr/sitemap.xml soumis dans Search Console (l'ancienne entrée « sitemap.xml. » avec un point final était en erreur).
- 22/11/2026 : harmonisation demandée par Assiata. (1) Toutes les couleurs Sintra (verts, marine, cuivre, or) passées à la charte : #055388, #1E8482, #48D4D1, #E6F9F8, #E6F4FD, #F6F6F8, #1A1A1A. (2) Textes ACK au « nous » sur toutes les pages hors blog (le blog garde la voix d'Assiata) ; le parcours de la fondatrice est à la 3e personne. Les boutons et cases à la voix du visiteur (« Réserver mon appel », « J'accepte… ») restent inchangés. La mention « Dernière mise à jour » reste réservée aux pages légales.
- 22/11/2026 : ACK Sales Match quitte Lovable. Code récupéré via GitHub (dépôt commercial-pro-match, branche netlify-migration), site pré-généré sur Netlify (projet acksalesmatch), formulaires → Zoho par API directe (Self Client, jeton gardé dans Netlify Blobs), sans base de données. Chiffre 120–170 % remplacé par 130 % (objectifs de CA de la fondatrice). DNS OVH : A @ et A www → 75.2.60.5 ; MX/SPF OVH inchangés ; TXT lovable_verify à supprimer après résiliation.

## 22/11/2026 — Lot 1 d'optimisation (plan validé par Assiata, décisions 1 à 8)
- Images : 5 PNG de 1,2 à 1,4 Mo convertis en WebP (30 à 77 Ko) ; version JPEG conservée pour les images de partage (réseaux sociaux) ; 1 image inutilisée supprimée. Vérification : aucune image de plus de 400 Ko.
- Blog : données structurées « Article » (auteur, date de publication) ajoutées aux 10 articles qui n'en avaient pas.
- Correction d'une erreur héritée de Sintra : sur 7 articles, les accents des titres s'affichaient en code (« réussi »). Corrigés ; la comparaison avec le site Sintra lit désormais ces accents décodés. Vérification ajoutée.
- Titres Google de plus de 65 caractères raccourcis (11 pages) et descriptions de plus de 175 caractères raccourcies (10 pages), sans changer les informations (prix, durées, Qualiopi, OPCO). Vérifications ajoutées.
- /mise-en-relation-commerciaux retirée de Google (noindex) et du plan du site : la recherche « commercial freelance » revient à acksalesmatch.fr (décision 7). Le lien du menu reste.
- Clics vers Calendly (« Réserver un appel ») comptés dans Google Analytics (événement « reservation_appel »), uniquement après accord du visiteur (nouveau script assets/suivi.js, blocs verrouillés inchangés).
- Zéro Lead Perdu : « La structuration commerciale B2B » ajouté sous « Zéro Lead Perdu » dans le titre principal (H1), validé par Assiata le 22/11/2026. Lot 1 validé par Assiata le 22/11/2026.

## 22/11/2026 — Lot 4 : positionnement direction commerciale opérationnelle (brief correctif, décisions d'Assiata)
- Voix : « nous » partout (hors blog). Accueil : titre principal (H1) remplacé par « Conseil et formation commerciale B2B pour un véritable pilotage de vos ventes » (choix d'Assiata ; recherches : formation commerciale 900/mois, conseil commercial 200, pilotage commercial 150) ; accroche validée conservée ; le titre Google garde « Formation & conseil commercial B2B ».
- Pas de mot « recrutement » pour ACK : « constitution et intégration de l'équipe », « embaucher » à la place de « recruter ».
- Management et pilotage commercial : section de la page Directrice commerciale externalisée (ancre #management), pas une page séparée.
- Chiffres : « 0 → 2 M€ » et « 0 → 1 M€ » sont deux expériences différentes, précisées « dans une entreprise précédente » ; 130 % précisé « en entreprise ».
- Offres de second plan : offre spéciale organismes de formation, ACK Sales Squad, traitement de leads (fin du menu Prestations, ligne sous les offres de l'accueil).
- Boutons de prise de rendez-vous unifiés : « Échanger sur mon besoin commercial » (pages formations : « Échanger sur mon besoin de formation ») ; « Demander un devis » conservé pour les formations et les propositions. En-tête et pieds de page (blocs verrouillés) : à aligner après validation.
- Accueil : section « Ce que nous prenons en charge » (Structurer, Construire, Manager, Piloter) et méthode en 5 étapes. À propos : activité actuelle distinguée de l'expérience passée.
- Qualiopi (demande d'Assiata, nouvelle exigence) : certificat n° CERT_S1225_1438 (CEVA Solution, 09/02/2026 → 08/02/2029) en ligne (/assets/docs/certificat-qualiopi-ack-consulting.pdf) ; chaque logo Qualiopi du site ouvre le certificat ; encadré « ACK Consulting est certifié Qualiopi » sur la page Formations et chaque fiche formation. Vérifications ajoutées.
