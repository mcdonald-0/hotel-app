from django import forms
from django.forms import ModelForm
from django.contrib.admin import widgets
from django.contrib.admin.widgets import AdminDateWidget


from booking.models import RoomBooking
from registration.models import Hotel

class BookingARoomForm(ModelForm):
	is_booked = forms.BooleanField()
	date_checked_out = forms.DateField(widget=AdminDateWidget)

	class Meta:
		model = RoomBooking
		fields = ['is_booked', 'date_checked_out']

	# def __init__(self, *args, **kwargs):
	# 	super(BookingARoomForm, self).__init__(*args, **kwargs)
	# 	self.fields['date_checked_out'].widget = widgets.AdminDateWidget()



