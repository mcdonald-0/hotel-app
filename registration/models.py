from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models
from helpers.models import TrackingModel

from django.urls import reverse
from django.template.defaultfilters import slugify

from phonenumber_field.modelfields import PhoneNumberField


class Location(TrackingModel):
    name = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.name}'


def get_hotel_image_filepath(self, *args, **kwargs):
    return f"hotel-images/{self.slug}/{'display-image.png'}"


def get_default_hotel_image():
    return 'images/default.png'


class Hotel(TrackingModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField()
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    hotel_location = models.CharField(max_length=3000)
    phone_number = PhoneNumberField(unique=True, null=False, blank=False)
    email = models.EmailField(unique=True)
    display_image = models.ImageField(max_length=255, upload_to=get_hotel_image_filepath, default=get_default_hotel_image)
    number_of_rooms = models.IntegerField(default=0, validators=[
        MaxValueValidator(25), MinValueValidator(5)
    ])
    number_of_booked_rooms = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    no_rooms_available = models.BooleanField(default=False)
    description = models.CharField(max_length=150)
    full_description = models.TextField()
    date_of_hotel_profile_update = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('booking:view_rooms', kwargs={'hotel_slug': self.slug})

    def save(self, *args, **kwargs):
        # This makes sure that if there is no image, it results to the default image
        if not self.display_image:
            self.display_image = get_default_hotel_image()
        
        # This here makes it that the number of rooms is equal to the total of the rooms under each room types in the hotel
        for i in self.room_types.all():
            self.number_of_rooms += i.number_of_rooms

        # This slugifies the name of the hotel to be for the url
        if not self.slug:
            self.slug = slugify(self.name)

        # This is the real save function
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
