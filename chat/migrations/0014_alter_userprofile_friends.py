# Generated by Django 3.2.6 on 2021-08-27 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0013_auto_20210827_2113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='user_friends', to='chat.UserProfile'),
        ),
    ]