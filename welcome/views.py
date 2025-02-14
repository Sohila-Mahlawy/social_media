from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
    return render(request, 'home.html')


# Register View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('register')
        
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login')
    
    return render(request, 'register.html')

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('home')  # Redirect to a home page or dashboard
        else:
            messages.error(request, "Invalid username or password!")
            return redirect('login')
    
    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')
