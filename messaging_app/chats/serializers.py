from rest_framework import serializers
from .models import User, Message, Conversation

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested User Serializer

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)  # Nested Messages

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']

