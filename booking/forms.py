from datetime import date, timedelta

from django import forms
from django.forms import ModelForm
from django.forms.widgets import NumberInput

from django.contrib.admin.widgets import AdminDateWidget


from booking.models import RoomBooking

# from booking.views.book_a_room import hotel

import booking.views

global ROOMS


today = date.today()
tommorow = today + timedelta(days=1)


# CHOICES = [('1', 'First'), ('2', 'Second')]

a = ROOMS
CHOICES = []

for i in range(a):
    CHOICES.append((i+1, f'Room number {i+1}'))


print(CHOICES)


class BookingARoomForm(ModelForm):
	date_to_check_in = forms.DateField(widget=forms.TextInput(attrs={'min': today, 'value': today, 'type': 'date'}), required=True)
	date_to_check_out = forms.DateField(widget=forms.TextInput(attrs={'min': today, 'value': tommorow, 'type': 'date'}), required=True)
	room_number = forms.ChoiceField(choices=CHOICES)


	class Meta:
		model = RoomBooking
		fields = ['date_to_check_in', 'date_to_check_out']


a = 9
choices = []

for i in range(a):
    choices.append((i+1, f'Room number {i+1}'))


print(choices)
