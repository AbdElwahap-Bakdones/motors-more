from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from rest_framework import serializers
from auction import models


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = ['id', 'username', 'email', 'password', 'email', 'first_name', 'last_name', 'phone', 'location']


class ClientCreateSerializer(serializers.ModelSerializer):
    user_id = UserCreateSerializer

    class Meta:
        model = models.Client
        fields = ['id', 'gender', 'user_id']
