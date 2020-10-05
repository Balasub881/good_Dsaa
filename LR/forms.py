from .models import Expense
from django import forms
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ['user']

class FilterForm(forms.Form):
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'placeholder': 'Start Date'}))
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date', 'placeholder': 'End Date'}))