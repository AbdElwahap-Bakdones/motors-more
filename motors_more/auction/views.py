from django.shortcuts import render
from rest_framework import mixins
from . import serializers, models
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import copy


@api_view(['GET', 'POST'])
def test(request):
    car_brands = {
        'Kia': ['Rio', 'Optima', 'Forte', 'Sportage', 'Sorento'],
        'Toyota': ['Camry', 'Corolla', 'Prius', 'RAV4', 'Highlander'],
        'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Odyssey'],
        'Ford': ['Focus', 'Fusion', 'Mustang', 'Escape', 'Explorer'],
        'Chevrolet': ['Malibu', 'Cruze', 'Camaro', 'Equinox', 'Traverse'],
        'Volkswagen': ['Golf', 'Jetta', 'Passat', 'Tiguan', 'Atlas'],
        'Hyundai': ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Kona'],
        'Nissan': ['Altima', 'Sentra', 'Rogue', 'Murano', 'Pathfinder'],
        'BMW': ['3 Series', '5 Series', 'X3', 'X5', '7 Series'],
        'Mercedes-Benz': ['C-Class', 'E-Class', 'GLC', 'GLE', 'S-Class'],
        'Audi': ['A3', 'A4', 'Q5', 'Q7', 'A8'],
        'Subaru': ['Impreza', 'Legacy', 'Forester', 'Outback', 'Crosstrek'],
        'Mazda': ['Mazda3', 'Mazda6', 'CX-5', 'CX-9', 'MX-5 Miata'],
        'Jeep': ['Wrangler', 'Grand Cherokee', 'Cherokee', 'Renegade', 'Compass'],
        'Land Rover': ['Range Rover Evoque', 'Discovery Sport', 'Range Rover Sport', 'Range Rover Velar', 'Defender']
    }
    for brand in car_brands:
        models.CarBrand(name=brand).save()
        brand_pk = models.CarBrand.objects.filter(name=brand).get()
        for model in car_brands[brand]:
            models.CarModels(name=model, brand_id=brand_pk).save()
    data = models.CarModels.objects.all().values()
    return Response(data=data, status=status.HTTP_200_OK)


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


class Cars(generics.ListCreateAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = models.Car.objects.filter(user_id__email=request.user)
        # queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):

        request.data['user_id'] = request.user.pk
        # request.data['user_id']='ee@gg.com'
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # except Exception as e:
        #     print(f'Error in Cars.create  {str(e)}')
        #     return Response({'message':'server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
