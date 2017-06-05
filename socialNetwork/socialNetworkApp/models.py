# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=10)
    time_online = models.IntegerField(default=0)
    friends = models.ManyToManyField(through=UserFriends)


class UserFriends(models.Model):
    first_user = models.ForeignKey(User, on_delete=models.CASCADE())
    second_user = models.ForeignKey(User, on_delete=models.CASCADE())