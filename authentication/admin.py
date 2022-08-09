from django.contrib import admin

from authentication.models import User, Guest

admin.site.register(User)
admin.site.register(Guest)
