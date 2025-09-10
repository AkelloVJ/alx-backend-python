from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification, Conversation


@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    """
    Signal to automatically create a notification when a new message is created.
    """
    if created:
        # Create notification for the receiver
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
        
        # Update conversation timestamp
        try:
            conversation = Conversation.objects.filter(
                participants=instance.sender
            ).filter(
                participants=instance.receiver
            ).first()
            
            if conversation:
                conversation.save()  # This will update the updated_at field
            else:
                # Create new conversation if it doesn't exist
                conversation = Conversation.objects.create()
                conversation.participants.add(instance.sender, instance.receiver)
        except Exception as e:
            print(f"Error updating conversation: {e}")


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal to log message edits before saving.
    """
    if instance.pk:  # Only for existing messages (edits)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                # Create message history entry
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_message.content,
                    edited_by=instance.sender
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass


@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal to clean up all user-related data when a user is deleted.
    """
    try:
        # Delete all messages sent by the user
        Message.objects.filter(sender=instance).delete()
        
        # Delete all messages received by the user
        Message.objects.filter(receiver=instance).delete()
        
        # Delete all notifications for the user
        Notification.objects.filter(user=instance).delete()
        
        # Delete all message history entries edited by the user
        MessageHistory.objects.filter(edited_by=instance).delete()
        
        # Delete conversations where the user was the only participant
        conversations = Conversation.objects.filter(participants=instance)
        for conversation in conversations:
            if conversation.participants.count() <= 1:
                conversation.delete()
            else:
                conversation.participants.remove(instance)
        
        print(f"Cleaned up all data for user: {instance.username}")
        
    except Exception as e:
        print(f"Error cleaning up user data for {instance.username}: {e}")


@receiver(post_save, sender=Message)
def mark_message_as_read_on_reply(sender, instance, created, **kwargs):
    """
    Signal to mark parent message as read when someone replies to it.
    """
    if created and instance.parent_message:
        try:
            parent_message = instance.parent_message
            if parent_message.receiver == instance.sender:
                parent_message.read = True
                parent_message.save(update_fields=['read'])
        except Exception as e:
            print(f"Error marking parent message as read: {e}")
