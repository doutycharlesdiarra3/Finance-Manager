from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Profil utilisateur étendu"""
    CURRENCY_CHOICES = [
        ('EUR', '€ Euro'),
        ('USD', '$ Dollar'),
        ('GBP', '£ Livre'),
        ('XOF', 'CFA Franc'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='EUR', verbose_name='Devise')
    monthly_income_goal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Objectif de revenu mensuel')
    monthly_savings_goal = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Objectif d\'épargne mensuel')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='Photo de profil')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Profil utilisateur'
        verbose_name_plural = 'Profils utilisateurs'
    
    def __str__(self):
        return f"Profil de {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil lors de la création d'un utilisateur"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde le profil lors de la sauvegarde de l'utilisateur"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
