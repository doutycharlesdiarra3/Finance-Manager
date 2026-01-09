from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'currency', 'monthly_income_goal', 'monthly_savings_goal']
    list_filter = ['currency']
    search_fields = ['user__username', 'user__email']
