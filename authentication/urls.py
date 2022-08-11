from django.urls import path

from authentication.views import create_guest

app_name = 'authentication'
urlpatterns = [
    path('guest/', create_guest, name='create_guest'),
]
