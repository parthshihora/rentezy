from django.contrib import admin
from .models import CarOwner
from .models import Car
from .models import Reservation
from .models import Reg

admin.site.register(CarOwner)
admin.site.register(Car)
admin.site.register(Reg)
admin.site.register(Reservation)

class MyModelAdmin(admin.ModelAdmin):
    #fields = ("name",)

    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.created_by = request.user
        obj.save()