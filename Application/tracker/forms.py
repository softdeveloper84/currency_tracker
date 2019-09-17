from django import forms
from .models import CurrencyModel


class CurrencyForm(forms.ModelForm):
    """
    Form for adding currency pairs
    """
    base = forms.CharField(label="Base current", max_length=10)
    target = forms.CharField(label="Target current", max_length=10)

    class Meta:
        model = CurrencyModel
        fields = ('base', 'target', )
