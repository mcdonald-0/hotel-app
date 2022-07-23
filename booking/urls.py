from django.urls import path
from booking.views import *

urlpatterns = [
    path('', index, name="index"),
    path('<slug:slug>', book_a_room, name="book"),
]