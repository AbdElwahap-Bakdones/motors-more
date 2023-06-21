from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

# router = SimpleRouter()
# router.register('create_user', views.CreateClientMixin)

urlpatterns = [
    path('create_client', views.CreateClientMixin.as_view()),
    path('car', views.Car.as_view()),
    path('country', views.Country.as_view()),
    path('province/<int:country_id>', views.Province.as_view()),
]
