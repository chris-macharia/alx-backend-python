import logging
import time
from datetime import datetime
from django.http import HttpResponseForbidden
from collections import defaultdict



# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.FileHandler('requests.log')
handler.setFormatter(logging.Formatter('%(message)s'))
logger.addHandler(handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        """
        Initialize the middleware. This method is called once when the server starts.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        This method is called on each request.
        Log the request details (timestamp, user, and request path).
        """
        # Get user info and request path
        user = request.user if request.user.is_authenticated else 'Anonymous'
        request_path = request.path

        # Log the information
        logger.info(f"{datetime.now()} - User: {user} - Path: {request_path}")

        # Proceed to the next middleware or view
        response = self.get_response(request)

        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the current server time (24-hour format)
        current_hour = datetime.now().hour

        # Define restricted hours: outside 6 PM (18:00) to 9 PM (21:00)
        if not (18 <= current_hour < 21):  # Restrict access outside this range
            return HttpResponseForbidden("Access to the messaging app is restricted during these hours.")

        # Proceed with the request
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_logs = defaultdict(list)  # Stores IP logs with timestamps

    def __call__(self, request):
        # Limit settings
        time_window = 60  # Time window in seconds (1 minute)
        max_messages = 5  # Maximum messages allowed in the time window

        # Get the IP address of the client
        ip_address = self.get_client_ip(request)

        # If the request is a POST (sending a message)
        if request.method == "POST":
            current_time = time.time()
            message_times = self.request_logs[ip_address]

            # Remove timestamps older than the time window
            self.request_logs[ip_address] = [
                t for t in message_times if current_time - t <= time_window
            ]

            # Check if the limit is exceeded
            if len(self.request_logs[ip_address]) >= max_messages:
                return HttpResponseForbidden("Message limit exceeded. Try again later.")

            # Log the current message timestamp
            self.request_logs[ip_address].append(current_time)

        # Proceed with the request
        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        """Retrieve the client IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]  # Get the first IP in the list
        return request.META.get('REMOTE_ADDR')

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define roles that have access
        allowed_roles = ['admin', 'moderator']

        # Check if the user is authenticated and has a valid role
        if request.user.is_authenticated:
            user_role = getattr(request.user, 'role', None)  # Get the role attribute
            if user_role not in allowed_roles:
                return HttpResponseForbidden("You do not have permission to perform this action.")
        else:
            # If user is not authenticated, block access
            return HttpResponseForbidden("You must be logged in to perform this action.")

        # Proceed with the request
        return self.get_response(request)
