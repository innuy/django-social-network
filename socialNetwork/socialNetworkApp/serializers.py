from rest_framework import serializers



class UserSerializer(serializers.Serializer):

    @staticmethod
    def read(user):
        user_json = {}
        user_json['id'] = user.id
        user_json['username'] = user.username
        user_json['time_online'] = user.time_spent_online

        return user_json
