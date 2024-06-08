from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import TokenSerializer, UserSerializer, AuthSerializer, OTPSerializer, MediaSerializer
from .models import User, Auth, OTP, Token, Media
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import random
import string
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from datetime import datetime, timedelta, timezone
import smtplib
from dotenv import load_dotenv

load_dotenv()

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
    
@api_view(['POST', 'PUT', 'DELETE'])
def manage_user(request, pk=None):
    if request.method == 'POST':
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

    if request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'PUT', 'DELETE'])
def manage_auth(request, pk=None):
    if request.method == 'POST':
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

    if request.method == 'PUT':
        serializer = AuthSerializer(auth, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST', 'PUT', 'DELETE'])
def manage_otp(request, pk=None):
    if request.method == 'POST':
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

    if request.method == 'PUT':
        serializer = OTPSerializer(otp, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        otp.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
  
@api_view(['POST', 'PUT', 'DELETE'])  
def manage_token(request, pk=None):
    if request.method == 'POST':
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

    if request.method == 'PUT':
        serializer = TokenSerializer(token, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):    
    data = request.data      
    salt = data['salt']
    hashed_password = data['password']
    uid = random.randint(0, 999999999)
    user_data = {
        'uid': uid,
        'uname': data['uname'],
        'uemail': data['uemail'],
    }
    user_serializer = UserSerializer(data=user_data)
    if user_serializer.is_valid():
        user = user_serializer.save()
        userPassword = {
            'uid': uid,
            'hash': hashed_password,
            'salt': salt
        }
        auth_serializer = AuthSerializer(data=userPassword)
        if auth_serializer.is_valid():
            auth_serializer.save()
            
        expiry_date = datetime.now() + timedelta(minutes=10) 
        otp_code = ''.join(random.choices(string.digits, k=6))
        otp_data = {
            'uid': uid,
            'otp': otp_code,
            'expiry_date': expiry_date.strftime('%Y-%m-%d %H:%M:%S')
        }

        otp_serializer = OTPSerializer(data=otp_data)
        if otp_serializer.is_valid():
            otp_serializer.save()
            
        send_otp_email(data['uemail'], otp_code, expiry_date)
        
        
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verifyOTP(request):
    data = request.data
    uid = data.get('uid')
    otp_code = data.get('otp')
    
    if not uid or not otp_code:
        return Response({'error': 'UID and OTP are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        otp_entry = OTP.objects.get(uid=uid, otp=otp_code)
    except OTP.DoesNotExist:
        return Response({'error': 'Invalid UID or OTP'}, status=status.HTTP_400_BAD_REQUEST)
    
    if otp_entry.expiry_date < datetime.now(timezone.utc):
        return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
    
    token = ''
    for i in range(40):
        token += random.choice(string.ascii_letters + string.digits)
    print(token)
    
    if(otp_entry.otp == otp_code):
        token_data = {
            'uid': uid,
            'token': token
        }
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
        
        return Response({'token': token}, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

def send_otp_email(to_email, otp_code, expiry_date):
    from_email = 'bitforge.capstone@gmail.com'
    from_password = os.getenv('APP_PASSWORD')
    subject = 'Your OTP Code'
    
    body = f'Your OTP code is {otp_code}.\n It will expire on {expiry_date}.'
    
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        text = message.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")      

@api_view(['POST'])
def otpRegenerate(request):
    data = request.data
    uid = data.get('uid')
    uemail = data.get('uemail')
    
    if not uid:
        return Response({'error': 'UID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        otp_entry = OTP.objects.get(uid=uid)
    except OTP.DoesNotExist:
        return Response({'error': 'Invalid UID'}, status=status.HTTP_400_BAD_REQUEST)
    
    expiry_date = datetime.now() + timedelta(minutes=10) 
    otp_code = ''.join(random.choices(string.digits, k=6)) 
    otp_entry.otp = otp_code
    otp_entry.expiry_date = expiry_date.strftime('%Y-%m-%d %H:%M:%S')
    otp_entry.save()
    
    send_otp_email(uemail, otp_code, expiry_date)
    
    return Response({'message': 'OTP regenerated successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def hvstat(request):
    return Response({'message': 'Server is running'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def getSalt(request):
    data = request.data
    uemail = data.get('uemail')  

    print(uemail)    
    
    if not uemail:
        return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    if User.objects.filter(uemail=uemail).exists():
        user = User.objects.get(uemail=uemail)
    else:
        user = User.objects.get(uname=uemail) 
        
    uid = user.uid
    salt = Auth.objects.get(uid=uid).salt 
       
    try:
        return Response({'salt': salt, 'uid': uid}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    data = request.data
    uid = data.get('uid')
    password = data.get('password')
    uemail = User.objects.get(uid=uid).uemail
    
    hash = Auth.objects.get(uid=uid).hash
         
    if hash == password:   
        expiry_date = datetime.now() + timedelta(minutes=10) 
        otp_code = ''.join(random.choices(string.digits, k=6))
        otp_data = {
            'uid': uid,
            'otp': otp_code,
            'expiry_date': expiry_date.strftime('%Y-%m-%d %H:%M:%S')
        }

        otp_serializer = OTPSerializer(data=otp_data)
        if otp_serializer.is_valid():
            otp_serializer.save()
            
        send_otp_email(uemail, otp_code, expiry_date)
               
        return Response({'message': 'User signed in successfully'}, status=status.HTTP_200_OK)   
    return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def signout(request):
    data = request.data
    token = data.get('token')
    
    if not token:
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    databaseToken = Token.objects.get(token=token)
    if not databaseToken:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        token_entry = Token.objects.get(token=token)
        token_entry.delete()
        return Response({'message': 'User signed out successfully'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)    
  
@api_view(['POST'])
@permission_classes([AllowAny])    
def getToken(request):
    data = request.data
    uid = data.get('uid')
    password = data.get('password')
    
    if not uid or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        auth = Auth.objects.get(uid=uid)
        if auth.hash == password:
            token = ''
            for i in range(40):
                token += random.choice(string.ascii_letters + string.digits)
            print(token)
            token_data = {
                'uid': uid,
                'token': token
            }
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
            
            return Response({'token': token}, status=status.HTTP_200_OK)
            
        return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
    except Auth.DoesNotExist:
        return Response({'error': 'Auth entry not found for user'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def changePassword(request):
    data = request.data
    uid = data.get('uid')
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    token = data.get('token')
        
    if not token:
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        dataToken = Token.objects.get(uid=uid)
    except Token.DoesNotExist:
        return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if dataToken.token != token:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not uid or not old_password or not new_password:
        return Response({'error': 'Username, old password and new password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        auth = Auth.objects.get(uid=uid)
        if auth.hash == old_password:
            auth.hash = new_password
            auth.save()
            return Response({'message': 'Password changed successfully', 'status': '200'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
    except Auth.DoesNotExist:
        return Response({'error': 'Auth entry not found for user'}, status=status.HTTP_400_BAD_REQUEST)    
    
@api_view(['POST'])
@permission_classes([AllowAny])
def changeUserDetails(request):
    data = request.data
    uid = data.get('uid')
    uname = data.get('uname')
    uemail = data.get('uemail')
    token = data.get('token')
    
    if not token:
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        dataToken = Token.objects.get(uid=uid)
    except Token.DoesNotExist:
        return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if dataToken.token != token:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not uid:
        return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(uid=uid)
        user.uname = uname
        user.uemail = uemail
        user.save()
        return Response({'message': 'User details updated successfully', 'status': "200"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
   
@api_view(['POST'])
@permission_classes([AllowAny])
def upload_video(request):
    if request.method == 'POST':
        data = request.data
        uid = data.get('uid')
        token = data.get('token')
        print(data)
        
        if not token:
            return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
    
        try:    
            dataToken = Token.objects.get(uid=uid)
        except Token.DoesNotExist:
            return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)        
    
        if dataToken.token != token:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = MediaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            server_url = serializer.data['media_url']
            return Response({'server_url': server_url}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def list_videos(request):
    videos = Media.objects.all()
    return render(request, 'list_videos.html', {'videos': videos}) 

@api_view(['POST'])
@permission_classes([AllowAny])
def upload_success(request):
    return render(request, 'upload_success.html')
    
@api_view(['POST'])
@permission_classes([AllowAny])
def lookup(request):
    data = request.data
    uid = data.get('uid')
    token = data.get('token')
    
    if not token:
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:    
        dataToken = Token.objects.get(uid=uid)
    except Token.DoesNotExist:
        return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)        
    
    if dataToken.token != token:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)   
    
    if not uid:
        return Response({'error': 'UID is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        media = Media.objects.filter(uid=uid)
        serializer = MediaSerializer(media, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Media.DoesNotExist:
        return Response({'error': 'Media not found'}, status=status.HTTP_404_NOT_FOUND)    
    
def verifyToken(uid, token):
    if not token:
        return Response({'error': 'Token is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:    
        dataToken = Token.objects.get(uid=uid)
    except Token.DoesNotExist:
        return Response({'error': 'Token not found'}, status=status.HTTP_404_NOT_FOUND)        
    
    if dataToken.token != token:
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([AllowAny])    
def devLogin(request):
    uname = request.data.get('uname')
    print(uname)
    
    uid = User.objects.get(uname=uname).uid
    hash = Auth.objects.get(uid=uid).hash
    
    uemail = User.objects.get(uid=uid).uemail
    uname = User.objects.get(uid=uid).uname
    
    token = ''
    for i in range(40):
        token += random.choice(string.ascii_letters + string.digits)
    print(token)
    
    token_data = {
        'uid': uid,
        'token': token
    }
    
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
        
    return Response({'token': token, 'uid': uid, 'uemail': uemail, uname: 'uname'}, status=status.HTTP_200_OK)