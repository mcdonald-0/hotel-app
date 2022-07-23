from django import forms
from django.forms import ModelForm

from booking.models import RoomBooking
from registration.models import Hotel

class BookingARoomForm(ModelForm):
	is_booked = forms.BooleanField()

	class Meta:
		model = RoomBooking
		fields = ['is_booked']


