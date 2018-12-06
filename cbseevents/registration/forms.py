from django import forms

from .models import *


class TransactionForm(forms.ModelForm):
    amount = forms.FloatField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Amount'}), required=True)
    remark = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Remark'}), required=False, max_length=50)

    class Meta:
        model = TransactionRecord
        fields = ['amount', 'remark']

    def clean_amount(self):
        amount = self.cleaned_data['registration_start']
        if amount > 0:
            return amount
        raise forms.ValidationError("Invalid Start Date")
