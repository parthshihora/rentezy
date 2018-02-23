from django.contrib import admin
from .models import CarOwner
from .models import Car

admin.site.register(CarOwner)
admin.site.register(Car)