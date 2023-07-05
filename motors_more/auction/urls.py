from django.urls import path, include, re_path
from . import views
from rest_framework.routers import SimpleRouter

# router = SimpleRouter()
# router.register('create_user', views.CreateClientMixin)

urlpatterns = [
    path('create_client', views.CreateClientMixin.as_view()),
    path('car/', views.Cars.as_view(), name='car-list'),
    path('car/<int:pk>/', views.Car.as_view(), name='car-detail'),
    path('country', views.Country.as_view()),
    path('province/<int:country_id>', views.Province.as_view()),
    path('brands', views.Brands.as_view()),
    path('car_model/<int:brand_id>', views.CarModel.as_view()),
    path('test', views.test),
]
