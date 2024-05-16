from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ProfileForm
from .models import Profile

# DRF imports
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProfileSerializer
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Existing views
def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Your account has been created!')
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()
    return render(request, 'profiles/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are logged in as {username}.")
                return redirect('profile')  # Redirect to the profile page after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'profiles/login.html', {'form': form})

@login_required
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('login')  # Or redirect to another suitable page

    return render(request, 'profiles/profile.html', {
        'user': request.user,
        'profile': profile
    })

# DRF API views
class RegisterView(APIView):
    @csrf_exempt
    def post(self, request):
        data = request.data
        print("Received data:", data)  # Debugging line
        with transaction.atomic():
            user_serializer = UserSerializer(data=data)
            if user_serializer.is_valid():
                user = user_serializer.save()
                Profile.objects.create(user=user)
                return Response(user_serializer.data, status=status.HTTP_201_CREATED)
            print("Errors:", user_serializer.errors)  # Debugging line
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    @csrf_exempt
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        return Response({"message": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
