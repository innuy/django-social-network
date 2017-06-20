from django.forms import ModelForm
from models import UserFriend


class UserFriendForm(ModelForm):
    class Meta:
        model = UserFriend
        fields = ['first_user', 'second_user']
