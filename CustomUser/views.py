from django.shortcuts import render, redirect
from .forms import Registration, Login
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def registration(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration Successful.')
            return redirect('login')
    else:
        form = Registration()
    return render(request, 'customuser/registration.html',{'form':form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = Login(request.POST)
        if request.POST['email'] and request.POST['password']:
            if form.is_valid():
                email = request.POST['email']
                password = request.POST['password']
                user = authenticate(email=email, password=password)
                print(user)
                if user:
                    login(request, user)
                    messages.success(request,'Login Successfully.')
                    print("Login Successfully.")
                    return redirect('home')
            else:
                messages.error(request,'Invalid username and password.')
                return redirect('login')  
        else:
            messages.error(request,'Fill both field')
            return render(request, 'customuser/login.html',{'form':form})
    else:
        form = Login()
    return render(request, 'customuser/login.html',{'form':form})

def userlogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logout Successfully.')
        return redirect('home')
    return redirect('login')