"""
Role Permission Middleware

Checks the user's role before allowing access to specific actions.
Only admin or moderator users can access certain endpoints.
"""

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


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
