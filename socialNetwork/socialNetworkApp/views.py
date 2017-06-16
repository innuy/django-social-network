# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from _curses import use_default_colors

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from rest_framework import permissions

from serializers import UserSerializer

import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from forms import UserFriendForm

from models import User, UserFriend, Post


# Create your views here.

# class ValidateUserLogged(APIView):
#    def get(self, request):

class RestrictedView(APIView):
    permission_classes = (permissions.IsAuthenticated,)


class UserView(RestrictedView):
    def get(self, request):
        """
        Get all the users that are not on the user friends list
        :return: render
        """
        users_dictionary = list(request.user.get_unknown_users().values('id', 'username'))
        logged_user = {'logged_user': request.user}

        return render(request, 'addFriend.html', {'users': users_dictionary, 'logged_user': logged_user})


class UserFriendsView(RestrictedView):
    def get(self, request):
        """
        Get all the user friends
        :return: renders userFriends.html or status code 403 if user is not logged in
        """
        user = request.user
        user_friend_dictionary = []
        users = UserFriend.get_user_friends(user.id)
        for user in users:
            dictionary = {
                'id': user.id,
                'username': user.username,
            }
            user_friend_dictionary.append(dictionary)

        return render(request, 'userFriends.html', {'users': user_friend_dictionary})

    def post(self, request):
        """
        Add a new friend
        :return: status code 200, 403 if user is not logged in or 204 if the friend to add is not found
        """
        try:
            second_user_pk = request.POST.get("second_user", None)
            second_user = User.objects.get(id=second_user_pk)
            first_user = request.user

            UserFriend.objects.create(first_user=first_user, second_user=second_user)
            return HttpResponse(status=200)

        except User.DoesNotExist:
            return HttpResponse(status=204)


class RankingView(APIView):
    """
    Shows the users that spent more time online
    :return: Json with the ranking of users
    """

    def get(self, request):
        user_ranking_dictionary = []
        top_ten_users = User.top_ten_logged_users()

        for user in top_ten_users:
            dictonary = {
                'username': user.username,
                'time_online': user.time_spent_online,
            }
            user_ranking_dictionary.append(dictonary)

        return JsonResponse({'users': user_ranking_dictionary}, safe=False)


class IndexView(RestrictedView):
    def get(self, request):
        """
        Get all user messages and the logged in user
        :return: render index.html on success or login.html if user isn't authorized
        """

        logged_user = {'logged_user': request.user}
        posts_dictionary = list(
        Post.objects.all().order_by("-date_posted").values('id', 'title', 'description', 'date_posted',
                                                               'author'))

        return render(request, 'index.html', {'posts': posts_dictionary, 'user': logged_user})


class LoginView(APIView):
    def post(self, request):
        """
        User authentication
        :return: redirects to index on success or reloads login.html on failure
        """
        user = auth.authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('index')

        else:
            return render(request, 'registration/login.html', status=403)


class LogoutView(RestrictedView):
    def post(self, request):
        """
        User logout
        :return: Status code 200 on success or 403 if user isn't logged in
        """
        user = request.user
        user.set_time_online()
        auth.logout(request)
        return HttpResponse(status=200)
