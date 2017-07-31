# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils import timezone

from socialNetwork import settings

logger = logging.getLogger(__name__)


class UserFriend(models.Model):
    first_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='first_user')
    second_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='second_user')

    @staticmethod
    def get_user_friends(user_id):
        """
        Get user friends from a user id
        :type user_id: int
        :param user_id: User identifier
        :return: list of user objects
        """
        friendship_list = UserFriend.objects.filter(Q(first_user=user_id) | Q(second_user=user_id))

        user_friends = [friendship.first_user if friendship.first_user.id != user_id else friendship.second_user for
                        friendship in friendship_list.iterator()]

        return user_friends

    def save(self, *args, **kwargs):
        """
        Always saves the user with smaller id on the first
        user and the bigger on the second user.
        Doing this we avoid to add repeated friendships
        """

        bigger = self.first_user if self.first_user.id >= self.second_user.id else self.second_user
        smaller = self.first_user if bigger == self.second_user else self.second_user
        self.first_user = smaller
        self.second_user = bigger
        super(UserFriend, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("first_user", "second_user")


    def __str__(self):
        return self.second_user.username

class User(AbstractUser):
    time_spent_online = models.IntegerField(default=0)
    profile_image = models.ImageField(upload_to='users', blank=True, null=True)

    def image_tag(self):
        return u'<img src="%s" />' % '/static/users'
    image_tag.short_description = 'Images'
    image_tag.allow_tags = True

    @staticmethod
    def top_ten_logged_users():
        """
        Get the 10 users that spent more time online
        :return: list of user objects
        """
        users = User.objects.order_by("-time_spent_online")[:10]
        return [user for user in users.iterator()]

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
        user = self
        time_logged = timezone.now() - user.last_login
        user.time_spent_online += time_logged.total_seconds() // 60
        user.save()

    class Meta:
        db_table = 'auth_user'


class Post(models.Model):
    """
    User messages
    """
    title = models.CharField(max_length=10, null=False)
    description = models.CharField(max_length=50)
    date_posted = models.DateTimeField(blank=True, default=timezone.now)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
