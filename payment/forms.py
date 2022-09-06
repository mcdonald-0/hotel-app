from django import forms

from payment.models import Payment


class PaymentForm(forms.ModelForm):
    amount = forms.IntegerField(label="Amount", widget=forms.TextInput(attrs={
        'class': 'disabled',
    }))

    class Meta:
        model = Payment
        fields = ['guest', 'room_information', 'amount']

