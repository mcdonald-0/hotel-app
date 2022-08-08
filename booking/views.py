from datetime import timedelta

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect

from booking.models import RoomBooking, Room
from booking.forms import BookingARoomForm, CheckInARoomForm

from registration.models import Hotel


def book_a_room(request, *args, **kwargs):
	hotel_slug = kwargs['slug']
	hotel = Hotel.objects.get(slug=hotel_slug)

	# This logic makes sure the number of rooms the hotel has is equal to the number of rooms available in the dropdown
	if hotel.number_of_rooms == Room.objects.filter(hotel__name=hotel.name).count():
		pass
	else:
		Room.objects.filter(hotel__name=hotel.name).delete()
		for i in range(hotel.number_of_rooms):
			Room.objects.get_or_create(hotel=hotel, room_number=i+1)

	# This makes sure that if the number of booked room equals the number of rooms, no_rooms_available would be equals to True
	hotel.number_of_booked_rooms = Room.objects.filter(hotel__slug=hotel_slug, is_booked=True).count()
	if hotel.number_of_rooms == hotel.number_of_booked_rooms:
		hotel.no_rooms_available = True
	hotel.save()			

	form = BookingARoomForm(slug=hotel_slug)

	if request.method == 'POST':
		form = BookingARoomForm(request.POST, slug=hotel_slug)
		if form.is_valid():

			# This makes sure that the date a user wants to check in comes before the date a user wants to check out
			if form.cleaned_data['date_to_check_out'] - form.cleaned_data['date_to_check_in'] < timedelta(days=1):
				messages.error(request, 'Improperly configured dates')
				messages.info(request, 'Check the date you want to check in, make sure it is before the date you want to check out')
				return redirect('booking:book_a_room', slug=hotel_slug)

			# The entire logic here checks if the hotel has available rooms, if it does not, a hotel is not booked. if it does a hotel is booked and the number of rooms is incremented by one.
			if hotel.number_of_booked_rooms < hotel.number_of_rooms:
				hotel.no_rooms_available = False
				if hotel.no_rooms_available == False:
					hotel.number_of_booked_rooms += 1
					hotel.save()
					# This creates a room booking object then get the room a user books and updates the room_information
					RoomBooking.objects.create(hotel=hotel, guest=request.user, **form.cleaned_data)
					try:
						RoomBooking.objects.get(hotel=hotel, guest=request.user, **form.cleaned_data)
					except RoomBooking.MultipleObjectsReturned:
						messages.error(request, 'You already booked this room!')

					room_booking = RoomBooking.objects.get(hotel=hotel, guest=request.user, **form.cleaned_data)
					room_number = room_booking.room_booked.room_number
					Room.objects.filter(room_number=room_number, hotel=hotel).update(room_information=room_booking, is_booked=True)

					room = Room.objects.get(room_number=room_number, hotel__name=hotel)
					return redirect('booking:check_in', hotel_slug=hotel_slug, room_slug=room.slug)

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
	hotel_slug, room_slug = kwargs.values()
	room = Room.objects.get(slug=room_slug, hotel__slug=hotel_slug)

	form = CheckInARoomForm

	if request.method == 'POST':
		form = CheckInARoomForm(request.POST)
		if form.is_valid():
			room.checked_in = True
			room.save()

			return HttpResponse('<h1>Yeey! you checked into a room🎇</h1>')

	context = {
		'room': room,
		'form': form,
	}

	return render(request, 'booking/check_in.html', context)


def check_out(request, *args, **kwargs):
	room = Room.objects.get(slug=kwargs['room_slug'], hotel__slug=kwargs['hotel_slug'])

	room.checked_in = False
	room.is_booked = False
	room.save()

	return HttpResponse('<h1>Thank you for lodging with us... come back again</h1>')

# Todo: I need to create a view that shows all the rooms i have booked and i have checked  into.
