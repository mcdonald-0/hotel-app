from django.urls import path

from authentication.views import create_guest, authenticate_guest

app_name = 'authentication'
urlpatterns = [
    path('guest/', create_guest, name='create_guest'),
    path('guest/activate/<str:uidb64>/<str:token>', authenticate_guest, name='authenticate_guest'),

]
