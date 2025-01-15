from django.shortcuts import render, get_object_or_404
from .models import Message
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.contrib.auth import get_user_model
from .utils import get_threaded_messages

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
