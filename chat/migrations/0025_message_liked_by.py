# Generated by Django 3.2.6 on 2021-09-04 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0024_userprofile_rooms_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='liked_by',
            field=models.CharField(default='', max_length=256),
        ),
    ]
