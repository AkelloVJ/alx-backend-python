from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification, Conversation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    parent_message = serializers.PrimaryKeyRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'receiver', 'content', 'timestamp', 
            'edited', 'read', 'parent_message', 'replies'
        ]
        read_only_fields = ['id', 'timestamp', 'edited']
    
    def get_replies(self, obj):
        """Get direct replies to this message."""
        replies = obj.replies.all().order_by('timestamp')
        return MessageSerializer(replies, many=True).data


class MessageHistorySerializer(serializers.ModelSerializer):
    edited_by = UserSerializer(read_only=True)
    
    class Meta:
        model = MessageHistory
        fields = ['id', 'old_content', 'edited_at', 'edited_by']


class NotificationSerializer(serializers.ModelSerializer):
    message = MessageSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'message', 'created_at', 'read']


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'created_at', 'updated_at', 'message_count']
    
    def get_message_count(self, obj):
        return obj.get_messages().count()


class SendMessageSerializer(serializers.Serializer):
    receiver_id = serializers.IntegerField()
    content = serializers.CharField(max_length=1000)
    parent_message_id = serializers.IntegerField(required=False, allow_null=True)
    
    def validate_receiver_id(self, value):
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Receiver not found")
        return value
    
    def validate_parent_message_id(self, value):
        if value is not None:
            try:
                Message.objects.get(id=value)
            except Message.DoesNotExist:
                raise serializers.ValidationError("Parent message not found")
        return value


class EditMessageSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=1000)
