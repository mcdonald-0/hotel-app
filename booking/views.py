from django.shortcuts import render, redirect
from django.template.defaultfilters import slugify
from django.http import HttpResponse

from booking.models import RoomBooking, Room
from booking.forms import BookingARoomForm

from registration.models import Hotel


def book_a_room(request, *args, **kwargs):
	hotel_slug = kwargs['slug']
	hotel = Hotel.objects.get(slug=hotel_slug)

	# This logic makes sure the number of rooms the hotel has is equal to the number of rooms available in the dropdown
	if hotel.number_of_rooms == Room.objects.filter(hotel__name=hotel.name).count():
		pass
	else:
		for i in range(hotel.number_of_rooms):
			Room.objects.get_or_create(hotel=hotel, room_number=i+1)

	form = BookingARoomForm(slug=hotel_slug)

	if request.method == 'POST':
		form = BookingARoomForm(request.POST, slug=hotel_slug)
		if form.is_valid():

			# The entire logic here checks if the hotel has available rooms, if it does not, a hotel is not booked.
			# if it does a hotel is booked and the number of rooms is incremented by one.
			if hotel.number_of_booked_rooms < hotel.number_of_rooms:
				hotel.no_rooms_available = False
				if hotel.no_rooms_available == False:
					hotel.number_of_booked_rooms += 1
					hotel.save()
					# This creates a room booking object then get the room a user books and updates the room_information
					RoomBooking.objects.create(hotel=hotel, guest=request.user, **form.cleaned_data).save()
					room_booking = RoomBooking.objects.get(hotel=hotel, guest=request.user, **form.cleaned_data)
					room_number = room_booking.room_booked.room_number
					Room.objects.filter(room_number=room_number, hotel=hotel).update(room_information=room_booking, is_booked=True)

				return redirect('booking:check_in', slug=hotel_slug)

			else:
				hotel.no_rooms_available = True
				hotel.number_of_booked_rooms = hotel.number_of_rooms
				hotel.save()
				if hotel.no_rooms_available == True:
					return HttpResponse('<h1>This hotel is maximally booked...</h1>')

	context = {
		'hotel': hotel,
		'form': form,
	}

	return render(request, 'booking/booking.html', context)


def check_in(request, *args, **kwargs):
	hotel_slug = kwargs['slug']
	hotel = Hotel.objects.get(slug=hotel_slug)



	context = {
		'hotel': hotel,
	}

	return render(request, 'booking/check_in.html', context)
	

