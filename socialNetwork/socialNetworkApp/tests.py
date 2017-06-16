# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import datetime
from time import timezone

from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse

from socialNetworkApp.models import User, UserFriend, Post


class UserFriendTestCase(TestCase):
    def setUp(self):
        self.first_user = User.objects.create(username="paul", email="a")
        self.second_user = User.objects.create(username="jhon", password="a", email="a")
        self.first_user.set_password("a")
        self.first_user.save()

    def test_get_user_friends(self):
        """
        Gets pauls friends
        :return:
        """
        UserFriend.objects.create(first_user=self.first_user, second_user=self.second_user)
        client = Client()
        client.login(username="paul", password="a")
        response = client.get(reverse("friends"))
        # Get paul's friend: Jhon
        data = response.context["users"][0]['username']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, self.second_user.username)

    def test_get_user_friends_unauthorized_user(self):
        UserFriend.objects.create(first_user=self.first_user, second_user=self.second_user)
        client = Client()
        response = client.get(reverse("friends"))
        self.assertEqual(response.status_code, 403)

    def test_add_new_friend_unauthorized_user(self):
        client = Client()
        data = {"second_user": self.second_user}

        response = client.post(reverse("friends"), data, content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_add_new_friend(self):
        client = Client()
        client.login(username="paul", password="a")
        data = {"second_user": self.second_user.id}

        response = client.post(reverse("friends"), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, UserFriend.objects.all().count())

    def test_add_unexistent_new_friend(self):
        """
        pre: doesen't exist a user with id 99999999
        Tries to add a friend that doesen't exists
        """
        client = Client()
        client.login(username="paul", password="a")
        data = {"second_user": 99999999}

        response = client.post(reverse("friends"), data)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, UserFriend.objects.all().count())

class UserTestCase(TestCase):
    def test_get_unknown_users(self):
        """
        Get all the users that aren't included in the logged user friends list.
        Three friends are created: paul, jhon and bob. Bob is the only one that is not paul's friend list.
        """
        first_user = User.objects.create(username="paul", email="a")
        second_user = User.objects.create(username="jhon", password="a", email="a")
        third_user = User.objects.create(username="bob", password="a", email="a")
        UserFriend.objects.create(first_user=first_user, second_user=second_user)
        first_user.set_password("a")
        first_user.save()
        client = Client()
        client.login(username="paul", password="a")
        response = client.get(reverse("users"))
        self.assertEqual(response.status_code, 200)
        data = response.context['users']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['username'], "bob")


class RankingTestCase(TestCase):
    def test_get_top_user_logged_users(self):
        """
        Get the users that spent more time logged in.
        The first user on the returned list will be tha last one on the ranking board. Jhon is the one that spent less time online.
        """
        first_user = User.objects.create(username="paul", email="a", time_spent_online=5)
        second_user = User.objects.create(username="jhon", password="a", email="a", time_spent_online=2)
        third_user = User.objects.create(username="bob", password="a", email="a", time_spent_online=7)
        first_user.set_password("a")
        first_user.save()
        client = Client()
        response = client.get(reverse("ranking"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        users = data['users']
        #
        self.assertEqual(users[0]['username'], "jhon")


class PostTestCase(TestCase):
    def setUp(self):
        first_user = User.objects.create(username="paul", email="a")
        first_user.set_password("a")
        first_user.save()
        Post.objects.create(title="post", author=first_user, date_posted=datetime.date.today())
        Post.objects.create(title="secondPost", author=first_user, date_posted=datetime.date(2013, 10, 7))
        Post.objects.create(title="thirdPost", author=first_user, date_posted=datetime.date(2011, 10, 7))

    def test_get_posts(self):
        """
        Get all the users posts sorted by the date posted. Two posts are created on the setUp. The first post on the list is the most recent.
        """
        client = Client()
        client.login(username="paul", password="a")
        response = client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['posts'][0]['date_posted'].year, 2017)
        response = client.post(reverse("logout"), content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_get_posts_unauthorized_user(self):
        second_user = User.objects.create(username="jhon", email="a", password="b")
        client = Client()
        client.login(username="jhon", password="a")
        response = client.get(reverse("index"))
        self.assertEqual(response.status_code, 403)


class TimeOnlineTestCase(TestCase):
    def test_time_online(self):
        # [TODO] calculate time online
        """
        Test that the time that the user spent online is setted correctly
        :return:
        """
        first_user = User.objects.create(username="paul", email="a")
        first_user.set_password("a")
        first_user.save()
        client = Client()
        client.login(username="paul", password="a")
        first_user.last_login = datetime.datetime.now() - datetime.timedelta(minutes=10)
        first_user.save()
        response = client.post(reverse("logout"), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = client.post(reverse("logout"), content_type='application/json')
        # TODO: CHECK THIS
        self.assertEqual(first_user.time_spent_online, 10)


class LoginTestCase(TestCase):
    def test_user_login_succes(self):
        user = User.objects.create(username="paul", email="a")
        user.set_password("a")
        user.save()
        data = {"username": "paul", "password": "a"}
        client = Client()
        response = client.post(reverse("login"), data)
        self.assertRedirects(response, reverse("index"), 302)

    def test_user_login_fail(self):
        user = User.objects.create(username="paul", email="a")
        user.set_password("a")
        user.save()
        data = {"username": "jhon", "password": "b"}
        client = Client()
        response = client.post(reverse("login"), data)
        self.assertEqual(response.status_code, 403)
