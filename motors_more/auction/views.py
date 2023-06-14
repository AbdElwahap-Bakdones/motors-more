from django.shortcuts import render
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from auction import serializers, models


class CreateClientMixin(CreateModelMixin, UpdateModelMixin, RetrieveModelMixin):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientCreateSerializer
