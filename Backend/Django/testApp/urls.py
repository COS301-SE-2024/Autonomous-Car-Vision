from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuthViewSet, OTPViewSet, manage_auth, manage_user, manage_otp

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'auths', AuthViewSet)
router.register(r'otps', OTPViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/', manage_user, name='update_delete_user'),
    path('auth/', manage_auth, name='create_auth'),
    path('auth/<int:pk>/', manage_auth, name='update_delete_auth'),
    path('otp/', manage_otp, name='create_otp'),
    path('otp/<int:pk>/', manage_otp, name='update_delete_otp'),
]
