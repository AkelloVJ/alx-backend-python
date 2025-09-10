from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User
from .serializers import UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token obtain view that returns user data along with tokens
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Get user data
            email = request.data.get('email')
            try:
                user = User.objects.get(email=email)
                user_data = UserSerializer(user).data
                response.data['user'] = user_data
            except User.DoesNotExist:
                pass
        
        return response


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user
    """
    data = request.data
    
    # Validate required fields
    required_fields = ['email', 'password', 'first_name', 'last_name']
    for field in required_fields:
        if not data.get(field):
            return Response(
                {'error': f'{field} is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    # Check if user already exists
    if User.objects.filter(email=data['email']).exists():
        return Response(
            {'error': 'User with this email already exists'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Validate password
    try:
        validate_password(data['password'])
    except ValidationError as e:
        return Response(
            {'error': 'Password validation failed', 'details': list(e.messages)}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create user
    try:
        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data.get('username', data['email']),  # Use email as username if not provided
            phone_number=data.get('phone_number', ''),
            role=data.get('role', 'guest')
        )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        # Return user data and tokens
        user_data = UserSerializer(user).data
        return Response({
            'user': user_data,
            'access': str(access_token),
            'refresh': str(refresh)
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': 'Failed to create user', 'details': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Login user and return JWT tokens
    """
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': 'Email and password are required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Authenticate user
    user = authenticate(request, username=email, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # Generate tokens
    refresh = RefreshToken.for_user(user)
    access_token = refresh.access_token
    
    # Return user data and tokens
    user_data = UserSerializer(user).data
    return Response({
        'user': user_data,
        'access': str(access_token),
        'refresh': str(refresh)
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def logout_user(request):
    """
    Logout user by blacklisting the refresh token
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {'message': 'Successfully logged out'}, 
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Refresh token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    except Exception as e:
        return Response(
            {'error': 'Invalid token'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
def get_user_profile(request):
    """
    Get current user's profile
    """
    user_data = UserSerializer(request.user).data
    return Response(user_data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
def update_user_profile(request):
    """
    Update current user's profile
    """
    user = request.user
    data = request.data
    
    # Fields that can be updated
    allowed_fields = ['first_name', 'last_name', 'phone_number', 'role']
    
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])
    
    try:
        user.save()
        user_data = UserSerializer(user).data
        return Response(user_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': 'Failed to update profile', 'details': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )
