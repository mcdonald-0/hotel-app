from django.urls import path

from payment.views import initiate_payment, verified_payment

app_name = 'payment'
urlpatterns = [
    path('initiate/<slug:hotel_slug>/<slug:room_type_slug>/<slug:room_slug>/', initiate_payment, name='initiate_payment'),
    path('verified/<str:ref>/', verified_payment, name='verify_payment')
]
