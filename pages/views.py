from django.shortcuts import render, redirect
# from .models import *
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CreateUserForm
from django.contrib import messages


def register_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        form = CreateUserForm
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get("username")
                messages.success(request, "Account created successfully for " + user)
                return redirect("login")

        context = {"form": form}
        return render(request, "register.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "!!Please, try again")
        context = {}
        return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    return redirect("login")


@login_required(login_url='login')
def home_page(request):
    context = {}
    return render(request, "home.html", context)
