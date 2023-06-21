from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from rest_framework import serializers
from . import models


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'phone', 'location',]


class ClientCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(source='user_id',read_only=True)
    class Meta:
        model = models.Client
        fields = ['id', 'user', 'gender']

    # def create(self, validated_data):
    #     print(validated_data)
    #     user_data = validated_data.pop('user_id')
    #     user = models.User.objects.create(**user_data)
    #     client = models.Client.objects.create(user_id=user, **validated_data)
        # return client
    
class CarSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(source='user_id',read_only=True)
    manufacturing_year_ = serializers.DateField(source ='manufacturing_year',format='%Y-%m-%d')

    class Meta:
        model = models.Car
        fields = ['user_id','user','mileage','color','type','manufacturing_year_',
                  'clean_title','engine_type','gear_type','cylinders','notes','price','location']
        