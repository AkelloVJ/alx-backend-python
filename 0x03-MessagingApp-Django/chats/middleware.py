import logging
import time
from datetime import datetime, time as dt_time
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from collections import defaultdict, deque
import os
from pathlib import Path

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / 'requests.log'

# Configure logging for requests
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


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
        
        # Log the request information in the exact format required
        log_message = f"{datetime.now()} - User: {user_info} - Path: {request.path}"
        logger.info(log_message)
        
        # Process the request
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware(MiddlewareMixin):
    """
    Middleware that restricts access to the messaging app during certain hours of the day.
    Denies access outside 9PM and 6PM (6PM to 9PM is allowed).
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def __call__(self, request):
        # Check if the request is for chat/messaging endpoints
        if request.path.startswith('/api/') and any(endpoint in request.path for endpoint in ['messages', 'conversations', 'chats']):
            current_time = datetime.now().time()
            
            # Define allowed time window (6PM to 9PM)
            start_time = dt_time(18, 0)  # 6PM
            end_time = dt_time(21, 0)    # 9PM
            
            # Check if current time is outside the allowed window
            if not (start_time <= current_time <= end_time):
                return JsonResponse({
                    'error': 'Access denied',
                    'message': 'Messaging service is only available between 6PM and 9PM',
                    'current_time': current_time.strftime('%H:%M:%S'),
                    'allowed_hours': '18:00 - 21:00'
                }, status=403)
        
        # Process the request if within allowed time
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware(MiddlewareMixin):
    """
    Middleware that limits the number of chat messages a user can send within a certain time window,
    based on their IP address. Implements rate limiting: 5 messages per minute.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
        
        # Store request counts per IP address
        self.request_counts = defaultdict(deque)
        self.max_requests = 5  # Maximum 5 messages per minute
        self.time_window = 60  # 1 minute in seconds
    
    def __call__(self, request):
        # Check if the request is for sending messages
        if (request.method == 'POST' and 
            request.path.startswith('/api/') and 
            'messages' in request.path):
            
            # Get client IP address
            ip_address = self.get_client_ip(request)
            current_time = time.time()
            
            # Clean old requests outside the time window
            self.clean_old_requests(ip_address, current_time)
            
            # Check if IP has exceeded the rate limit
            if len(self.request_counts[ip_address]) >= self.max_requests:
                return JsonResponse({
                    'error': 'Rate limit exceeded',
                    'message': f'You can only send {self.max_requests} messages per minute',
                    'retry_after': self.get_retry_after(ip_address, current_time)
                }, status=429)
            
            # Add current request to the count
            self.request_counts[ip_address].append(current_time)
        
        # Process the request
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        """Get the client's IP address from the request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def clean_old_requests(self, ip_address, current_time):
        """Remove requests older than the time window."""
        while (self.request_counts[ip_address] and 
               current_time - self.request_counts[ip_address][0] > self.time_window):
            self.request_counts[ip_address].popleft()
    
    def get_retry_after(self, ip_address, current_time):
        """Calculate seconds until the oldest request expires."""
        if self.request_counts[ip_address]:
            oldest_request = self.request_counts[ip_address][0]
            return int(self.time_window - (current_time - oldest_request))
        return self.time_window


class RolePermissionMiddleware(MiddlewareMixin):
    """
    Middleware that checks the user's role before allowing access to specific actions.
    Only admin or moderator users can access certain endpoints.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
        
        # Define protected endpoints that require admin/moderator access
        self.protected_endpoints = [
            '/api/users/',  # User management
            '/api/admin/',  # Admin endpoints
        ]
        
        # Define admin/moderator roles
        self.allowed_roles = ['admin', 'moderator']
    
    def __call__(self, request):
        # Check if the request is for protected endpoints
        if any(request.path.startswith(endpoint) for endpoint in self.protected_endpoints):
            user = getattr(request, 'user', None)
            
            # Check if user is authenticated
            if not user or not user.is_authenticated:
                return JsonResponse({
                    'error': 'Authentication required',
                    'message': 'You must be logged in to access this resource'
                }, status=401)
            
            # Check if user has the required role
            user_role = getattr(user, 'role', None)
            
            if user_role not in self.allowed_roles:
                return JsonResponse({
                    'error': 'Access denied',
                    'message': 'You do not have permission to access this resource',
                    'required_roles': self.allowed_roles,
                    'your_role': user_role
                }, status=403)
        
        # Process the request
        response = self.get_response(request)
        return response


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


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Middleware to add security headers to responses.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response