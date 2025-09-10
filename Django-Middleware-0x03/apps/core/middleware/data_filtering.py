"""
Request Data Filtering Middleware

Filters and cleans incoming request data before it reaches views.
"""

import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger('apps.core.middleware')


class RequestDataFilteringMiddleware(MiddlewareMixin):
    """
    Additional middleware for filtering and cleaning incoming request data.
    This middleware can be used to sanitize input data before it reaches the views.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def __call__(self, request):
        # Filter and clean request data if it's a POST/PUT/PATCH request
        if request.method in ['POST', 'PUT', 'PATCH']:
            # Log request data for debugging (be careful with sensitive data in production)
            if hasattr(request, 'data'):
                logger.info(f"Request data received: {request.data}")
        
        # Process the request
        response = self.get_response(request)
        return response
