from django.contrib import admin

from .models import *

admin.site.register(Car)
admin.site.register(Reg)
admin.site.register(Reservation)
admin.site.register(Reg_Customer)
admin.site.register(Reg_Owner)
admin.site.register(Reg_Admin)

class MyModelAdmin(admin.ModelAdmin):
    #fields = ("name",)

    def save_model(self, request, obj, form, change):
        if not change:
            # the object is being created, so set the user
            obj.created_by = request.user
        obj.save()