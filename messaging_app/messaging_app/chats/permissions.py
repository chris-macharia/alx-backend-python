from rest_framework.permissions import BasePermission

class IsMessageOwner(BasePermission):
    """
    Custom permission to only allow owners of a message to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the sender or recipient of the message
        return obj.sender_id == request.user or obj.recipient_id == request.user
