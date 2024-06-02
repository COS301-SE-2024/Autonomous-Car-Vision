from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, AuthViewSet, OTPViewSet, TokenViewSet, manage_auth, manage_token, manage_user, manage_otp, signup, verifyOTP, otpRegenerate, getSalt, signin, signout, hvstat, changePassword,changeUserDetails

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'auths', AuthViewSet)
router.register(r'otps', OTPViewSet)
router.register(r'tokens', TokenViewSet)

urlpatterns = [
    path('', include(router.urls)),
#     path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/<int:pk>/', manage_user, name='update_delete_user'),
    path('auth/', manage_auth, name='create_auth'),
    path('auth/<int:pk>/', manage_auth, name='update_delete_auth'),
    path('otp/', manage_otp, name='create_otp'),
    path('otp/<int:pk>/', manage_otp, name='update_delete_otp'),
    path('token/', manage_token, name='create_token'),
    path('token/<int:pk>/', manage_token, name='update_delete_token'),
    path('hvstat/', hvstat),
    path('signup/', signup),
    path('verifyOTP/', verifyOTP),
    path('otpRegenerate/', otpRegenerate),
    path('getSalt/', getSalt),
    path('signin/', signin),
    path('signout/', signout),
    path('changePassword/', changePassword),
    path('changeUserDetails/', changeUserDetails),
]
