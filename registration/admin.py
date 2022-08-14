from django.contrib import admin

from registration.models import Location, Hotel
from booking.models import RoomType


class RoomTypeInline(admin.TabularInline):
    model = RoomType
    extra = 1
    exclude = ['number_of_booked_rooms']


class HotelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Hotel information', {'fields': ['name', 'location', 'hotel_location', 'phone', 'email'], 'classes': ('wide', 'extrapretty'), 'description': "This contain the hotel's <b>basic</b> information"}),
        ('Hotel details', {'fields': ['number_of_rooms', 'display_image', 'description', 'full_description'], 'classes': ('wide', 'extrapretty'), 'description': "This contain <b>detail</b> about the hotel"}),
        ('More details', {'fields': ['no_rooms_available', 'rating', 'number_of_booked_rooms', 'created_at', 'date_of_hotel_profile_update', 'slug'], 'classes': ('collapse',)}),
    ]
    inlines = [RoomTypeInline]
    list_display = ('name', 'location', 'no_rooms_available')
    readonly_fields = ['id', 'date_of_hotel_profile_update', 'rating', 'no_rooms_available', 'number_of_booked_rooms', 'created_at']
    list_filter = ['no_rooms_available', 'date_of_hotel_profile_update']
    search_fields = ['location__name', 'name']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Location)
admin.site.register(Hotel, HotelAdmin)
