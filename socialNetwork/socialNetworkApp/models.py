# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.utils import timezone

from MySQLdb.constants.FLAG import UNIQUE
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from socialNetwork import settings


class UserFriend(models.Model):
    first_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='first_user')
    second_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='second_user')

    @staticmethod
    def get_user_friends(user_id):
        return UserFriend.objects.filter(Q(first_user=user_id) | Q(second_user=user_id))

    class Meta:
        unique_together = ("first_user", "second_user")


class User(AbstractUser):
    time_spent_online = models.IntegerField(default=0)
    friends = models.ManyToManyField(UserFriend, max_length=20)

    @staticmethod
    def top_ten_logged_users():
        top_ten_users = []
        users = User.objects.all().order_by("time_spent_online")
        for user in users[:10]:
            top_ten_users.append(user)

        return top_ten_users

    # Update time online if the user is logged. If not it gets updated in the logout
    def set_time_online(self):
        user = User.objects.get(id=self.id)

        if user.is_logged:
            time_logged = timezone.now() - user.last_login_date
            user.time_spent_online += time_logged.seconds // 60

    class Meta:
        db_table = 'auth_user'


class Post(models.Model):
    title = models.CharField(max_length=10)
    description = models.CharField(max_length=50)
    date_posted = models.DateTimeField(blank=True, default=timezone.now)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
