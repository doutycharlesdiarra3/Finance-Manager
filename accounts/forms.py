from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegistrationForm(UserCreationForm):
    """Formulaire d'inscription utilisateur"""
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=False, label='Prénom')
    last_name = forms.CharField(max_length=30, required=False, label='Nom')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['password1'].label = 'Mot de passe'
        self.fields['password2'].label = 'Confirmation du mot de passe'
        
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})


class UserLoginForm(AuthenticationForm):
    """Formulaire de connexion"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['password'].label = 'Mot de passe'
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Mot de passe'})


class UserProfileForm(forms.ModelForm):
    """Formulaire de modification du profil"""
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=False, label='Prénom')
    last_name = forms.CharField(max_length=30, required=False, label='Nom')
    
    class Meta:
        model = UserProfile
        fields = ['currency', 'monthly_income_goal', 'monthly_savings_goal', 'avatar']
        labels = {
            'currency': 'Devise préférée',
            'monthly_income_goal': 'Objectif de revenu mensuel',
            'monthly_savings_goal': 'Objectif d\'épargne mensuel',
            'avatar': 'Photo de profil',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        
        for field_name in self.fields:
            if field_name != 'avatar':
                self.fields[field_name].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            user = profile.user
            user.email = self.cleaned_data['email']
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.save()
            profile.save()
        return profile
