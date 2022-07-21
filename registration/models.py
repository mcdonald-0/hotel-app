from django.db import models
from helpers.models import TrackingModel

class Hotel(TrackingModel):
    name = models.CharField(max_length=120, null=True)

    def __str__(self):
        return f'{ self.name }'
