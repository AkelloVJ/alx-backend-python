from django.contrib import admin
from .models import User, Conversation, Message


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-created_at',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('conversation_id', 'participants_id', 'created_at')
    list_filter = ('created_at', 'participants_id__role')
    search_fields = ('conversation_id', 'participants_id__first_name', 'participants_id__last_name')
    ordering = ('-created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'conversation', 'sent_at')
    list_filter = ('sent_at', 'conversation')
    search_fields = ('message_body', 'sender__first_name', 'sender__last_name')
    ordering = ('-sent_at',)
