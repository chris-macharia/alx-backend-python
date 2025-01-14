from django.shortcuts import render, get_object_or_404
from .models import Message

def view_message_history(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    history = message.edit_history.all()
    return render(request, 'messaging/message_history.html', {'message': message, 'history': history})
