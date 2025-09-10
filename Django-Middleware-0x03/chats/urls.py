from django.urls import path, include
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers as nested_routers
from rest_framework_simplejwt.views import TokenRefreshView
from .views import ConversationViewSet, MessageViewSet, UserViewSet
from .auth import (
    CustomTokenObtainPairView,
    register_user,
    login_user,
    logout_user,
    get_user_profile,
    update_user_profile
)

# Create a router and register our viewsets
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'users', UserViewSet, basename='user')

# Create nested router for messages within conversations
nested_router = nested_routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Authentication URLs
auth_urlpatterns = [
    path('auth/register/', register_user, name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/logout/', logout_user, name='logout'),
    path('auth/profile/', get_user_profile, name='user_profile'),
    path('auth/profile/update/', update_user_profile, name='update_profile'),
]

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
    path('', include(auth_urlpatterns)),
]
