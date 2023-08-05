from .schedule import check_auction_time
import time
import schedule
from django.shortcuts import render
from rest_framework import mixins
from . import serializers, models
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
import copy
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Value, CharField, Field
from rest_framework.parsers import JSONParser


@api_view(['GET', 'POST'])
def test(request):
    data = models.Media.objects.filter(
        car_id__user_id__email='admin@g.com').values_list('car_id', 'image_id__image')

    return Response(data={'data': data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@parser_classes([JSONParser])
def add_car_to_auction(request):
    cars_id = request.data['cars_id']
    auction_id = request.data['auction_id']
    print(cars_id)
    for car in cars_id:
        seri = serializers.CarInAuctionSerializer(data={'car_id': car, 'auction_id': auction_id, 'status': 'for sale'})
        seri.is_valid(raise_exception=True)
        seri.save()
        models.RequestAuction.objects.filter(car_id=car).update(status='accepted')

    return Response({'message': 'ok'}, status=status.HTTP_201_CREATED)


def view_auctions_request(request):
    auctions_request = models.RequestAuction.objects.all()
    auctions = models.Auction.objects.filter(status__in=['later auction'])
    return render(request, 'request_auction.html', {'auctions_request': auctions_request, 'auctions': auctions})


def get_images(request, user_email: str, car_id=0):

    if car_id > 0:
        query = models.Media.objects.filter(
            car_id__user_id__email=user_email, car_id=car_id).values_list('car_id', 'image_id__image')
    else:
        query = models.Media.objects.filter(
            car_id__user_id__email=user_email).values_list('car_id', 'image_id__image')

    data = {}

    current_site = get_current_site(request)
    for car_id, image_id__image in query:
        absolute_url = settings.MEDIA_URL + str(image_id__image)
        if car_id in data:
            data[car_id].append('http://'+current_site.domain+absolute_url)
        else:
            data[car_id] = [('http://'+current_site.domain+absolute_url)]

    return data


@api_view(['POST'])
def upload_images(request):
    if request.FILES:
        uploaded_files = request.FILES.getlist('file[]')
        image_IDs = []
        car_id = request.data['car_id']
        for uploaded_file in uploaded_files:
            image = models.Images(image=uploaded_file)
            image.save()
            media_serializer = serializers.MediaSerializer(data={'car_id': car_id,
                                                                 'image_id': image.pk, 'kind': 'image'})
            media_serializer.is_valid(raise_exception=True)
            media_serializer.save()
            image_IDs.append(image.pk)
        return Response(data={'message': 'ok'}, status=status.HTTP_201_CREATED)
    return Response(data={'message': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)


class CreateClientMixin(generics.CreateAPIView, generics.ListAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientCreateSerializer
    permission_classes = [AllowAny]

    def create_user(self, request):
        user_data = request.data
        user_data['username'] = request.data['first_name'] + request.data['last_name']
        user_data['user_kind'] = 'User'
        user_serializer = serializers.UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        return models.User.objects.get(username=user_data['username']).pk

    def create(self, request, *args, **kwargs):

        client_data = {'gender': '', 'user_id': ''}
        client_data['gender'] = dict(request.data).pop('gender')

        client_data['user_id'] = self.create_user(request)
        client_serializer = self.get_serializer(data=client_data)
        client_serializer.is_valid(raise_exception=True)
        self.perform_create(client_serializer)
        headers = self.get_success_headers(client_serializer.data)
        return Response(client_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({}, status=status.HTTP_201_CREATED)


class Cars(generics.ListCreateAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = models.Car.objects.filter(user_id__email=request.user)
        # queryset = models.Car.objects.filter(user_id__email='admin@g.com')
        # images = get_images(request=request, user_email=request.user.email)

        # queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # for car in serializer.data:
        # for car in serializer.data:
        #     if car['id'] in images:
        #         car['images'] = images[car['id']]
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        try:
            car_instance = 0
            request.data['user_id'] = request.user.pk
            # request.data['user_id']='ee@gg.com'
            print(request.data)
            technical_condition = request.data.pop('technical_condition')
            print(technical_condition)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            car_instance = serializer.instance
            print(car_instance)

            for item in technical_condition:
                technical_serializer = serializers.TechnicalConditionSerializer(
                    data={'main_section_id': item['main_section_id'],
                          'car_id': car_instance.pk, 'status': item['status']})
                technical_serializer.is_valid(raise_exception=True)
                technical_serializer.save()

            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(f'Error in Cars.create  {str(e)}')
            if car_instance != 0:
                models.Car.objects.filter(pk=car_instance.pk).delete()
            return Response({'message': 'server Error'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Car(generics.RetrieveUpdateDestroyAPIView, generics.DestroyAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer
    permission_classes = [IsAuthenticated]


class Country(generics.ListAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    permission_classes = [AllowAny]


class Province(generics.ListAPIView):
    queryset = models.Province.objects.all()
    serializer_class = serializers.ProvinceSerializer
    permission_classes = [AllowAny]

    def list(self, request, country_id, *args, **kwargs):
        queryset = models.Province.objects.filter(country_id=country_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class Brands(generics.ListAPIView):
    queryset = models.CarBrand.objects.all()
    serializer_class = serializers.BrandSerializer


class CarModel(generics.ListAPIView):
    queryset = models.CarModels.objects.all()
    serializer_class = serializers.CarModelSerializer

    def list(self, request, brand_id, *args, **kwargs):
        print(brand_id)
        queryset = self.queryset.filter(brand_id=brand_id)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RequestAuction(generics.ListCreateAPIView):
    queryset = models.RequestAuction.objects.all()
    serializer_class = serializers.RequestAuctionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not models.Car.objects.filter(pk=request.data['car_id'], user_id=request.user.pk).exists():
            return Response({'message': 'car_id not found'}, status=status.HTTP_404_NOT_FOUND)
        request_obj = models.RequestAuction.objects.filter(
            user_id=request.user)
        if request_obj.filter(
                user_id__user_kind='User', status='pending').exists():
            return Response({'message': 'you already have pending request'}, status=status.HTTP_400_BAD_REQUEST)
        elif request_obj.filter(car_id=request.data['car_id'], status__in=['pending', 'accepted']).exists():
            return Response({'message': 'the car already in request'}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data
        data['user_id'] = request.user.pk
        data['status'] = 'pending'
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = models.RequestAuction.objects.filter(user_id=request.user.pk)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MainSection(generics.ListAPIView):
    queryset = models.MainSection.objects.all()
    serializer_class = serializers.MainSectionSerializer


class Auction(generics.ListAPIView):
    queryset = models.Auction.objects.all()
    serializer_class = serializers.AuctionSerializer


class CarInAuction(generics.ListAPIView):
    serializer_class = serializers.CarInAuctionSerializer

    def get_queryset(self):
        try:
            print(self.request.query_params)
            auction_id = self.request.query_params.get('auction_id', None)
            if auction_id:
                queryset = models.CarInAuction.objects.filter(auction_id=auction_id).order_by('car_id')
            else:
                queryset = models.CarInAuction.objects.all().order_by('car_id')
            return queryset
        except Exception as e:
            print('Error in CarInAuction.get_queryset : ', e)


class RequestJoinAuction(generics.CreateAPIView):
    queryset = models.UserInAuction.objects.all()
    serializer_class = serializers.UserInAuctionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if not request.user.user_kind == 'User':
            message = 'you dont have permission to join auction'
            print(message)
            return Response({'message': message})
        if not models.UserInAuction.objects.filter(
                auction_id=request.data['auction_id'],
                user_id=request.user.pk, status='waiting').exists():
            request.data['user_id'] = request.user.pk
            request.data['status'] = 'waiting'
            print(request.data)
            return super().create(request, *args, **kwargs)
        message = 'you already joined'
        print(message)
        return Response({'message': message})
