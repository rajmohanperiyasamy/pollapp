from django.db import models
from django.conf import settings
from photo_library.signals import photo_submit
User = settings.AUTH_USER_MODEL

class PhotoLibrary(models.Model):
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User,null=True,blank=True)
    photo_url=models.CharField(max_length=300,unique=True)
    tags=models.CharField(max_length=300,null=True,blank=True)
    summary=models.CharField(max_length=500,null=True,blank=True)
    is_staff=models.BooleanField(default=True)

from photo_library.tasks import * 