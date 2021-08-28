from django.db.utils import Error
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db import IntegrityError
from django.db.models import Q, Value, F
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
    friends = request.user.profile.friends.all()
    invitations = models.Invitation.objects.filter(send_to=request.user.profile).select_related('send_by')

    context = {'friends': friends, 'invitations': invitations}
    return render(request, 'chat/friends.html', context)


@login_required(login_url='login')
def search(request, input):
    if request.is_ajax():
        search_results = models.UserProfile.objects.only('pk', 'username', 'profile_img') \
        .filter(username__istartswith=input) \
        .filter(~Q(username=request.user.username)) \
        .annotate(is_friend=Value(F('pk') in request.user.profile.friends.all()))
        
        results = []
        for result in search_results:
            results.append({
                'pk': result.id, 
                'username': result.username, 
                'profile_img': result.profile_img.url if result.profile_img else '/static/chat/img/default_profile.png',
                'is_friend': result.is_friend
            })

        print(results)

        return JsonResponse(data=results, safe=False)
    
    return HttpResponseNotFound()


@login_required(login_url='login')
def invite_friend(request, pk):
    if request.is_ajax():
        friend = models.UserProfile.objects.get(pk=pk)
        
        invitation = models.Invitation()
        invitation.send_by = request.user.profile
        invitation.send_to = friend
        invitation.save()

        return JsonResponse(data={'status': 200}, safe=False)

    return HttpResponseNotFound();


@login_required(login_url='login')
def accept_invitation(request, pk):
    if request.is_ajax():
        invitation = models.Invitation.objects.get(send_by__pk=pk)
        send_to = invitation.send_to
        send_by = invitation.send_by

        send_to.friends.add(send_by)
        send_to.save()

        send_by.friends.add(send_to)
        send_by.save()

        invitation.delete()

        return JsonResponse(
            data={
                'status': 200, 
                'senderUsername': send_by.username, 
                'senderProfileImg': send_by.profile_img.url \
                    if send_by.profile_img else '/static/chat/img/default_profile.png'
                }, 
            safe=False
        )

    return HttpResponseNotFound();


@login_required(login_url='login')
def decline_invitation(request, pk):
    if request.is_ajax():
        invitation = models.Invitation.objects.get(send_by__pk=pk)
        invitation.delete()
        
        return JsonResponse(data={'status': 200}, safe=False)

    return HttpResponseNotFound();



