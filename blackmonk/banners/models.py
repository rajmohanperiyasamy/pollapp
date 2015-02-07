#Python Libs
import sys
import os
import uuid

#Django Libs
from django.db import models

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.defaultfilters import slugify
from django.conf import settings as my_settings
from django.conf import settings

from easy_thumbnails.fields import ThumbnailerImageField
from common.models import Basetable

User = settings.AUTH_USER_MODEL
SLOT_TYPES = (('','Select a Type'),('T', 'Top'),('R', 'Right'),('B', 'Bottom'))

def get_banner_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('banners/logo', filename)

class BannerPayment(models.Model):
    level = models.CharField(max_length=30,null=True)
    impressions = models.IntegerField(default=0, null=True,  blank=True)
    price_impressions = models.FloatField(default=0.0)
    created_by = models.ForeignKey(User, null=True)
    created_on = models.DateTimeField(auto_now = True,null=True) 

class BannerSections(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=200,null=True)    
    status = models.CharField(max_length=1,default="A") #I Inactive A Active B Blocked
    
    def __unicode__(self):
        return self.name

class BannerZones(models.Model):
    name = models.CharField(max_length=200)
    sections = models.ManyToManyField("BannerSections",null=True,blank=True,related_name='module_zones')
    slot = models.CharField(max_length=2,choices=SLOT_TYPES) #T=Top R=Right B=Bottom
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name    

class HeroBanners(Basetable):
    title = models.CharField(max_length=300, null=True, blank=True)  
    image = models.ImageField(upload_to=get_banner_logo_path,null=True,blank=True)
    is_new_tab = models.BooleanField(default=True)
    destination_url = models.URLField(null=True)
    display_order = models.IntegerField(null=True,  blank=True)
    
    def __unicode__(self):
        return self.title
    
    def get_default_image(self):
        return my_settings.STATIC_URL+"ui/images/global/img-none.png"   
    
    def get_status(self):
        if self.status =='P':sts = 'published'
        elif self.status =='N':sts = 'pending' 
        elif self.status =='D':sts = 'drafted'
        elif self.status =='R':sts = 'rejected' 
        else: sts = 'blocked' 
        return sts 

class BannerAdvertisements(Basetable):  
    section = models.ForeignKey("BannerSections", null=True,  blank=True, on_delete=models.SET_NULL)  
    zones = models.ForeignKey("BannerZones", null=True,  blank=True)  
    #image = models.OneToOneField("BannerLogo",null=True,blank=True,on_delete=models.SET_NULL)
    image = models.ImageField(upload_to=get_banner_logo_path,null=True,blank=True)
    caption = models.CharField(max_length=300, null=True, blank=True)
    is_new_tab = models.BooleanField(default=True)
    destination_url = models.URLField(null=True)
    is_script = models.BooleanField(default=False)
    banner_script = models.TextField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType,null=True,  blank=True)
    object_id = models.IntegerField(null=True,  blank=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    is_paid = models.BooleanField(default=False)
    payment = models.ForeignKey("BannerPayment", null=True)
    payment_type = models.CharField(max_length=1,null=True,blank=True) #Y-Yearly , I-Impressions
    impressions = models.IntegerField(null=True,  blank=True)
    total_amount = models.FloatField(default=0.0)
    temp_impressions = models.IntegerField(null=True,  blank=True)
    temp_amount = models.FloatField(default=0.0)
    
    def __unicode__(self):
        return self.caption
    
    def get_default_image(self):
        return my_settings.STATIC_URL+"ui/images/global/img-none.png"   
    def get_status(self):
        if self.status =='P':sts = 'published'
        elif self.status =='N':sts = 'pending' 
        elif self.status =='D':sts = 'drafted'
        elif self.status =='R':sts = 'rejected' 
        else: sts = 'blocked' 
        return sts 
    def get_total_banner_views(self):
        try:return BannerReports.objects.filter(banner = self, is_clicked = False).count()
        except:return 0
    def get_visits(self):
        return self.get_total_banner_views()
    def get_total_banner_clicks(self):
        try:return BannerReports.objects.filter(banner = self, is_clicked = True).count()
        except:return 0    
    def get_payment_title(self):
        return self.caption
    def get_preview_url(self):
        return reverse('staff_banners_preview_banner') + "?bid=" + str(self.id)
    def get_modified_time(self):
        return self.modified_on 
    
class BannerReports(models.Model):
    banner = models.ForeignKey("BannerAdvertisements",related_name="banner_report") 
    views = models.IntegerField(default=0)
    viewed_on = models.DateField(null=True)
    clicks = models.IntegerField(default=0)
    is_clicked = models.BooleanField(default=False)
    ipaddress = models.CharField(max_length=200, null=True, blank=True)
    source_url = models.CharField(max_length=600, null=True, blank=True)
    
    