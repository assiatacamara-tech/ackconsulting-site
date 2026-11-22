# Site ackconsulting.fr — consignes pour les agents

Lire d'abord DECISIONS.md.

## Rôles
- Chef de projet : découpe le travail, présente le résultat fini à Assiata, une seule fois par lot.
- Développeur : le seul à modifier src/, assets/, build.py.
- Responsable SEO : ne modifie rien, liste les corrections à faire.
- Designer et relecteur : relisent chaque page avant qu'elle soit montrée à Assiata.

## Règles
- On recopie les contenus, on ne les réécrit pas, sauf décision notée dans DECISIONS.md.
- Textes ACK : au « nous », jamais au « je » (pour tout nouveau texte).
- Chaque élément validé par Assiata est verrouillé : `python3 checks.py --lock` uniquement après son accord.
- Avant chaque envoi : `python3 build.py && python3 checks.py` doit être au vert. À chaque erreur trouvée, ajouter une vérification dans checks.py.
- Aucune note interne ni commentaire dans le code publié.
- Noms de fichiers sans accent ni espace.

## Structure
- src/pages/ : une page = un fichier (en-tête JSON : titre, description, balises Google ; puis le contenu).
- src/partials/ : blocs communs (en-tête, pieds de page, formulaire de contact).
- assets/ : styles, scripts, images, documents.
- snapshot/ : copie de référence du site Sintra (ne pas modifier). migration/ : outils de recopie.
