from django.db import models
import uuid


class User(models.Model):
    uid = models.IntegerField(primary_key=True)
    uname = models.TextField(unique=True)
    uemail = models.TextField(unique=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.uname


class Auth(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="auth", db_column="uid"
    )
    hash = models.CharField(max_length=255)
    salt = models.CharField(max_length=255)

    class Meta:
        db_table = "auth"

    def __str__(self):
        return f"Auth for {self.uid.uname}"


class OTP(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="otp", db_column="uid"
    )
    otp = models.CharField(max_length=6)
    creation_date = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()

    class Meta:
        db_table = "otp"

    def __str__(self):
        return f"OTP for {self.uid.uname}"


class Token(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="token", db_column="uid"
    )
    token = models.CharField(max_length=40, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tokens"

    def __str__(self):
        return f"Token for {self.uid.uname}"


class Media(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="video", db_column="uid"
    )
    media_id = models.TextField(unique=True)
    media_name = models.TextField()
    media_url = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    aid = models.TextField()

    class Meta:
        db_table = "media"

    def __str__(self):
        return f"Media {self.media_name} by {self.uid.uname}"


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f"media/user_{instance.uid.id}/{filename}"
