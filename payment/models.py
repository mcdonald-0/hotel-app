import secrets

from django.db import models

from booking.models import Guest, RoomBooking

from helpers.models import TrackingModel


class Payment(TrackingModel):
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True)
    room_information = models.ForeignKey(RoomBooking, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"Payment {self.amount}"

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(60)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

