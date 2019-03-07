from django.db import models, transaction
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver

from phonenumber_field.modelfields import PhoneNumberField


User    =   settings.AUTH_USER_MODEL



class Domain(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Student(models.Model):
    user            =   models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    division        =   models.CharField(max_length=4, blank=False)
    roll_no         =   models.IntegerField(blank=False)
    domain          =   models.OneToOneField(Domain, on_delete=models.CASCADE, blank=False)


    def __str__(self):
        return self.user.username

class Teacher(models.Model):
    user            =   models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    domain          =   models.OneToOneField(Domain, on_delete=models.CASCADE, blank=False)

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    user            =   models.OneToOneField(User, on_delete=models.CASCADE)
    is_student      =   models.BooleanField(default=False)
    is_teacher      =   models.BooleanField(default=False)
    phonenumber     =   PhoneNumberField()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

