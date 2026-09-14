# Coffre à Mdp

Un mini-logiciel de bureau (Python + tkinter) pour stocker ses mots de passe en sécurité, protégé par un seul mot de passe maître. Pas d'application web, pas de compte en ligne : tout reste chiffré localement, sur ta machine.

## Fonctionnalités

- Un seul mot de passe maître à retenir pour déverrouiller tout le coffre
- Stockage chiffré (PBKDF2 + Fernet/AES) des entrées : catégorie, nom, mot de passe
- Jusqu'à 5 champs personnalisés par entrée (ex : numéro de compte, code PIN, question secrète...)
- Génération de mots de passe forts et aléatoires
- Copie rapide du mot de passe dans le presse-papier
- Changement du mot de passe maître (re-chiffrement automatique du coffre)
- Gestion des erreurs (fichier corrompu, mauvais mot de passe) sans plantage brutal
- Interface graphique simple (tkinter/ttk)
- Disponible en exécutable Windows (`.exe`), sans besoin d'installer Python

## Stack technique

- **Python 3** — langage principal
- **tkinter / ttk** — interface graphique native
- **cryptography** — dérivation de clé (PBKDF2-SHA256) et chiffrement symétrique (Fernet/AES)
- **hashlib** — vérification du mot de passe maître par hachage (SHA-256 + sel)
- **secrets** — génération de sel et de mots de passe cryptographiquement sûrs
- **json** — structuration des données avant chiffrement
- **PyInstaller** — génération de l'exécutable `.exe`

## Comment ça marche (en bref)

1. **Premier lancement** : tu crées un mot de passe maître. Il n'est jamais stocké en clair, seul son empreinte (hash + sel) est conservée pour vérification.
2. **À chaque connexion** : ton mot de passe maître sert à dériver une clé de chiffrement (PBKDF2), utilisée pour déchiffrer le fichier `vault.enc` contenant toutes tes entrées.
3. **Toute donnée sensible** (mots de passe, champs personnalisés) est chiffrée sur le disque — jamais stockée en clair.

**Important** : si tu oublies ton mot de passe maître, il n'existe **aucun moyen de récupérer l'accès** au coffre. C'est un choix de sécurité volontaire : le mot de passe maître n'est stocké nulle part, ni en clair ni chiffré.

## Installation et lancement

### Option 1 — Exécutable Windows

Télécharge `CoffreAMdp.exe` (dossier `dist/` si tu build toi-même) et double-clique dessus. Aucune installation de Python requise.

### Option 2 — Depuis le code source

```bash
git clone https://github.com/arielagb/coffre_mdp.git
cd coffre_mdp
pip install cryptography
python main.py
```

### Regénérer l'exécutable soi-même

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name CoffreAMdp --icon=icon.ico main.py
```

L'exécutable sera généré dans le dossier `dist/`.

## Structure du projet

```
coffre_mdp/
├── main.py                      # Point d'entrée : connexion → chargement du coffre → fenêtre principale
├── etape1_cle.py                 # Génération du sel + dérivation de clé (PBKDF2)
├── etape2_encryption.py          # Chiffrement/déchiffrement avec Fernet
├── etape3_storage.py             # Sauvegarde/chargement du coffre chiffré (JSON) sur disque
├── etape4_vault_logic.py         # Logique métier : ajouter/modifier/supprimer/lister, générer un mot de passe
├── etape5_login.py               # Fenêtre de connexion (création/vérification du mot de passe maître)
├── etape6_main_window.py         # Fenêtre principale + formulaire d'ajout/édition d'entrée
├── etape8_change_password.py     # Changement du mot de passe maître
├── icon.ico                      # Icône de l'application
└── .gitignore
```

## Fichiers volontairement absents du dépôt

Ces fichiers sont générés localement et ne sont jamais poussés sur GitHub (voir `.gitignore`) :

- `vault.enc` — le coffre chiffré contenant tes vraies données
- `config.json` — le sel et le hash de ton mot de passe maître
- `build/`, `dist/`, `*.spec` — artefacts générés par PyInstaller

## Pistes d'amélioration possibles

- Clé de secours pour récupérer l'accès en cas d'oubli du mot de passe maître
- Recherche/filtre dans la liste des entrées
- Export/import du coffre
- Historique des mots de passe modifiés

## Avertissement

Ce projet a été réalisé à but personnel . Il n'a pas fait l'objet d'un audit de sécurité professionnel. Pour un usage critique, préférez un gestionnaire de mots de passe établi et audité (Bitwarden, KeePass, 1Password...).
