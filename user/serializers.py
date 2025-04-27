from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Visit


class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ["id", "user", "timestamp"]
        read_only_fields = ["timestamp"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "profile_picture"
        ]
        extra_kwargs = {"password": {"write_only": True, "required": True}}
