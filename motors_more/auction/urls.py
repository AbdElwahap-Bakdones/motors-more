from django.conf import settings
from django.conf.urls.static import static

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
    path('main_section', views.MainSection.as_view()),
    path('request_auction', views.RequestAuction.as_view()),
    path('auctions_request/', views.view_auctions_request, name='view_auctions'),
    path('auction', views.Auction.as_view()),
    path('upload_images', views.upload_images),
    path('test', views.test),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
