"""
Users app URLs for testing role permissions.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='user-list'),
    path('admin/', views.AdminView.as_view(), name='admin'),
]
