from django.shortcuts import get_object_or_404, render
from .models import Message

def get_message_with_replies(message_id):
    # Fetch a message with its sender, recipient, and immediate replies
    return Message.objects.select_related('sender', 'recipient').prefetch_related('replies').get(id=message_id)


def get_threaded_messages(message):
    threaded_messages = []

    def fetch_replies(message):
        replies = message.replies.all().select_related('sender', 'recipient')
        for reply in replies:
            threaded_messages.append(reply)
            fetch_replies(reply)  # Recursively fetch replies of this reply

    fetch_replies(message)
    return threaded_messages
