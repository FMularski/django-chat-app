# Generated by Django 3.2.6 on 2021-08-27 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0017_invitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='friend',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='friends', to='chat.userprofile'),
        ),
    ]
