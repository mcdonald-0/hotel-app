from django.contrib import admin

from registration.models import Location, Hotel

class HotelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)} 

admin.site.register(Location)
admin.site.register(Hotel, HotelAdmin)
