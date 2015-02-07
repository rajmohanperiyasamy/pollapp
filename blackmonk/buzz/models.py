from django.db import models
from common.models import Basetable
from django.conf import settings
User = settings.AUTH_USER_MODEL

class Category(Basetable):
    name = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=300,null=True)
    slug = models.CharField(max_length=200,null=True)
    occupied = models.BooleanField(default=False)
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=300,null=True)
    c_order  = models.IntegerField(default=1)
    
    def __unicode__(self):
        return self.name
    
    def get_occupied_list(self):
        try:list=BuzzTwitterLists.objects.get(category=self)
        except:list=False
        return list

    
#Model to save mybangalore twitter account lists     
class BuzzTwitterLists(Basetable):
    lists_name = models.CharField(max_length=50)
    list_description = models.CharField(max_length=300)
    category = models.ForeignKey('Category',related_name='buzz_twitter_listcat')
    
    def __unicode__(self):
        return self.lists_name
    
#Model to save the buzz home page keywords to filter from twitter
class BuzzTwitterKeywords(Basetable):
    keyword = models.CharField(max_length=50)
    

class TwitterAPISettings(models.Model):
    twitter_user = models.CharField(max_length=150, null=True, blank=True)
    twitter_auth_key = models.CharField(max_length=150, null=True, blank=True)#'oJ7O134b63sZ6UsFXY0QQ'
    twitter_auth_secret = models.CharField(max_length=150, null=True, blank=True)#'jdo5PFdy5G2ecJ1BnwH5l7DEkJyjYRxhDXSkuHgUv0'
    twitter_consumer_key= models.CharField(max_length=150, null=True, blank=True)#'oJ7O134b63sZ6UsFXY0QQ'
    twitter_consumer_secret=  models.CharField(max_length=150, null=True, blank=True)#'jdo5PFdy5G2ecJ1BnwH5l7DEkJyjYRxhDXSkuHgUv0'
    
    

    