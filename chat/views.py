from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from . import models, forms



@login_required(login_url='login')
def index(request):
    context = {}
    return render(request, 'chat/index.html', context)


def register(request):
    pass


def login_user(request):
    context = {'form': forms.LoginForm()}

    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            authenticated_user = form.user_cache

            if not authenticated_user:
                messages.error(request, 'Invalid credentials.')
                return redirect(reverse('login', ))

            login(request, authenticated_user)
            return redirect(reverse('index', ))


    return render(request, 'chat/login.html', context)


def logout_user(request):
    logout(request)
    return redirect(reverse('login', ))


