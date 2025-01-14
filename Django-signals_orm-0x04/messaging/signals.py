from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification

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
        except Message.DoesNotExist:
            pass
