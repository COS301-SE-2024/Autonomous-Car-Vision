from rest_framework import serializers
from .models import User, Auth, OTP, Token, Media, Corporation, TokenCorporation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uid", "uname", "uemail", "cid", "is_admin"]


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ["id", "uid", "hash", "salt"]


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ["id", "uid", "otp", "creation_date", "expiry_date"]


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ["id", "uid", "token"]


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ["id", "uid", "mid", "media_name", "media_url", "aid"]

    def get_media_url(self, obj):
        request = self.context.get("request")
        if obj.media_url:
            return request.build_absolute_uri(obj.media_url)
        return None

class CorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporation
        fields = ["cname"]
        
class TokenCorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenCorporation
        fields = ["token", "email"]        
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["profile_photo"]        