from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone_number', 'role']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            username=validated_data['email'],  # Use email as username
            **validated_data
        )
        return user


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_id', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.first_name', read_only=True)
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_name', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sender', 'sent_at']

    def create(self, validated_data):
        # Set the sender to the current user
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)