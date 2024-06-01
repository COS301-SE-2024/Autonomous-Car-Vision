from rest_framework import viewsets
from .serializers import UserSerializer, AuthSerializer, OTPSerializer
from .models import User, Auth, OTP
from rest_framework.permissions import IsAuthenticated

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

# # User Views
# def user_list(request):
#     users = User.objects.all()
#     return render(request, 'myapp/user_list.html', {'users': users})

# def user_create(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = UserForm()
#     return render(request, 'myapp/user_form.html', {'form': form})

# def user_update(request, uid):
#     user = get_object_or_404(User, uid=uid)
#     if request.method == 'POST':
#         form = UserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user_list')
#     else:
#         form = UserForm(instance=user)
#     return render(request, 'myapp/user_form.html', {'form': form})

# def user_delete(request, uid):
#     user = get_object_or_404(User, uid=uid)
#     if request.method == 'POST':
#         user.delete()
#         return redirect('user_list')
#     return render(request, 'myapp/user_confirm_delete.html', {'object': user})

# # Auth Views
# def auth_list(request):
#     auths = Auth.objects.all()
#     return render(request, 'myapp/auth_list.html', {'auths': auths})

# def auth_create(request):
#     if request.method == 'POST':
#         form = AuthForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('auth_list')
#     else:
#         form = AuthForm()
#     return render(request, 'myapp/auth_form.html', {'form': form})

# def auth_update(request, id):
#     auth = get_object_or_404(Auth, id=id)
#     if request.method == 'POST':
#         form = AuthForm(request.POST, instance=auth)
#         if form.is_valid():
#             form.save()
#             return redirect('auth_list')
#     else:
#         form = AuthForm(instance=auth)
#     return render(request, 'myapp/auth_form.html', {'form': form})

# def auth_delete(request, id):
#     auth = get_object_or_404(Auth, id=id)
#     if request.method == 'POST':
#         auth.delete()
#         return redirect('auth_list')
#     return render(request, 'myapp/auth_confirm_delete.html', {'object': auth})

# # OTP Views
# def otp_list(request):
#     otps = OTP.objects.all()
#     return render(request, 'myapp/otp_list.html', {'otps': otps})

# def otp_create(request):
#     if request.method == 'POST':
#         form = OTPForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('otp_list')
#     else:
#         form = OTPForm()
#     return render(request, 'myapp/otp_form.html', {'form': form})

# def otp_update(request, id):
#     otp = get_object_or_404(OTP, id=id)
#     if request.method == 'POST':
#         form = OTPForm(request.POST, instance=otp)
#         if form.is_valid():
#             form.save()
#             return redirect('otp_list')
#     else:
#         form = OTPForm(instance=otp)
#     return render(request, 'myapp/otp_form.html', {'form': form})

# def otp_delete(request, id):
#     otp = get_object_or_404(OTP, id=id)
#     if request.method == 'POST':
#         otp.delete()
#         return redirect('otp_list')
#     return render(request, 'myapp/otp_confirm_delete.html', {'object': otp})