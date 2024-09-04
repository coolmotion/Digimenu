from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .froms import SignUpForm

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 
    return render(request, 'index.html', )

def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the homepage or dashboard
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('login')  # Redirect back to the login page
    
    # If GET request, render the login page
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You’ve Been Logged Out")
    return redirect('home')

def signup(request):
    if request.user.is_authenticated:
        logout(request)
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # log in user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Your account was created...")
                return redirect('dashboard')
            else:
                messages.error(request, "Authentication failed, please try again.")
        else:
            for field, errors in form.errors.items():
                if errors:  # Check if there are errors for the field
                    first_error = errors[0]  # Get the first error
                    messages.error(request, f"{field.capitalize()}: {first_error}")

    return render(request, 'signup.html', {'form': form})

def signup_thanks(request):
    return render(request, 'signupthanks.html', )

def product(request):
    messages.error(request, "This page is under construction.")
    return redirect('home')

def feature(request):
    messages.error(request, "This page is under construction.")
    return redirect('home')

def contact(request):
    messages.error(request, "This page is under construction.")
    return redirect('home')

def about(request):
    messages.error(request, "This page is under construction.")
    return redirect('home')
