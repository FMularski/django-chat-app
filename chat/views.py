from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import models



@login_required(login_url='login')
def index(request):
    context = {}
    return render(request, 'chat/index.html', context)


def login_user(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if not user:
            messages.error(request, 'Invalid credentials.')
            return redirect(reverse('login', ))

        login(request, user)
        return redirect(reverse('index', ))


    return render(request, 'chat/login.html', context)


def logout_user(request):
    logout(request)
    return redirect(reverse('login', ))


