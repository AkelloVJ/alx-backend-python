from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission class that:
    - Allows only authenticated users to access the API
    - Allows only participants in a conversation to send, view, update and delete messages
    """
    
    def has_permission(self, request, view):
        """
        Check if the user is authenticated
        """
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is a participant in the conversation
        """
        # For conversation objects, check if user is a participant
        if hasattr(obj, 'participants_id'):
            return obj.participants_id == request.user
        
        # For message objects, check if user is a participant in the conversation
        if hasattr(obj, 'conversation'):
            return obj.conversation.participants_id == request.user
        
        # For other objects, deny access by default
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the object.
        return obj.user_id == request.user.user_id


class IsConversationParticipant(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        return obj.participants_id == request.user


class IsMessageSenderOrConversationParticipant(permissions.BasePermission):
    """
    Custom permission to allow message senders and conversation participants to access messages.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow if user is the sender of the message
        if obj.sender == request.user:
            return True
        
        # Allow if user is a participant in the conversation
        return obj.conversation.participants_id == request.user


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners or admins to access user data.
    """
    
    def has_object_permission(self, request, view, obj):
        # Allow if user is accessing their own data
        if obj.user_id == request.user.user_id:
            return True
        
        # Allow if user is admin
        return request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow read-only access to non-admin users and full access to admins.
    """
    
    def has_permission(self, request, view):
        # Allow read-only access to authenticated users
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Allow full access to admin users
        return request.user.is_authenticated and request.user.is_staff


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission that allows:
    - Read access to authenticated users
    - Write access to object owners
    - Full access to admins
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Allow read access to authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow write access to object owners
        if hasattr(obj, 'user_id') and obj.user_id == request.user.user_id:
            return True
        
        # Allow full access to admins
        return request.user.is_staff


class CanAccessOwnData(permissions.BasePermission):
    """
    Custom permission to ensure users can only access their own data.
    """
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # For user objects, check if it's the same user
        if hasattr(obj, 'user_id'):
            return obj.user_id == request.user.user_id
        
        # For conversation objects, check if user is a participant
        if hasattr(obj, 'participants_id'):
            return obj.participants_id == request.user
        
        # For message objects, check if user is sender or conversation participant
        if hasattr(obj, 'sender') and hasattr(obj, 'conversation'):
            return (obj.sender == request.user or 
                   obj.conversation.participants_id == request.user)
        
        return False
