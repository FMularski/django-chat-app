from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save


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
    profile_img = models.ImageField(null=True, blank=True)
    friend = models.ForeignKey('UserProfile', related_name='friends', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}\'s profile'


class Invitation(models.Model):
    send_by = models.ForeignKey(UserProfile, null=False, on_delete=models.CASCADE, related_name='invitations_sent')
    send_to = models.ForeignKey(UserProfile, null=False, on_delete=models.CASCADE, related_name='invitations_received')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'from {self.send_by.username} to {self.send_to.username}'


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