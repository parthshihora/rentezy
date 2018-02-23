from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class CarOwner(AbstractBaseUser):
	#ownerId = models.IntegerField()
	firstName = models.CharField(max_length=200)
	lastname = models.CharField(max_length=200)
	#phoneNumber = models.IntegerField()
	email = models.EmailField(max_length=254)
	password = models.CharField(max_length=200)

	USERNAME_FIELD = 'email'


class Car(models.Model):
	#ownerId = models.ForeignKey('auth.User',on_delete=models.CASCADE)
	modelNumber = models.CharField(max_length=200)
	modelName = models.CharField(max_length=200)
	regNumber = models.CharField(max_length=200)
	insNumber = models.CharField(max_length=200)


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

	