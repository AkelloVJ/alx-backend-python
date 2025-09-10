"""
Core app views for middleware testing.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class TestView(APIView):
    """
    Test view to verify middleware functionality.
    """
    
    def get(self, request):
        return Response({
            'message': 'Middleware test endpoint working!',
            'user': str(request.user) if request.user.is_authenticated else 'Anonymous',
            'path': request.path,
            'method': request.method
        })


class MessageView(APIView):
    """
    Message view for testing rate limiting and time restrictions.
    """
    
    def get(self, request):
        return Response({
            'message': 'Messages endpoint accessed successfully',
            'user': str(request.user) if request.user.is_authenticated else 'Anonymous',
            'path': request.path,
            'method': request.method
        })
    
    def post(self, request):
        return Response({
            'message': 'Message created successfully',
            'data': request.data if hasattr(request, 'data') else 'No data',
            'user': str(request.user) if request.user.is_authenticated else 'Anonymous',
            'path': request.path,
            'method': request.method
        }, status=status.HTTP_201_CREATED)


class ConversationView(APIView):
    """
    Conversation view for testing middleware functionality.
    """
    
    def get(self, request):
        return Response({
            'message': 'Conversations endpoint accessed successfully',
            'user': str(request.user) if request.user.is_authenticated else 'Anonymous',
            'path': request.path,
            'method': request.method
        })
    
    def post(self, request):
        return Response({
            'message': 'Conversation created successfully',
            'data': request.data if hasattr(request, 'data') else 'No data',
            'user': str(request.user) if request.user.is_authenticated else 'Anonymous',
            'path': request.path,
            'method': request.method
        }, status=status.HTTP_201_CREATED)
