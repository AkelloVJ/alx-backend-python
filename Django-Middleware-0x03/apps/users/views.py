"""
Users app views for testing role permissions.
"""
from rest_framework.views import APIView
from rest_framework.response import Response


class UserListView(APIView):
    """
    User list view - protected by role permissions middleware.
    """
    
    def get(self, request):
        return Response({
            'message': 'User list accessed successfully',
            'user': str(request.user) if request.user.is_authenticated else 'Anonymous',
            'user_role': getattr(request.user, 'role', 'No role') if request.user.is_authenticated else 'No role',
            'path': request.path,
            'method': request.method
        })


class AdminView(APIView):
    """
    Admin view - protected by role permissions middleware.
    """
    
    def get(self, request):
        return Response({
            'message': 'Admin panel accessed successfully',
            'user': str(request.user) if request.user.is_authenticated else 'Anonymous',
            'user_role': getattr(request.user, 'role', 'No role') if request.user.is_authenticated else 'No role',
            'path': request.path,
            'method': request.method
        })
