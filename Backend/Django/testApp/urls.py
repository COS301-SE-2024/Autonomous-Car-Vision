from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuthViewSet, OTPViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'auths', AuthViewSet)
router.register(r'otps', OTPViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
