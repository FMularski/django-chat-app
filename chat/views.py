from django.db.utils import Error
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse, HttpResponseNotFound
from django.utils import dateformat
from . import models, forms



@login_required(login_url='login')
def index(request):
    context = {
        'invites_count': models.Invitation.objects.filter(send_to=request.user.profile).count(),
        'rooms_notifications': len(str(request.user.profile.rooms_notifications).split(sep='R')) - 1
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
                'profile_img': result.profile_img.url if result.profile_img \
                    else 'https://django-chat-app-bucket.s3.eu-central-1.amazonaws.com/chat/img/default_profile.png',
                'status': status
            })

        return JsonResponse(data=results, safe=False)
    
    return HttpResponseNotFound()


def invite_friend(request, pk):
    if request.is_ajax():
        friend = models.UserProfile.objects.get(pk=pk)
        
        invitation = models.Invitation()
        invitation.send_by = request.user.profile
        invitation.send_to = friend
        invitation.save()

        return JsonResponse(data={'status': 200}, safe=False)

    return HttpResponseNotFound();


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
                    if send_by.profile_img else 'https://django-chat-app-bucket.s3.eu-central-1.amazonaws.com/chat/img/default_profile.png'
                }, 
            safe=False
        )

    return HttpResponseNotFound();


def decline_invitation(request, pk):
    if request.is_ajax():
        invitation = models.Invitation.objects.get(pk=pk)
        invitation.delete()
        return JsonResponse(data={'status': 200}, safe=False)

    return HttpResponseNotFound();


def delete_friend(request, pk):
    if request.is_ajax():
        friend_to_delete = models.UserProfile.objects.get(pk=pk)
        user_profile = models.UserProfile.objects.get(pk=request.user.profile.pk)

        user_profile.friends.remove(friend_to_delete)
        friend_to_delete.friends.remove(user_profile)

        return JsonResponse({'username': friend_to_delete.username}, safe=False)

    return HttpResponseNotFound()


# def filter_friends(request, input=''):
#     if request.is_ajax():
#         filtered_out = list(request.user.profile.friends.filter(~Q(username__istartswith=input)).values('pk'))
        
#         filtered_out_ids = [dictionary.get('pk') for dictionary in filtered_out]    

#         return JsonResponse(data={'idsToHide': filtered_out_ids})
#     return HttpResponseNotFound()


@login_required(login_url='login')
def chat_rooms(request, pk=None):
    # room = models.Room.objects.get(pk=pk) if pk else None
    room = get_object_or_404(models.Room, pk=pk) if pk else None
    members = None

    ''' 
        If room exists, get members and check if user is one of them.
        If not, don't allow to enter 

    '''
    if room:
        members = room.members.all()

        if request.user.profile not in members:
            return HttpResponseNotFound()

        # clear room notifications
        request.user.profile.rooms_notifications = \
            str(request.user.profile.rooms_notifications).replace(f'{room.pk}R', '')
        request.user.profile.save()

    room_data = {
        'pk': room.pk,
        'name': room.name,
        'members': ', '.join([member.username for member in members])
    } if room else None

    friends = request.user.profile.friends.only('pk', 'username', 'profile_img')
    
    form = forms.RoomForm()

    context = {'form': form, 'room_data': room_data, 'room_friends': friends}
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
            welcome_msg.text = f'[System] {request.user.username} has created room \'{room.name}\'.'
            welcome_msg.sender = request.user.profile
            welcome_msg.room = room
            welcome_msg.save()
            
            return redirect(reverse('chat_rooms', kwargs={'pk': room.pk}))
        
        messages.error(request, 'Error while creating a chat room.')
        return redirect(reverse('chat_rooms', ))
    return HttpResponseNotFound()


# def filter_rooms(request, input=''):
#     if request.is_ajax():
#         filtered_out = list(request.user.profile.room_set.filter(~Q(name__istartswith=input)).values('pk'))
        
#         filtered_out_ids = [dictionary.get('pk') for dictionary in filtered_out]    

#         return JsonResponse(data={'idsToHide': filtered_out_ids})
#     return HttpResponseNotFound()


def send_message(request):
    if request.is_ajax():
        message = models.Message()
        message.text = request.POST.get('text')
        message.sender = request.user.profile
        message.room = models.Room.objects.get(pk=request.POST.get('room-pk'))
        message.save()

        request.user.profile.rooms_notifications = str(request.user.profile.rooms_notifications).replace(f'{message.room.pk}R', '')
        request.user.profile.save()

        return JsonResponse(data={
            'pk': message.pk,
            'text': message.text,
            'senderUsername': message.sender.username,
            'senderProfileImg': message.sender.profile_img.url if message.sender.profile_img \
                else 'https://django-chat-app-bucket.s3.eu-central-1.amazonaws.com/chat/img/default_profile.png',
            'createdAt': dateformat.format(message.created_at, 'd.m.Y, H:i')
        }, safe=False)

    return HttpResponseNotFound()


def fetch_messages(request, room_pk):
    if request.is_ajax():
        messages_objs = models.Message.objects \
            .select_related('sender', 'room') \
            .filter(room__pk=room_pk) \
            .order_by('created_at')

        request.user.profile.rooms_notifications = str(request.user.profile.rooms_notifications).replace(f'{room_pk}R', '')
        request.user.profile.save()
        
        messages = []
        for message in messages_objs:
            messages.append({
                'pk': message.pk,
                'createdAt': dateformat.format(message.created_at, 'd.m.Y, H:i'),
                'text': message.text,
                'cssClass': 'user-message' if message.sender.pk == request.user.pk else 'friend-message',
                # 'attachedImg': message.attached_img,
                'likes': message.likes,
                'senderUsername': message.sender.username,
                'senderPK': message.sender.pk,
                'senderProfileImg': message.sender.profile_img.url if message.sender.profile_img \
                    else 'https://django-chat-app-bucket.s3.eu-central-1.amazonaws.com/chat/img/default_profile.png',
                'likedBy': message.liked_by
            })

        return JsonResponse(data={'messages': messages}, safe=False)

    return HttpResponseNotFound()


def fetch_rooms(request):
    if request.is_ajax():
        rooms_obj = request.user.profile.room_set.all()
        
        rooms = []
        for room in rooms_obj:

            last_message =  room.message_set.first()
            last_message_sender = last_message.sender

            rooms.append({
                'pk': room.pk,
                'name': room.name,
                'members': room.members.count(),
                'lastMsgAt': dateformat.format(last_message.created_at, 'd.m.Y, H:i'),
                'lastMsgText': last_message.text[:25] + '...',
                'senderProfileImg': last_message_sender.profile_img.url if last_message.sender.profile_img \
                    else 'https://django-chat-app-bucket.s3.eu-central-1.amazonaws.com/chat/img/default_profile.png',
                'senderUsername': last_message_sender.username,
                'notifications': str(request.user.profile.rooms_notifications).count(f'{room.pk}R')
            })

        return JsonResponse(data={'rooms': rooms}, safe=False)
    
    return HttpResponseNotFound()


def leave_room(request, pk):
    if request.method == 'POST':
        room = models.Room.objects.prefetch_related('members').get(pk=pk)

        goodbye_msg = models.Message()
        goodbye_msg.text = f'[System] {request.user.username} has left the room.'
        goodbye_msg.sender = request.user.profile
        goodbye_msg.room = room
        goodbye_msg.save()

        room.members.remove(request.user.profile)
        messages.success(request, f'You have left \'{room.name}\'.')
        
        if not room.members.count():
            room.delete()
        return redirect(reverse('chat_rooms',)) 

    return HttpResponseNotFound()


def like_message(request, pk):
    if request.is_ajax():
        message = get_object_or_404(models.Message, pk=pk)
        if f'{request.user.profile.pk}L' in message.liked_by:
            message.liked_by = str(message.liked_by).replace(f'{request.user.profile.pk}L', '')
            message.likes -= 1
        else:
            message.liked_by += f'{request.user.profile.pk}L'
            message.likes += 1
        message.save()

        return JsonResponse(data={'status': 200}, safe=True)


    return HttpResponseNotFound()