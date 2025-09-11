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
    list_filter = ('created_at',)
    search_fields = ('participants_id__email', 'participants_id__first_name')
    ordering = ('-created_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'sender', 'conversation', 'sent_at')
    list_filter = ('sent_at', 'sender__role')
    search_fields = ('sender__email', 'message_body')
    ordering = ('-sent_at',)