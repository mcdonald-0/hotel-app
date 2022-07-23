from django.db import models
from helpers.models import TrackingModel

from django.urls import reverse
from django.template.defaultfilters import slugify



class Location(TrackingModel):
    name = models.CharField(max_length=120)
    
    def __str__(self):
        return f'{ self.name }'

class Hotel(TrackingModel):
    name = models.CharField(max_length=120, null=True)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    hotel_location = models.CharField(max_length=3000, null=True)
    phone = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    number_of_rooms = models.IntegerField(null=True)
    number_of_booked_rooms = models.IntegerField(null=True)
    rating = models.IntegerField(null=True)
    no_rooms_available = models.BooleanField(default=False)
    date_of_hotel_profile_update = models.DateTimeField(auto_now_add=True, null=True)

    slug = models.SlugField(null=True)


    # def get_absolute_url(self):
    #     return reverse('questions:question', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): 
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{ self.name }'
