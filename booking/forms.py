from datetime import date, timedelta

from django import forms
from django.forms import ModelForm
from django.forms.widgets import NumberInput

from django.contrib.admin.widgets import AdminDateWidget


from booking.models import RoomBooking
from registration.models import Hotel



today = date.today()
tommorow = today + timedelta(days=1)


class BookingARoomForm(ModelForm):
	date_to_check_in = forms.DateField(widget=forms.TextInput(attrs={'min': today, 'value': today, 'type': 'date'}), required=True)
	date_to_check_out = forms.DateField(widget=forms.TextInput(attrs={'min': today, 'value': tommorow, 'type': 'date'}), required=True)


	class Meta:
		model = RoomBooking
		fields = ['date_to_check_in', 'date_to_check_out']



