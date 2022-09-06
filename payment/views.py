from django.shortcuts import render

from payment.forms import PaymentForm


def initiate_payment(request, *args, **kwargs):
    form = PaymentForm()
    context = {
        'form': form
    }
    return render(request, 'payment/initiate_payment.html', context)
