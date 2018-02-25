from django.contrib import admin
from .models import CarOwner
from .models import Car

admin.site.register(CarOwner)
admin.site.register(Car)

class MyModelAdmin(admin.ModelAdmin):
    #fields = ("name",)

    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.created_by = request.user
        obj.save()