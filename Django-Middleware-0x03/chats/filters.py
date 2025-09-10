import django_filters
from django.db import models
from django_filters import rest_framework as filters
from .models import Message, Conversation, User


class MessageFilter(filters.FilterSet):
    """
    Filter class for messages with various filtering options
    """
    
    # Filter by sender (user)
    sender = filters.UUIDFilter(field_name='sender__user_id', lookup_expr='exact')
    sender_email = filters.CharFilter(field_name='sender__email', lookup_expr='icontains')
    sender_name = filters.CharFilter(field_name='sender__first_name', lookup_expr='icontains')
    
    # Filter by conversation
    conversation = filters.UUIDFilter(field_name='conversation__conversation_id', lookup_expr='exact')
    
    # Filter by time range
    sent_after = filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    sent_date = filters.DateFilter(field_name='sent_at', lookup_expr='date')
    sent_date_range = filters.DateFromToRangeFilter(field_name='sent_at')
    
    # Filter by message content
    message_contains = filters.CharFilter(field_name='message_body', lookup_expr='icontains')
    message_exact = filters.CharFilter(field_name='message_body', lookup_expr='exact')
    message_startswith = filters.CharFilter(field_name='message_body', lookup_expr='startswith')
    
    # Filter by conversation participants
    participant = filters.UUIDFilter(field_name='conversation__participants_id__user_id', lookup_expr='exact')
    participant_email = filters.CharFilter(field_name='conversation__participants_id__email', lookup_expr='icontains')
    
    # Ordering
    ordering = filters.OrderingFilter(
        fields=(
            ('sent_at', 'sent_at'),
            ('-sent_at', '-sent_at'),
            ('sender__first_name', 'sender_name'),
            ('-sender__first_name', '-sender_name'),
            ('message_body', 'message_body'),
            ('-message_body', '-message_body'),
        ),
        field_labels={
            'sent_at': 'Sent At (Oldest First)',
            '-sent_at': 'Sent At (Newest First)',
            'sender_name': 'Sender Name (A-Z)',
            '-sender_name': 'Sender Name (Z-A)',
            'message_body': 'Message Body (A-Z)',
            '-message_body': 'Message Body (Z-A)',
        }
    )
    
    class Meta:
        model = Message
        fields = [
            'sender', 'sender_email', 'sender_name',
            'conversation', 'participant', 'participant_email',
            'sent_after', 'sent_before', 'sent_date', 'sent_date_range',
            'message_contains', 'message_exact', 'message_startswith',
            'ordering'
        ]


class ConversationFilter(filters.FilterSet):
    """
    Filter class for conversations
    """
    
    # Filter by participant
    participant = filters.UUIDFilter(field_name='participants_id__user_id', lookup_expr='exact')
    participant_email = filters.CharFilter(field_name='participants_id__email', lookup_expr='icontains')
    participant_name = filters.CharFilter(field_name='participants_id__first_name', lookup_expr='icontains')
    
    # Filter by creation time
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_date = filters.DateFilter(field_name='created_at', lookup_expr='date')
    created_date_range = filters.DateFromToRangeFilter(field_name='created_at')
    
    # Ordering
    ordering = filters.OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
            ('-created_at', '-created_at'),
            ('participants_id__first_name', 'participant_name'),
            ('-participants_id__first_name', '-participant_name'),
        ),
        field_labels={
            'created_at': 'Created At (Oldest First)',
            '-created_at': 'Created At (Newest First)',
            'participant_name': 'Participant Name (A-Z)',
            '-participant_name': 'Participant Name (Z-A)',
        }
    )
    
    class Meta:
        model = Conversation
        fields = [
            'participant', 'participant_email', 'participant_name',
            'created_after', 'created_before', 'created_date', 'created_date_range',
            'ordering'
        ]


class UserFilter(filters.FilterSet):
    """
    Filter class for users (admin use)
    """
    
    # Filter by name
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    full_name = filters.CharFilter(method='filter_full_name')
    
    # Filter by email
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    
    # Filter by role
    role = filters.ChoiceFilter(choices=User._meta.get_field('role').choices)
    
    # Filter by creation time
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_date = filters.DateFilter(field_name='created_at', lookup_expr='date')
    created_date_range = filters.DateFromToRangeFilter(field_name='created_at')
    
    # Filter by phone number
    phone_number = filters.CharFilter(field_name='phone_number', lookup_expr='icontains')
    
    # Ordering
    ordering = filters.OrderingFilter(
        fields=(
            ('first_name', 'first_name'),
            ('-first_name', '-first_name'),
            ('last_name', 'last_name'),
            ('-last_name', '-last_name'),
            ('email', 'email'),
            ('-email', '-email'),
            ('created_at', 'created_at'),
            ('-created_at', '-created_at'),
            ('role', 'role'),
        ),
        field_labels={
            'first_name': 'First Name (A-Z)',
            '-first_name': 'First Name (Z-A)',
            'last_name': 'Last Name (A-Z)',
            '-last_name': 'Last Name (Z-A)',
            'email': 'Email (A-Z)',
            '-email': 'Email (Z-A)',
            'created_at': 'Created At (Oldest First)',
            '-created_at': 'Created At (Newest First)',
            'role': 'Role (A-Z)',
        }
    )
    
    def filter_full_name(self, queryset, name, value):
        """
        Filter by full name (first_name + last_name)
        """
        return queryset.filter(
            models.Q(first_name__icontains=value) | 
            models.Q(last_name__icontains=value) |
            models.Q(first_name__icontains=value.split()[0]) if value.split() else models.Q()
        )
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'full_name',
            'email', 'role', 'phone_number',
            'created_after', 'created_before', 'created_date', 'created_date_range',
            'ordering'
        ]
