from django.db import models 
from django.contrib.auth.models import User

from registration.models import Hotel

from helpers.models import TrackingModel

class RoomBooking(TrackingModel):
	hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
	guest = models.OneToOneField(User, on_delete=models.CASCADE)
	is_booked = models.BooleanField(default=False)


# I need to put a room number when booking a hotel maybe later along the code...
