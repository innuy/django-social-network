# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from django.utils import timezone

from MySQLdb.constants.FLAG import UNIQUE
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from socialNetwork import settings
import logging


class UserFriend(models.Model):
    first_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='first_user')
    second_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='second_user')

    @staticmethod
    def get_user_friends(user_id):
        """
        Get user friends from a user id
        :param user_id: User identifier (integer)

        :return: list of user objects
        """
        friendships = UserFriend.objects.filter(Q(first_user=user_id) | Q(second_user=user_id))
        user_friends = []
        for friendship in friendships:
            try:
                # Select friend from UserFriend relationship
                if friendship.first_user.id != user_id:
                    user_friends.append(friendship.first_user)
                else:
                    user_friends.append(friendship.second_user)
            except Exception as e:
                # [TODO] see log
                # TODO: check log traceback
                logger.exception(e)

        return user_friends

    class Meta:
        unique_together = ("first_user", "second_user")


class User(AbstractUser):
    time_spent_online = models.IntegerField(default=0)
    friends = models.ManyToManyField(UserFriend)

    @staticmethod
    def top_ten_logged_users():
        """
        Get the 10 users that spent more time online
        :return: list of user objects
        """
        top_ten_users = []
        users = User.objects.order_by("time_spent_online")[:10]
        for user in users:
            top_ten_users.append(user)

        return top_ten_users

    def get_unknown_users(self):
        """
        Get users that are not in the user's friends list.
        :return: list of user objects
        """
        users = UserFriend.get_user_friends(self.id)
        friends_ids = [user.pk for user in users]
        unknown_users = User.objects.exclude(pk__in=friends_ids + [self.id])

        return unknown_users

    def set_time_online(self):
        """
        Update the time that the user spent logged in.
        Triggered by logout operation.
        """
        user = User.objects.get(id=self.id)
        time_logged = timezone.now() - user.last_login
        self.time_spent_online += time_logged.total_seconds() // 60
        User.save(self)

    class Meta:
        db_table = 'auth_user'


class Post(models.Model):
    """
    User messages
    """
    title = models.CharField(max_length=10)
    description = models.CharField(max_length=50)
    date_posted = models.DateTimeField(blank=True, default=timezone.now)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
