from django.db import models
from helpers.models import TrackingModel

from django.urls import reverse
from django.template.defaultfilters import slugify


def get_hotel_image_filepath(self, *args, **kwargs):
    return f"hotel_images/{self.slug}/{'display_image.png'}"


def get_default_hotel_image():
    return 'images/default.png'


class Location(TrackingModel):
    name = models.CharField(max_length=120)

    def __str__(self):
        return f'{self.name}'


class Hotel(TrackingModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField()
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    hotel_location = models.CharField(max_length=3000)
    phone = models.IntegerField()
    email = models.EmailField()
    display_image = models.ImageField(max_length=255, upload_to=get_hotel_image_filepath, null=True, blank=True,
                                      default=get_default_hotel_image)
    number_of_rooms = models.IntegerField()
    number_of_booked_rooms = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    no_rooms_available = models.BooleanField(default=False)
    description = models.CharField(max_length=150)
    full_description = models.TextField()
    date_of_hotel_profile_update = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('booking:book_a_room', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'

# Todo: I need to add a range value in the number of rooms so it does not exceeds 50 and the number of rooms is not lower than 5
