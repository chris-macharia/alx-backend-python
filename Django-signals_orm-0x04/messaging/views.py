from django.shortcuts import render, get_object_or_404
from .models import Message
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import get_user_model
from .utils import get_threaded_messages
from django.views.decorators.cache import cache_page

# Handles the deletion of a user account
@login_required
def delete_user(request):
    try:
        user = request.user
        # Delete related data
        user.delete()  # This will automatically trigger post_delete signal for the user
        messages.success(request, "Your account has been deleted successfully.")
        return redirect('home')  # Redirect to a relevant page after deletion
    except get_user_model().DoesNotExist:
        raise Http404("User does not exist.")


def view_message_history(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    history = message.edit_history.all()
    return render(request, 'messaging/message_history.html', {'message': message, 'history': history})


def message_thread_view(request, message_id):
    parent_message = get_object_or_404(
        Message.objects.select_related('sender', 'recipient').prefetch_related('replies'),
        id=message_id
    )
    threaded_messages = get_threaded_messages(parent_message)

    return render(request, 'messages/thread.html', {
        'parent_message': parent_message,
        'threaded_messages': threaded_messages,
    })

def message_detail_view(request, message_id):
    # Ensure only messages the user is involved in are queried
    message = get_object_or_404(
        Message.objects.select_related('sender', 'recipient').prefetch_related('replies'),
        id=message_id,
        sender=request.user  # Ensures sender is the logged-in user
    )

    # Fetch threaded messages
    threaded_messages = get_threaded_messages(message)

    return render(request, 'messages/message_detail.html', {
        'message': message,
        'threaded_messages': threaded_messages,
    })

def user_messages_view(request):
    # Fetch all messages for the logged-in user, optimizing the query
    messages = Message.objects.filter(
        models.Q(sender=request.user) | models.Q(recipient=request.user) #["receiver"]
    ).select_related('sender', 'recipient').prefetch_related('replies')

    return render(request, 'messages/user_messages.html', {
        'messages': messages,
    })

def unread_messages_view(request):
    # Fetch unread messages for the logged-in user
    unread_messages = Message.unread.for_user(request.user)

    return render(request, 'messages/unread_messages.html', {
        'unread_messages': unread_messages,
    })

def inbox(request):
    """
    View to display the user's inbox with only unread messages.
    Optimized to retrieve only necessary fields using .only().
    """
    if request.user.is_authenticated:
        # Use .only() to optimize the query
        unread_messages = Message.unread.for_user(request.user).only('id', 'sender', 'message_body', 'sent_at') # Message.unread.unread_for_user
        context = {'unread_messages': unread_messages}
        return render(request, 'messaging/inbox.html', context)
    else:
        return render(request, 'messaging/login.html')

@cache_page(60)  # Cache the view for 60 seconds
def conversation_messages(request, conversation_id):
    """
    View to display messages in a conversation.
    Uses caching to improve performance.
    """
    if request.user.is_authenticated:
        messages = Message.objects.filter(conversation_id=conversation_id).select_related('sender', 'recipient')
        context = {'messages': messages}
        return render(request, 'messaging/conversation.html', context)
    else:
        return render(request, 'messaging/login.html')
