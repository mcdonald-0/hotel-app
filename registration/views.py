from django.shortcuts import render

from registration.models import Hotel
from authentication.models import Guest
from booking.models import RoomBooking


def homepage(request, *args, **kwargs):
	hotel_list = Hotel.objects.all()

	for hotel in hotel_list:
		image = hotel.display_image

	context = {
		'hotels': hotel_list,
	}

	return render(request, 'registration/homepage.html', context)


def activity_log(request, *args, **kwargs):
	user_id = kwargs["user_id"]

	guest = Guest.objects.get(pk=user_id)
	booking_made = RoomBooking.objects.filter(guest=guest.user)

	context = {
		'guest': guest,
		'bookings': booking_made,
	}
	return render(request, 'registration/activity_log.html', context)