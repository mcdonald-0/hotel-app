from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.http import HttpResponse

from booking.models import RoomBooking
from booking.forms import BookingARoomForm


from registration.models import Hotel




def index(request, *args, **kwargs):
	hotel_list = Hotel.objects.all()

	context = {
		'hotels': hotel_list,
	}

	return render(request, 'booking/index.html', context)


def book_a_room(request, *args, **kwargs):
	hotel_slug = kwargs['slug']
	hotel = Hotel.objects.get(slug=hotel_slug)

	form = BookingARoomForm()

	if request.method == 'POST':
		form = BookingARoomForm(request.POST)
		if form.is_valid():
			RoomBooking.objects.create(hotel=hotel, guest=request.user, **form.cleaned_data)

		return HttpResponse('<h1>You just booked a hotel</h1>')


	context = {
		'room': hotel,
		'form': form
	}

	return render(request, 'booking/booking.html', context)

