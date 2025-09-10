"""
Request Logging Middleware

Logs each user's requests to a file, including timestamp, user and request path.
"""

import logging
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('apps.core.middleware')


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware that logs each user's requests to a file, including timestamp, user and request path.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def __call__(self, request):
        # Log the request before processing
        user = getattr(request, 'user', None)
        if user and hasattr(user, 'username'):
            user_info = user.username
        elif user and hasattr(user, 'email'):
            user_info = user.email
        else:
            user_info = "Anonymous"
        
        # Log the request information
        log_message = f"{datetime.now()} - User: {user_info} - Path: {request.path}"
        logger.info(log_message)
        
        # Process the request
        response = self.get_response(request)
        
        return response
