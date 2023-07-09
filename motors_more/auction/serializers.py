from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from rest_framework import serializers
from . import models


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'phone', 'location',]


class ClientCreateSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(source='user_id', read_only=True)
    # user_ID = UserCreateSerializer(source='user_id', write_only=True)

    class Meta:
        model = models.Client
        fields = ['id', 'user_id', 'gender', 'user']

    # def create(self, validated_data):
    #     print(validated_data)
    #     user_data = validated_data.pop('user_id')
    #     user = models.User.objects.create(**user_data)
    #     client = models.Client.objects.create(user_id=user, **validated_data)
        # return client


class CarSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(source='user_id', read_only=True)

    class Meta:
        model = models.Car
        fields = ['user_id', 'user', 'mileage', 'color', 'type', 'manufacturing_year',
                  'clean_title', 'engine_type', 'gear_type', 'cylinders', 'notes', 'price', 'location', 'car_models']


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = '__all__'


class ProvinceSerializer(serializers.ModelSerializer):
    country = serializers.ReadOnlyField(source='country_id.country_name')

    class Meta:
        model = models.Province
        fields = ['id', 'province_name', 'country']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarBrand
        fields = '__all__'


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarModels
        fields = '__all__'
