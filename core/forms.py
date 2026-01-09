from django import forms
from .models import Transaction, Category, Budget
from datetime import date


class TransactionForm(forms.ModelForm):
    """Formulaire standard pour les transactions"""
    class Meta:
        model = Transaction
        fields = ['type', 'category', 'amount', 'date', 'description']
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }
    
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
        
        if not self.instance.pk:
            self.fields['date'].initial = date.today()

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        trans_type = cleaned_data.get('type')
        
        if category and trans_type and category.type != trans_type:
            raise forms.ValidationError(
                "Le type de transaction doit correspondre au type de catégorie sélectionnée."
            )
        return cleaned_data


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type', 'icon', 'color']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'period', 'alert_threshold']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'period': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM'}),
            'alert_threshold': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user, type='EXPENSE')


class ReportFilterForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.none(), required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    type = forms.ChoiceField(choices=[('', 'Tous'), ('INCOME', 'Revenu'), ('EXPENSE', 'Dépense')], required=False, widget=forms.Select(attrs={'class': 'form-select'}))
    
    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
