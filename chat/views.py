from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from . import models, forms



@login_required(login_url='login')
def index(request):
    context = {}
    return render(request, 'chat/index.html', context)


def register(request):
    form = forms.RegisterForm()

    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'User \'{username}\' has been registered. You can now log in.')
            return redirect(reverse('login', ))

    context = {'form': form}
    return render(request, 'chat/register.html', context)


def login_user(request):
    form = forms.LoginForm()

    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.user_cache)
            return redirect(reverse('index', ))
        
    context = {'form': form}
    return render(request, 'chat/login.html', context)


def logout_user(request):
    logout(request)
    return redirect(reverse('login', ))


@login_required(login_url='login')
def edit(request):
    form = forms.UserProfileForm(instance=request.user.profile)
    context = {'form': form}
    return render(request, 'chat/edit.html', context)


