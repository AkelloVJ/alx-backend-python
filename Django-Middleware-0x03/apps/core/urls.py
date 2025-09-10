"""
Core app URLs for middleware testing endpoints.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.TestView.as_view(), name='test'),
    path('messages/', views.MessageView.as_view(), name='messages'),
    path('conversations/', views.ConversationView.as_view(), name='conversations'),
]
