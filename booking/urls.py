from django.urls import path

from booking.views import *

app_name = 'booking'
urlpatterns = [
    path('<slug:slug>', book_a_room, name="book_a_room"),
    path('check-in/<slug:slug>', check_in, name='check_in'),
]
