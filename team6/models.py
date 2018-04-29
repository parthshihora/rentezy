from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


class Reg(models.Model):
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    role = models.CharField(max_length=200)
    status = models.CharField(max_length=200,default="")
    location = models.CharField(max_length=100,default="",blank=True)

class Reg_Admin(models.Model):
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    role = models.CharField(max_length=200, default="admin")

class Reg_Owner(models.Model):
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    status = models.CharField(max_length=200,default="")
    role = models.CharField(max_length=200,default="owner")

class Reg_Customer(models.Model):
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    status = models.CharField(max_length=200,default="")
    location = models.CharField(max_length=100,default="",blank=True)
    role = models.CharField(max_length=200,default="customer")

class UserData(models.Model):
    owner = models.ForeignKey(Reg_Owner, editable=False)
    class Meta:
        abstract = True


class Car(UserData):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    owner = models.ForeignKey(Reg_Owner, on_delete=models.CASCADE, default="")
    # user = models.OneToOneField(User)
    car_pic = models.FileField()
    # car_pic =   models.ImageField(upload_to = 'static/pic_folder/',default='static/pic_folder/no.jpeg')
    modelNumber = models.CharField(max_length=200)
    modelName = models.CharField(max_length=200)
    regNumber = models.CharField(max_length=200)
    insNumber = models.CharField(max_length=200)
    priceperhour = models.IntegerField(default="")
    pickuplocation = models.CharField(max_length=200, default="")
    Reserved = models.CharField(max_length=100,default="No")
    cartype = models.CharField(max_length=25, default="compact")
    passengerCapacity = models.IntegerField(default="")
    

class Reservation(models.Model):
    customer = models.ForeignKey(Reg_Customer, default="")
    pickup_date = models.DateField(default=datetime.utcnow())
    pickup_time = models.TimeField(default=datetime.utcnow())
    drop_date = models.DateField(default=str(datetime.utcnow()))
    drop_time = models.TimeField(default=datetime.utcnow())
    owner = models.ForeignKey(Reg_Owner, default="")
    carid = models.ForeignKey(Car, default="")
    status = models.CharField(max_length=20,default="")