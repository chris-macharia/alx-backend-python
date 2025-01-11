from rest_framework import viewsets
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .permissions import IsParticipantOfConversation

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    # Add filtering and searching capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['participants_id']  # Example: Filter by participant
    search_fields = ['participants_id']     # Example: Search by participant

    def get_queryset(self):
        # Ensure users see only their conversations
        return self.queryset.filter(participants=self.request.user)

    # Create a new conversation (POST method)
    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        participants = request.data.get('participants', [])
        if not participants:
            return Response({"error": "Participants list is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate participants
        users = User.objects.filter(id__in=participants)
        if users.count() != len(participants):
            return Response({"error": "One or more participants are invalid"}, status=status.HTTP_400_BAD_REQUEST)

        if request.user.id not in participants:
            participants.append(request.user.id)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()
        
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]  # Apply custom permission

    # Add filtering and searching capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['conversation_id', 'sender_id']  # Example: Filter by conversation or sender
    search_fields = ['message_body']  # Example: Search within message body

    def get_queryset(self):
        # Ensure users can access only messages in their conversations
        return self.queryset.filter(conversation__participants=self.request.user)

    # Send a message to an existing conversation (POST method)
    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        conversation = self.get_object()
        sender = request.user
        message_body = request.data.get('message_body', '')

        # Ensure the user is a participant in the conversation
        if request.user not in conversation.participants.all():
            raise PermissionDenied("You are not a participant in this conversation.")

        if not message_body:
            return Response({"error": "Message body is required"}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
