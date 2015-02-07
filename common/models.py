from django.db import models
from django.conf import settings as my_settings


User = my_settings.AUTH_USER_MODEL

class Basetable(models.Model):
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User,related_name='%(class)s_createdby')
    modified_by = models.ForeignKey(User,related_name='%(class)s_modifiedby',null=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=1,default='D')
    class Meta:
        abstract = True
