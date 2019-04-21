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
    rubric1 = models.IntegerField(default=0)
    rubric2 = models.IntegerField(default=0)
    rubric3 = models.IntegerField(default=0)
    rubric4 = models.IntegerField(default=0)
    rubric5 = models.IntegerField(default=0)
    rubric6 = models.IntegerField(default=0)
    rubric7 = models.IntegerField(default=0)
    rubric8 = models.IntegerField(default=0)
    rubric9 = models.IntegerField(default=0)
    rubric10 = models.IntegerField(default=0)
    rubric11 = models.IntegerField(default=0)
    rubric12 = models.IntegerField(default=0)
    rubric13 = models.IntegerField(default=0)
    rubric14 = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now,blank=True)
