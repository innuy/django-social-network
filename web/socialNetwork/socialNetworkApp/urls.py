from django.conf.urls import url
from socialNetworkApp.views import UserView, UserFriendsView, RankingView,IndexView, LoginView, LogoutView, EditUserView, RegistrationView
from django.contrib.auth.views import login
from django.contrib.auth.views import logout


urlpatterns = [
    url(r'^$', IndexView.as_view(), name= "index"),
    url(r'^login/$', LoginView.as_view(), name= "login"),
    url(r'^register/$', RegistrationView.as_view(), name= "register"),
    url(r'^friends/$', UserFriendsView.as_view(), name= "friends"),
    url(r'^ranking/$', RankingView.as_view(), name = "ranking"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^users/$', UserView.as_view(), name = "users"),
    url(r'^edit/$', EditUserView.as_view(), name = "edit_user"),

]