# Script pour créer des données de test
# Exécutez avec: py manage.py shell < create_test_data.py

from django.contrib.auth.models import User
from core.models import Category, Transaction, Budget
from datetime import date, timedelta
from decimal import Decimal

# Créer un utilisateur de test (si nécessaire)
username = "demo"
if not User.objects.filter(username=username).exists():
    user = User.objects.create_user(
        username=username,
        email="demo@example.com",
        password="demo123",
        first_name="Utilisateur",
        last_name="Demo"
    )
    print(f"✓ Utilisateur '{username}' créé (mot de passe: demo123)")
else:
    user = User.objects.get(username=username)
    print(f"✓ Utilisateur '{username}' existe déjà")

# Créer des catégories de revenus
income_categories = [
    {"name": "Salaire", "icon": "💼", "color": "#10b981"},
    {"name": "Freelance", "icon": "💻", "color": "#059669"},
    {"name": "Investissements", "icon": "📈", "color": "#34d399"},
    {"name": "Autres revenus", "icon": "💰", "color": "#6ee7b7"},
]

for cat_data in income_categories:
    cat, created = Category.objects.get_or_create(
        user=user,
        name=cat_data["name"],
        type="INCOME",
        defaults={"icon": cat_data["icon"], "color": cat_data["color"]}
    )
    if created:
        print(f"✓ Catégorie de revenu créée: {cat.name}")

# Créer des catégories de dépenses
expense_categories = [
    {"name": "Alimentation", "icon": "🍔", "color": "#ef4444"},
    {"name": "Transport", "icon": "🚗", "color": "#f97316"},
    {"name": "Logement", "icon": "🏠", "color": "#dc2626"},
    {"name": "Loisirs", "icon": "🎮", "color": "#f59e0b"},
    {"name": "Santé", "icon": "⚕️", "color": "#ec4899"},
    {"name": "Shopping", "icon": "🛍️", "color": "#8b5cf6"},
    {"name": "Éducation", "icon": "📚", "color": "#6366f1"},
    {"name": "Abonnements", "icon": "📱", "color": "#3b82f6"},
]

for cat_data in expense_categories:
    cat, created = Category.objects.get_or_create(
        user=user,
        name=cat_data["name"],
        type="EXPENSE",
        defaults={"icon": cat_data["icon"], "color": cat_data["color"]}
    )
    if created:
        print(f"✓ Catégorie de dépense créée: {cat.name}")

# Créer des transactions de test pour les 3 derniers mois
today = date.today()

# Revenus mensuels
for i in range(3):
    month_date = today - timedelta(days=30 * i)
    
    # Salaire
    Transaction.objects.get_or_create(
        user=user,
        date=month_date.replace(day=1),
        type="INCOME",
        defaults={
            "category": Category.objects.get(user=user, name="Salaire", type="INCOME"),
            "amount": Decimal("2500.00"),
            "description": "Salaire mensuel"
        }
    )

# Dépenses variées
expense_data = [
    ("Alimentation", 350.50, "Courses du mois"),
    ("Transport", 80.00, "Abonnement transport"),
    ("Logement", 800.00, "Loyer"),
    ("Loisirs", 120.00, "Cinéma et sorties"),
    ("Santé", 45.00, "Pharmacie"),
    ("Shopping", 200.00, "Vêtements"),
    ("Abonnements", 35.99, "Netflix, Spotify"),
]

for i in range(3):
    month_date = today - timedelta(days=30 * i)
    
    for cat_name, amount, desc in expense_data:
        try:
            category = Category.objects.get(user=user, name=cat_name, type="EXPENSE")
            Transaction.objects.get_or_create(
                user=user,
                date=month_date.replace(day=15),
                category=category,
                type="EXPENSE",
                defaults={
                    "amount": Decimal(str(amount)),
                    "description": desc
                }
            )
        except Category.DoesNotExist:
            pass

print(f"✓ Transactions de test créées")

# Créer des budgets pour le mois en cours
current_period = today.strftime("%Y-%m")

budget_data = [
    ("Alimentation", 400.00, 80),
    ("Transport", 100.00, 75),
    ("Loisirs", 150.00, 85),
    ("Shopping", 250.00, 80),
]

for cat_name, amount, threshold in budget_data:
    try:
        category = Category.objects.get(user=user, name=cat_name, type="EXPENSE")
        budget, created = Budget.objects.get_or_create(
            user=user,
            category=category,
            period=current_period,
            defaults={
                "amount": Decimal(str(amount)),
                "alert_threshold": threshold
            }
        )
        if created:
            print(f"✓ Budget créé: {cat_name} - {amount}€")
    except Category.DoesNotExist:
        pass

print("\n" + "="*50)
print("✅ Données de test créées avec succès!")
print("="*50)
print(f"\nConnectez-vous avec:")
print(f"  Nom d'utilisateur: {username}")
print(f"  Mot de passe: demo123")
print("\nAccédez à l'application: http://127.0.0.1:8000/")
