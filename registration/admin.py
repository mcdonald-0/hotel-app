from django.contrib import admin

from registration.models import Location, Hotel


class HotelAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Hotel information', {'fields': ['name', 'slug', 'location', 'hotel_location', 'phone', 'email']}),
        ('Hotel details', {'fields': ['number_of_rooms', 'display_image', 'description', 'full_description']}),
        ('More details', {'fields': ['no_rooms_available', 'rating', 'number_of_booked_rooms', 'created_at', 'date_of_hotel_profile_update']}),

    ]
    list_display = ('name', 'location', 'no_rooms_available')
    readonly_fields = ('id', 'date_of_hotel_profile_update', 'rating', 'no_rooms_available', 'number_of_booked_rooms', 'created_at')
    list_filter = ['location', 'no_rooms_available', 'date_of_hotel_profile_update']
    search_fields = ['location__name', 'name']
    prepopulated_fields = {'slug': ('name',)} 


admin.site.register(Location)
admin.site.register(Hotel, HotelAdmin)
