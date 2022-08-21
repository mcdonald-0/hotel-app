from django.db import models

from django.template.defaultfilters import slugify

from registration.models import Hotel
from authentication.models import Guest, User

from helpers.models import TrackingModel


class RoomType(TrackingModel):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    hotel = models.ForeignKey(Hotel, related_name='room_types', on_delete=models.CASCADE, null=True)
    price_per_night = models.IntegerField()
    number_of_rooms = models.IntegerField()
    number_of_booked_rooms = models.IntegerField(default=0)
    no_rooms_available = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} at {self.hotel}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class RoomBooking(TrackingModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    room_booked = models.ForeignKey('Room', on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    date_booked = models.DateTimeField(auto_now=True)
    date_to_check_in = models.DateField()
    date_to_check_out = models.DateField()

    @property
    def duraton_of_stay(self):
        return self.date_to_check_out - self.date_to_check_in
    

    def __str__(self):
        return f'Booking of room {self.room_booked.room_number} at {self.hotel}'


class Room(TrackingModel):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    slug = models.SlugField()
    room_information = models.ForeignKey(RoomBooking, on_delete=models.SET_NULL, blank=True, null=True)
    room_number = models.IntegerField()
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    is_booked = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)

    def __str__(self):
        return f'{ self.room_type.name }{self.room_number} at {self.hotel}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'Room {self.room_number}')
        return super().save(*args, **kwargs)


def get_room_images_filepath(self, *args, **kwargs):
    return f"hotel-images/{self.room.hotel.slug}/{self.room.room_type.slug}-images/room-{self.room.room_number}-images/{'image.png'}"


class Image(TrackingModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    image = models.ImageField(max_length=255, upload_to=get_room_images_filepath, null=True, blank=True)



