import secrets

from django.core.validators import MinLengthValidator
from django.db import models

from registration.models import Hotel

from booking.models import Guest, RoomBooking

from helpers.models import TrackingModel

from payment.paystack import PayStack


class HotelBankAccount(TrackingModel):
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=15, validators=[MinLengthValidator(8)])
    bank_name = models.CharField(max_length=200)
    bank_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.hotel.name} bank account"


class Payment(TrackingModel):
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True)
    room_information = models.ForeignKey(RoomBooking, on_delete=models.SET_NULL, null=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment {self.amount}"

    def amount_value(self):
        return self.amount * 100

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(60)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False


