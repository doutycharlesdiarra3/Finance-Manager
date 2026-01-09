from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # Transactions
    path('transactions/', views.transaction_list_view, name='transaction_list'),
    path('transactions/add/', views.transaction_create_view, name='transaction_create'),
    path('transactions/<int:pk>/edit/', views.transaction_update_view, name='transaction_update'),
    path('transactions/<int:pk>/delete/', views.transaction_delete_view, name='transaction_delete'),
    
    # Categories
    path('categories/', views.category_list_view, name='category_list'),
    path('categories/add/', views.category_create_view, name='category_create'),
    
    # Budgets
    path('budgets/', views.budget_list_view, name='budget_list'),
    path('budgets/add/', views.budget_create_view, name='budget_create'),
    path('budgets/<int:pk>/edit/', views.budget_update_view, name='budget_update'),
    path('budgets/<int:pk>/delete/', views.budget_delete_view, name='budget_delete'),
    
    # Reports
    path('reports/', views.reports_view, name='reports'),
    path('export/csv/', views.export_transactions_csv, name='export_csv'),
]
