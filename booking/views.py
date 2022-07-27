from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.http import HttpResponse

from booking.models import RoomBooking, Room
from booking.forms import BookingARoomForm

from registration.models import Hotel

ROOMS = 0


def book_a_room(request, *args, **kwargs):
	hotel_slug = kwargs['slug']
	hotel = Hotel.objects.get(slug=hotel_slug)

	global ROOMS

	ROOMS = hotel.number_of_rooms

	form = BookingARoomForm()

	if request.method == 'POST':
		form = BookingARoomForm(request.POST)
		if form.is_valid():

			# The entire logic here checks if the hotel has available rooms, if it does not, a hotel is not booked. if it does a hotel is booked and the number of rooms is incremented by one.
			if hotel.number_of_booked_rooms < hotel.number_of_rooms:
				hotel.no_rooms_available = False
				if hotel.no_rooms_available == False:
					hotel.number_of_booked_rooms += 1
					hotel.save()
					room_booking = RoomBooking.objects.create(hotel=hotel, guest=request.user, **form.cleaned_data)
					Room.objects.create(hotel=hotel, room_information=room_booking, is_booked=True, checked_in=True, **form.cleaned_data)

				return HttpResponse('<h1>You just booked a hotel</h1>')

			else:
				hotel.no_rooms_available = True
				hotel.number_of_booked_rooms = hotel.number_of_rooms
				hotel.save()
				if hotel.no_rooms_available == True:
					return HttpResponse('<h1>This hotel is maximally booked...</h1>')

		print(ROOMS)

	context = {
		'hotel': hotel,
		'form': form,
		'rooms_available': hotel.number_of_rooms,
	}

	return render(request, 'booking/booking.html', context)

print(ROOMS)

# def checkout(request, *args, **kwargs):
	

