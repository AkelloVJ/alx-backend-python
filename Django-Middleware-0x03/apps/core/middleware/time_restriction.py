"""
Time Restriction Middleware

Restricts access to the messaging app during certain hours of the day.
Denies access outside 6PM and 9PM (6PM to 9PM is allowed).
"""

from datetime import datetime, time as dt_time
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


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
