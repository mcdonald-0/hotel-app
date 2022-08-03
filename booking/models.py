from django.db import models 
from django.contrib.auth.models import User

from registration.models import Hotel

from helpers.models import TrackingModel


class RoomBooking(TrackingModel):
	hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
	room_booked = models.ForeignKey('Room', on_delete=models.CASCADE)
	guest = models.ForeignKey(User, on_delete=models.CASCADE)
	date_booked = models.DateTimeField(auto_now=True)
	date_to_check_in = models.DateField()
	date_to_check_out = models.DateField()

	def __str__(self):
		return f'{ self.guest } booked a room at { self.hotel }'


class Room(TrackingModel):
	hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
	room_information = models.ForeignKey(RoomBooking, on_delete=models.CASCADE, null=True)
	room_number = models.IntegerField()
	is_booked = models.BooleanField(default=False)
	checked_in = models.BooleanField(default=False)

	def __str__(self):
		return f'Room { self.room_number } of { self.hotel }'

# I need to put a room number when booking a hotel maybe later along the code...
