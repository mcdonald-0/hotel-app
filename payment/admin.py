from django.contrib import admin

from payment.models import Payment, HotelBankAccount


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('room_information', 'amount', 'verified')
    list_filter = ['verified']
    readonly_fields = ['amount', 'ref', 'guest', 'room_information', 'verified']


class HotelBankAccountAdmin(admin.ModelAdmin):
    list_display = ('account_name', 'account_number', 'bank_name', '__str__')
    readonly_fields = ['hotel', 'bank_code']


admin.site.register(Payment, PaymentAdmin)
admin.site.register(HotelBankAccount, HotelBankAccountAdmin)
