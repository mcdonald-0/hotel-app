from django.urls import path

from payment.views import initiate_payment

app_name = 'payment'
urlpatterns = [
    path('', initiate_payment, name='initiate_payment'),
]
