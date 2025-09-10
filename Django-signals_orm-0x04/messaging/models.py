from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .managers import UnreadMessagesManager


class Message(models.Model):
    """
    Message model with threading support, read status, and edit tracking.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    # Custom managers
    objects = models.Manager()
    unread = UnreadMessagesManager()
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['receiver', 'read']),
            models.Index(fields=['sender', 'timestamp']),
            models.Index(fields=['parent_message']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}: {self.content[:50]}..."
    
    def get_thread(self):
        """
        Get all messages in the same thread (replies to the same parent or the message itself).
        """
        if self.parent_message:
            # This is a reply, get all replies to the same parent
            return Message.objects.filter(parent_message=self.parent_message).order_by('timestamp')
        else:
            # This is a top-level message, get all its replies
            return Message.objects.filter(parent_message=self).order_by('timestamp')
    
    def get_all_replies(self):
        """
        Recursively get all replies to this message.
        """
        replies = []
        direct_replies = self.replies.all().order_by('timestamp')
        
        for reply in direct_replies:
            replies.append(reply)
            replies.extend(reply.get_all_replies())
        
        return replies


class MessageHistory(models.Model):
    """
    Model to store message edit history.
    """
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='edit_history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-edited_at']
    
    def __str__(self):
        return f"Edit history for message {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    """
    Notification model to store user notifications for new messages.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'message']
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.message.content[:30]}..."


class Conversation(models.Model):
    """
    Model to represent conversations between users.
    """
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        participant_names = [p.username for p in self.participants.all()]
        return f"Conversation between {', '.join(participant_names)}"
    
    def get_messages(self):
        """
        Get all messages in this conversation.
        """
        return Message.objects.filter(
            models.Q(sender__in=self.participants.all()) |
            models.Q(receiver__in=self.participants.all())
        ).order_by('timestamp')
    
    def get_unread_count(self, user):
        """
        Get unread message count for a specific user in this conversation.
        """
        return Message.unread.for_user(user).filter(
            models.Q(sender__in=self.participants.all()) |
            models.Q(receiver__in=self.participants.all())
        ).count()