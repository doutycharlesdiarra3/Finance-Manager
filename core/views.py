from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import HttpResponse
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import csv
import json
from decimal import Decimal

from .models import Transaction, Category, Budget
from .forms import TransactionForm, CategoryForm, BudgetForm, ReportFilterForm


@login_required
def dashboard_view(request):
    """Tableau de bord principal"""
    user = request.user
    today = date.today()
    current_month = today.strftime('%Y-%m')
    
    # Statistiques du mois en cours
    current_month_transactions = Transaction.objects.filter(
        user=user,
        date__year=today.year,
        date__month=today.month
    )
    
    income_month = current_month_transactions.filter(type='INCOME').aggregate(
        total=Sum('amount'))['total'] or Decimal('0.00')
    expense_month = current_month_transactions.filter(type='EXPENSE').aggregate(
        total=Sum('amount'))['total'] or Decimal('0.00')
    balance = income_month - expense_month
    
    # Solde total (tous les temps)
    total_income = Transaction.objects.filter(user=user, type='INCOME').aggregate(
        total=Sum('amount'))['total'] or Decimal('0.00')
    total_expense = Transaction.objects.filter(user=user, type='EXPENSE').aggregate(
        total=Sum('amount'))['total'] or Decimal('0.00')
    total_balance = total_income - total_expense
    
    # Dernières transactions
    recent_transactions = Transaction.objects.filter(user=user)[:10]
    
    # Budgets avec alertes
    budgets = Budget.objects.filter(user=user, period=current_month)
    budget_alerts = [b for b in budgets if b.is_over_threshold()]
    
    # Données pour les graphiques (6 derniers mois)
    months_data = []
    for i in range(5, -1, -1):
        month_date = today - relativedelta(months=i)
        month_str = month_date.strftime('%Y-%m')
        month_label = month_date.strftime('%b %Y')
        
        month_income = Transaction.objects.filter(
            user=user,
            type='INCOME',
            date__year=month_date.year,
            date__month=month_date.month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        month_expense = Transaction.objects.filter(
            user=user,
            type='EXPENSE',
            date__year=month_date.year,
            date__month=month_date.month
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        months_data.append({
            'label': month_label,
            'income': float(month_income),
            'expense': float(month_expense)
        })
    
    # Répartition par catégorie (mois en cours)
    expense_categories = Category.objects.filter(user=user, type='EXPENSE')
    category_data = []
    for cat in expense_categories:
        cat_total = current_month_transactions.filter(category=cat).aggregate(
            total=Sum('amount'))['total'] or Decimal('0.00')
        if cat_total > 0:
            category_data.append({
                'name': cat.name,
                'amount': float(cat_total),
                'color': cat.color
            })
    
    context = {
        'income_month': income_month,
        'expense_month': expense_month,
        'balance': balance,
        'total_balance': total_balance,
        'recent_transactions': recent_transactions,
        'budget_alerts': budget_alerts,
        'months_data': months_data,
        'category_data': category_data,
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def transaction_list_view(request):
    """Liste des transactions avec filtres"""
    transactions = Transaction.objects.filter(user=request.user)
    
    # Filtres
    type_filter = request.GET.get('type')
    category_filter = request.GET.get('category')
    month_filter = request.GET.get('month')
    
    if type_filter:
        transactions = transactions.filter(type=type_filter)
    if category_filter:
        transactions = transactions.filter(category_id=category_filter)
    if month_filter:
        try:
            year, month = map(int, month_filter.split('-'))
            transactions = transactions.filter(date__year=year, date__month=month)
        except:
            pass
    
    categories = Category.objects.filter(user=request.user)
    # Pré-calcul du selected pour chaque catégorie
    for cat in categories:
        if str(cat.id) == category_filter:
            cat.selected = "selected"
        else:
            cat.selected = ""
    
    # transactions = Transaction.objects.all()

    for t in transactions:
        if t.type == "INCOME":
            t.css_class = "text-success"
            t.sign = "+"
        else:
            t.css_class = "text-danger"
            t.sign = "-"

    # FORMATAGE DU MONTANT CÔTÉ PYTHON
    # t.display_amount = f"{t.amount:.2f}"
    
    context = {
        'transactions': transactions,
        'categories': categories,
        'type_filter': type_filter,
        'category_filter': category_filter,
        'month_filter': month_filter,
        "is_income": type_filter == "INCOME",
        "is_expense": type_filter == "EXPENSE",
    }
    
    return render(request, 'transactions/list.html', context)


@login_required
def transaction_create_view(request):
    """Créer une nouvelle transaction"""
    if request.method == 'POST':
        form = TransactionForm(user=request.user, data=request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction ajoutée avec succès!')
            return redirect('core:transaction_list')
    else:
        form = TransactionForm(user=request.user)
    
    return render(request, 'transactions/form.html', {'form': form, 'action': 'Ajouter'})


@login_required
def transaction_update_view(request, pk):
    """Modifier une transaction"""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TransactionForm(user=request.user, data=request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction modifiée avec succès!')
            return redirect('core:transaction_list')
    else:
        form = TransactionForm(user=request.user, instance=transaction)
    
    return render(request, 'transactions/form.html', {'form': form, 'action': 'Modifier'})


@login_required
def transaction_delete_view(request, pk):
    """Supprimer une transaction"""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction supprimée avec succès!')
        return redirect('core:transaction_list')
    
    return render(request, 'transactions/delete.html', {'transaction': transaction})


@login_required
def category_list_view(request):
    """Liste des catégories"""
    categories = Category.objects.filter(user=request.user)
    return render(request, 'transactions/categories.html', {'categories': categories})


@login_required
def category_create_view(request):
    """Créer une nouvelle catégorie"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Catégorie créée avec succès!')
            return redirect('core:category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'transactions/category_form.html', {'form': form, 'action': 'Créer'})


@login_required
def budget_list_view(request):
    """Liste des budgets"""
    budgets = Budget.objects.filter(user=request.user)
    
    # Ajouter les informations de dépenses pour chaque budget
    budgets_with_data = []
    for budget in budgets:
        budgets_with_data.append({
            'budget': budget,
            'spent': budget.get_spent_amount(),
            'percentage': budget.get_percentage_used(),
            'remaining': budget.amount - budget.get_spent_amount(),
        })
    
    return render(request, 'budgets/list.html', {'budgets_with_data': budgets_with_data})


@login_required
def budget_create_view(request):
    """Créer un nouveau budget"""
    if request.method == 'POST':
        form = BudgetForm(user=request.user, data=request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, 'Budget créé avec succès!')
            return redirect('core:budget_list')
    else:
        form = BudgetForm(user=request.user)
    
    return render(request, 'budgets/form.html', {'form': form, 'action': 'Créer'})


@login_required
def budget_update_view(request, pk):
    """Modifier un budget"""
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = BudgetForm(user=request.user, data=request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget modifié avec succès!')
            return redirect('core:budget_list')
    else:
        form = BudgetForm(user=request.user, instance=budget)
    
    return render(request, 'budgets/form.html', {'form': form, 'action': 'Modifier'})


@login_required
def budget_delete_view(request, pk):
    """Supprimer un budget"""
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    
    if request.method == 'POST':
        budget.delete()
        messages.success(request, 'Budget supprimé avec succès!')
        return redirect('core:budget_list')
    
    return render(request, 'budgets/delete.html', {'budget': budget})


@login_required
def reports_view(request):
    """Vue des rapports et analyses"""
    user = request.user
    form = ReportFilterForm(user=user, data=request.GET or None)
    
    # Filtres par défaut: mois en cours
    transactions = Transaction.objects.filter(user=user)
    
    if form.is_valid():
        if form.cleaned_data.get('start_date'):
            transactions = transactions.filter(date__gte=form.cleaned_data['start_date'])
        if form.cleaned_data.get('end_date'):
            transactions = transactions.filter(date__lte=form.cleaned_data['end_date'])
        if form.cleaned_data.get('category'):
            transactions = transactions.filter(category=form.cleaned_data['category'])
        if form.cleaned_data.get('type'):
            transactions = transactions.filter(type=form.cleaned_data['type'])
    
    # Statistiques
    total_income = transactions.filter(type='INCOME').aggregate(
        total=Sum('amount'))['total'] or Decimal('0.00')
    total_expense = transactions.filter(type='EXPENSE').aggregate(
        total=Sum('amount'))['total'] or Decimal('0.00')
    net_balance = total_income - total_expense
    
    # Répartition par catégorie
    categories_income = []
    categories_expense = []
    
    for cat in Category.objects.filter(user=user, type='INCOME'):
        cat_total = transactions.filter(category=cat).aggregate(
            total=Sum('amount'))['total'] or Decimal('0.00')
        if cat_total > 0:
            categories_income.append({
                'name': cat.name,
                'amount': float(cat_total),
                'color': cat.color
            })
    
    for cat in Category.objects.filter(user=user, type='EXPENSE'):
        cat_total = transactions.filter(category=cat).aggregate(
            total=Sum('amount'))['total'] or Decimal('0.00')
        if cat_total > 0:
            categories_expense.append({
                'name': cat.name,
                'amount': float(cat_total),
                'color': cat.color
            })

    # categories_income_json = json.dumps(categories_income)
    # categories_expense_json = json.dumps(categories_expense)
    
    context = {
        'form': form,
        'transactions': transactions,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_balance': net_balance,
        'categories_income': categories_income,
        'categories_expense': categories_expense,
        # 'categories_income': categories_income_json,
        # 'categories_expense': categories_expense_json,
    }
    
    return render(request, 'reports/reports.html', context)


@login_required
def export_transactions_csv(request):
    """Exporter les transactions en CSV"""
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    response.write('\ufeff')  # BOM pour Excel
    
    writer = csv.writer(response)
    writer.writerow(['Date', 'Type', 'Catégorie', 'Montant', 'Description'])
    
    for trans in transactions:
        writer.writerow([
            trans.date.strftime('%Y-%m-%d'),
            trans.get_type_display(),
            trans.category.name if trans.category else '',
            str(trans.amount),
            trans.description
        ])
    
    return response
