from django.db import models
from django.core.urlresolvers import reverse
from common.utils import get_global_settings
from django.conf import settings
User = settings.AUTH_USER_MODEL

class FlowerApiSettings(models.Model):
    api_key = models.CharField(max_length=300)
    api_password = models.CharField(max_length=300)
    
    
class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    parent = models.ForeignKey("Category", null=True,related_name='subcategories')
    code = models.CharField(max_length=75)
    catid = models.IntegerField(null=True,blank=True)  
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('flowers_flowers_home')+self.slug 
    
class Flowers(models.Model):
    flower_code = models.CharField(max_length=250)
    name = models.CharField(max_length=400)
    slug = models.CharField(max_length=400)
    created_by = models.ForeignKey(User)  
    created_on = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField("Category",null=True,related_name='categories')
    description = models.CharField(max_length=2000,null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    image_large = models.CharField(max_length=600,null=True,blank=True)
    image_thumbnail = models.CharField(max_length=600,null=True,blank=True)
    is_active = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('flowers_flowers_home')+self.slug+'.html'   