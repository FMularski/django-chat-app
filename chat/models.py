from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.utils import timezone


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=False, null=False)
    last_name = models.CharField(max_length=150, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=150, null=False)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(null=False)
    profile_img = models.ImageField(null=True, blank=True, upload_to='uploads')
    friends = models.ManyToManyField('UserProfile', related_name='profiles_with_this_in_friends', blank=True)
    rooms_notifications = models.CharField(max_length=1024, default='', blank=True)

    def __str__(self):
        return f'{self.user.username}\'s profile'

    class Meta:
        ordering = 'username',


class Invitation(models.Model):
    send_by = models.ForeignKey(UserProfile, null=False, on_delete=models.CASCADE, related_name='invitations_sent')
    send_to = models.ForeignKey(UserProfile, null=False, on_delete=models.CASCADE, related_name='invitations_received')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'from {self.send_by.username} to {self.send_to.username}'


class Room(models.Model):
    name = models.CharField(max_length=100)
    last_message_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(UserProfile, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = '-last_message_at', 


class Message(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null=True, blank=True)
    attached_img = models.ImageField(null=True, blank=True)
    likes = models.PositiveSmallIntegerField(default=0)
    sender = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    liked_by = models.CharField(max_length=256, default='')

    class Meta:
        ordering = '-created_at',

    def __str__(self):
        return self.text


@receiver(post_save, sender=User)
def user_post_save_handler(instance, created, **kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.username = instance.username
        profile.first_name = instance.first_name
        profile.last_name = instance.last_name
        profile.email = instance.email
        profile.save()

@receiver(post_save, sender=UserProfile)
def user_profile_post_save_handler(instance, created, **kwargs):
    if not created:
        instance.user.username = instance.username
        instance.user.first_name = instance.first_name
        instance.user.last_name = instance.last_name
        instance.user.email = instance.email
        instance.user.save()


@receiver(post_save, sender=Message)
def message_post_save_handler(instance, created, **kwargs):
    instance.room.last_message_at = timezone.now()
    instance.room.save()

    if created:
        members = instance.room.members.all()
        for member in members:
            if instance.sender.pk != member.pk:
                member.rooms_notifications += f'{instance.room.pk}R'
                member.save()