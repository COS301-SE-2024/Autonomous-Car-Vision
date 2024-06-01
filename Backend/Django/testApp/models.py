from django.db import models

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    uname = models.TextField(unique=True)
    uemail = models.TextField(unique=True)

    def __str__(self):
        return self.uname

class Auth(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='auth')
    hash = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)

    def __str__(self):
        return f"Auth for {self.uid.uname}"

class OTP(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp')
    otp = models.CharField(max_length=6)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    def __str__(self):
        return f"OTP for {self.uid.uname}"