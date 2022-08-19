from django.urls import path
from registration.views import *

app_name = 'registration'
urlpatterns = [
    path('', homepage, name="homepage"),
    path('guest/<int:user_id>', view_my_profile, name="view_my_profile"),
]
