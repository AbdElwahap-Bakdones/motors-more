from django.contrib import admin
from django.apps import apps
from . import models

# Register your models here.
app = apps.get_app_config('auction')
for model_name, model in app.models.items():

    admin.site.register(model)
