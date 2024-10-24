from django import forms
from .models import User, Auth, OTP, Token, Video, Corporation, TokenCorporation


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["uname", "uemail", "cid", "is_admin", "last_signin"]

class AuthForm(forms.ModelForm):
    class Meta:
        model = Auth
        fields = ["hash", "salt"]

class OTPForm(forms.ModelForm):
    class Meta:
        model = OTP
        fields = ["otp", "expiry_date"]


class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = ["token"]


class MediaForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["media_name", "media_url"]

class CorporationForm(forms.ModelForm):
    class Meta:
        model = Corporation
        fields = ["cname"]        
        
class TokenCorporationForm(forms.ModelForm):
    class Meta:
        model = TokenCorporation
        fields = ["token", "email"]        