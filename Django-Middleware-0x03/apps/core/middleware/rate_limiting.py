"""
Rate Limiting Middleware (Offensive Language Middleware)

Limits the number of chat messages a user can send within a certain time window,
based on their IP address. Implements rate limiting: 5 messages per minute.
"""

import time
from collections import defaultdict, deque
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


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
