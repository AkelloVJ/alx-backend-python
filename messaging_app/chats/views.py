from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer, 
    ConversationSerializer, 
    ConversationListSerializer,
    MessageSerializer,
    MessageCreateSerializer,
    ConversationCreateSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return conversations where the current user is a participant
        """
        return Conversation.objects.filter(participants_id=self.request.user)
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == 'list':
            return ConversationListSerializer
        elif self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer
    
    def list(self, request):
        """
        List all conversations for the authenticated user
        """
        conversations = self.get_queryset()
        serializer = self.get_serializer(conversations, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """
        Create a new conversation
        """
        # For now, create a conversation with the current user as participant
        # In a real app, you might want to add other participants
        conversation_data = {
            'participants_id': request.user.user_id
        }
        serializer = self.get_serializer(data=conversation_data)
        if serializer.is_valid():
            conversation = serializer.save()
            # Return full conversation details
            full_serializer = ConversationSerializer(conversation)
            return Response(full_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific conversation with its messages
        """
        conversation = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """
        Add a participant to an existing conversation
        Note: This is a placeholder since our current model only supports one participant
        """
        conversation = get_object_or_404(self.get_queryset(), pk=pk)
        # In a real implementation, you would add logic to add participants
        return Response(
            {'message': 'Adding participants not implemented in current model'}, 
            status=status.HTTP_501_NOT_IMPLEMENTED
        )


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return messages from conversations where the current user is a participant
        """
        user_conversations = Conversation.objects.filter(participants_id=self.request.user)
        return Message.objects.filter(conversation__in=user_conversations)
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer
    
    def list(self, request):
        """
        List all messages for the authenticated user
        """
        messages = self.get_queryset().order_by('-sent_at')
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        """
        Create a new message in a conversation
        """
        # Ensure the user is a participant in the conversation
        conversation_id = request.data.get('conversation')
        if not conversation_id:
            return Response(
                {'error': 'conversation field is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id,
                participants_id=request.user
            )
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found or access denied'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        message_data = {
            'sender': request.user.user_id,
            'conversation': conversation.conversation_id,
            'message_body': request.data.get('message_body', '')
        }
        
        serializer = self.get_serializer(data=message_data)
        if serializer.is_valid():
            message = serializer.save()
            # Return full message details
            full_serializer = MessageSerializer(message)
            return Response(full_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific message
        """
        message = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = MessageSerializer(message)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_conversation(self, request):
        """
        Get messages for a specific conversation
        """
        conversation_id = request.query_params.get('conversation_id')
        if not conversation_id:
            return Response(
                {'error': 'conversation_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id,
                participants_id=request.user
            )
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found or access denied'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        messages = Message.objects.filter(conversation=conversation).order_by('sent_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Get recent messages for the authenticated user
        """
        limit = int(request.query_params.get('limit', 10))
        messages = self.get_queryset().order_by('-sent_at')[:limit]
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return users based on permissions
        """
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(user_id=self.request.user.user_id)
    
    def list(self, request):
        """
        List users (admin only or own profile)
        """
        if not request.user.is_staff:
            # Non-staff users can only see their own profile
            serializer = self.get_serializer([request.user], many=True)
            return Response(serializer.data)
        
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        Retrieve a specific user
        """
        if not request.user.is_staff and str(request.user.user_id) != str(pk):
            return Response(
                {'error': 'Access denied'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = get_object_or_404(User, user_id=pk)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    def update(self, request, pk=None):
        """
        Update user profile
        """
        if str(request.user.user_id) != str(pk):
            return Response(
                {'error': 'Can only update your own profile'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        user = get_object_or_404(User, user_id=pk)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
