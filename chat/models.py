from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save


class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}\'s profile'


@receiver(post_save, sender=User)
def user_pre_save_handler(instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
