from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


admin.site.register(models.User, UserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.UserProfile, UserProfileAdmin)