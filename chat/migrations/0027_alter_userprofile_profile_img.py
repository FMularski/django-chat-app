# Generated by Django 3.2.6 on 2021-09-05 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0026_alter_userprofile_rooms_notifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
