"""hotel_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from django.views import i18n

urlpatterns = [
    path('', include('registration.urls')),
    path('booking/', include('booking.urls')),
    path('create/', include('authentication.urls')),
    path('payment/', include('payment.urls')),

    # path('admin/', admin.site.urls),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('who-are-you/i-am-the-admin/', admin.site.urls),

    # path('jsi18n/', i18n.JavaScriptCatalog.as_view(), name='jsi18n'),

] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG: 
    
    import debug_toolbar
    urlpatterns = [
        path('__debug_panel__/', include(debug_toolbar.urls)),
    ] + urlpatterns


admin.site.site_header = "Hotel App"
admin.site.site_title = "Hotel App Inc. Administration"
admin.site.index_title = "Administration"
