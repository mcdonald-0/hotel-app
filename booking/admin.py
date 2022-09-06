from django.contrib import admin
from booking.models import RoomType, RoomBooking, Room, RoomTypeImage


class RoomTypeImageInline(admin.TabularInline):
    model = RoomTypeImage
    extra = 1
    exclude = ['thumbnail']


class RoomTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic information', {'fields': ['name', 'hotel', 'price_per_night']}),
        ('Status', {'fields': ['number_of_rooms', 'number_of_booked_rooms', 'no_rooms_available']}),
    ]
    list_display = ('__str__', 'no_rooms_available')
    inlines = [RoomTypeImageInline]


class RoomAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Important information', {'fields': ['hotel', 'slug', 'room_type', 'room_number', 'room_information']}),
        ('Room status', {'fields': ['is_booked', 'checked_in']}),
    ]
    list_display = ('__str__', 'is_booked', 'checked_in')
    list_filter = ['is_booked', 'checked_in', 'hotel__name', 'hotel__location']


class RoomBookingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Important information', {'fields': ['hotel', 'room_booked', 'room_type', 'guest']}),
        ('Date information', {'fields': ['date_to_check_in', 'date_to_check_out']}),
    ]
    list_display = ('__str__', 'date_to_check_in', 'date_to_check_out', 'cost')
    list_filter = ['date_booked']


admin.site.register(RoomTypeImage)
admin.site.register(RoomType, RoomTypeAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomBooking, RoomBookingAdmin)
