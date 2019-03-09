from django.db import models
from django.contrib.auth.models import Group
from datetime import datetime

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    
class ProjectGroup(models.Model):
    project_id = models.ForeignKey(Project,primary_key=True,on_delete=models.DO_NOTHING)
    group_id = models.ForeignKey(Group,on_delete=models.DO_NOTHING)
