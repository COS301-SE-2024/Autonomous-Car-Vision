from django import forms
from .models import User, Auth, OTP, Token

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['uname', 'uemail']

class AuthForm(forms.ModelForm):
    class Meta:
        model = Auth
        fields = ['hash', 'salt']

class OTPForm(forms.ModelForm):
    class Meta:
        model = OTP
        fields = ['otp', 'expiry_date']
        
class TokenForm(forms.ModelForm):
    class Meta:
        model = Token
        fields = ['token']