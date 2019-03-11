from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from datetime import datetime

User = settings.AUTH_USER_MODEL

# Create your models here.
class Review(models.Model):
    review_no = models.IntegerField()
    reviewer = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group,on_delete=models.DO_NOTHING)
    marks = models.IntegerField()
    created_at = models.DateTimeField(default=datetime.now,blank=True)
