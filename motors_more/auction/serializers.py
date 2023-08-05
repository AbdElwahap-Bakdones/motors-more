from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer
from rest_framework import serializers
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from . import models


class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'phone', 'location', 'user_kind']


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


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Images
        fields = '__all__'


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CarModels
        fields = '__all__'


class TechnicalConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TechnicalCondition
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer(source='user_id', read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    car_model = serializers.CharField(source='car_models', read_only=True)
    car_brand = serializers.CharField(source='car_models.brand_id.name', read_only=True)
    price = serializers.CharField(read_only=True)
    province_name = serializers.CharField(source='location.province_name', read_only=True)
    country_name = serializers.CharField(source='location.country_id.country_name', read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Car
        fields = [
            'id', 'user_id', 'user', 'mileage', 'color', 'type', 'manufacturing_year', 'clean_title', 'engine_type',
            'gear_type', 'cylinders', 'notes', 'price', 'location', 'province_name', 'country_name', 'car_model',
            'car_models', 'car_brand', 'engine_capacity', 'damage', 'drive_type', 'images', 'status']

    def get_images(self, obj):
        query = models.Media.objects.filter(car_id=obj.pk).values_list('image_id__image', flat=True)

        data = []

        current_site = get_current_site(self.context['request'])
        for image_id__image in query:
            print(image_id__image)
            absolute_url = settings.MEDIA_URL + str(image_id__image)
            data.append('http://'+current_site.domain+absolute_url)

        return data

    def get_status(self, obj):
        query = models.CarInAuction.objects.filter(car_id=obj.pk, status='sold')
        if query.exists():
            return 'sold'
        else:
            return 'for sale'


class RequestAuctionSerializer(serializers.ModelSerializer):
    car_info = CarSerializer(source='car_id', read_only=True)

    class Meta:
        model = models.RequestAuction
        fields = ['id', 'user_id', 'car_id',  'car_info', 'status']


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


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Media
        fields = '__all__'


class MainSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MainSection
        fields = '__all__'


class AuctionSerializer(serializers.ModelSerializer):
    title = serializers.TimeField(source='time')
    extendedProps = serializers.SerializerMethodField()

    def get_extendedProps(self, obj):
        return {'status': obj.status, 'notebook_conditions': obj.notebook_conditions, 'kind': obj.kind}

    class Meta:
        model = models.Auction
        fields = ['id', 'date', 'title', 'extendedProps']


class CarInAuctionSerializer(serializers.ModelSerializer):
    car_info = CarSerializer(source='car_id', read_only=True)
    auction_date = serializers.DateField(source='auction_id.date', read_only=True)
    auction_status = serializers.SerializerMethodField(read_only=True)
    status = serializers.CharField(write_only=True)

    class Meta:
        model = models.CarInAuction
        fields = ['auction_id', 'auction_date', 'car_id', 'status', 'car_info',
                  'auction_status']

    def get_auction_status(self, obj):
        return obj.auction_id.status


class UserInAuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInAuction
        fields = '__all__'


class AutoSoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AutoSold
        fields = '__all__'
