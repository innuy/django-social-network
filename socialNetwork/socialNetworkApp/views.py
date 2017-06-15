# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from _curses import use_default_colors

from django.contrib import auth
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

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


class UserView(APIView):
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)

            if user.is_authenticated:
                users = User.objects.all()
                logged_user = {'logged_user': request.user}
                users_dictionary = []
                for user in users:
                    dictionary = {
                        'id': user.id,
                        'username': user.username,
                    }
                    users_dictionary.append(dictionary)

                return render(request, 'addFriend.html', {'users': users_dictionary, 'logged_user': logged_user})
            else:
                return HttpResponse(status=401)

        except User.DoesNotExist:
            return HttpResponse(status=403)


class UserFriendsView(APIView):
    def get(self, request):
        try:
            user = User.objects.get(id=request.user.id)

            if user.is_authenticated:
                user = request.user
                user_friend_dictionary = []
                friends = UserFriend.get_user_friends(user.id)
                for friend in friends:
                    dictionary = {
                        'id': friend.id,
                        'first_user': friend.first_user.username,
                        'second_user': friend.second_user.username,
                    }
                    user_friend_dictionary.append(dictionary)

                return render(request, 'userFriends.html', {'friends': user_friend_dictionary})
            else:
                return HttpResponse(status=401)

        except User.DoesNotExist:
            return HttpResponse(status=403)

    def post(self, request):
        try:
            user_friend_form = request.POST
            second_user_pk = request.POST.get("second_user", None)
            second_user = User.objects.get(id=second_user_pk)
            first_user = request.user
            if first_user.is_authenticated:
                UserFriend.objects.create(first_user=first_user, second_user=second_user)

                return HttpResponse(status=200)

            else:
                return HttpResponse(status=401)

        except User.DoesNotExist:
            return HttpResponse(status=403)


class RankingView(APIView):
    def get(self, request):
        user_ranking_dictonary = []
        top_ten_users = User.top_ten_logged_users()

        for user in top_ten_users:
            dictonary = {
                'user': UserSerializer(user)
            }
            user_ranking_dictonary.append(dictonary)

        return JsonResponse(user_ranking_dictonary, safe=False)


class IndexView(APIView):
    def get(self, request):
        posts_dictionary = []
        logged_user = {'logged_user': request.user}
        posts = Post.objects.all().order_by("date_posted")
        for post in posts:
            dictionary = {
                'title': post.title,
                'description': post.description,
                'date_posted': post.date_posted,
                'author': post.author
            }
            posts_dictionary.append(dictionary)

        return render(request, 'index.html', {'posts': posts_dictionary, 'user': logged_user})


class LoginView(APIView):
    def post(self, request):

        user = auth.authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('index')

        else:
            return render(request, 'registration/login.html', status=403)


class LogoutView(APIView):
    def post(self, request):
        user = request.user
        if user.is_authenticated:
            auth.logout(request)
            return HttpResponse(status=200)

        return HttpResponse(status=403)
