from django.shortcuts import render
from rest_framework import mixins
from . import serializers, models
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
import copy


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
        return models.User.objects.get(username=user_data['username']).pk

    def create(self, request, *args, **kwargs):

        client_data = {'gender': '', 'user_id': ''}
        client_data['gender'] = dict(request.data).pop('gender')

        client_data['user_id'] = self.create_user(request)
        print(client_data)
        client_serializer = self.get_serializer(data=client_data)
        client_serializer.is_valid(raise_exception=True)
        self.perform_create(client_serializer)
        headers = self.get_success_headers(client_serializer.data)
        return Response(client_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        return Response({}, status=status.HTTP_201_CREATED)
    
class Cars(generics.ListCreateAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer
    permission_classes =[AllowAny]
    def list(self, request, *args, **kwargs):
        # queryset = models.Car.objects.filter(user_id__email= request.user)
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        try:
            # request.data['user_id']=request.user.pk
            request.data['user_id']='ee@gg.com'
            print(request.data)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            print(f'Error in Cars.create  {str(e)}')
            return Response({'message':'server Error'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class Car(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Car.objects.all()
    serializer_class = serializers.CarSerializer
    permission_classes =[IsAuthenticated]
    def retrieve(self, request,pk, *args, **kwargs):
        print('retrive')
        print(request.user)
        return super().retrieve(request, pk,*args, **kwargs)
    

class Country(generics.ListAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer
    permission_classes = [AllowAny]

class Province(generics.ListAPIView):
    queryset = models.Province.objects.all()
    serializer_class = serializers.ProvinceSerializer
    permission_classes = [AllowAny]

    def list(self, request,country_id, *args, **kwargs):
        queryset = models.Province.objects.filter(country_id=country_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)