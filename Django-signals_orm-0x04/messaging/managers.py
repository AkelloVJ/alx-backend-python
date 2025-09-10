from django.db import models


class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a specific user.
    """
    def unread_for_user(self, user):
        """
        Filter unread messages for a specific user.
        """
        return self.filter(receiver=user, read=False)
    
    def unread_count(self, user):
        """
        Get count of unread messages for a specific user.
        """
        return self.unread_for_user(user).count()
    
    def for_user(self, user):
        """
        Alias for unread_for_user for backward compatibility.
        """
        return self.unread_for_user(user)
