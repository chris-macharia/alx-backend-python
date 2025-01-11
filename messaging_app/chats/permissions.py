from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsMessageOwner(BasePermission):
    """
    Custom permission to only allow owners of a message to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the sender or recipient of the message
        return obj.sender_id == request.user or obj.recipient_id == request.user


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only authenticated users who are participants 
    in a conversation to send, view, update, or delete messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Check if the user is a participant in the conversation
        # Assuming `obj` is a Message instance and `conversation` has a `participants` field
        return request.user in obj.conversation.participants.all()


