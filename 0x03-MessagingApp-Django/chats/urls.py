from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'chats'

urlpatterns = [
    # Authentication endpoints
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/profile/', views.user_profile, name='user_profile'),
    
    # Conversation endpoints
    path('conversations/', views.ConversationListCreateView.as_view(), name='conversation-list'),
    path('conversations/<uuid:pk>/', views.ConversationDetailView.as_view(), name='conversation-detail'),
    
    # Message endpoints
    path('messages/', views.MessageListCreateView.as_view(), name='message-list'),
    path('messages/<uuid:pk>/', views.MessageDetailView.as_view(), name='message-detail'),
]