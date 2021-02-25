from django.contrib.auth import login, logout
from django.shortcuts import render, redirect

from accounts.forms import SignUpForm, EmailLoginForm

# Create your views here.


def my_account(request):
    """Display logged in user's account page"""
    return render(request, "registration/account.html")


def signup_view(request, backend="django.contrib.auth.backends.ModelBackend"):
    """Signup users into their accounts"""
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(
                request, user, backend="django.contrib.auth.backends.ModelBackend",
            )
            return redirect("my_account")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    """Log in users into their accounts"""
    if request.method == "POST":
        form = EmailLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("my_account")
    else:
        form = EmailLoginForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    """Log out users from their accounts"""
    logout(request)
    return render(request, "registration/logged_out.html")
