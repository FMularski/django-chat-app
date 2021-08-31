# from chatapp.chat.views import register
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


admin.site.register(models.User, UserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.UserProfile, UserProfileAdmin)


class InvitationAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Invitation, InvitationAdmin)


class RoomAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Room, RoomAdmin)


class MessageAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Message, MessageAdmin)