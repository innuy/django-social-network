# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.contrib import auth
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from rest_framework.views import APIView

from constants import *
from models import User, UserFriend, Post

logger = logging.getLogger(__name__)


class AuthRequiredMiddleware(object):
    def process_request(self, request):
        """
        Redirect to login page if there is no user logged in.
        :return: renders login.html if not logged in or do nothing if logged in
        """
        if not request.user.is_authenticated():
            if exempt_urls.__contains__(request.get_full_path()):
                return None
            return redirect(reverse('login'))
        return None


class UserView(APIView):
    def get(self, request):
        """
        Get all the users that are not on the user friends list
        :return: render
        """
        users_dictionary = list(request.user.get_unknown_users().values('id', 'username'))
        return render(request, 'addFriend.html', {'users': users_dictionary})


class UserFriendsView(APIView):
    def get(self, request):
        """
        Get all the user friends
        :return: renders userFriends.html or status code 403 if user is not logged in
        """
        user = request.user
        users = UserFriend.get_user_friends(user.id)
        user_friend_dictionary = [{'id': user.id, 'username': user.username} for user in users]

        return render(request, 'userFriends.html', {'users': user_friend_dictionary})

    def post(self, request):
        """
        Add a new friend
        :return: status code 200 or 400 if the friend's data to add is bad requested
        """
        response = HttpResponse(status=200)
        try:
            second_user_pk = request.POST.get("second_user", None)
            second_user = User.objects.get(id=second_user_pk)
            first_user = request.user
            UserFriend.objects.create(first_user=first_user, second_user=second_user)
        except User.DoesNotExist as e:
            # logger.exception(e)
            response = HttpResponse(status=400)
        except IntegrityError as e:
            # logger.exception(e)
            response = HttpResponse(status=409)
        return response


class RankingView(APIView):
    """
    Shows the users that spent more time online
    :return: Json with the ranking of users
    """

    def get(self, request):
        top_ten_users = User.top_ten_logged_users()

        user_ranking_dictionary = [{'username': user.username, 'time_online': user.time_spent_online} for user in
                                   top_ten_users]

        return JsonResponse({'users': user_ranking_dictionary}, safe=False)


class IndexView(APIView):
    def get(self, request):
        """
        Get all user messages and the logged in user
        :return: render index.html on success or login.html if user isn't authorized
        """
        posts_dictionary = list(Post.objects.all().order_by("-date_posted").values('id', 'title', 'description',
                                                                                   'date_posted', 'author'))

        return render(request, 'index.html', {'posts': posts_dictionary, 'logged_user': request.user})


class LoginView(APIView):
    def get(self, request):
        """
        :return: render login page
        """
        return render(request, 'login.html')

    def post(self, request):
        """
        User authentication
        :return: redirects to index on success or reloads login.html on failure
        """
        response = render(request, 'login.html', status=403)
        user = auth.authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            auth.login(request, user)
            response = redirect('index')
        return response


class LogoutView(APIView):
    def post(self, request):
        """
        User logout
        :return: Status code 200 on success or redirects to login page if isn't logged in
        """
        user = request.user
        user.set_time_online()
        user.save()
        auth.logout(request)
        return HttpResponse(status=200)
