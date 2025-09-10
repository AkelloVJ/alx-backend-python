"""
Listings app URLs.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListingListView.as_view(), name='listing-list'),
]
