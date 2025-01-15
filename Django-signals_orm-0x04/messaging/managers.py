from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Filters unread messages for a specific user.
        Optimizes the query to retrieve only necessary fields.
        """
        return self.filter(recipient=user, read=False).only('id', 'sender', 'message_body', 'sent_at')
