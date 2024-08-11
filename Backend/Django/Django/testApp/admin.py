from django.contrib import admin
from .models import User, Auth, OTP, Token, Media, Corporation

admin.site.register(User)
admin.site.register(Auth)
admin.site.register(OTP)
admin.site.register(Token)
admin.site.register(Media)
admin.site.register(Corporation)
