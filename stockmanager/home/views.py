# Loek van Steijn

from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def index(request):
    """Renders the homepage"""
    return render(request, "home/index.html")

def login_view(request):
    """Renders the login page"""
    return render(request, "user/login.html")

def register(response):
    """Checks if user registration form has been filled out correctly and saves data"""

    if response.method == "POST":
        form = RegisterForm(response.POST)

        # If valid response it creates account and redirects to login page
        if form.is_valid():
            form.save()
            return redirect("login")

    # else it renders the register form again
    form = RegisterForm()
    return render(response, "user/register.html", {"form":form})
