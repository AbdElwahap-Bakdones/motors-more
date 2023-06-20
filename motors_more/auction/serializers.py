from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from rest_framework import serializers
from . import models


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'phone', 'location',]


class ClientCreateSerializer(serializers.ModelSerializer):
    user_id = UserCreateSerializer

    class Meta:
        model = models.Client
        fields = ['id', 'user_id', 'gender']
