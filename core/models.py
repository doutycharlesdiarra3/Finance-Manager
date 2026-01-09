from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Category(models.Model):
    """Catégorie pour les transactions (revenus ou dépenses)"""
    TYPE_CHOICES = [
        ('INCOME', 'Revenu'),
        ('EXPENSE', 'Dépense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100, verbose_name='Nom')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='Type')
    icon = models.CharField(max_length=50, default='💰', verbose_name='Icône')
    color = models.CharField(max_length=7, default='#3498db', verbose_name='Couleur')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['name']
        unique_together = ['user', 'name', 'type']
    
    def __str__(self):
        return f"{self.icon} {self.name}"


class Transaction(models.Model):
    """Transaction financière (revenu ou dépense)"""
    TYPE_CHOICES = [
        ('INCOME', 'Revenu'),
        ('EXPENSE', 'Dépense'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions', verbose_name='Catégorie')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Montant')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name='Type')
    date = models.DateField(verbose_name='Date')
    description = models.TextField(blank=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return f"{self.get_type_display()} - {self.amount}€ - {self.date}"
    
    def save(self, *args, **kwargs):
        # Assurer que le type correspond à la catégorie
        if self.category and self.category.type != self.type:
            raise ValueError("Le type de transaction doit correspondre au type de catégorie")
        super().save(*args, **kwargs)


class Budget(models.Model):
    """Budget mensuel pour une catégorie de dépenses"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets', verbose_name='Catégorie')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], verbose_name='Montant budgété')
    period = models.CharField(max_length=7, verbose_name='Période (YYYY-MM)', help_text='Format: 2026-01')
    alert_threshold = models.IntegerField(
        default=80,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Seuil d\'alerte (%)',
        help_text='Pourcentage du budget à partir duquel une alerte est déclenchée'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'
        ordering = ['-period']
        unique_together = ['user', 'category', 'period']
    
    def __str__(self):
        return f"Budget {self.category.name} - {self.period}"
    
    def get_spent_amount(self):
        """Calcule le montant dépensé pour ce budget"""
        from datetime import datetime
        year, month = map(int, self.period.split('-'))
        spent = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            type='EXPENSE',
            date__year=year,
            date__month=month
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
        return spent
    
    def get_percentage_used(self):
        """Calcule le pourcentage du budget utilisé"""
        spent = self.get_spent_amount()
        if self.amount > 0:
            return (spent / self.amount * 100)
        return 0
    
    def is_over_threshold(self):
        """Vérifie si le budget a dépassé le seuil d'alerte"""
        return self.get_percentage_used() >= self.alert_threshold
    
    def is_exceeded(self):
        """Vérifie si le budget est dépassé"""
        return self.get_spent_amount() > self.amount
