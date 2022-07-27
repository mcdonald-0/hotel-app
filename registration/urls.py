from django.urls import path
from registration.views import *

app_name = 'registration'
urlpatterns = [
    path('', homepage, name="homepage"),
]
