from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
import os
import sys
import urllib
import uuid

from common.getunique import getUniqueValue
from easy_thumbnails.fields import ThumbnailerImageField


User = settings.AUTH_USER_MODEL
path=sys.path[0]
fs = FileSystemStorage(location=path+'/analytics_key_file')

def get_upload_path(instance, filename):
    slug=slugify(CommonConfigure.get_obj().domain)
    return os.path.join(path+"/analytics_key_file", "%s_%s" %(slug,filename))

COMMENT_STATUS = (('N','Need Approval'),('A','Published'))
MODULE_STATUS = ((False,'Need Approval'),(True,'Published'))
M_CLASSIFIED_STATUS = (('P','Published'),('H','Need Approval'))
PAYMENT_EVENT = ((False,'Not Required'),(True,'Required'))
PAYMENT_BUSINESS = ((False,'Not Required'),(True,'Required'))
PAYMENT_ARTICLE = ((False,'Not Required'),(True,'Required'))
PAYMENT_CLASSIFIED = ((False,'Not Required'),(True,'Required'))
AD_OPTION=(('O','OpenId'),('D','DoubleClick'))
WEATHER_OPTIONS=(('WO','WorldweatherOnline'),('WN','WeatherNetwork'))
NEWSLETTER_OPTIONS=(('MC','MailChimp'),('CC','Constant Contact'))
EMAILSETTING_OPTIONS=(('A','On_Add'),('U','On_Update'),('C','On_Claim'),('P','On_Purchase'),)
SMTP_AUTH_TYPES = (('TLS','TLS'),('SSL','SSL'),('None','None'))

def get_sitelogo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('sitelogo', filename)

def get_venuegallery_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('venues', filename)   

class Basetable(models.Model):
    created_on = models.DateTimeField(auto_now_add = True)
    modified_on = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User,related_name='%(class)s_createdby')
    modified_by = models.ForeignKey(User,related_name='%(class)s_modifiedby',null=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=1,default='D')#P=published N= Pending  D= Draft  R=rejected B= Blocked E=Expired
    class Meta:
        abstract = True


class VenueType(models.Model):
    title=models.CharField(max_length=100)
    slug = models.CharField(max_length=150,blank=True,null=True)
    seo_title = models.CharField(max_length=150,null=True,blank=True)
    seo_description = models.CharField(max_length=400,null=True,blank=True)
    
    def __unicode__(self):
        return self.title


class VenuePhoto(models.Model):    
    venue = models.ForeignKey("Address",null=True)
    title = models.CharField(max_length=200,null=True)
    photo = ThumbnailerImageField(upload_to=get_venuegallery_path,resize_source=dict(size=(700, 0), crop='smart'),)
    uploaded_on = models.DateTimeField('createdonvenuphoto', auto_now_add=True)
    uploaded_by = models.ForeignKey(User,related_name='venphotouploaded_by') 
     
    def get_delete_url(self):
        return reverse('admin_locality_ajax_delete_photos', args=[self.id])

class Address(Basetable):
    venue   = models.CharField(max_length=100,null=True,blank=True)
    type = models.ForeignKey(VenueType,null=True,blank=True)
    address_type = models.CharField(max_length = 20,null=True,default = "venue",blank=True)
    slug = models.CharField(max_length=150,blank=True,null=True)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200,blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    description=models.TextField(null=True)
    telephone1=models.CharField(max_length=20,blank=True,null=True)
    telephone2=models.CharField(max_length=20,blank=True,null=True)
    mobile=models.CharField(max_length=20,blank=True)
    fax=models.CharField(max_length=20,blank=True)
    email=models.EmailField(max_length=75,null=True)
    website=models.URLField(max_length=250,null=True)
    zip = models.CharField(max_length=16,null=True)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    zoom = models.SmallIntegerField(null=True)
    seo_title = models.CharField(max_length=150,null=True,blank=True)
    seo_description = models.CharField(max_length=400,null=True,blank=True)
    
    
    def __unicode__(self):
        if self.venue:
            return self.venue
        else:
            return "None"
    
    def save(self, *args, **kwargs):
        self.slug=getUniqueValue(Address,slugify(self.venue),instance_pk=self.id)
        super(Address, self).save(*args, **kwargs) 
        
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
    
    def check_website(self):
        if self.website:
            a = self.website[0:7]
            if a=='http://':
                return self.website
            else:
                return 'http://'+self.website
        else:
            return False
    
def get_coverphoto_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('coverphoto/', filename)

class CoverPhoto(models.Model):
    photo  = ThumbnailerImageField(upload_to=get_coverphoto_path, resize_source=dict(size=(800, 0), crop='smart'), null=True)
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.IntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def get_delete_url(self):
        return reverse('common_delete_cover_photo', args=[self.id])
    
    def get_update_url(self):
        return reverse('common_update_cover_photo', args=[self.id])
    
    def delete(self, *args, **kwargs):
        self.photo.delete()
        super(CoverPhoto, self).delete(*args, **kwargs)


class ModuleNames(models.Model):
    name = models.CharField(max_length=70)
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    modified_by = models.ForeignKey(User, null=True)
    modified_on = models.DateTimeField(auto_now = True,null=True)
    def __unicode__(self):
        return self.name
     
    @classmethod
    def get_module_seo(cls,name):
        try:return ModuleNames.objects.get(name=name)
        except: return ModuleNames(name=name)
    
class PaymentConfigure(models.Model):   
    currency_symbol = models.CharField(max_length=4)#CURRENCY SYMBOL
    currency_code = models.CharField(max_length=5)#CURRENCY CODE
    invoice_payment = models.BooleanField(default=False)
    online_payment = models.BooleanField(default=False)
    paypal_payment = models.BooleanField(default=False)
    paypal_receiver_email = models.EmailField(null=True, blank=True)
    google_checkout = models.BooleanField(default=False)
    merchant_id = models.CharField(max_length=150,null=True,blank=True)
    merchant_key = models.CharField(max_length=150,null=True,blank=True)
    authorize = models.BooleanField(default=False)
    login_id = models.CharField(max_length=150,null=True,blank=True)
    transaction_key = models.CharField(max_length=150,null=True,blank=True)
    stripe = models.BooleanField(default=False)
    stripe_public_key=  models.CharField(max_length=150,null=True,blank=True)
    stripe_private_key=  models.CharField(max_length=150,null=True,blank=True)
    allow_subscription = models.BooleanField(default=False)
    def __unicode__(self):
        return "Payment Configurations"
    @classmethod
    def get_payment_settings(cls):
        return PaymentConfigure.objects.all()[:1][0]

class CommonConfigure(models.Model):
    site_title = models.CharField(max_length=100)
    city = models.CharField(max_length=80)#calgary
    domain = models.CharField(max_length=100)#onlinecalgary.com
    country = models.CharField(max_length=80)#Canada
    country_code = models.CharField(max_length=10,default='CA')#Canada
    info_email = models.EmailField()#info@onlinecalgary.com
    phone = models.CharField(max_length=20,null=True, blank=True)
    website_url = models.CharField(max_length=100)#http://onlinecalgary.com
    company_name = models.CharField(max_length=100)#Name of the company
    company_address = models.CharField(max_length=150)#Company Address
    
    logo = ThumbnailerImageField(upload_to=get_sitelogo_path,null=True, blank=True)#/site_media/themes/green/images/global/logo.png
    fav_ico = ThumbnailerImageField(upload_to=get_sitelogo_path,null=True, blank=True)
    iphone_logo = ThumbnailerImageField(upload_to=get_sitelogo_path,null=True, blank=True)#/site_media/themes/green/images/global/logo.png
    
    google_map_key = models.CharField(max_length=150, null=True, blank=True )#'ABQIAAAA7cJ9xBYH0NEN1QoB0DvXAhRUKgQvc54lX8Fscp2dQRsrFDDpxhR7HT8R6jBiVad39YRmOWW4fQE5jg'
    google_map_lat = models.FloatField(null=True, blank=True)#51.054344119247425
    google_map_lon = models.FloatField(null=True, blank=True)#-114.07516479492188
    google_map_zoom = models.IntegerField(null=True, blank=True)#10
    google_analytics_script = models.CharField(max_length=600, null=True, blank=True)
    google_meta = models.CharField(max_length=600, null=True, blank=True)
    
    twitter_url = models.CharField(max_length=60, null=True, blank=True)#'http://twitter.com/ocalgary'
    facebook_page_url = models.CharField(max_length=255, null=True, blank=True)#'http://www.facebook.com/onlinecalgary'
    googleplus_url = models.CharField(max_length=150, null=True, blank=True)#'http://plus.google.com/ocalgary'
    pinterest  = models.CharField(max_length=300, null=True, blank=True)#'http://pinterest.com/onlinecalgary/'
    
    currency = models.CharField(max_length=15, null=True, blank=True)
    disqus_forum_name = models.CharField(max_length=300, null=True,blank=True)
    copyright = models.CharField(max_length=400, null=True,blank=True)
    
    site_dateformat = models.CharField(max_length=20, null=True,blank=True,default="%d - %b - %Y")
    site_timeformat = models.CharField(max_length=20, null=True,blank=True,default="%I:%M %p")
    
    twitter_widget_id = models.CharField(max_length=60, null=True, blank=True)
    
    def __unicode__(self):
        return "Global Configurations"
    @classmethod
    def get_obj(cls):
        try:
            obj = CommonConfigure.objects.filter()[:1][0]
        except IndexError:
            obj = CommonConfigure(
                site_title = "Blackmonk",
                city = "calgary",
                domain = "onlinecalgary.com",
                country = "Canada",
                info_email = "info@onlinecalgary.com",
                phone = "",
                website_url = "http://onlinecalgary.com",
                company_name = "Doublespring",
                company_address = "Bangalore",
                
                logo = "/static/themes/green/images/global/logo.png",
                fav_ico = "",
                iphone_logo = "",
                
                google_map_key = 'ABQIAAAA7cJ9xBYH0NEN1QoB0DvXAhRUKgQvc54lX8Fscp2dQRsrFDDpxhR7HT8R6jBiVad39YRmOWW4fQE5jg',
                google_map_lat = 51.054344119247425,
                google_map_lon = -114.07516479492188,
                google_map_zoom = 10,
                google_analytics_script = "",
                google_meta = "",
                
                twitter_url = 'http://twitter.com/ocalgary',
                facebook_page_url = 'http://www.facebook.com/onlinecalgary',
                googleplus_url = 'http://plus.google.com/ocalgary',
                pinterest = 'http://pinterest.com/onlinecalgary/',
                
                currency = "",
                disqus_forum_name = "",
                copyright = "copyright 2013",
                
                site_dateformat = "%d - %b - %Y",
                site_timeformat = "%I:%M %p"
            )
            obj.save()
        return obj
    def get_facebook_page_url(self):
        return urllib.quote_plus(self.facebook_page_url)
    def get_delete_logo_url(self):
        return reverse('admin_configuration_ajax_delete_logo')
    def get_delete_fav_url(self):
        return reverse('admin_configuration_ajax_delete_fav')
    def get_delete_iphonelogo_url(self):
        return reverse('admin_configuration_ajax_delete_iphonelogo')

class ModuleSetting(models.Model):
    #Modules
    event_add = models.BooleanField(default=False)
    article_add = models.BooleanField(default=False)
    video_active = models.BooleanField(default=False)
    business_adding = models.BooleanField(default=False)
    gallery_photo_active= models.BooleanField(default=False)
    classified_active = models.CharField(max_length=1,    choices=M_CLASSIFIED_STATUS)# Classified Fields
    advice_active = models.BooleanField(default=False)# Q&A
    topics_active = models.BooleanField(default=False)# Form
    event_payment = models.BooleanField(default=True)
    business_payment = models.BooleanField(default=True)
    article_payment = models.BooleanField(default=True)
    classified_payment = models.BooleanField(default=True)
    
    #Comments
    article_comment = models.CharField(max_length=1,      choices=COMMENT_STATUS, help_text=_('When article is commented?'))
    movie_comment = models.CharField(max_length=1,        choices=COMMENT_STATUS)
    theatre_comment = models.CharField(max_length=1,      choices=COMMENT_STATUS)
    event_comment = models.CharField(max_length=1,        choices=COMMENT_STATUS)
    venue_comment = models.CharField(max_length=1,        choices=COMMENT_STATUS)
    video_comment = models.CharField(max_length=1,        choices=COMMENT_STATUS)
    business_review = models.CharField(max_length=1,      choices=COMMENT_STATUS)
    gallery_comment = models.CharField(max_length=1,      choices=COMMENT_STATUS)
    classified_comment = models.CharField(max_length=1,   choices=COMMENT_STATUS)
    advice_comment = models.CharField(max_length=1,       choices=COMMENT_STATUS)
  
    def __unicode__(self):
        return "Application Settings"
    def get_obj(self):
        ms = ModuleSetting.objects.order_by('-id')[:1]
        for m in ms:
            return m
        return False

class ApprovalSettings(models.Model):
    name = models.CharField(max_length=70)
    
    # for the following boolean fields - True (Do Auto Publish) & False (Don't Auto Publish)
    free = models.BooleanField(default=False)
    free_update = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    paid_update = models.BooleanField(default=False)
    
    
    modified_by = models.ForeignKey(User, null=True)
    modified_on = models.DateTimeField(auto_now = True,null=True)
    
    def __unicode__(self):
        return self.name

class SocialSettings(models.Model):
    fb_like = models.BooleanField(default=False)
    twitter = models.BooleanField(default=False)
    google_plus = models.BooleanField(default=False)
    pinterest = models.BooleanField(default=False)
    
    @staticmethod
    def get_or_create_obj():
        try:return SocialSettings.objects.all()[:1][0]
        except:return SocialSettings().save()
    def __unicode__(self):
        return "Social Settings"
    
    
class Views_Reports(models.Model):
    element_id=models.CharField(max_length=50)
    referral_url=models.URLField()
    module_name=models.CharField(max_length=50)
    viewed_on = models.DateTimeField(null=True)
    ip_address=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    listing_type=models.CharField(max_length=50)
    clicks = models.BooleanField(default=False)
    
    def __str__(self):
        return '%s %s' % (self.element_id, self.module_name)
    
class AnalyticDefaultData(models.Model):
    total_visits=models.CharField(max_length=150) 
    unique_visits=models.CharField(max_length=150) 
    pageviews=models.CharField(max_length=150) 
    avg_visit_time=models.CharField(max_length=150)
    daily_page_views=models.TextField()
    daily_visits=models.TextField()
    weekly_page_views=models.TextField()
    weekly_visits=models.TextField()
    monthly_page_views=models.TextField()
    monthly_visits=models.TextField()
    
    def __unicode__(self):
        return self.daily_page_views
        
class SignupSettings(models.Model):
    openid = models.BooleanField(default=False)
    facebook = models.BooleanField(default=False)
    twitter = models.BooleanField(default=False)
    facebook_app_id = models.CharField(max_length=100, null=True, blank=True)#
    facebook_secret_key = models.CharField(max_length=150, null=True, blank=True)#'0a4a5bff65056d101a27b0885842f8d4'
    twitter_consumer_key= models.CharField(max_length=150, null=True, blank=True)#'oJ7O134b63sZ6UsFXY0QQ'
    twitter_consumer_secret=  models.CharField(max_length=150, null=True, blank=True)
    linkedin_app_id = models.CharField(max_length=100, null=True, blank=True)#
    linkedin_secret_key = models.CharField(max_length=150, null=True, blank=True)
    linkedin = models.BooleanField(default=False)
    
    @staticmethod
    def get_or_create_obj():
        try:return SignupSettings.objects.all()[:1][0]
        except:return SignupSettings().save()
    
class GallerySettings(models.Model):
    flickr_api_key = models.CharField(max_length=150, null=True)#'bdc6b318570afc875df6fa95cbc1d508'
    flickr_api_secret = models.CharField(max_length=150, null=True)#'9c50ae8ff403f31a'
    flickr_email = models.CharField(max_length=150, null=True, blank=True)#'onlineplano@yahoo.in'
    flickr_password = models.CharField(max_length=64, null=True, blank=True)#'mybangalore'
    vimeo_api_key = models.CharField(max_length=150, null=True)#'bdc6b318570afc875df6fa95cbc1d508'
    vimeo_api_secret = models.CharField(max_length=150, null=True)#'9c50ae8ff403f31a'
    
    @classmethod
    def get_obj(cls):
        ms = GallerySettings.objects.order_by('-id')[:1]
        try:return ms[0]
        except:return False
class Advertisement(models.Model):
    adoption = models.CharField(max_length=1,choices=AD_OPTION)   # O=>OPENID  D=>DOUBLECLICK
    header_section = models.TextField()
    
    def __unicode__(self):
        return "Advertisement Settings"
    @classmethod
    def get_obj(cls):
        ms = Advertisement.objects.order_by('-id')[:1]
        try:return ms[0]
        except:return False
    
class BannerAdds(models.Model):
    name = models.CharField(max_length=100)    
    top = models.TextField(null=True, blank=True)
    right = models.TextField(null=True, blank=True)
    bottom = models.TextField(null=True, blank=True)
    
class Pages(models.Model):
    name = models.CharField(max_length=30)
    slug = models.CharField(max_length=40)
    content= models.TextField()
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    modified_by = models.ForeignKey(User, null=True)
    modified_on = models.DateTimeField(auto_now = True,null=True)  
    is_static = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False) 
    
    def __unicode__(self):
        return self.name    
    
class AvailableModules(models.Model):
    level = models.CharField(max_length=10) #header-->Main Menus, exp--> Sub Menus, footer-->Footer Menus
    name = models.CharField(max_length=200)
    parent = models.ForeignKey("AvailableModules", null=True,related_name='children')
    slug = models.SlugField()
    base_url = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name 
    
    def get_sub_menus(self):
        return AvailableModules.objects.filter(parent=self).order_by('order')
    
    class Meta:
        ordering = ["order"]
   
class WeatherApiSettings(models.Model):
    option = models.CharField(max_length=2,choices=WEATHER_OPTIONS)   # WO=>WorldweatherOnline  WN=>WeatherNetwork
    weather_xml = models.CharField(max_length=400, null=True,blank=True)
    weather_unit = models.CharField(max_length=10, null=True)

class NewsLetterApiSettings(models.Model):
    option = models.CharField(max_length=2,choices=NEWSLETTER_OPTIONS)   # MC = MailChimp ,CC = Constant Contact
    api_key = models.CharField(max_length=500, null=True,blank=True)
    list_id = models.CharField(max_length=100, null=True)
    subscribe_url = models.CharField(max_length=500, null=True)
 
class AvailableApps(models.Model):
    name = models.CharField(max_length=200,unique=True)
    slug = models.SlugField()
    status = models.CharField(max_length=1,default='N')
    sitemap = models.CharField(max_length=1,default='N')
    comment = models.CharField(max_length=5,default='N')
    app= models.BooleanField(default=False)
    #comment = models.BooleanField(default=False)
    module_name=models.CharField(max_length=15,unique=True,null=True,blank=True)
    type = models.CharField(max_length=1,default='N')#A=>API/AFFILIATE O=>OWN APP N=>None
    contest = models.CharField(max_length=1,default='N')
    def __unicode__(self):
        return self.name
    
    @staticmethod
    def get_inactive_app_slug():
        if not cache.get('inactive_apps'):
            app_slug_list=[app.slug for app in AvailableApps.objects.all().exclude(status='A')]
            cache.set('inactive_apps',app_slug_list,60*60*24)
        return cache.get('inactive_apps')
    
    @staticmethod
    def get_active_apps_module_name():
        return AvailableApps.objects.filter(status='A',module_name__isnull=False)
    
class StaffEmailSettings(models.Model):
    availableapps   = models.ForeignKey(AvailableApps,related_name='availableapps_emailsettigs')
    action          = models.CharField(max_length=2,choices=EMAILSETTING_OPTIONS)   
    emails          = models.CharField(max_length=400, null=True,blank=True)
    
    def __unicode__(self):
        return self.availableapps.name
    
class Contacts(models.Model):
    name = models.CharField(max_length=300)
    type = models.CharField(max_length=2) # A=Advertisement C=Contact
    company = models.CharField(max_length=600,null=True,blank=True)
    website = models.CharField(max_length=800,null=True,blank=True)
    phone = models.CharField(max_length=30,null=True,blank=True)
    email = models.EmailField(max_length=200,null=True,blank=True)
    subject = models.CharField(max_length=500,null=True,blank=True)
    notes = models.CharField(max_length=2500,null=True,blank=True)
    created_on = models.DateTimeField(_(u"Creation date"), auto_now=True, auto_now_add=True)
    
    def __unicode__(self):
        return self.name   

class HomeFeatureContent(models.Model):
    order = models.IntegerField(max_length=10,null=True)
    title = models.CharField(max_length=800,null=True)
    slug = models.CharField(max_length=800,null=True)
    photo_url = models.CharField(max_length=500,null=True,blank=True)
    module = models.CharField(max_length=20,null=True,blank=True)


class Notification(models.Model):
    user =  models.ForeignKey(User,null=True,related_name='notification_createdby')
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add = True,null=True)
    object_title = models.CharField(max_length=500,null=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50)
    def __unicode__(self):
        return self.object_title  


class MiscAttribute(models.Model):
    attr_name = models.CharField(max_length=100,null=True,blank=True)    
    attr_key = models.CharField(max_length=100,unique=True)
    attr_value = models.CharField(max_length=300,null=True,blank=True)    
    def __unicode__(self):
        return self.attr_key
    
class CommentSettings(models.Model):
    discuss_comment     = models.BooleanField(default=False)
    discuss_shortcut    = models.CharField(max_length=100,null=True,blank=True)
    like_dislike        = models.BooleanField(default=False)
    flag                = models.BooleanField(default=False)
    approval            = models.BooleanField(default=False)
    threaded            = models.BooleanField(default=False)
    anonymous           = models.BooleanField(default=False)
    avatar              = models.BooleanField(default=False)
    rating              = models.BooleanField(default=False)
    sort                = models.CharField(max_length=1,default='N')
    
    def __unicode__(self):
        return _('Comment Setting')
    
    @staticmethod
    def get_or_create_obj():
        try:return CommentSettings.objects.all()[:1][0]
        except:
            cc=CommentSettings(like_dislike=True,flag=True,threaded=True,avatar=True,rating=True)
            cc.save()
            return cc
        
class Feedback(models.Model):
    user = models.ForeignKey(User, verbose_name=_(u"User"), blank=True, null=True)
    name = models.CharField(_('Your Name'),max_length=300,null=False)
    type = models.CharField(_('Type'),max_length=100) # S=Suggestion P=Problem
    email =  models.EmailField(_('Your E-mail'),null=False)
    module = models.CharField(_('Module'),max_length=30,null=False)
    message = models.CharField(_('Message'),max_length=1000,null=False)
    created_on = models.DateTimeField(_(u"Creation date"), auto_now=True, auto_now_add=True)
    
    def __unicode__(self):
        return self.name
    
class SeoSettings(models.Model):
    code = models.CharField(max_length=2)  
    title = models.CharField(max_length=100,null=True,blank=True)  
    order = models.CharField(max_length=5,default='TCD')  #TCD--> Title | Category | Domain
    created_by  =  models.ForeignKey(User)
    
    def __unicode__(self):
        return self.title
    
class SmtpConfigurations(models.Model):
    email_host = models.CharField(max_length = 100)  
    email_port = models.CharField(max_length = 100)  
    email_host_user = models.CharField(max_length = 100)  
    email_host_password = models.CharField(max_length = 120) 
    is_secure = models.BooleanField(default = True) 
    secure_type = models.CharField(max_length = 5, choices = SMTP_AUTH_TYPES) 
    default_from_mail = models.CharField(max_length = 100)
    created_by  =  models.ForeignKey(User)  


class CSVfile(models.Model):
    file = models.FileField(upload_to="common/csvfiles/")
    module = models.CharField(max_length=12,null=True)#business, events, articles, classifieds, user 
    status = models.CharField(max_length=10,null=True)#pending = 'N' | processing = 'P' | success = 'S' | error = 'E'
    log = models.TextField(default='')
    uploaded_on = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User)
    
    def __unicode__(self):
        return str(self.file).split('/')[-1]
    
    def get_status(self):
        return {"N": "Pending", "P": "Processing", "S": "Success", "E": "Error"}[self.status]
    
    def get_status_color(self):
        return {"N": "#A7B2D9", "P": "#929EAF", "S": "#84BD76", "E": "#D46C6C"}[self.status]
        
    def get_short_log(self):
        return self.log.split('\n')[0]
    
    def get_log_url(self):
        return CommonConfigure.get_obj().website_url + reverse("csvfile_log", args=[self.id,])
    
    def delete(self, *args, **kwargs):
        self.file.delete()
        super(CSVfile, self).delete(*args, **kwargs)
        
class ContactEmails(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    name = models.CharField(max_length=75)
    email = models.EmailField(max_length=100)
    phone_no = models.CharField(max_length=25)
    subject = models.CharField(max_length=70)
    message = models.CharField(max_length=600)
    status = models.CharField(max_length=2, default='NR')
    created_by = models.ForeignKey(User,null=True,blank=True)
    created_on = models.DateTimeField(auto_now_add = True)
    
    def get_status(self):
        if self.status =='P':
            sts = 'published'
        elif self.status =='N':
            sts = 'pending'
        return sts

class CommonFaq(models.Model):
    question = models.CharField(max_length=600)
    answer = models.TextField(null=True)
    created_by =models.ForeignKey(User)
    created_on =models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self. question      
        
from common.notification_task import * 
from common.staffmail_task import * 
