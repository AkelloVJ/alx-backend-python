"""
URL configuration for Django Middleware project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.core.urls')),
    path('api/users/', include('apps.users.urls')),
    path('api/listings/', include('apps.listings.urls')),
]
