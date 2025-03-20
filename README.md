# Résumés d'enquêtes de la Commission de la fonction publique du Québec

Ce projet permet de télécharger et d'organiser automatiquement les résumés des enquêtes publiées par la Commission de la fonction publique du Québec (CFP) à partir de leur site web officiel, disponible à l'adresse [cfp.gouv.qc.ca](https://www.cfp.gouv.qc.ca/fr/documentation/resumes-denquete.html).

## Structure du projet

Le projet est organisé comme suit :

- **`main.py`** : Script principal pour extraire automatiquement les résumés d'enquêtes depuis le site de la CFP.
- **`requirements.txt`** : Liste des dépendances Python nécessaires au fonctionnement du projet.
- **`resumes_rapports_enquete/`** : Répertoire où sont sauvegardés les résumés d'enquêtes, organisés par année dans des sous-dossiers (par exemple, `resumes_rapports_enquete/Enquêtes 2025/`).
- **`resumes_rapports_enquete.log`** : Fichier journal qui enregistre les opérations d'extraction (succès, erreurs, etc.).

## Prérequis

Pour exécuter ce projet, vous aurez besoin des bibliothèques Python suivantes :

- **`requests`** : Pour effectuer des requêtes HTTP vers le site web.
- **`beautifulsoup4`** : Pour analyser le contenu HTML des pages web.
- **`fake-useragent`** : Pour générer des en-têtes HTTP aléatoires simulant différents navigateurs.

Ces dépendances sont listées dans le fichier `requirements.txt`.

## Installation

Suivez ces étapes pour configurer le projet sur votre machine :

1. **Clonez le dépôt** :
   ```bash
   git clone [URL_du_dépôt]
   cd [nom_du_dépôt]
   ```

2. **Installez les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

## Utilisation

Le script `main.py` peut être exécuté de deux manières :

### 1. Télécharger tous les résumés disponibles
Pour scraper les résumés d'enquêtes de toutes les années disponibles sur le site :
```bash
python main.py
```

Le script effectuera les actions suivantes :
- Récupère la liste des années disponibles sur la page principale.
- Télécharge les résumés d'enquêtes pour chaque année, page par page (en gérant la pagination).
- Sauvegarde les données dans des fichiers JSON organisés par année dans le dossier `resumes_rapports_enquete/`.
- Enregistre les détails des opérations dans `resumes_rapports_enquete.log`.

### 2. Télécharger les résumés d'une année spécifique
Pour cibler une année particulière (par exemple, 2025) :
```bash
python main.py --year 2025
```

Cela limite le scraping aux enquêtes de l’année spécifiée et sauvegarde les résultats dans `resumes_rapports_enquete/Enquêtes 2025/Enquêtes 2025.json`.

## Structure des données

Les résumés d'enquêtes sont stockés au format JSON dans le répertoire `resumes_rapports_enquete/`. Voici comment les données sont organisées :

- Chaque sous-dossier correspond à une année (par exemple, `Enquêtes 2025/`).
- Dans chaque sous-dossier, un fichier JSON (par exemple, `Enquêtes 2025.json`) contient une liste d’objets représentant les enquêtes de cette année.
- Chaque objet d’enquête inclut au moins les champs suivants :
  - **`title`** : Le titre de l’enquête (extrait de la balise `<h2>`).
  - **`content`** : Le résumé ou contenu principal (extrait de la section `div.item-intro`).

Exemple de fichier JSON (`resumes_rapports_enquete/2025/2025.json`) :
```json
[
    {
        "title": "Enquête sur la gestion des ressources",
        "content": "Cette enquête a examiné les pratiques de gestion dans le secteur public."
    },
    {
        "title": "Enquête sur les conflits d'intérêts",
        "content": "Un cas de conflit d'intérêts a été identifié dans une nomination récente."
    }
]
```

Les données sont extraites directement du site officiel de la CFP.

## Licence

© 2025 - Tous droits réservés

## Disclaimer

Ce projet n’est pas affilié à la Commission de la fonction publique du Québec (CFP). Les données sont extraites de sources publiques à des fins d’information uniquement. L’exactitude et l’actualité des données ne sont pas garanties. Pour les informations les plus récentes, consultez le site officiel [cfp.gouv.qc.ca](https://www.cfp.gouv.qc.ca).

Les résumés d’enquêtes collectés sont des données publiques disponibles sur le site de la CFP. Ce projet vise uniquement à faciliter leur accès et leur organisation.

**Note légale** : Ce document ne constitue pas un avis juridique. Pour toute question légale, veuillez consulter un professionnel du droit qualifié.

## Contribution

Si vous souhaitez contribuer au projet, suivez ces étapes :

1. **Créez une branche** :
   ```bash
   git checkout -b feature/amelioration
   ```

2. **Effectuez vos modifications et commitez** :
   ```bash
   git commit -am 'Ajout d’une nouvelle fonctionnalité'
   ```

3. **Poussez vos changements** :
   ```bash
   git push origin feature/amelioration
   ```

4. **Créez une Pull Request** sur le dépôt principal.

---
