# Guide de Configuration avec Environnement Virtuel

## Pourquoi utiliser un environnement virtuel ?

Un environnement virtuel Python permet de :
- Isoler les dépendances du projet
- Éviter les conflits entre différents projets
- Faciliter le déploiement
- Maintenir des versions spécifiques de packages

---

## Installation avec Environnement Virtuel

### Étape 1 : Créer l'environnement virtuel

```bash
cd C:\Users\DIARRA\.gemini\antigravity\scratch\finance_manager
py -m venv venv
```

Cela créera un dossier `venv` contenant l'environnement virtuel.

### Étape 2 : Activer l'environnement virtuel

**Sur Windows (PowerShell)** :
```powershell
.\venv\Scripts\Activate.ps1
```

**Sur Windows (CMD)** :
```cmd
venv\Scripts\activate.bat
```

**Sur Linux/Mac** :
```bash
source venv/bin/activate
```

Vous verrez `(venv)` apparaître au début de votre ligne de commande.

### Étape 3 : Installer les dépendances

Une fois l'environnement activé :
```bash
pip install -r requirements.txt
```

### Étape 4 : Vérifier l'installation

```bash
pip list
```

Vous devriez voir tous les packages installés dans l'environnement virtuel.

### Étape 5 : Créer le super utilisateur

```bash
py manage.py createsuperuser
```

### Étape 6 : (Optionnel) Charger les données de test

```bash
py manage.py shell < create_test_data.py
```

### Étape 7 : Lancer le serveur

```bash
py manage.py runserver
```

---

## Commandes Utiles

### Activer l'environnement
```bash
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat
```

### Désactiver l'environnement
```bash
deactivate
```

### Mettre à jour requirements.txt
Si vous installez de nouveaux packages :
```bash
pip freeze > requirements.txt
```

### Supprimer l'environnement virtuel
Simplement supprimer le dossier `venv` :
```bash
# Windows
rmdir /s venv

# Linux/Mac
rm -rf venv
```

---

## Structure du Projet avec venv

```
finance_manager/
├── venv/                     # Environnement virtuel (à ne pas commiter)
├── finance_manager/          # Configuration Django
├── accounts/                 # App authentification
├── core/                     # App principale
├── templates/                # Templates HTML
├── static/                   # Fichiers statiques
├── db.sqlite3               # Base de données
├── manage.py                # Script Django
├── requirements.txt         # Dépendances
├── README.md                # Documentation
└── create_test_data.py      # Script de test
```

---

## .gitignore Recommandé

Créez un fichier `.gitignore` pour ne pas commiter l'environnement virtuel :

```
# Environnement virtuel
venv/
env/
ENV/

# Base de données
*.sqlite3
db.sqlite3

# Fichiers Python
__pycache__/
*.py[cod]
*$py.class
*.so

# Django
*.log
local_settings.py
staticfiles/
media/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
```

---

## Avantages de cette Approche

✅ **Isolation** : Les packages n'affectent pas le système global
✅ **Reproductibilité** : Même environnement sur toutes les machines
✅ **Propreté** : Facile de supprimer et recréer
✅ **Sécurité** : Versions contrôlées des dépendances
✅ **Collaboration** : Autres développeurs peuvent reproduire l'environnement

---

## Démarrage Rapide (Résumé)

```bash
# 1. Créer et activer l'environnement
cd C:\Users\DIARRA\.gemini\antigravity\scratch\finance_manager
py -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Créer un super utilisateur
py manage.py createsuperuser

# 4. Lancer le serveur
py manage.py runserver
```

---

## Note Importante

⚠️ **Les packages ont déjà été installés globalement** dans votre système lors de la création initiale du projet. Vous pouvez :

1. **Continuer sans venv** : Le projet fonctionne déjà
2. **Migrer vers venv** : Suivre les étapes ci-dessus pour une meilleure pratique

Pour les projets futurs, il est recommandé de créer l'environnement virtuel **avant** d'installer les packages.
