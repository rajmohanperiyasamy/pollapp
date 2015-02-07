from django.db import models
from django.conf import settings
from common.models import ModuleNames
from common.utils import get_global_settings
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from common.getunique import getUniqueValue
from common.models import VenueType

User = settings.AUTH_USER_MODEL

class Zipcode(models.Model):
    zip = models.CharField(max_length=16,null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    zoom = models.IntegerField(null=True)
    def __unicode__(self):
        return self.zip
                               
class Locality(models.Model):
    name = models.CharField(max_length=100)
    zipcodes = models.ManyToManyField(Zipcode,null=True,related_name='zipcodes')
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    zoom = models.IntegerField(null=True)
    
    def __unicode__(self):
        return self.name
    
    def namefirstchar(self):
        return self.name[:1].upper()
"""
class Venue(models.Model):
    venue   = models.CharField(max_length=100)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200,blank=True)
    slug = models.CharField(max_length=150,blank=True,null=True)
    #type=models.CharField(max_length=100,default="others")
    type=models.ForeignKey(VenueType)
    telephone=models.CharField(max_length=20,blank=True)
    mobile=models.CharField(max_length=20,blank=True)
    email=models.EmailField(max_length=75,null=True)
    website=models.URLField(max_length=250,null=True)
    description=models.TextField(null=True)
    zip = models.CharField(max_length=16,null=True)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    zoom = models.SmallIntegerField(null=True)
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User,related_name='vencreated_by')
    modified_on = models.DateTimeField(auto_now = True)
    modified_by = models.ForeignKey(User,related_name='venmodified_by')
    seo_title = models.CharField(max_length=150,null=True,blank=True)
    seo_description = models.CharField(max_length=400,null=True,blank=True)
    
    def __unicode__(self):
        return self.venue
    
    def save(self, *args, **kwargs):
        self.slug=getUniqueValue(Venue,slugify(self.venue),instance_pk=self.id)
        super(Venue, self).save(*args, **kwargs) 
        
    def get_venue_photo(self):
        try:
            return VenuePhoto.objects.filter(venue=self).order_by('id')[:1][0]
        except:
            False
    def get_venue_photos(self):
        return VenuePhoto.objects.filter(venue=self).order_by('id')
    
    def get_first_venue_photo(self):
        photos = VenuePhoto.objects.filter(venue=self).order_by('id')[:1]
        try:
            return photos[0].photo
        except:return False  
    def get_events(self):
        from events.models import Event
        events = Event.objects.filter(venue=self).order_by('id')
        try:
            return events
        except:return False   
import uuid
import os
def get_venuegallery_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('venues', filename)   
"""
        