from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    # Check if the message already exists in the database
    if instance.pk:
        try:
            # Fetch the existing message
            old_message = Message.objects.get(pk=instance.pk)

            # If the content has changed, log the old content
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    previous_content=old_message.content
                )
                # Mark the message as edited
                instance.edited = True
                instance.edited_by = getattr(instance, '_edited_by', None)
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=get_user_model())
def delete_user_related_data(sender, instance, **kwargs):
    # Delete all messages sent by or received by the user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete all notifications related to the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories related to the user
    MessageHistory.objects.filter(message__sender=instance).delete()
    MessageHistory.objects.filter(message__receiver=instance).delete()
