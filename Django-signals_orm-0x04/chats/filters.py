import django_filters
from .models import Message
from django_filters import DateFromToRangeFilter

class MessageFilter(django_filters.FilterSet):
    # Filter by conversation ID
    conversation_id = django_filters.UUIDFilter(field_name='conversation__id', lookup_expr='exact')
    # Filter by sender ID
    sender_id = django_filters.UUIDFilter(field_name='sender__id', lookup_expr='exact')
    # Filter messages sent within a date range
    date_range = DateFromToRangeFilter(field_name='sent_at', label='Date range')

    class Meta:
        model = Message
        fields = ['conversation_id', 'sender_id', 'date_range']
