from django.db import models
from django.contrib.auth.models import Group
from datetime import datetime

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    group = models.OneToOneField(Group,on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.name
    
