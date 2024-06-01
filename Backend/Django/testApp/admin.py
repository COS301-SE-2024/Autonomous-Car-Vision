from django.contrib import admin
from .models import User, Auth, OTP

admin.site.register(User)
admin.site.register(Auth)
admin.site.register(OTP)

