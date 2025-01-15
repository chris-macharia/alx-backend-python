from django.urls import path
from . import views

urlpatterns = [
    path('message/<int:message_id>/', views.message_thread_view, name='message_thread'),
]
