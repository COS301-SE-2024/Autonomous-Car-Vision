from django.test import TestCase
from django.utils import timezone
from .models import User, Auth, OTP, Token, Media
import datetime


class ModelsTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            uid=1, uname="testuser1", uemail="testuser1@example.com"
        )
        self.user2 = User.objects.create(
            uid=2, uname="testuser2", uemail="testuser2@example.com"
        )

        self.auth1 = Auth.objects.create(uid=self.user1, hash="hash1", salt="salt1")
        self.auth2 = Auth.objects.create(uid=self.user2, hash="hash2", salt="salt2")

        self.otp1 = OTP.objects.create(
            uid=self.user1,
            otp="123456",
            creation_date=timezone.now(),
            expiry_date=timezone.now() + datetime.timedelta(minutes=5),
        )
        self.otp2 = OTP.objects.create(
            uid=self.user2,
            otp="654321",
            creation_date=timezone.now(),
            expiry_date=timezone.now() + datetime.timedelta(minutes=5),
        )

        self.token1 = Token.objects.create(uid=self.user1, token="token1")
        self.token2 = Token.objects.create(uid=self.user2, token="token2")

        self.media1 = Media.objects.create(
            uid=self.user1,
            mid="media1",
            media_name="Media 1",
            media_url="media/media1.mp4",
        )
        self.media2 = Media.objects.create(
            uid=self.user2,
            mid="media2",
            media_name="Media 2",
            media_url="media/media2.mp4",
        )

    def test_user_creation(self):
        user = User.objects.get(uid=1)
        self.assertEqual(user.uname, "testuser1")
        self.assertEqual(user.uemail, "testuser1@example.com")

    def test_user_unique_constraints(self):
        with self.assertRaises(Exception):
            User.objects.create(
                uid=1, uname="duplicateuser", uemail="duplicate@example.com"
            )

    def test_auth_creation(self):
        auth = Auth.objects.get(uid=self.user1)
        self.assertEqual(auth.hash, "hash1")
        self.assertEqual(auth.salt, "salt1")

    def test_auth_string_representation(self):
        auth = Auth.objects.get(uid=self.user1)
        self.assertEqual(str(auth), "Auth for testuser1")

    def test_otp_creation(self):
        otp = OTP.objects.get(uid=self.user1)
        self.assertEqual(otp.otp, "123456")

    def test_otp_string_representation(self):
        otp = OTP.objects.get(uid=self.user1)
        self.assertEqual(str(otp), "OTP for testuser1")

    def test_token_creation(self):
        token = Token.objects.get(uid=self.user1)
        self.assertEqual(token.token, "token1")

    def test_token_string_representation(self):
        token = Token.objects.get(uid=self.user1)
        self.assertEqual(str(token), "Token for testuser1")

    def test_media_creation(self):
        media = Media.objects.get(uid=self.user1)
        self.assertEqual(media.media_name, "Media 1")
        self.assertEqual(media.media_url, "media/media1.mp4")

    def test_media_string_representation(self):
        media = Media.objects.get(uid=self.user1)
        self.assertEqual(str(media), "Media Media 1 by testuser1")

    def test_media_unique_constraints(self):
        with self.assertRaises(Exception):
            Media.objects.create(
                uid=self.user1,
                mid="media1",
                media_name="Duplicate Media",
                media_url="media/media1.mp4",
            )

    # def test_media_file_deletion(self):
    #     media = Media.objects.get(uid=self.user1)
    #     media.delete()
    #     self.assertFalse(media.media_url.exists())

    # def test_media_file_deletion_on_object_deletion(self):
    #     media = Media.objects.get(uid=self.user1)
    #     media.delete()
    #     with self.assertRaises(Exception):
    #         Media.objects.get(uid=self.user1)
    #     self.assertFalse(media.media_url.exists())

    # def test_media_file_deletion_on_object_update(self):
    #     media = Media.objects.get(uid=self.user1)
    #     media.media_url = "media/media3.mp4"
    #     media.save()
    #     self.assertFalse(media.media_url.exists())

    # def test_media_file_deletion_on_object_update_with_new_file(self):
    #     media = Media.objects.get(uid=self.user1)
    #     media.media_url = "media/media3.mp4"
    #     media.save()
    #     self.assertFalse(media.media_url.exists())

    # def test_media_file_deletion_on_object_update_with_new_file(self):
    #     media = Media.objects.get(uid=self.user1)
    #     media.media_url = "media/media3.mp4"
    #     media.save()
    #     self.assertFalse(media.media_url.exists())
