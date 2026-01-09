from django.contrib import admin
from .models import Category, Transaction, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'icon', 'color', 'user', 'created_at']
    list_filter = ['type', 'user']
    search_fields = ['name', 'user__username']
    ordering = ['type', 'name']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'type', 'category', 'amount', 'user', 'description']
    list_filter = ['type', 'category', 'date', 'user']
    search_fields = ['description', 'user__username']
    date_hierarchy = 'date'
    ordering = ['-date', '-created_at']


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['category', 'period', 'amount', 'alert_threshold', 'user']
    list_filter = ['period', 'user', 'category']
    search_fields = ['category__name', 'user__username']
    ordering = ['-period']
