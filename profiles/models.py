from django.db import models, transaction
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.dispatch import receiver

from phonenumber_field.modelfields import PhoneNumberField

class Domain(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class MyUser(AbstractUser):
    is_student      =   models.BooleanField(default=False)
    is_teacher      =   models.BooleanField(default=False)
    phonenumber     =   PhoneNumberField()


# class Teacher(models.Model):
#     user            =   models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     domain          =   models.OneToOneField(Domain, on_delete=models.CASCADE, blank=False)
#
#     def __str__(self):
#         return self.user.username


class Student(models.Model):
    user            =   models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    division        =   models.CharField(max_length=4, blank=False)
    roll_no         =   models.IntegerField(blank=False)


    def __str__(self):
        return self.user.username



