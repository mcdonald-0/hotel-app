from django.contrib import admin
from booking.models import RoomType, RoomBooking, Room, Image


class RoomImageInline(admin.TabularInline):
    model = Image
    extra = 4


class RoomAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Important information', {'fields': ['hotel', 'slug', 'room_type', 'room_number', 'room_information']}),
        ('Room status', {'fields': ['is_booked', 'checked_in']}),
    ]
    inlines = [RoomImageInline]
    list_display = ('__str__', 'is_booked', 'checked_in')
    list_filter = ['is_booked', 'checked_in', 'hotel__name', 'hotel__location']


class RoomBookingAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Important information', {'fields': ['hotel', 'room_booked', 'room_type', 'guest']}),
        ('Date information', {'fields': ['date_to_check_in', 'date_to_check_out']}),
    ]
    list_display = ('__str__', 'date_to_check_in', 'date_to_check_out')
    list_filter = ['date_booked']


admin.site.register(Image)
admin.site.register(RoomType)
admin.site.register(Room, RoomAdmin)
admin.site.register(RoomBooking, RoomBookingAdmin)
