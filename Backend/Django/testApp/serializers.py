from rest_framework import serializers
from .models import User, Auth, OTP, Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['uid', 'uname', 'uemail']

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ['id', 'uid', 'hash', 'salt']

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ['id', 'uid', 'otp', 'creation_date', 'expiry_date']
        
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['uid', 'token']        