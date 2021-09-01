from django.db.utils import Error
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotFound
from . import models, forms



@login_required(login_url='login')
def index(request):
    context = {
        'invites_count': models.Invitation.objects.filter(send_to=request.user.profile).count()
    }
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
def search(request, input=''):
    if request.is_ajax():
        search_results = models.UserProfile.objects.only('pk', 'username', 'profile_img') \
        .filter(username__istartswith=input) \
        .filter(~Q(username=request.user.username))
        
        currentFriends = list(map(lambda friend: friend.username, request.user.profile.friends.all()))
        results = []
        for result in search_results:

            is_pending = models.Invitation.objects.filter(send_to=result, send_by=request.user.profile).exists()
            status = 'pending' if is_pending else 'is_friend' if result.username in currentFriends else 'available'
            
            results.append({
                'pk': result.id, 
                'username': result.username, 
                'profile_img': result.profile_img.url if result.profile_img else '/static/chat/img/default_profile.png',
                'status': status
            })

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
        invitation = models.Invitation.objects.get(pk=pk)

        send_to = invitation.send_to
        send_by = invitation.send_by

        send_to.friends.add(send_by)
        send_by.friends.add(send_to)

        invitation.delete()

        return JsonResponse(
            data={
                'status': 200,
                'senderId': send_by.pk, 
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
        invitation = models.Invitation.objects.get(pk=pk)
        invitation.delete()
        return JsonResponse(data={'status': 200}, safe=False)

    return HttpResponseNotFound();


@login_required(login_url='login')
def delete_friend(request, pk):
    if request.is_ajax():
        friend_to_delete = models.UserProfile.objects.get(pk=pk)
        user_profile = models.UserProfile.objects.get(pk=request.user.profile.pk)

        user_profile.friends.remove(friend_to_delete)
        friend_to_delete.friends.remove(user_profile)

        return JsonResponse({'username': friend_to_delete.username}, safe=False)

    return HttpResponseNotFound()


@login_required(login_url='login')
def filter_friends(request, input=''):
    if request.is_ajax():
        filtered_out = list(request.user.profile.friends.filter(~Q(username__istartswith=input)).values('pk'))
        
        filtered_out_ids = [dictionary.get('pk') for dictionary in filtered_out]    

        return JsonResponse(data={'idsToHide': filtered_out_ids})
    return HttpResponseNotFound()


@login_required(login_url='login')
def chat_rooms(request, pk=None):
    all_rooms = request.user.profile.room_set \
        .prefetch_related('message_set', 'message_set__sender') \
        .prefetch_related('members') \
        .all()

    room = all_rooms.get(pk=pk) if pk else None
    friends = request.user.profile.friends.only('pk', 'username', 'profile_img')
    
    form = forms.RoomForm()

    context = {'form': form, 'room': room, 'rooms': all_rooms, 'room_friends': friends}
    return render(request, 'chat/chat_rooms.html', context)


@login_required(login_url='login')
def create_room(request):
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid():
            room = models.Room()
            room.name = form.cleaned_data.get('name')
            room.save()

            invited_friends = models.UserProfile.objects.filter(pk__in=request.POST.getlist('friends'))
            room.members.add(request.user.profile, *invited_friends)

            welcome_msg = models.Message()
            welcome_msg.text = 'Hey! I have just created this room, let\'s chat!'
            welcome_msg.sender = request.user.profile
            welcome_msg.room = room
            welcome_msg.save()

            
            return redirect(reverse('chat_rooms', kwargs={'pk': room.pk}))
    return HttpResponseNotFound()


@login_required(login_url='login')
def filter_rooms(request, input=''):
    if request.is_ajax():
        filtered_out = list(request.user.profile.room_set.filter(~Q(name__istartswith=input)).values('pk'))
        
        filtered_out_ids = [dictionary.get('pk') for dictionary in filtered_out]    

        return JsonResponse(data={'idsToHide': filtered_out_ids})
    return HttpResponseNotFound()

