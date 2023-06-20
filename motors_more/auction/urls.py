from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter

# router = SimpleRouter()
# router.register('create_user', views.CreateClientMixin)

urlpatterns = [
    path('', views.CreateClientMixin.as_view()),
]
