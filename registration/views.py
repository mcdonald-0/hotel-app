from django.shortcuts import render
from django.http import HttpResponse

from registration.models import Hotel


def homepage(request, *args, **kwargs):
	hotel_list = Hotel.objects.all()

	context = {
		'hotels': hotel_list,
	}

	return render(request, 'registration/homepage.html', context)
