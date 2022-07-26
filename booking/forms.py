from datetime import date, timedelta

from django import forms
from django.forms import ModelForm

from booking.models import RoomBooking, Room

today = date.today()
tomorrow = today + timedelta(days=1)

a_year_from_today = today + timedelta(days=365)
a_year_from_tomorrow = a_year_from_today + timedelta(days=1)


class BookingARoomForm(ModelForm):
	date_to_check_in = forms.DateField(widget=forms.TextInput(attrs={'min': today, 'max': a_year_from_today, 'value': today, 'type': 'date'}), required=True)
	date_to_check_out = forms.DateField(widget=forms.TextInput(attrs={'min': today, 'max': a_year_from_tomorrow, 'value': tomorrow, 'type': 'date'}), required=True)
	room_booked = forms.ModelChoiceField(queryset=Room.objects.none(), empty_label="Select the room you want to book")

	# This down here helps to filter the room objects by the hotel.
	# That is when you want to book a room, it would only show the number of rooms in the hotel rather than all the hotel object
	def __init__(self, *args, **kwargs):
		hotel_slug = kwargs.pop('hotel_slug')
		room_type_slug = kwargs.pop('room_type_slug')
		super(BookingARoomForm, self).__init__(*args, **kwargs)
		self.fields['room_booked'].queryset = Room.objects.filter(hotel__slug=hotel_slug, room_type__slug=room_type_slug, is_booked=False, checked_in=False).order_by('room_number')

	class Meta:
		model = RoomBooking
		fields = ['date_to_check_in', 'date_to_check_out', 'room_booked']


class CheckInARoomForm(ModelForm):
	checked_in = forms.BooleanField(widget=forms.CheckboxInput())

	class Meta:
		model = Room
		fields = ['checked_in']