from django.urls import path

from django.views.decorators.csrf import csrf_exempt

from authentication.views import create_guest, authenticate_guest, validate_first_name, validate_last_name, validate_email, validate_phone_number

app_name = 'authentication'
urlpatterns = [
    path('guest/', create_guest, name='create_guest'),
    path('guest/activate-account/<str:uidb64>/<str:token>', authenticate_guest, name='authenticate_guest'),

    path('validate-first-name', csrf_exempt(validate_first_name), name="validate_first_name"),
    path('validate-last-name', csrf_exempt(validate_last_name), name="validate_last_name"),
    path('validate-email', csrf_exempt(validate_email), name="validate_email"),
    path('validate-phone-number', csrf_exempt(validate_phone_number), name="validate_phone_number"),
]
