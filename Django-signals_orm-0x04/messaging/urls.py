from django.urls import path
from . import views

urlpatterns = [
    # Message endpoints
    path('messages/send/', views.send_message, name='send_message'),
    path('messages/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('messages/<int:message_id>/read/', views.mark_as_read, name='mark_as_read'),
    path('messages/<int:message_id>/thread/', views.message_thread, name='message_thread'),
    path('messages/<int:message_id>/history/', views.message_history, name='message_history'),
    path('messages/unread/', views.unread_messages, name='unread_messages'),
    
    # Conversation endpoints
    path('conversations/', views.conversations_list, name='conversations_list'),
    path('conversations/<int:conversation_id>/messages/', views.conversation_messages, name='conversation_messages'),
    
    # Notification endpoints
    path('notifications/', views.user_notifications, name='user_notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    # User management
    path('user/delete/', views.delete_user_account, name='delete_user_account'),
]
