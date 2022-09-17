from django import forms
from django.contrib import admin

from registration.models import Location, Hotel
from booking.models import RoomType
from payment.models import HotelBankAccount

from phonenumber_field.widgets import PhoneNumberPrefixWidget


class HotelAccountInline(admin.TabularInline):
    model = HotelBankAccount


class RoomTypeInline(admin.TabularInline):
    model = RoomType
    extra = 1
    exclude = ['number_of_booked_rooms', 'slug', 'no_rooms_available']


# This gives a dropdown of available countries regional code
class HotelAdminForm(forms.ModelForm):
    class Meta:
        model = Hotel
        widgets = {
            'phone_number': PhoneNumberPrefixWidget(),
        }
        fields = '__all__'


class HotelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Hotel information', {'fields': ['name', 'location', 'hotel_location', 'phone_number', 'email'], 'classes': ('wide', 'extrapretty'), 'description': "This contain the hotel's <b>basic</b> information"}),
        ('Hotel details', {'fields': ['display_image', 'description', 'full_description'], 'classes': ('wide', 'extrapretty'), 'description': "This contain <b>detail</b> about the hotel"}),
        ('More details', {'fields': ['number_of_rooms', 'number_of_booked_rooms', 'no_rooms_available', 'rating', 'created_at', 'date_of_hotel_profile_update', 'slug'], 'classes': ('collapse',)}),
    ]
    # form = HotelAdminForm
    inlines = [RoomTypeInline, HotelAccountInline]
    list_display = ('name', 'location', 'no_rooms_available')
    readonly_fields = ['id', 'number_of_rooms', 'slug', 'date_of_hotel_profile_update', 'rating', 'no_rooms_available', 'number_of_booked_rooms', 'created_at']
    list_filter = ['no_rooms_available', 'date_of_hotel_profile_update']
    search_fields = ['location__name', 'name']

    # prepopulated_fields = {'slug': ('name',)}


admin.site.register(Location)
admin.site.register(Hotel, HotelAdmin)
