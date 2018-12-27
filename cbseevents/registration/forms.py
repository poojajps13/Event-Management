from django import forms

from .models import TransactionRecord


class TransactionForm(forms.ModelForm):
    amount = forms.FloatField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Amount'}), required=True, max_value=10002, min_value=-10002)
    remark = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Remark'}), required=False, max_length=50)

    class Meta:
        model = TransactionRecord
        fields = ['amount', 'remark']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if -10000 <= amount <= 10000:
            return amount
        raise forms.ValidationError("Invalid Amount")
