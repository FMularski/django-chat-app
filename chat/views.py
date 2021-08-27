from django.db.utils import Error
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.core import serializers
from . import models, forms
import json



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

    if request.method == 'POST':
        form = forms.UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'User profile has been updated.')
            except Error as e:
                messages.error(request, e)

    context = {'form': form}
    return render(request, 'chat/edit.html', context)


@login_required(login_url='login')
def friends(request):
    context = {}
    return render(request, 'chat/friends.html', context)


def search(request, input):
    if request.is_ajax():
        search_results = models.UserProfile.objects.only('pk', 'username', 'profile_img').filter(username__istartswith=input)
        
        results = []
        for result in search_results:
            results.append({
                'pk': result.id, 
                'username': result.username, 
                'profile_img': result.profile_img.url if result.profile_img else '/static/chat/img/default_profile.png'
            })

        return JsonResponse(data=results, safe=False)
    
    return HttpResponseNotFound()

