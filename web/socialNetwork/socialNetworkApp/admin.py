# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from copy import deepcopy

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, UserFriend

# Register your models here.


class CustomUserAdmin(UserAdmin):

     def get_fieldsets(self, request, obj=None):
         fieldsets = deepcopy(self.fieldsets)
         new_fieldsets = fieldsets + (("Custom fields", {"fields": ("time_spent_online", "profile_image")}),)
         return new_fieldsets

admin.site.register(User, CustomUserAdmin)
admin.site.register(Post)
admin.site.register(UserFriend)