from django.shortcuts import render
from rest_framework import mixins
from . import serializers, models
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import copy
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Value, CharField, Field


@api_view(['GET', 'POST'])
def test(request):
    query = models.Media.objects.values_list('car_id', 'image_id__image')

    data = {}

    current_site = get_current_site(request)
    for car_id, image_id__image in query:
        absolute_url = settings.MEDIA_URL + str(image_id__image)
        if car_id in data:
            data[car_id].append('http://'+current_site.domain+absolute_url)
        else:
            data[car_id] = [('http://'+current_site.domain+absolute_url)]

  # data.annotate(images=Value(absolute_urls, output_field=CharField()))

    # car_sections = [
    #     "Engine Maintenance",
    #     "Brakes and Suspension",
    #     "Electrical System",
    #     "Fluids and Lubrication",
    #     "Tires and Wheels",
    #     "Body and Interior",
    #     "HVAC System"
    # ]
    # car_dict = {}
    # car_dict["Engine Maintenance"] = ["Oil changes", "Filter replacements",
    #                                   "Spark plug replacements", "Timing belt inspection", "Air intake cleaning"]
    # car_dict["Brakes and Suspension"] = ["Brake pad replacements", "Rotor replacements",
    #                                      "Suspension checks", "Wheel bearing inspection", "Shock absorber replacements"]
    # car_dict["Electrical System"] = ["Battery health check", "Alternator replacement",
    #                                  "Wiring inspection", "Starter motor replacement", "Fuse box inspection"]
    # car_dict["Fluids and Lubrication"] = ["Coolant level check", "Transmission fluid replacement",
    #                                       "Power steering fluid top-up", "Brake fluid flush", "Windshield washer fluid refill"]
    # car_dict["Tires and Wheels"] = ["Tire pressure maintenance", "Tire rotation",
    #                                 "Wheel alignment", "Tire tread depth check", "Wheel balancing"]
    # car_dict["Body and Interior"] = ["Car washing", "Interior cleaning",
    #                                  "Cosmetic repairs", "Seat upholstery cleaning", "Dashboard polishing"]
    # car_dict["HVAC System"] = ["Filter replacements", "Refrigerant level check",
    #                            "System functionality test", "Heater core inspection", "A/C compressor replacement"]
    # for kind in car_dict:
    #     pk = models.MainSection.objects.filter(name=kind)
    #     for d in car_dict[kind]:
    #         models.TechnicalCondition()
    # data = models.MainSection.objects.all().values()
    return Response(data={'data': data}, status=status.HTTP_200_OK)


class CreateClientMixin(generics.CreateAPIView, generics.ListAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientCreateSerializer
    permission_classes = [AllowAny]

    def create_user(self, request):
        user_data = request.data
        user_data['username'] = request.data['first_name'] + request.data['last_name']
        user_serializer = serializers.UserCreateSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        print('done 11')
        return models.User.objects.get(username=user_data['username']).pk

    def create(self, request, *args, **kwargs):

        client_data = {'gender': '', 'user_id': ''}
        client_data['gender'] = dict(request.data).pop('gender')

        client_data['user_id'] = self.create_user(request)
        print(client_data)
        client_serializer = self.get_serializer(data=client_data)
        print(client_serializer.is_valid(raise_exception=True))
        client_serializer.is_valid(raise_exception=True)
        print('done 22')
        self.perform_create(client_serializer)
        print('done 33')
        headers = self.get_success_headers(client_serializer.data)
        print('done 44')
        return Response(client_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({}, status=status.HTTP_201_CREATED)


'''

def get_images(self):
        data = models.Media.objects.filter(car_id__user_id__email='admin@g.com').values_list('car_id', 'image_id__image')
        images_dict = {}
        current_site = get_current_site(self.request)
        for car_id, image_path in data:
            absolute_url = settings.MEDIA_URL + str(image_path)
            image_url = 'http://' + current_site.domain + absolute_url
            if car_id in images_dict:
                images_dict[car_id].append(image_url)
            else:
                images_dict[car_id] = [image_url]
        return images_dict

def list(self, request, *args, **kwargs):
    images_dict = self.get_images()
    queryset = self.get_queryset()

    serialized_data = []
    for car in queryset:
        serialized_car = self.serializer_class(car).data
        car_id = serialized_car['id']
        if car_id in images_dict:
            serialized_car['images'] = images_dict[car_id]
        serialized_data.append(serialized_car)

    return Response(serialized_data)
'''


class Cars(generics.ListCreateAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer
    permission_classes = [AllowAny]

    def get_images(self, request):
        # data = models.Media.objects.filter(
        #     car_id__user_id__email='admin@g.com').values_list('image_id__image', flat=True)
        query = models.Media.objects.filter(
            car_id__user_id__email='admin@g.com').values_list('car_id', 'image_id__image')

        data = {}

        current_site = get_current_site(request)
        for car_id, image_id__image in query:
            absolute_url = settings.MEDIA_URL + str(image_id__image)
            if car_id in data:
                data[car_id].append('http://'+current_site.domain+absolute_url)
            else:
                data[car_id] = [('http://'+current_site.domain+absolute_url)]

        return data

    def list(self, request, *args, **kwargs):
        # queryset = models.Car.objects.filter(user_id__email=request.user)
        images = self.get_images(request)
        queryset = models.Car.objects.filter(
            user_id__email='admin@g.com')  # .annotate(images=Value(images, output_field=CharField()))

        # queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        # for car in serializer.data:
        for car in serializer.data:
            if car['id'] in images:
                car['images'] = images[car['id']]
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        try:
            request.data['user_id'] = request.user.pk
            # request.data['user_id']='ee@gg.com'
            # print(request.data['121'])
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            print(serializer.instance.pk)

            if request.FILES:
                uploaded_files = request.FILES.getlist('file[]')

            for uploaded_file in uploaded_files:
                print(uploaded_file)
                image = models.Images(image=uploaded_file)
                image.save()
                media_serializer = serializers.MediaSerializer(data={'car_id': serializer.instance.pk,
                                                                     'image_id': image.pk, 'kind': 'image'})
                media_serializer.is_valid(raise_exception=True)
                media_serializer.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(f'Error in Cars.create  {str(e)}')
            return Response({'message': 'server Error'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Car(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, pk, *args, **kwargs):
        print('retrive')
        print(request.user)
        return super().retrieve(request, pk, *args, **kwargs)


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


class MainSection(generics.ListAPIView):
    queryset = models.MainSection.objects.all()
    serializer_class = serializers.MainSectionSerializer
