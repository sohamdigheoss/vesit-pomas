from django.db import models
from django.contrib.auth.models import Group
from datetime import datetime

# Create your models here.
class Report(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    rating = models.IntegerField()
    remark = models.TextField()
    
