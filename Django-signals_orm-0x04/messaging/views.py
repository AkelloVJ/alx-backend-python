from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Prefetch
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Message, MessageHistory, Notification, Conversation
from .serializers import MessageSerializer, MessageHistorySerializer, NotificationSerializer
import json


@cache_page(60)  # Cache for 60 seconds
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation_messages(request, conversation_id):
    """
    Cached view to retrieve messages in a conversation.
    Uses select_related and prefetch_related for optimization.
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)
    
    # Check if user is a participant
    if request.user not in conversation.participants.all():
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Optimize queries with select_related and prefetch_related
    messages = conversation.get_messages().select_related(
        'sender', 'receiver', 'parent_message'
    ).prefetch_related(
        'replies__sender',
        'replies__receiver',
        'edit_history__edited_by'
    ).only(
        'id', 'content', 'timestamp', 'edited', 'read', 'parent_message_id',
        'sender__username', 'receiver__username'
    )
    
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_messages(request):
    """
    Get unread messages for the authenticated user using custom manager.
    """
    unread_messages = Message.unread.for_user(request.user).select_related(
        'sender', 'receiver'
    ).only(
        'id', 'content', 'timestamp', 'sender__username', 'receiver__username'
    )
    
    serializer = MessageSerializer(unread_messages, many=True)
    return Response({
        'unread_count': Message.unread.unread_count(request.user),
        'messages': serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_thread(request, message_id):
    """
    Get threaded conversation for a specific message.
    """
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user is involved in the conversation
    if request.user not in [message.sender, message.receiver]:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    # Get the root message (top-level message in the thread)
    root_message = message.parent_message if message.parent_message else message
    
    # Get all messages in the thread
    thread_messages = [root_message] + root_message.get_all_replies()
    
    serializer = MessageSerializer(thread_messages, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def message_history(request, message_id):
    """
    Get edit history for a specific message.
    """
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user is involved in the conversation
    if request.user not in [message.sender, message.receiver]:
        return Response({'error': 'Access denied'}, status=status.HTTP_403_FORBIDDEN)
    
    history = message.edit_history.select_related('edited_by').order_by('-edited_at')
    serializer = MessageHistorySerializer(history, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    """
    Send a new message.
    """
    data = request.data
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    parent_message_id = data.get('parent_message_id')
    
    if not receiver_id or not content:
        return Response({'error': 'Receiver ID and content are required'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        receiver = User.objects.get(id=receiver_id)
    except User.DoesNotExist:
        return Response({'error': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)
    
    parent_message = None
    if parent_message_id:
        try:
            parent_message = Message.objects.get(id=parent_message_id)
        except Message.DoesNotExist:
            return Response({'error': 'Parent message not found'}, status=status.HTTP_404_NOT_FOUND)
    
    message = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content,
        parent_message=parent_message
    )
    
    serializer = MessageSerializer(message)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_message(request, message_id):
    """
    Edit an existing message.
    """
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user is the sender
    if message.sender != request.user:
        return Response({'error': 'You can only edit your own messages'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    content = request.data.get('content')
    if not content:
        return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    message.content = content
    message.save()
    
    serializer = MessageSerializer(message)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, message_id):
    """
    Mark a message as read.
    """
    message = get_object_or_404(Message, id=message_id)
    
    # Check if user is the receiver
    if message.receiver != request.user:
        return Response({'error': 'You can only mark your own received messages as read'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    message.read = True
    message.save(update_fields=['read'])
    
    return Response({'status': 'Message marked as read'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user_account(request):
    """
    Delete the authenticated user's account.
    This will trigger the post_delete signal to clean up all related data.
    """
    user = request.user
    username = user.username
    
    # Delete the user (this will trigger the post_delete signal)
    user.delete()
    
    return Response({'message': f'User {username} and all related data have been deleted'}, 
                   status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_notifications(request):
    """
    Get notifications for the authenticated user.
    """
    notifications = Notification.objects.filter(user=request.user).select_related(
        'message__sender', 'message__receiver'
    ).order_by('-created_at')
    
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_notification_read(request, notification_id):
    """
    Mark a notification as read.
    """
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.read = True
    notification.save(update_fields=['read'])
    
    return Response({'status': 'Notification marked as read'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversations_list(request):
    """
    Get list of conversations for the authenticated user.
    """
    conversations = Conversation.objects.filter(participants=request.user).prefetch_related(
        'participants'
    ).order_by('-updated_at')
    
    data = []
    for conv in conversations:
        data.append({
            'id': conv.id,
            'participants': [p.username for p in conv.participants.all() if p != request.user],
            'created_at': conv.created_at,
            'updated_at': conv.updated_at,
            'unread_count': conv.get_unread_count(request.user)
        })
    
    return Response(data)