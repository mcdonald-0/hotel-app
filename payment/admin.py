from django.contrib import admin

from payment.models import Payment, HotelBankAccount


class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ['amount', 'ref', 'guest', 'room_information', 'verified']


class HotelBankAccountAdmin(admin.ModelAdmin):
    readonly_fields = ['hotel', 'bank_code']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(HotelBankAccount, HotelBankAccountAdmin)
