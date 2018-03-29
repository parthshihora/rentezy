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


class CarOwner(AbstractBaseUser):
    # ownerId = models.IntegerField()
    firstName = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    # phoneNumber = models.IntegerField()
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=200)

    USERNAME_FIELD = 'email'


class UserData(models.Model):
    user = models.ForeignKey(User, editable=False)

    class Meta:
        abstract = True


class Car(UserData):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.ForeignKey(User, default="10000000000")
    # user = models.OneToOneField(User)
    car_pic = models.FileField()
    # car_pic =   models.ImageField(upload_to = 'static/pic_folder/',default='static/pic_folder/no.jpeg')
    modelNumber = models.CharField(max_length=200)
    modelName = models.CharField(max_length=200)
    regNumber = models.CharField(max_length=200)
    insNumber = models.CharField(max_length=200)
    priceperhour = models.IntegerField(default=" ")
    pickuplocation = models.CharField(max_length=200, default=" ")


class Reservation(models.Model):
    user = models.ForeignKey(User, default="")
    pickup_date = models.DateField(default=datetime.utcnow())
    pickup_time = models.TimeField(default=datetime.utcnow())
    drop_date = models.DateField(default=datetime.utcnow())
    drop_time = models.TimeField(default=datetime.utcnow())
    customer_id = models.CharField(max_length=200, default="cid")
    carid = models.ForeignKey(Car, default="10000000000")


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
