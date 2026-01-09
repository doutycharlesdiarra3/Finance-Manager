# Finance Manager - Système de Gestion Financière

Application Django complète pour gérer vos finances personnelles, suivre vos dépenses, planifier vos budgets et analyser vos habitudes financières.

## 🚀 Fonctionnalités

### ✅ Authentification
- Inscription et connexion utilisateur
- Gestion de profil avec préférences (devise, objectifs financiers)
- Photo de profil

### 💰 Gestion des Transactions
- Ajout, modification et suppression de transactions
- Catégorisation personnalisée (revenus et dépenses)
- Filtrage par type, catégorie et période
- Historique complet des transactions

### 📊 Tableau de Bord
- Vue d'ensemble financière (revenus, dépenses, solde)
- Graphiques interactifs (évolution mensuelle, répartition par catégorie)
- Alertes budgétaires
- Dernières transactions

### 🎯 Budgets
- Création de budgets mensuels par catégorie
- Suivi en temps réel de la consommation budgétaire
- Seuils d'alerte personnalisables
- Indicateurs visuels (barres de progression)

### 📈 Rapports et Analyses
- Rapports détaillés avec filtres avancés
- Graphiques de répartition par catégorie
- Export des données en CSV
- Statistiques complètes

## 🛠️ Technologies Utilisées

- **Backend**: Django 5.0.14
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Graphiques**: Chart.js
- **Base de données**: SQLite (développement)
- **Formulaires**: django-crispy-forms avec Bootstrap 5
- **Icônes**: Bootstrap Icons

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

#### Option 1 : Avec environnement virtuel (Recommandé)

1. **Créer un environnement virtuel**
   ```bash
   cd finance_manager
   py -m venv venv
   ```

2. **Activer l'environnement virtuel**
   
   Windows PowerShell:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   Windows CMD:
   ```cmd
   venv\Scripts\activate.bat
   ```
   
   Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

#### Option 2 : Installation globale

1. **Installer les dépendances directement**
   ```bash
   py -m pip install -r requirements.txt
   ```

**Note**: Si vous utilisez un environnement virtuel, assurez-vous qu'il est activé avant d'exécuter les commandes suivantes.

3. **Créer les migrations** (déjà fait)
   ```bash
   py manage.py makemigrations
   py manage.py migrate
   ```

4. **Créer un super utilisateur**
   ```bash
   py manage.py createsuperuser
   ```
   Suivez les instructions pour créer votre compte administrateur.

5. **Lancer le serveur de développement**
   ```bash
   py manage.py runserver
   ```

6. **Accéder à l'application**
   - Application: http://127.0.0.1:8000/
   - Interface d'administration: http://127.0.0.1:8000/admin/

## 🎨 Interface Utilisateur

L'application dispose d'une interface moderne et responsive avec:
- Design premium avec gradients et animations
- Mode responsive (mobile, tablette, desktop)
- Thème violet/bleu élégant
- Cartes statistiques animées
- Graphiques interactifs
- Formulaires validés côté client et serveur

## 📱 Pages Principales

### Pour les utilisateurs non connectés:
- `/accounts/login/` - Connexion
- `/accounts/register/` - Inscription

### Pour les utilisateurs connectés:
- `/` - Tableau de bord
- `/transactions/` - Liste des transactions
- `/transactions/add/` - Ajouter une transaction
- `/budgets/` - Gestion des budgets
- `/reports/` - Rapports et analyses
- `/categories/` - Gestion des catégories
- `/accounts/profile/` - Profil utilisateur

## 🗂️ Structure du Projet

```
finance_manager/
├── finance_manager/          # Configuration du projet
│   ├── settings.py          # Paramètres Django
│   ├── urls.py              # Routes principales
│   └── wsgi.py              # Configuration WSGI
├── accounts/                 # Application d'authentification
│   ├── models.py            # Modèle UserProfile
│   ├── views.py             # Vues d'authentification
│   ├── forms.py             # Formulaires utilisateur
│   └── urls.py              # Routes accounts
├── core/                     # Application principale
│   ├── models.py            # Modèles: Transaction, Category, Budget
│   ├── views.py             # Vues principales
│   ├── forms.py             # Formulaires de gestion
│   ├── urls.py              # Routes core
│   └── admin.py             # Configuration admin
├── templates/                # Templates HTML
│   ├── base.html            # Template de base
│   ├── dashboard.html       # Tableau de bord
│   ├── accounts/            # Templates authentification
│   ├── transactions/        # Templates transactions
│   ├── budgets/             # Templates budgets
│   └── reports/             # Templates rapports
├── static/                   # Fichiers statiques
│   ├── css/
│   │   └── style.css        # Styles personnalisés
│   └── js/
│       └── main.js          # Scripts JavaScript
├── db.sqlite3               # Base de données SQLite
├── manage.py                # Script de gestion Django
└── requirements.txt         # Dépendances Python
```

## 🔧 Configuration

### Langue et Fuseau Horaire
Le projet est configuré en français avec le fuseau horaire Europe/Paris.
Modifiez dans `settings.py` si nécessaire:
```python
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
```

### Base de Données
Par défaut, SQLite est utilisé. Pour PostgreSQL ou MySQL, modifiez `DATABASES` dans `settings.py`.

## 📊 Modèles de Données

### Category
- Nom, type (revenu/dépense), icône, couleur
- Associée à un utilisateur

### Transaction
- Montant, type, date, description
- Liée à une catégorie et un utilisateur
- Validation du type avec la catégorie

### Budget
- Montant budgété, période (YYYY-MM)
- Seuil d'alerte personnalisable
- Calcul automatique des dépenses et pourcentages

### UserProfile
- Devise préférée
- Objectifs financiers mensuels
- Photo de profil

## 🎯 Utilisation

1. **Créer un compte** via la page d'inscription
2. **Créer des catégories** personnalisées (revenus et dépenses)
3. **Ajouter des transactions** avec montant, date et catégorie
4. **Définir des budgets** mensuels pour contrôler vos dépenses
5. **Consulter le tableau de bord** pour voir vos statistiques
6. **Générer des rapports** avec filtres personnalisés
7. **Exporter vos données** en CSV pour analyse externe

## 🔒 Sécurité

- Authentification requise pour toutes les fonctionnalités
- Protection CSRF sur tous les formulaires
- Validation des données côté serveur
- Isolation des données par utilisateur

## 🚀 Déploiement en Production

Pour déployer en production:

1. Modifier `DEBUG = False` dans `settings.py`
2. Configurer `ALLOWED_HOSTS`
3. Utiliser une base de données production (PostgreSQL recommandé)
4. Configurer les fichiers statiques avec `collectstatic`
5. Utiliser un serveur WSGI (Gunicorn, uWSGI)
6. Configurer HTTPS

## 📝 Licence

Projet éducatif - Libre d'utilisation

## 👨‍💻 Support

Pour toute question ou problème:
- Vérifiez que toutes les dépendances sont installées
- Assurez-vous que les migrations sont appliquées
- Consultez les logs Django pour les erreurs

## 🎉 Fonctionnalités Futures Possibles

- Notifications par email
- Graphiques avancés (tendances, prévisions)
- Import de transactions depuis fichiers bancaires
- Application mobile
- Mode sombre
- Multi-devises avec conversion automatique
- Objectifs d'épargne avec suivi
- Partage de budgets entre utilisateurs

---

**Développé avec Django et Bootstrap 5** 💙
