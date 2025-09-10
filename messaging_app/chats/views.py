from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer, 
    ConversationSerializer, 
    ConversationListSerializer,
    MessageSerializer,
    MessageCreateSerializer,
    ConversationCreateSerializer
)
from .permissions import (
    IsParticipantOfConversation,
    IsConversationParticipant,
    IsMessageSenderOrConversationParticipant,
    IsOwnerOrAdmin,
    CanAccessOwnData
)
from .pagination import MessagePagination, ConversationPagination, UserPagination
from .filters import MessageFilter, ConversationFilter, UserFilter


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations
    """
    permission_classes = [IsParticipantOfConversation]
    pagination_class = ConversationPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ConversationFilter
    search_fields = ['participants_id__first_name', 'participants_id__last_name', 'participants_id__email']
    ordering_fields = ['created_at', 'participants_id__first_name']
    ordering = ['-created_at']
    
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
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['message_body', 'sender__first_name', 'sender__last_name', 'sender__email']
    ordering_fields = ['sent_at', 'sender__first_name', 'message_body']
    ordering = ['-sent_at']
    
    def get_queryset(self):
        """
        Return messages from conversations where the current user is a participant
        """
        # Handle nested router parameter
        conversation_pk = self.kwargs.get('conversation_pk')
        if conversation_pk:
            # Filter messages for specific conversation
            try:
                conversation = Conversation.objects.get(
                    conversation_id=conversation_pk,
                    participants_id=self.request.user
                )
                return Message.objects.filter(conversation=conversation)
            except Conversation.DoesNotExist:
                return Message.objects.none()
        
        # Return all messages for user's conversations
        user_conversations = Conversation.objects.filter(participants_id=self.request.user)
        return Message.objects.filter(conversation__in=user_conversations)
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        """
        if self.action == 'create':
            return MessageCreateSerializer
        return MessageSerializer
    
    def list(self, request, **kwargs):
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
    
    @action(detail=False, methods=['get'])
    def by_sender(self, request):
        """
        Get messages filtered by sender
        """
        sender_id = request.query_params.get('sender_id')
        if not sender_id:
            return Response(
                {'error': 'sender_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        messages = self.get_queryset().filter(sender__user_id=sender_id)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_date_range(self, request):
        """
        Get messages filtered by date range
        """
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {'error': 'start_date and end_date parameters are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        messages = self.get_queryset().filter(
            sent_at__date__gte=start_date,
            sent_at__date__lte=end_date
        )
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        Search messages by content
        """
        query = request.query_params.get('q')
        if not query:
            return Response(
                {'error': 'q parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        messages = self.get_queryset().filter(message_body__icontains=query)
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = UserFilter
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['first_name', 'last_name', 'email', 'created_at', 'role']
    ordering = ['first_name']
    
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
