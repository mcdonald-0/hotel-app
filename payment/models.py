import secrets

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models

from registration.models import Hotel

from booking.models import Guest, RoomBooking

from helpers.models import TrackingModel

from payment.paystack import PayStack
from payment.bank_list import BANK_LIST, BANK_LIST_WITH_CODES, get_key_from_dict_value


class HotelBankAccount(TrackingModel):
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE, related_name='bank_account')
    account_name = models.CharField(max_length=100, unique=True)
    account_number = models.CharField(max_length=15, validators=[MinLengthValidator(8)], unique=True)
    paystack_subaccount_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    bank_name = models.CharField(max_length=200, choices=BANK_LIST)
    bank_code = models.CharField(max_length=300)
    response = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.hotel.name} bank account"

    def create_hotel_subaccount(self, *args, **kwargs):
        bank_list = dict(BANK_LIST_WITH_CODES)
        bank_code = get_key_from_dict_value(self.bank_name, bank_list)
        self.bank_code = bank_code

        # This is to create the hotel sub account if it does not already has one
        while not self.paystack_subaccount_number:
            paystack = PayStack()
            status, result, data = paystack.create_hotel_sub_account(
                business_name = self.account_name,
                account_number = self.account_number,
                bank_code = self.bank_code,
                percentage_charge = 10
                )

            self.response = status, result
            self.paystack_subaccount_number = data['subaccount_code']


    def save(self, *args, **kwargs):
        self.create_hotel_subaccount()
        return super().save(*args, **kwargs)


class Payment(TrackingModel):
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200, unique=True)
    guest = models.ForeignKey(Guest, on_delete=models.SET_NULL, null=True)
    room_information = models.ForeignKey(RoomBooking, on_delete=models.SET_NULL, null=True)
    verified = models.BooleanField(default=False)
    authorization_url = models.CharField(max_length=200, null=True, blank=True)
    response = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment {self.amount}"

    def amount_value(self):
        return self.amount * 100

    def save(self, *args, **kwargs):
        while not self.response:
            paystack = PayStack()

            status, result, data = paystack.initialize_payment(
                email=self.guest.email, 
                amount=self.amount * 100, 
                subaccount=self.room_information.hotel.bank_account.paystack_subaccount_number
            )
            self.response = status, result, data
            self.authorization_url = data['authorization_url']

        while not self.ref:
            ref = secrets.token_urlsafe(60)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
                
        return super().save(*args, **kwargs)

    # def initialize_payment(self):

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
