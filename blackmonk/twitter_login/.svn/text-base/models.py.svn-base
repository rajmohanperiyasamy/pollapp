from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class TwitterUser(models.Model):
    screen_name = models.CharField(max_length=40)
    user = models.ForeignKey(User)
    def __unicode__(self):
        return "Screen Name %s with user %s" % (self.screen_name, self.user)