from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Message
from .serializers import MessageSerializer

class UserMessagesListView(generics.ListAPIView):
    """
    Retrieve all messages belonging to the authenticated user.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(recipient_id=user.id)
