from django.db import models 
from django.contrib.auth.models import User

from registration.models import Hotel

from helpers.models import TrackingModel

class RoomBooking(TrackingModel):
	hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
	guest = models.ForeignKey(User, on_delete=models.CASCADE)
	date_booked = models.DateTimeField(auto_now=True, null=True)
	date_to_check_in = models.DateField(null=True)
	date_to_check_out = models.DateField(null=True)

	def __str__(self):
		return f'{ self.guest } booked a room at { self.hotel }'


# I need to put a room number when booking a hotel maybe later along the code...
