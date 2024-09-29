from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from django.http import JsonResponse
from django.shortcuts import render
import psycopg2
import requests
from rest_framework import viewsets

from .serializers import (
    TokenCorporationSerializer,
    TokenSerializer,
    UserSerializer,
    AuthSerializer,
    OTPSerializer,
    MediaSerializer,
    CorporationSerializer,
    TokenCorporationSerializer,
)
from .models import User, Auth, OTP, Token, Media, Corporation, TokenCorporation
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import random
import string
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from datetime import datetime, time, timedelta, timezone
import smtplib
from dotenv import load_dotenv
import requests
import time
import concurrent.futures

load_dotenv()

HOST_IP = os.getenv("HOST_IP")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class AuthViewSet(viewsets.ModelViewSet):
    queryset = Auth.objects.all()
    serializer_class = AuthSerializer
    permission_classes = [IsAuthenticated]


class OTPViewSet(viewsets.ModelViewSet):
    queryset = OTP.objects.all()
    serializer_class = OTPSerializer
    permission_classes = [IsAuthenticated]


class TokenViewSet(viewsets.ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer
    permission_classes = [IsAuthenticated]


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]
    
class CorporationViewSet(viewsets.ModelViewSet):
    queryset = Corporation.objects.all()
    serializer_class = CorporationSerializer
    permission_classes = [IsAuthenticated]    


@api_view(["POST", "PUT", "DELETE"])
def manage_user(request, pk=None):
    if request.method == "POST":
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if pk is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST", "PUT", "DELETE"])
def manage_auth(request, pk=None):
    if request.method == "POST":
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if pk is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        auth = Auth.objects.get(pk=pk)
    except Auth.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = AuthSerializer(auth, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST", "PUT", "DELETE"])
def manage_otp(request, pk=None):
    if request.method == "POST":
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if pk is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        otp = OTP.objects.get(pk=pk)
    except OTP.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = OTPSerializer(otp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        otp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST", "PUT", "DELETE"])
def manage_token(request, pk=None):
    if request.method == "POST":
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if pk is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        token = Token.objects.get(pk=pk)
    except Token.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = TokenSerializer(token, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    data = request.data
    salt = data["salt"]
    hashed_password = data["password"]
    # check if uid is in request
    uid = 0
    if "uid" in data:
        uid = data["uid"]
    else:    
        uid = random.randint(0, 9999999999)
    user_data = {
        "uid": uid,
        "uname": data["uname"],
        "uemail": data["uemail"],
        "cid": Corporation.objects.get(cname=data["cname"]).cid,
        "is_admin": data["is_admin"],
    }
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        userPassword = {"uid": uid, "hash": hashed_password, "salt": salt}
        auth_serializer = AuthSerializer(data=userPassword)
        if auth_serializer.is_valid():
            auth_serializer.save()

        expiry_date = datetime.now() + timedelta(minutes=10)
        otp_code = "".join(random.choices(string.digits, k=6))
        otp_data = {
            "uid": uid,
            "otp": otp_code,
            "expiry_date": expiry_date.strftime("%Y-%m-%d %H:%M:%S"),
        }

        otp_serializer = OTPSerializer(data=otp_data)
        if otp_serializer.is_valid():
            otp_serializer.save()

        send_otp_email(data["uemail"], otp_code, expiry_date)

        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def verifyOTP(request):
    data = request.data
    uid = data.get("uid")
    otp_code = data.get("otp")

    if not uid or not otp_code:
        return Response(
            {"error": "UID and OTP are required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        otp_entry = OTP.objects.get(uid=uid, otp=otp_code)
    except OTP.DoesNotExist:
        return Response(
            {"error": "Invalid UID or OTP"}, status=status.HTTP_400_BAD_REQUEST
        )

    if otp_entry.expiry_date < datetime.now():
        return Response(
            {"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST
        )

    token = ""
    for i in range(40):
        token += random.choice(string.ascii_letters + string.digits)
    print(token)

    if otp_entry.otp == otp_code:
        token_data = {"uid": uid, "token": token}
        try:
            token_entry = Token.objects.get(uid=uid)
            token_entry.token = token
            token_entry.save()
        except Token.DoesNotExist:
            tokenSerializer = TokenSerializer(data=token_data)
            if tokenSerializer.is_valid():
                tokenSerializer.save()
            else:
                return Response(
                    tokenSerializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        return Response({"token": token}, status=status.HTTP_200_OK)

    return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


def send_otp_email(to_email, otp_code, expiry_date):
    from_email = "bitforge.capstone@gmail.com"
    from_password = os.getenv("APP_PASSWORD")
    subject = "Your OTP Code"

    body = f"Your OTP code is {otp_code}.\n It will expire on {expiry_date}."

    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, from_password)
        text = message.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

@api_view(["POST"])
def otpRegenerate(request):
    data = request.data
    uid = data.get("uid")
    uemail = data.get("uemail")

    if not uid:
        return Response(
            {"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        otp_entry = OTP.objects.get(uid=uid)
    except OTP.DoesNotExist:
        return Response({"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)

    expiry_date = datetime.now() + timedelta(minutes=10)
    otp_code = "".join(random.choices(string.digits, k=6))
    otp_entry.otp = otp_code
    otp_entry.expiry_date = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
    otp_entry.save()

    send_otp_email(uemail, otp_code, expiry_date)

    return Response(
        {"message": "OTP regenerated successfully"}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def hvstat(request):
    return Response({"message": "Server is running"}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def getSalt(request):
    data = request.data
    uemail = data.get("uemail")

    print(uemail)

    if not uemail:
        return Response(
            {"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(uemail=uemail).exists():
        user = User.objects.get(uemail=uemail)
    else:
        user = User.objects.get(uname=uemail)

    uid = user.uid
    salt = Auth.objects.get(uid=uid).salt

    try:
        return Response({"salt": salt, "uid": uid}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid username"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def signin(request):
    data = request.data
    uid = data.get("uid")
    password = data.get("password")
    uemail = User.objects.get(uid=uid).uemail

    hash = Auth.objects.get(uid=uid).hash

    if hash == password:
        expiry_date = datetime.now() + timedelta(minutes=10)
        otp_code = "".join(random.choices(string.digits, k=6))
        otp_data = {
            "uid": uid,
            "otp": otp_code,
            "expiry_date": expiry_date.strftime("%Y-%m-%d %H:%M:%S"),
        }

        otp_serializer = OTPSerializer(data=otp_data)
        if otp_serializer.is_valid():
            otp_serializer.save()

        send_otp_email(uemail, otp_code, expiry_date)

        return Response(
            {"message": "User signed in successfully"}, status=status.HTTP_200_OK
        )
    return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def signout(request):
    data = request.data
    token = data.get("token")

    if not token:
        return Response(
            {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    databaseToken = Token.objects.get(token=token)
    if not databaseToken:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        token_entry = Token.objects.get(token=token)
        token_entry.delete()
        return Response(
            {"message": "User signed out successfully"}, status=status.HTTP_200_OK
        )
    except Token.DoesNotExist:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def getToken(request):
    data = request.data
    uid = data.get("uid")
    password = data.get("password")

    if not uid or not password:
        return Response(
            {"error": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        auth = Auth.objects.get(uid=uid)
        if auth.hash == password:
            token = ""
            for i in range(40):
                token += random.choice(string.ascii_letters + string.digits)
            print(token)
            token_data = {"uid": uid, "token": token}
            try:
                token_entry = Token.objects.get(uid=uid)
                token_entry.token = token
                token_entry.save()
            except Token.DoesNotExist:
                tokenSerializer = TokenSerializer(data=token_data)
                if tokenSerializer.is_valid():
                    tokenSerializer.save()
                else:
                    return Response(
                        tokenSerializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

            return Response({"token": token}, status=status.HTTP_200_OK)

        return Response(
            {"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
        )
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid username"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Auth.DoesNotExist:
        return Response(
            {"error": "Auth entry not found for user"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def changePassword(request):
    data = request.data
    uid = data.get("uid")
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    token = data.get("token")

    if not token:
        return Response(
            {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        dataToken = Token.objects.get(uid=uid)
    except Token.DoesNotExist:
        return Response({"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND)

    if dataToken.token != token:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    if not uid or not old_password or not new_password:
        return Response(
            {"error": "Username, old password and new password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        auth = Auth.objects.get(uid=uid)
        if auth.hash == old_password:
            auth.hash = new_password
            auth.save()
            return Response(
                {"message": "Password changed successfully", "status": "200"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST
        )
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid username"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Auth.DoesNotExist:
        return Response(
            {"error": "Auth entry not found for user"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def changeUserDetails(request):
    data = request.data
    uid = data.get("uid")
    uname = data.get("uname")
    uemail = data.get("uemail")
    token = data.get("token")

    if not token:
        return Response(
            {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        dataToken = Token.objects.get(uid=uid)
    except Token.DoesNotExist:
        return Response({"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND)

    if dataToken.token != token:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    if not uid:
        return Response(
            {"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(uid=uid)
        user.uname = uname
        user.uemail = uemail
        user.save()
        return Response(
            {"message": "User details updated successfully", "status": "200"},
            status=status.HTTP_200_OK,
        )
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid username"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
@permission_classes([AllowAny])
def upload_video(request):
    if request.method == "POST":
        data = request.data
        uid = data.get("uid")
        token = data.get("token")
        print(data)

        if not token:
            return Response(
                {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            dataToken = Token.objects.get(uid=uid)
        except Token.DoesNotExist:
            return Response(
                {"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if dataToken.token != token:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            server_url = serializer.data["media_url"]
            return Response({"server_url": server_url}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def list_videos(request):
    videos = Media.objects.all()
    return render(request, "list_videos.html", {"videos": videos})


@api_view(["POST"])
@permission_classes([AllowAny])
def upload_success(request):
    return render(request, "upload_success.html")


@api_view(["POST"])
@permission_classes([AllowAny])
def lookup(request):
    data = request.data
    uid = data.get("uid")
    token = data.get("token")

    if not token:
        return Response(
            {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        dataToken = Token.objects.get(uid=uid)
    except Token.DoesNotExist:
        return Response({"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND)

    if dataToken.token != token:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    if not uid:
        return Response(
            {"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        media = Media.objects.filter(uid=uid)
        serializer = MediaSerializer(media, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Media.DoesNotExist:
        return Response({"error": "Media not found"}, status=status.HTTP_404_NOT_FOUND)


def verifyToken(uid, token):
    if not token:
        return Response(
            {"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        dataToken = Token.objects.get(uid=uid)
    except Token.DoesNotExist:
        return Response({"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND)

    if dataToken.token != token:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([AllowAny])    
def devLogin(request):    
    uname = 'dev'
    uemail = 'dev@gmail.com'
    
    if not Corporation.objects.filter(cname='dev').exists():
        corporation_data = {
            'cname': 'dev'
        }
        corporation_serializer = CorporationSerializer(data=corporation_data)
        if corporation_serializer.is_valid():
            corporation_serializer.save()
        else:
            return Response(corporation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    

        
    if not User.objects.filter(uname=uname).exists():
        uid = random.randint(0, 999999999)
        user_data = {
            'uid': uid,
            'uname': "dev",
            'uemail': 'dev@gmail.com',
            'cid': Corporation.objects.get(cname='dev').cid,
            'is_admin': True
        }
        
        user_serializer = UserSerializer(data=user_data)
        if(user_serializer.is_valid()):
            user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
        uid = User.objects.get(uname=uname).uid

        salt = "a30855d328c251efd440ddd9103be85c"
        hash = "271139b6f8ce1ffe656b77703f664e838673a9a4cfcb145496135cf1616ed6a316ad47b538dbebd61e442ed43abf5dd6b211da3fde1a62d5e4ed527275bd6d05"
        
        auth_serializer = AuthSerializer(data={'uid': uid, 'hash': hash, 'salt': salt})
        if(auth_serializer.is_valid()):
            auth_serializer.save()
        else:
            return Response(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
    
    uid = User.objects.get(uname=uname).uid
    
    token = ''
    for i in range(40):
        token += random.choice(string.ascii_letters + string.digits)
    print(token)

    token_data = {"uid": uid, "token": token}

    try:
        token_entry = Token.objects.get(uid=uid)
        token_entry.token = token
        token_entry.save()
    except Token.DoesNotExist:
        tokenSerializer = TokenSerializer(data=token_data)
        if tokenSerializer.is_valid():
            tokenSerializer.save()
        else:
            return Response(tokenSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"token": token, "uid": uid, "uemail": uemail, "uname": uname},
        status=status.HTTP_200_OK,
    )


def download(request):
    return render(request, "./download.html")


@api_view(["POST"])
@permission_classes([AllowAny])
def uploadFile(request):
    data = request.data
    uid = data.get("uid")
    utoken = data.get("token")
    mediaName = data.get("media_name")
    mediaUrl = data.get("media_url")
    mid = data.get("mid")
    command = data.get("command")

    #! Commented for dev purposes
    if not utoken:
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        dataToken = Token.objects.get(uid=uid)
    except Token.DoesNotExist:
        return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)

    if dataToken.token != utoken:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.get(uid=uid)
    cid = user.cid.cname
    
    # corporation = Corporation.objects.get(cid=cid)
    
    print("Corporation: ", cid) 

    size = data.get("size")
    message = {"size": size, "uid": uid, "utoken": utoken, "corporation": cid}
    
    print("CORPORATION: ", cid)

    print(message)

    url = "http://" + HOST_IP + ":8006/brokerStore"
    response = requests.post(url, json=message)
    data = response.json()
    print(response.status_code)
    print(response.json())
    
    if command == "SEND":
        #! insert into media table
        #TODO Must fix this, then ip and other issues will fix too
        media_data = {
            "uid": uid,
            "mid": mid,
            "media_name": mediaName,
            "media_url": mediaUrl,
            "aid": response.json()["aid"],
        }
        
        media_serializer = MediaSerializer(data=media_data, context={'request': request})
        if media_serializer.is_valid():
            media_serializer.save()
        else:
            return Response(media_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {"aip": data["aip"], "aport": data["aport"]}, status=status.HTTP_200_OK
    )

@api_view(["POST"])
@permission_classes([AllowAny])
def getCID(request):
    data = request.data
    cname = data.get("cname")
    if not cname:
        return Response(
            {"error": "Corporation name is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    if Corporation.objects.filter(cname=cname).exists():
        corporation = Corporation.objects.get(cname=cname)
        return Response({"cid": corporation.cid}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Corporation not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(["POST"])
@permission_classes([AllowAny])
def isInCorporation(request):
    data = request.data
    uid = data.get("uid")
    cid = data.get("cid")
    if not uid or not cid:
        return Response(
            {"error": "UID and CID are required"}, status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(uid=uid, cid=cid).exists():
        return Response({"message": "User is in corporation"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "User is not in corporation"}, status=status.HTTP_404_NOT_FOUND)    
    
@api_view(["POST"])
@permission_classes([AllowAny])
def registerCorporation(request):
    data = request.data
    cname = data.get("cname")
    if not cname:
        return Response(
            {"error": "Corporation name is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    if Corporation.objects.filter(cname=cname).exists():
        return Response({"error": "Corporation already exists"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        corporation_data = {
            "cname": cname
        }
        corporation_serializer = CorporationSerializer(data=corporation_data)
        if corporation_serializer.is_valid():
            corporation_serializer.save()
            return Response(corporation_serializer.data, status=status.HTTP_201_CREATED)
        return Response(corporation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
@permission_classes([AllowAny])
def addUserToCorporation(request):
    data = request.data
    uid = data.get("uid")
    cid = data.get("cid")
    if not uid or not cid:
        return Response(
            {"error": "UID and CID are required"}, status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(uid=uid).exists():
        user = User.objects.get(uid=uid)
        user.cid = cid
        user.save()
        return Response({"message": "User added to corporation"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(["POST"])
@permission_classes([AllowAny])
def makeAdmin(request):
    data = request.data
    uid = data.get("uid")
    if not uid:
        return Response(
            {"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(uid=uid).exists():
        user = User.objects.get(uid=uid)
        user.is_admin = True
        user.save()
        return Response({"message": "User is now an admin"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["POST"])
@permission_classes([AllowAny])
def joinTeam(request):
    data = request.data
    uid = data.get("uid")
    cname = data.get("teamName")
    admin = data.get("admin")
    token = data.get("token")
    email = data.get("email")
    
    print(data)

    if not uid or not cname or not email or not token:
        print("error1")
        return Response(
            {"error": "UID and team name are required"}, status=status.HTTP_400_BAD_REQUEST
        )
        
    try:
        if(not Corporation.objects.filter(cname=cname).exists()):
            User.objects.get(uid=uid).delete()
            print("No corporation found")
            return Response(
                {"error": "Corporation not found"}, status=status.HTTP_404_NOT_FOUND
            )
            
        # check if email is in TokenCorporation and token matches
        if TokenCorporation.objects.filter(email=email, token=token).exists():
            print("email and token match")
        else:
            User.objects.get(uid=uid).delete()
            return Response(
                {"error": "Invalid email or token"}, status=status.HTTP_400_BAD_REQUEST
            ) 
        
        corporation, created = Corporation.objects.get_or_create(cname=cname)

        user = User.objects.get(uid=uid)
        user.cid = corporation 
        user.is_admin = admin
        user.save()
        
        return Response(
            {"message": "User joined team successfully"}, status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
@api_view(["POST"])
@permission_classes([AllowAny])
def createTeam(request):
    data = request.data
    cname = data.get("teamName")
    uid = data.get("uid")
    admin = data.get("admin", True)

    if not cname or not uid:
        return Response(
            {"error": "Team name and UID are required"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        if Corporation.objects.filter(cname=cname).exists():
            User.objects.get(uid=uid).delete()
            return Response({"error": "Team already exists"}, status=status.HTTP_400_BAD_REQUEST)

        corporation_data = {"cname": cname}
        corporation_serializer = CorporationSerializer(data=corporation_data)
        if corporation_serializer.is_valid():
            corporation = corporation_serializer.save()

            user = User.objects.get(uid=uid)
            user.cid = corporation
            user.is_admin = admin
            user.save()

            return Response({
                "message": "Team created successfully",
                "team": corporation_serializer.data,
                "user_updated": {
                    "uid": user.uid,
                    "is_admin": user.is_admin
                }
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(corporation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([AllowAny])
def send_invite_email(request):
    data = request.data
    emails = data.get("newMembers")
    teamName = data.get("teamName")
    
    print("Team name: ", teamName)
    print("Emails: ", emails)
    
    if not emails or not teamName:
        return Response(
            {"error": "Emails and team name are required"}, status=status.HTTP_400_BAD_REQUEST
        )
    
    # Generate a token
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=40))
    
    for email in emails:
        tokencorporation_data = {
            'token': token,  # Ensure 'token' matches the field name in the serializer/model
            'email': email
        }
        
        tokencorporation_serializer = TokenCorporationSerializer(data=tokencorporation_data)
        if tokencorporation_serializer.is_valid():
            tokencorporation_serializer.save()
        else:
            return Response(tokencorporation_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
    try:
        for email in emails:
            send_invite(teamName, email, token)
        return Response(
            {"message": "Invites sent successfully"}, status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
def send_invite(teamName, email, token):
    from_email = "bitforge.capstone@gmail.com"
    from_password = os.getenv("APP_PASSWORD")
    subject = "Join our team!"
    body = f"Hello, you have been invited to join {teamName} on our platform. Please sign up and join us! \n\n Download the app here: http://" + HOST_IP + ":8000/download \n\n Use the following token to join the team: " + token
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, from_password)
        text = message.as_string()
        server.sendmail(from_email, email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
  
@api_view(["POST"])
@permission_classes([AllowAny])        
def getTeamName(request):
    data = request.data
    uid = data.get("uid")
    
    if not uid:
        return Response(
            {"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST
        )
        
    print("UID: ", uid)    
    
    try:
        user = User.objects.get(uid=uid)
        teamID = user.cid
        print("Team ID: ", teamID)
        # teamName = Corporation.objects.get(cid=teamID).cname
        teamName = teamID.cname
        print("Team Name: ", teamName)
        return Response(
            {"teamName": teamName}, status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST
        )

@api_view(["POST"])
@permission_classes([AllowAny])        
def getTeamMembers(request):
    data = request.data
    uid = data.get("uid")
    
    if not uid:
        return Response(
            {"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user = User.objects.get(uid=uid)
        teamID = user.cid
        teamMembers = User.objects.filter(cid=teamID)
        
        for member in teamMembers:
            print("Member " + str(member.uid))
        # return each member's name, email, and admin statusw
        users = []
        for member in teamMembers:
            users.append({
                "uid": member.uid,
                "uname": member.uname,
                "uemail": member.uemail,
                "is_admin": member.is_admin,
                "last_signin": member.last_signin.strftime("%H:%M:%S %d-%m-%Y") if member.last_signin else "Never signed in"
            })
        return Response(
            {"teamMembers": users}, status=status.HTTP_200_OK)
        
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST
        )
        
@api_view(["POST"])        
@permission_classes([AllowAny])
def removeMember(request):
    data = request.data
    uid = data.get("uid")
    memberUID = data.get("memberUid")
    
    print(data)
    
    if not uid or not memberUID:
        return Response(
            {"error": "UID and member ID are required"}, status=status.HTTP_400_BAD_REQUEST
        )
      
    #! Put back soon    
    if(uid == memberUID):
        return Response(
            {"error": "Cannot remove yourself"}, status=status.HTTP_400_BAD_REQUEST)    
    
    try:
        user = User.objects.get(uid=uid)
        teamID = user.cid
        member = User.objects.get(uid=memberUID)
        print(member.uemail)
        tokenCorporation = TokenCorporation.objects.get(email=member.uemail)
        print(tokenCorporation.email)
        
        if member.cid == teamID:
            member.delete()
            tokenCorporation.delete()
            return Response(
                {"message": "Member removed successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Member not in team"}, status=status.HTTP_400_BAD_REQUEST
            )
    except User.DoesNotExist:
        return Response(
            {"error": "Invalid UID or member ID"}, status=status.HTTP_400_BAD_REQUEST
        )
        
@api_view(["POST"])
@permission_classes([AllowAny])
def userExists(request):
    data = request.data
    email = data.get("email")
    
    print("Running userExists")
    
    if not email:
        return Response(
            {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(uemail=email).exists():
        # return team name too
        user = User.objects.get(uemail=email)
        teamID = user.cid
        teamName = teamID.cname
        return Response(
            {"exists": True, "teamName": teamName}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"exists": False}, status=status.HTTP_200_OK
        )   
        
@api_view(["POST"])
@permission_classes([AllowAny])
def addUser(request):
    data = request.data
    uid = data.get("uid")
    uname = data.get("uname")
    uemail = data.get("uemail")
    cid = data.get("cid")
    is_admin = data.get("is_admin")
    
    if not uid or not uname or not uemail or not cid:
        return Response(
            {"error": "UID, name, email, and team ID are required"}, status=status.HTTP_400_BAD_REQUEST
        )
    
    if User.objects.filter(uid=uid).exists():
        return Response(
            {"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        user_data = {
            "uid": uid,
            "uname": uname,
            "uemail": uemail,
            "cid": cid,
            "is_admin": is_admin
        }
        
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response(
            {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
@api_view(["POST"])
@permission_classes([AllowAny])
def getCorporationUsers(request):
    data = request.data
    cid = data.get("cid")
    
    if not cid:
        return Response(
            {"error": "Team ID is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    
    if Corporation.objects.filter(cid=cid).exists():
        users = User.objects.filter(cid=cid)
        user_data = []
        for user in users:
            user_data.append({
                "uid": user.uid,
                "uname": user.uname,
                "uemail": user.uemail,
                "is_admin": user.is_admin
            })
        return Response(
            {"users": user_data}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND
        )  
        
@api_view(["POST"])
@permission_classes([AllowAny])
def getCorporationUsersID(request):
    data = request.data
    uid = data.get("uid")
    
    if not uid:
        return Response(
            {"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    
    cid = User.objects.get(uid=uid).cid.cid
    
    if Corporation.objects.filter(cid=cid).exists():
        users = User.objects.filter(cid=cid)
        user_data = []
        for user in users:
            user_data.append({
                "uid": user.uid,
                "uname": user.uname,
                "uemail": user.uemail,
                "is_admin": user.is_admin
            })
        return Response(
            {"users": user_data}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND
        )            
        
@api_view(["POST"])
@permission_classes([AllowAny])
def storeToken(request):
    data = request.data
    uid = data.get("uid")
    token = data.get("token")
    
    if not uid or not token:
        return Response(
            {"error": "UID and token are required"}, status=status.HTTP_400_BAD_REQUEST
        )
    
    print("Storing token")
    
    token_data = {"uid": uid, "token": token}
    try:
        token_entry = Token.objects.get(uid=uid)
        token_entry.token = token
        token_entry.save()
        return Response(
            {"message": "Token updated successfully"}, status=status.HTTP_200_OK
        )
    except Token.DoesNotExist:
        token_serializer = TokenSerializer(data=token_data)
        if token_serializer.is_valid():
            token_serializer.save()
            return Response(token_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(token_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def getAllAgentsForUser(request):
    data = request.data
    uid = data.get("uid")
    
    if not uid:
        return Response(
            {"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST
        )
        
    media = Media.objects.filter(uid=uid)
    serializer = MediaSerializer(media, many=True)
    
    return Response(
        {"agents": serializer.data}, status=status.HTTP_200_OK
    )    
    
@api_view(["POST"])
@permission_classes([AllowAny])
def getCID(request):
    data = request.data
    uid = data.get("uid")
    
    if not uid:
        return Response(
            {"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    
    cname = User.objects.get(uid=uid).cid.cname
    cid = Corporation.objects.get(cname=cname).cid
    
    return Response(
        {"cid": cid}, status=status.HTTP_200_OK
    )        
    
@api_view(["POST"])
@permission_classes([AllowAny])
def getUserData(request):
    data = request.data
    uid = data.get("uid")
    
    if not uid:
        return Response(
            {"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    
    user = User.objects.get(uid=uid)
    serializer = UserSerializer(user)
    
    return Response(
        serializer.data, status=status.HTTP_200_OK
    )

@api_view(["POST"])
@permission_classes([AllowAny])
def getLastSignin(request):
    data = request.data
    uid = data.get("uid")
    
    if not uid:
        return Response(
            {"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.get(uid=uid)
    last_signin = user.last_signin
    
    return Response(
        {"last_signin": last_signin}, status=status.HTTP_200_OK
    )
    
@api_view(["POST"])
@permission_classes([AllowAny])
def updateLastSignin(request):
    data = request.data
    uid = data.get("uid")
    
    if not uid:
        return Response(
            {"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST
        )
        
    user = User.objects.get(uid=uid)
    user.last_signin = datetime.now()
    user.save()
    
    return Response(
        {"message": "Last signin updated successfully"}, status=status.HTTP_200_OK
    )

@api_view(["POST"])
@permission_classes([AllowAny])
def getAgentUserConnections(request):
    data = request.data
    uid = data.get("uid")
    
    if not uid:
        return Response(
            {"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST
        )
        
    user = User.objects.get(uid=uid)
    agents = user.agents.all()
    users = user.users.all()
    
    return Response(
        {"agents": agents, "users": users}, status=status.HTTP_200_OK
    )
    
@api_view(["POST"])
@permission_classes([AllowAny])
def getUserAgentConnections(request):
    data = request.data
    uid = data.get("uid")
    
    if not uid:
        return Response(
            {"error": "UID is required"}, status=status.HTTP_400_BAD_REQUEST
        )
        
    user = User.objects.get(uid=uid)
    agents = user.agents.all()
    users = user.users.all()
    
    return Response(
        {"agents": agents, "users": users}, status=status.HTTP_200_OK
    )
    
def send_request_hvstat():
    url = "http://206.189.188.197:8000/hvstat/"
    # data = {"uid": "1234567890"}
    response = requests.get(url)
    # return response.json()

def send_request_verifyOTP():
    url = "http://206.189.188.197:8000/verifyOTP/"
    data = {"uid": "1234567890", "otp": "123456"}
    response = requests.post(url, data=data)
    # return response.json()

def send_request_otpRegenerate():
    url = "http://206.189.188.197:8000/otpRegenerate/"
    data = {"uid": "1234567890", "uemail": "test@test.com"}
    response = requests.post(url, data=data)
    # return response.json()

def send_request_getAgentUserConnections():
    url = "http://206.189.188.197:8000/getAgentUserConnections/"
    data = {"uid": "1"}
    response = requests.post(url, data=data)
    # return response.json()

def send_request_getSalt():
    url = "http://206.189.188.197:8000/getSalt/"
    data = {"uemail": "test@test.com"}
    response = requests.post(url, data=data)
    # return response.json()

def send_request_signin():
    url = "http://206.189.188.197:8000/signin/"
    data = {"uid": "1", "password": "password", "uemail": "dev@gmail.com"}
    response = requests.post(url, data=data)
    # return response.json()

def send_request_signout():
    url = "http://206.189.188.197:8000/signout/"
    data = {"uid": "1"}
    response = requests.post(url, data=data)
    # return response.json()

def send_request_devLogin():
    url = "http://206.189.188.197:8000/devLogin/"
    data = {"uid": "1", "password": "password", "uemail": "dev@gmail.com"}
    response = requests.post(url, data=data)
    # return response.json()
    
def send_request_findOpenPort():
    url = "http://206.189.188.197:8010/findOpenPort/"
    response = requests.get(url)
    # return response.json()
    
def send_request_test():
    url = "http://206.189.188.197:8006/test/"
    data = {"message": "hello"}
    response = requests.post(url, data=data)
    # return response.json()
    
def send_request_simStore():
    url = "http://206.189.188.197:8010/simStore/"
    response = requests.post(url)
    # return response.json()

def send_request_getUserData():
    url = "http://206.189.188.197:8000/getUserData/"
    data = {"uid": "1"}
    response = requests.post(url, data=data)
    # return response.json()

def run_stress_test(num_requests, functions):
    for i in functions:
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            futures = [executor.submit(i) for _ in range(num_requests)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
        end_time = time.time()
        print("Average time taken for ", i.__name__, ": ", (end_time - start_time)/num_requests)   
        
@api_view(["GET"])
@permission_classes([AllowAny])
def getTestData(request):
    num_requests = 100
    functions = [send_request_hvstat, send_request_verifyOTP, send_request_otpRegenerate, send_request_getAgentUserConnections, send_request_getSalt, send_request_signin, send_request_signout, send_request_devLogin]
    data = {}
    for i in functions:
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            futures = [executor.submit(i) for _ in range(num_requests)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
        end_time = time.time()
        print("Average time taken for ", i.__name__, ": ", (end_time - start_time)/num_requests)  
        data[i.__name__] = (end_time - start_time)/num_requests
                 
    print("Data: ", data)             
    return Response(
        {"data": data}, status=status.HTTP_200_OK
    )
        
     
@api_view(["GET"])
@permission_classes([AllowAny])
def requestUptime(request):  # Accept the 'request' argument
    # Retrieve environment variables
    API_TOKEN = os.getenv("API_TOKEN_CAKE")
    TEST_ID = os.getenv("TEST_ID")

    if not API_TOKEN or not TEST_ID:
        return Response({"error": "Missing API_TOKEN_CAKE or TEST_ID"}, status=500)

    # Set the URL for the API endpoint
    url = f'https://api.statuscake.com/v1/uptime/{TEST_ID}'

    # Set the headers with the Authorization token
    headers = {
        'Authorization': f'Bearer {API_TOKEN}',
        'Accept': 'application/json'  # Ensures JSON response
    }

    try:
        # Make the GET request
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()
            uptime = data['data']['uptime']
            return Response({"uptime": uptime}, status=200)
        else:
            return Response({"error": f"Failed to retrieve data. Status code: {response.status_code}"}, status=response.status_code)

    except requests.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)