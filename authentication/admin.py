from django.contrib import admin

from authentication.models import User, Guest


class UserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_email_verified', 'date_joined')
    list_filter = ['is_email_verified']


admin.site.register(User, UserAdmin)
admin.site.register(Guest)
