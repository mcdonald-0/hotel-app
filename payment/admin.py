from django.contrib import admin

from payment.models import Payment, HotelBankAccount


class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ['amount', 'ref', 'guest', 'room_information', 'verified']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(HotelBankAccount)
