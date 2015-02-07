from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class LinkedInUser(models.Model):
    user = models.ForeignKey(User, unique=True)
    lnid = models.CharField(max_length=100, unique=True)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)
    def __unicode__(self):
        return self.lnid