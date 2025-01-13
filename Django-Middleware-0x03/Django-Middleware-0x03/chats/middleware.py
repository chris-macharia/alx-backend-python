import logging
from datetime import datetime

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
