from datetime import date, timedelta

from django import forms
from django.forms import ModelForm

from booking.models import RoomBooking, Room

today = date.today()
tomorrow = today + timedelta(days=1)


class BookingARoomForm(ModelForm):
	date_to_check_in = forms.DateField(widget=forms.TextInput(attrs={'min': today, 'value': today, 'type': 'date'}), required=True)
	date_to_check_out = forms.DateField(widget=forms.TextInput(attrs={'min': today, 'value': tomorrow, 'type': 'date'}), required=True)
	room_booked = forms.ModelChoiceField(queryset=Room.objects.all(), empty_label="Select the room you want to book")

	class Meta:
		model = RoomBooking
		fields = ['date_to_check_in', 'date_to_check_out', 'room_booked']


