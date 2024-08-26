from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'index.html', )

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the homepage or dashboard
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')  # Redirect back to the login page
    
    # If GET request, render the login page
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('index')