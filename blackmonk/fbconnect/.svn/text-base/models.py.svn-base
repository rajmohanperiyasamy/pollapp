from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class FBUser(models.Model):
    fbid = models.CharField(max_length=100,primary_key=True)
    user = models.ForeignKey(User)
    logo=models.URLField(null=True)
    profile_url=models.URLField(null=True)
    def __unicode__(self):
        return "facebook id  %s with user %s" % (self.fbid, self.user)

