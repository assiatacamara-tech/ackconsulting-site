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
- En-tête et pieds de page : boutons « Échanger sur mon besoin commercial », Traitement de leads après ACK Sales Squad ; validés et reverrouillés avec l'accord d'Assiata (22/11/2026). Mise en ligne du lot 4 validée par Assiata.
- 22/11/2026 : accueil, titre principal (H1) remplacé par « Direction commerciale externalisée, conseil et formation commerciale B2B » (choix d'Assiata ; recherches France : formation commerciale 900/mois, directeur commercial externalisé 200, direction commerciale externalisée 50). Titre Google et description inchangés.
- 22/11/2026 : titre Google de l'accueil « Directeur commercial externalisé et formation | ACK Consulting » ; page /directrice-commerciale-externalisee : H1 et libellé du menu passés à « Direction commerciale externalisée » (choix d'Assiata, titre plus général).
- 22/11/2026 : description Google de l'accueil : « Direction commerciale externalisée pour PME : stratégie B2B, management des équipes, structuration et pilotage des ventes. Conseil et formation, certifié Qualiopi. » (choix d'Assiata).

## 23/11/2026 — Lot 5 : alignement du site sur les programmes de formation (demande d'Assiata)
- Référence : les programmes PDF du dossier Drive « Programmes – envoi automatique » (contenus Teachizy) ; le site s'aligne sur eux.
- « Développer la performance commerciale » devient « Prospection commerciale B2B ». La page /formations/performance-commerciale est supprimée et redirigée (301) vers /formations/prospection-commerciale ; liens, menus de pied de page (reverrouillés avec l'accord d'Assiata), catalogue et données structurées mis à jour. Modules de la page Prospection alignés sur Teachizy : structurer sa prospection B2B (5 h), techniques de vente et argumentation (6 h), posture de conseil (5 h), suivi et pilotage (5 h).
- Prix : ACK Consulting est en franchise de TVA (art. 293 B du CGI) ; « HT » retiré de tous les prix ACK, mention « TVA non applicable » à côté des tarifs ; CGV article 3 ajusté. Les prix cités d'autres organismes dans le blog restent HT.
- Organisation commerciale orientée performance : alignée sur le programme (60 h = environ 54 h d'e-learning + 6 séances de mentorat d'1 h, 6 modules), au lieu de 8 modules et 12 séances de coaching.
- Prise de parole en public et Gestion des conflits : section « Aussi en présentiel » (7 h, intra, jusqu'à 10 participants, dès 1 200 € la journée, frais de déplacement en sus).
- FAQ : liste des 8 formations, formats et durées à jour (formules Déclic / Accélération / Impact retirées). Accessibilité : numéro 07 80 71 20 36.
- Page Formations : section « Formations sur mesure » (réseau d'experts, 9 thématiques, démarche en 4 étapes, dès 1 200 € la journée) et « Ateliers courts » (3 h 30, dès 650 €), recopiées du catalogue ; lien depuis le haut de page. Lot 5 et prix du présentiel validés par Assiata le 23/11/2026 (« publie lot 5 »).

## 23/11/2026 — Lot 6 : pages formation aux couleurs de la charte, devis et programmes (demande d'Assiata)
- Journées Prise de parole et Gestion des conflits : toujours « présentiel ou classe virtuelle » (7 h, intra, jusqu'à 10 participants, dès 1 200 € la journée, frais de déplacement en sus en présentiel) ; deux cartes dédiées sur la page Formations ; PDF du Drive mis à jour.
- Page Formations : section sur mesure remontée juste après le haut de page, sur fond dégradé de la charte ; catalogue sur fond bleu clair, cartes avec bandeau coloré.
- Chaque page formation : barre colorée après le haut de page (Télécharger le programme, Demander un devis, Prendre rendez-vous).
- « Demander un devis » ouvre le formulaire /demande-de-devis (formation pré-remplie) ; la prise de rendez-vous reste proposée à côté.
- « Télécharger le programme » ouvre /telecharger-programme : le programme part uniquement par e-mail à l'adresse saisie (script Google « ACK – Envoi des programmes de formation » sur le compte d'Assiata, appelé par netlify/functions/programme-mail.mjs ; adresse et jeton dans les variables Netlify PROGRAMME_MAIL_URL et PROGRAMME_MAIL_TOKEN ; nouvel essai toutes les 15 min pendant 24 h). Aucun lien Drive sur le site (vérification ajoutée). Page non indexée par Google.
- Les deux formulaires arrivent dans Zoho (Prospects), comme les autres formulaires du site.
- 23/11/2026 : correction (demande d'Assiata, message en français) : Netlify retire « data-netlify » des formulaires à la mise en ligne, le script du site ne les interceptait donc plus et Netlify affichait « Thank you! » en anglais. site.js vise désormais « data-form » (reverrouillé avec son accord) ; vérification ajoutée. Les scripts et styles ne sont plus gardés 7 jours en cache par les navigateurs (images et polices seulement), pour que les corrections arrivent tout de suite. Lot 6 validé par Assiata le 23/11/2026 (« publie lot 6 »).
- 23/11/2026 : catalogue Formations (export d'Assiata, images recompressées à 150 dpi, liens conservés) en ligne à l'adresse courte /catalogue-formations (fichier /assets/docs/catalogue-formations.pdf).
- 23/11/2026 : ancien lien Sintra /documents/ACK_Catalogue_Formations.pdf redirigé (301) vers /catalogue-formations. À faire à réception des PDF : /documents/ACK_Catalogue_Prestations.pdf → /catalogue-prestations et /documents/ACK_Presentation_Generale_Slides.pdf → /presentation.
- 23/11/2026 : catalogue Prestations et Présentation générale (exports d'Assiata, versions de novembre au « nous ») en ligne à /catalogue-prestations et /presentation ; anciens liens /documents/ACK_Catalogue_Prestations.pdf et /documents/ACK_Presentation_Generale_Slides.pdf redirigés (301).
- 23/11/2026 : catalogue formations demandable sur le site (bouton sur /formations → /telecharger-programme?formation=catalogue), envoyé par e-mail comme les programmes (lien /catalogue-formations ; script Google mis à jour).

## Lot 7 — Diagnostic commercial sur la page d'accueil (23/11/2026)
- Bloc « Votre machine commerciale est-elle prête à grandir ? » ajouté en bas de la page d'accueil, avant l'appel final, vers le formulaire Tally LDZ0pj (?source=site-accueil).
- Le résultat s'affiche à l'écran à la fin du questionnaire ; pas d'envoi par e-mail (choix d'Assiata : l'e-mail automatique Tally demande Tally Pro).
