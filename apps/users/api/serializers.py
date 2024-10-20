from rest_framework import serializers

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["username", "name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"},
        }


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(default="username")
    password = serializers.CharField(default="password")
