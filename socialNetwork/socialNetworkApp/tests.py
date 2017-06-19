# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import json

from django.test import TestCase, Client

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
        Gets Paul's friends
        """
        UserFriend.objects.create(first_user=self.first_user, second_user=self.second_user)
        client = Client()
        client.login(username="paul", password="a")
        response = client.get(reverse("friends"))
        # Get paul's friend: John
        data = response.context["users"][0]['username']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, self.second_user.username)

    def test_get_user_friends_unauthorized_user(self):
        UserFriend.objects.create(first_user=self.first_user, second_user=self.second_user)
        client = Client()
        response = client.get(reverse("friends"))
        self.assertRedirects(response, reverse("login"), 302)

    def test_add_new_friend_unauthorized_user(self):
        client = Client()
        data = {"second_user": self.second_user}
        response = client.post(reverse("friends"), data, content_type='application/json')
        self.assertEqual(response.status_code, 302)

    def test_add_new_friend(self):
        client = Client()
        client.login(username="paul", password="a")
        data = {"second_user": self.second_user.id}
        response = client.post(reverse("friends"), data)
        self.assertEqual(response.status_code, 200)
        # TODO: Check if user added is the same as requested
        self.assertEqual(1, UserFriend.objects.all().count())
        # Check that the paul's friend id is actually john's id
        self.assertEqual(self.first_user.friends.first().second_user_id, self.second_user.id)

    def test_add_unexistent_new_friend(self):
        """
        pre: doesn't exist a user with id 99999999
        Tries to add a friend that doesn't exists
        """
        client = Client()
        client.login(username="paul", password="a")
        data = {"second_user": 99999999}
        response = client.post(reverse("friends"), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(0, UserFriend.objects.all().count())
        
    def test_add_friend_already_exists(self):
        client = Client()
        client.login(username="paul", password="a")
        UserFriend.objects.create(first_user=self.first_user, second_user=self.second_user)
        data = {"second_user": self.first_user.id}
        response = client.post(reverse("friends"), data)
        self.assertEqual(response.status_code, 409)
        # TODO: Create two times UserFriend with different friend order


class UserTestCase(TestCase):
    def setUp(self):
        self.first_user = User.objects.create(username="paul", email="a", time_spent_online=5)
        self.second_user = User.objects.create(username="john", password="a", email="a", time_spent_online=2)
        User.objects.create(username="bob", password="a", email="a", time_spent_online=7)
        self.first_user.set_password("a")
        self.first_user.save()
        UserFriend.objects.create(first_user=self.first_user, second_user=self.second_user)

    def test_get_unknown_users(self):
        """
        Get all the users that aren't included in the logged user friends list.
        Three friends are created: paul, john and bob. Bob is the only one that is not paul's friend list.
        """
        client = Client()
        client.login(username="paul", password="a")
        response = client.get(reverse("users"))
        self.assertEqual(response.status_code, 200)
        data = response.context['users']
        self.assertEqual(len(data), 1)
        expected = "bob"
        result = data[0]['username']
        self.assertEqual(result, expected)


class RankingTestCase(TestCase):
    def setUp(self):
        first_user = User.objects.create(username="paul", email="a", time_spent_online=5)
        User.objects.create(username="john", password="a", email="a", time_spent_online=2)
        User.objects.create(username="bob", password="a", email="a", time_spent_online=7)
        first_user.set_password("a")
        first_user.save()


    def test_get_top_user_logged_users(self):
        """
        Get the users that spent more time logged in.
        The first user on the returned list will be tha last one on the ranking board. 
        John is the one that spent less time online.
        """
        client = Client()
        response = client.get(reverse("ranking"))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        users = data['users']
        self.assertEqual(users[0]['username'], "john")


class PostTestCase(TestCase):
    def setUp(self):
        """
        One user and three posts are created
        """
        first_user = User.objects.create(username="paul", email="a")
        first_user.set_password("a")
        first_user.save()
        User.objects.create(username="john", email="a", password="b")
        Post.objects.create(title="secondPost", author=first_user, date_posted=datetime.date(2013, 10, 7))
        Post.objects.create(title="post", author=first_user, date_posted=datetime.date(2017, 10, 7))
        Post.objects.create(title="thirdPost", author=first_user, date_posted=datetime.date(2011, 10, 7))

    def test_get_posts(self):
        """
        Get all the users posts sorted by the date posted. 
        Two posts are created on the setUp. 
        The first post on the list is the most recent.
        """
        client = Client()
        client.login(username="paul", password="a")
        response = client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['posts'][0]['date_posted'].year, 2017)
        response = client.post(reverse("logout"), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_get_posts_unauthorized_user(self):
        client = Client()
        client.login(username="john", password="a")
        response = client.get(reverse("index"))
        self.assertRedirects(response, reverse("login"), 302)


class TimeOnlineTestCase(TestCase):
    def setUp(self):
        self.first_user = User.objects.create(username="paul", email="a")
        self.first_user.set_password("a")
        self.first_user.save()
    
    def test_time_online(self):
        # [TODO] calculate time online
        """
        Test that the time that the user spent online is setted correctly
        """
        client = Client()
        client.login(username="paul", password="a")
        self.first_user.last_login = datetime.datetime.now() - datetime.timedelta(minutes=10)
        self.first_user.save()
        response = client.post(reverse("logout"), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # TODO: CHECK THIS 
        self.assertEqual(self.first_user.time_spent_online, 10)


class LoginTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="paul", email="a")
        user.set_password("a")
        user.save()

    def test_user_login_succes(self):
        data = {"username": "paul", "password": "a"}
        client = Client()
        response = client.post(reverse("login"), data)
        self.assertRedirects(response, reverse("index"), 302)

    def test_user_login_fail(self):
        data = {"username": "john", "password": "b"}
        client = Client()
        response = client.post(reverse("login"), data)
        self.assertEqual(response.status_code, 403)
