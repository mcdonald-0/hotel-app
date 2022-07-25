from django.urls import path

from booking.views import index, book_a_room

app_name = 'booking'
urlpatterns = [
    path('', index, name="index"),
    path('<slug:slug>', book_a_room, name="book"),
]