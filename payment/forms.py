from django import forms

from payment.models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['guest', 'room_information', 'amount']

