from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    # Explicit CharField usage
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'phone_number',
            'role',
            'created_at',
            'date_joined',
            'last_login',
            'is_active',
            'is_staff',
            'is_superuser'
        ]
        read_only_fields = ['user_id', 'created_at', 'date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        """
        Create a new user with hashed password
        """
        password = validated_data.pop('password', None)
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update user instance
        """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message model
    """
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'sender_id',
            'message_body',
            'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at']

    def create(self, validated_data):
        """
        Create a new message
        """
        sender_id = validated_data.pop('sender_id')
        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Sender user does not exist")
        
        validated_data['sender'] = sender
        return Message.objects.create(**validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation model
    """
    participants_id = UserSerializer(read_only=True)
    participants_id_id = serializers.UUIDField(write_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants_id',
            'participants_id_id',
            'created_at',
            'messages',
            'message_count'
        ]
        read_only_fields = ['conversation_id', 'created_at']

    def get_message_count(self, obj):
        """
        Get the number of messages in this conversation
        """
        return obj.messages.count()

    def create(self, validated_data):
        """
        Create a new conversation
        """
        participants_id = validated_data.pop('participants_id_id')
        try:
            participant = User.objects.get(user_id=participants_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Participant user does not exist")
        
        validated_data['participants_id'] = participant
        return Conversation.objects.create(**validated_data)


class ConversationListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for conversation lists (without messages)
    """
    participants_id = UserSerializer(read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants_id',
            'created_at',
            'message_count',
            'last_message'
        ]

    def get_message_count(self, obj):
        """
        Get the number of messages in this conversation
        """
        return obj.messages.count()

    def get_last_message(self, obj):
        """
        Get the last message in this conversation
        """
        last_message = obj.messages.order_by('-sent_at').first()
        if last_message:
            return {
                'message_id': last_message.message_id,
                'message_body': last_message.message_body[:100] + '...' if len(last_message.message_body) > 100 else last_message.message_body,
                'sender': last_message.sender.first_name + ' ' + last_message.sender.last_name,
                'sent_at': last_message.sent_at
            }
        return None


class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating messages
    """
    class Meta:
        model = Message
        fields = [
            'sender',
            'conversation',
            'message_body'
        ]

    def create(self, validated_data):
        """
        Create a new message
        """
        return Message.objects.create(**validated_data)


class ConversationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating conversations
    """
    class Meta:
        model = Conversation
        fields = [
            'participants_id'
        ]

    def create(self, validated_data):
        """
        Create a new conversation
        """
        return Conversation.objects.create(**validated_data)
