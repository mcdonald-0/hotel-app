from django.urls import path

from booking.views import book_a_room, check_in, check_out, view_rooms

app_name = 'booking'
urlpatterns = [
    path('<slug:hotel_slug>', view_rooms, name="view_rooms"),
    path('<slug:hotel_slug>/<slug:room_type_slug>/', book_a_room, name="book_a_room"),
    path('<slug:hotel_slug>/<slug:room_type_slug>/<slug:room_slug>/check-in', check_in, name='check_in'),
    path('<slug:hotel_slug>/<slug:room_type_slug>/<slug:room_slug>/check-out', check_out, name='check_out'),
]
