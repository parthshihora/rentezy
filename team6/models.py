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

class Reg_Owner(models.Model):
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    role = models.CharField(max_length=200)
    status = models.CharField(max_length=200,default="")

class Reg_Customer(models.Model):
    username = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    role = models.CharField(max_length=200)
    status = models.CharField(max_length=200,default="")
    location = models.CharField(max_length=100,default="",blank=True)

class CarOwner(AbstractBaseUser):
    firstName = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=200)


class UserData(models.Model):
    user = models.ForeignKey(Reg, editable=False)
    class Meta:
        abstract = True


class Car(UserData):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.ForeignKey(Reg, default="")
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
    user = models.ForeignKey(Reg, default="")
    pickup_date = models.DateField(default=datetime.utcnow())
    pickup_time = models.TimeField(default=datetime.utcnow())
    drop_date = models.DateField(default=datetime.utcnow())
    drop_time = models.TimeField(default=datetime.utcnow())
    owner = models.CharField(max_length=200, default="")
    carid = models.ForeignKey(Car, default="")
    status = models.CharField(max_length=20,default="")



# def get_absolute_url(self):


#    return reverse('team6:home')


'''class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    #birth_date = models.DateField(null=True, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()'''
