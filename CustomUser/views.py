from django.shortcuts import render, redirect
from .forms import Registration, Login
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .custom_manager import CustomUserManager
from django.contrib import messages
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Create your views here.


def registration(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = Registration()
    if request.method == "POST":
        email = request.POST.get('email')
        if CustomUser.objects.filter(email=email).first():
            messages.success(request, 'Email is taken.')
            return redirect('registration')
        
        try:
            auth_token = str(uuid.uuid4())
            form = Registration(request.POST)
            
            if form.is_valid():
                subject = 'Your accounts need to be verified'
                message = f'Hi paste the link to verify your account http://127.0.0.1:8000/user/verify/{auth_token}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                res = send_mail(subject, message, email_from, recipient_list)

                new_form = form.save(commit=False)
                new_form.auth_token = auth_token
                new_form.save()
                #messages.success(request, 'Registration Successful.')
                return redirect('token_send')
        except Exception as e:
            print(e)

    return render(request, 'customuser/registration.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = Login(request.POST)
        if request.POST['email'] and request.POST['password']:
            email = request.POST['email']
            verify_user = CustomUser.objects.get(email=email)
            print(verify_user)
            print(verify_user.is_verified)
            if not verify_user.is_verified:
                messages.error(
                    request, 'Profile is not verified check your mail.')
                return redirect('token_send')
            if form.is_valid():
                password = request.POST['password']
                user = authenticate(email=email, password=password)
                print(user)
                if user:
                    login(request, user)
                    messages.success(request, 'Login Successfully.')
                    print("Login Successfully.")
                    return redirect('home')
            else:
                messages.error(request, 'Invalid username and password.')
                return redirect('login')

        else:
            messages.error(request, 'Fill both field')
            return render(request, 'customuser/login.html', {'form': form})
    else:
        form = Login()

    return render(request, 'customuser/login.html', {'form': form})


def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, 'Logout Successfully.')
        return redirect('home')
    return redirect('login')


def success(request):
    return render(request, 'customuser/success.html')


def token_send(request):
    return render(request, 'customuser/token_send.html')


def verify(request, auth_token):
    try:
        profile_obj = CustomUser.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')


def error_page(request):
    return render(request, 'error.html')
