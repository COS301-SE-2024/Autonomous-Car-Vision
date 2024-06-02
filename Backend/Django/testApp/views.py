from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from rest_framework import viewsets
from .serializers import TokenSerializer, UserSerializer, AuthSerializer, OTPSerializer
from .models import User, Auth, OTP, Token
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
import uuid

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
    salt = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
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
    uname = data.get('uname')
    uid = 0
    try:
        uid = User.objects.get(uname=uname)
    except User.DoesNotExist:
        return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
    otp_code = data.get('otp')
    
    uid = uid.uid
    
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
    uname = data.get('uname')
    uid = 0
    try:
        uid = User.objects.get(uname=uname)
    except User.DoesNotExist:
        return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
    
    uid = uid.uid
    
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
    uname = data.get('uname')
    
    if not uname:
        return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(uname=uname)
        auth = Auth.objects.get(uid=user.uid)
        return Response({'salt': auth.salt}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
    except Auth.DoesNotExist:
        return Response({'error': 'Auth entry not found for user'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def signin(request):
    data = request.data
    uemail = data.get('uemail')
    password = data.get('password')
    
    if not uemail or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(uemail=uemail)
        auth = Auth.objects.get(uid=user.uid)
        if auth.hash == password:
            token = ''
            for i in range(40):
                token += random.choice(string.ascii_letters + string.digits)
            print(token)
            token_data = {
                'uid': user.uid,
                'token': token
            }
            try:
                token_entry = Token.objects.get(uid=user.uid)
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
    uname = data.get('uname')
    password = data.get('password')
    
    if not uname or not password:
        return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(uname=uname)
        auth = Auth.objects.get(uid=user.uid)
        if auth.hash == password:
            token = ''
            for i in range(40):
                token += random.choice(string.ascii_letters + string.digits)
            print(token)
            token_data = {
                'uid': user.uid,
                'token': token
            }
            try:
                token_entry = Token.objects.get(uid=user.uid)
                token_entry.token = token
                token_entry.save()
            except Token.DoesNotExist:
                tokenSerializer = TokenSerializer(data=token_data)
            if tokenSerializer.is_valid():
                tokenSerializer.save()
            else:
                return Response(tokenSerializer.errors, status=status.HTTP_400_BAD_REQUEST) 
            
            return Response({'message': 'Token generated successfully'}, status=status.HTTP_200_OK)
            
        return Response({'error': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)
    except Auth.DoesNotExist:
        return Response({'error': 'Auth entry not found for user'}, status=status.HTTP_400_BAD_REQUEST)