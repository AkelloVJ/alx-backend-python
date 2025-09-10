from django.contrib import admin
from .models import Message, MessageHistory, Notification, Conversation


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'content_preview', 'timestamp', 'edited', 'read', 'parent_message']
    list_filter = ['edited', 'read', 'timestamp', 'sender', 'receiver']
    search_fields = ['content', 'sender__username', 'receiver__username']
    readonly_fields = ['timestamp']
    raw_id_fields = ['sender', 'receiver', 'parent_message']
    
    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ['message', 'old_content_preview', 'edited_at', 'edited_by']
    list_filter = ['edited_at', 'edited_by']
    search_fields = ['old_content', 'message__content', 'edited_by__username']
    readonly_fields = ['edited_at']
    raw_id_fields = ['message', 'edited_by']
    
    def old_content_preview(self, obj):
        return obj.old_content[:50] + "..." if len(obj.old_content) > 50 else obj.old_content
    old_content_preview.short_description = 'Old Content Preview'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message_preview', 'created_at', 'read']
    list_filter = ['read', 'created_at', 'user']
    search_fields = ['user__username', 'message__content']
    readonly_fields = ['created_at']
    raw_id_fields = ['user', 'message']
    
    def message_preview(self, obj):
        return obj.message.content[:30] + "..." if len(obj.message.content) > 30 else obj.message.content
    message_preview.short_description = 'Message Preview'


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'participants_list', 'created_at', 'updated_at', 'message_count']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['participants__username']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['participants']
    
    def participants_list(self, obj):
        return ', '.join([p.username for p in obj.participants.all()])
    participants_list.short_description = 'Participants'
    
    def message_count(self, obj):
        return obj.get_messages().count()
    message_count.short_description = 'Message Count'