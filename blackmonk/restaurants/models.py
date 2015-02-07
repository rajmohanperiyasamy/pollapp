#Python Libs
import sys
import os
import uuid

#Django Libs
from django.db import models
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.conf import settings as my_settings
User = my_settings.AUTH_USER_MODEL

from easy_thumbnails.fields import ThumbnailerImageField
from common.models import Basetable

def get_restaurant_logo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('restaurants/logo', filename)

def get_restaurant_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('restaurants/files', filename)

def get_restaurant_gallery_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('restaurants/gallery', filename)

Price_Range = ((25,'Under $25'),(50,'$25-$50'),(75,'$50-$75'),(100,'$75-$100'),(125,'Above $100'))
Rating_Options = ((1,'One Star'),(2,'Two Stars'),(3,'Three Stars'),(4,'Four Stars'),(5,'Five Stars'))



class Restaurants(Basetable):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    logo=models.OneToOneField("RestaurantLogo",null=True,blank=True,on_delete=models.SET_NULL)
    categories = models.ManyToManyField("RestaurantCategories",related_name='restaurant_categories',null=True)
    summary = models.CharField(max_length=350,null=True,blank=True)
    description = models.TextField(null=True)
    price_range = models.IntegerField(choices=Price_Range,null=True,blank=True)
    paymentoptions = models.ManyToManyField("PaymentOptions",related_name='restaurant_paymentoptions',null=True)
    operating_hours = models.BooleanField(default=False)
    workinghours = models.OneToOneField("RestaurantWorkingHours",null=True)
    votes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    ratings = models.IntegerField(choices=Rating_Options,null=True,blank=True)
    user_rating = models.IntegerField(default=0)
    user_service_rating = models.IntegerField(null=True,blank=True)
    user_food_rating = models.IntegerField(null=True,blank=True)
    user_ambiance_rating = models.IntegerField(null=True,blank=True)
    user_value_rating = models.IntegerField(null=True,blank=True) 
    meal_types = models.ManyToManyField("MealTypes",related_name='restaurant_meal_types',null=True,blank=True)
    cuisines = models.ManyToManyField("Cuisines",related_name='restaurant_cuisines',null=True,blank=True)
    features = models.ManyToManyField("RestaurantFeatures",related_name='restaurant_features',null=True,blank=True)
    tags = models.ManyToManyField("RestaurantTags",related_name='restaurant_tags',null=True,blank=True)
    #season_occasion = models.CharField(max_length=10,null=True,blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    featured_sponsored = models.CharField(max_length=1,null=True)#F=Featured    S=Sponsored   B=Basic/Free
    payment =  models.ForeignKey("RestaurantPrice",null=True)
    payment_type = models.CharField(max_length=1,null=True) #M-monthly , Y-yearly
    is_paid = models.BooleanField(default = False)
    fb_url = models.CharField(max_length=150,null=True)   #....on null it will be an empty string not NULL
    twitter_url= models.CharField(max_length=150,null=True)
    gooleplus_url = models.CharField(max_length=150,null=True)
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    
    def __unicode__(self):
        return self.name
    
    def get_action_type(self):
        if self.status=='P':return 'update'
        else:return 'delete'
    def get_absolute_url(self):
        return reverse('restaurants_restaurants_home')+self.slug+'.html'
    
    def get_preview_url(self):
        return reverse('staff_preview_restaurant', args=[self.id]) 
    
    def get_modified_time(self):
        return self.modified_on
    
    def get_status(self):
        if self.status =='P':
            sts = 'published'
        elif self.status =='N':
            sts = 'pending' 
        elif self.status =='D':
            sts = 'drafted'
        elif self.status =='R':
            sts = 'rejected' 
        else: sts = 'blocked' 
        return sts
    
    def getaddress(self):
        return RestaurantAddress.objects.filter(restaurant=self).order_by('id')



    
    def getcategories(self):
        return self.categories.all()
    
    def gettags(self):
        return self.tags.all()

    

    
class RestaurantCategories(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=150)
    seo_title = models.CharField(max_length=200,null=True,blank=True)
    seo_description = models.CharField(max_length=400,null=True,blank=True)
    introduction = models.CharField(max_length=1000,null=True,blank=True)
    
    def __unicode__(self):
        return self.name
    
    def get_active_restaurant_count(self):
        return Restaurants.objects.filter(categories = self,status='P').count()


class RestaurantWorkingHours(models.Model):
    mon_start = models.CharField(max_length=30, null=True)
    mon_end = models.CharField(max_length=30, null=True)
    tue_start = models.CharField(max_length=30, null=True)
    tue_end = models.CharField(max_length=30, null=True)
    wed_start = models.CharField(max_length=30, null=True)
    wed_end = models.CharField(max_length=30, null=True)
    thu_start = models.CharField(max_length=30, null=True)
    thu_end = models.CharField(max_length=30, null=True)
    fri_start = models.CharField(max_length=30, null=True)
    fri_end = models.CharField(max_length=30, null=True)
    sat_start = models.CharField(max_length=30, null=True)
    sat_end = models.CharField(max_length=30, null=True)
    sun_start = models.CharField(max_length=30, null=True)
    sun_end = models.CharField(max_length=30, null=True)
    notes = models.CharField(max_length=300, null=True)
    status = models.CharField(max_length=1, default='P')#P=published    H=private    D=draft
    
    
    
    




class RestaurantAddress(models.Model):
    restaurant = models.ForeignKey("Restaurants",related_name='restaurant_address')
    address1 = models.CharField(max_length=100,null=True)
    address2 = models.CharField(max_length=100,null=True)
    pin = models.CharField(max_length=16,null=True)
    city = models.CharField(max_length=60,null=True)
    telephone = models.CharField(max_length=20, null=True)
    fax = models.CharField(max_length=20, null=True)
    mobile_no = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True)
    website = models.CharField(max_length=200,null=True)
    pointer_lat = models.FloatField(null=True)
    pointer_lng = models.FloatField(null=True)
    map_zoom = models.SmallIntegerField(null=True)
    
    def __unicode__(self):
        return self.address1


class RestaurantImages(models.Model):
    title = models.CharField(max_length=200,null=True)
    restaurant = models.ForeignKey("Restaurants",related_name='restaurant_images')
    photo = ThumbnailerImageField(upload_to=get_restaurant_gallery_path)
    uploaded_on = models.DateTimeField('createdonrestphoto', auto_now_add=True)
    uploaded_by = models.ForeignKey(User,null=True)
    
    def __unicode__(self):
        if self.title:return self.title
        else:return "No caption"
        
    def get_delete_url(self):
        return reverse('staff_restaurant_ajax_delete_image', args=[self.id])
    
    def get_update_caption_url(self):
        return reverse('staff_restaurant_ajax_update_photo_caption', args=[self.id])
 
 
    
class RestaurantVideos(models.Model):
    title = models.CharField(max_length=200)
    restaurant = models.ForeignKey("Restaurants",related_name='restaurant_videos')
    video_url = models.CharField(max_length=255,null=True)
    is_vimeo = models.BooleanField(default=False)
    vimeo_image = models.CharField(max_length=500,null=True,blank=True)
    created_by = models.ForeignKey(User,null=True)
    created_on  = models.DateTimeField(auto_now_add = True)

    def __unicode__(self):
        if self.title:return self.title
        else:return "No Title"
        
    def get_hq_thumb(self):
        if self.is_vimeo:return self.vimeo_image
        else:return 'http://i2.ytimg.com/vi/%s/hqdefault.jpg'%(self.video_url)




class RestaurantFeatures(Basetable):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000,null=True,blank=True)
    def __unicode__(self):
        return self.name

    def get_active_restaurant_count(self):
        return Restaurants.objects.filter(features = self,status='P').count()


class RestaurantTags(models.Model):
    tag = models.CharField(max_length=150)
    def __unicode__(self):
        return self.tag




class RestaurantLogo(models.Model):
    logo  = ThumbnailerImageField(upload_to=get_restaurant_logo_path,resize_source=dict(size=(700, 0), crop='smart'), null=True)
    uploaded_on = models.DateTimeField('createdonrestrntlogo', auto_now_add=True)
    uploaded_by=models.ForeignKey(User,null=True)   
    
    def get_delete_url(self):
        return reverse('restaurant_delete_logo', args=[self.id])
        
    
 
class MealTypes(Basetable):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000,null=True,blank=True)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        
class RestaurantMenus(models.Model):
    title = models.CharField(max_length=120,null=True,blank=True)
    restaurant = models.ForeignKey("Restaurants",related_name='restaurant_menus')
    categories = models.ManyToManyField("MealTypes",related_name='restaurant_menu_categories',null=True)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=50,null=True,blank=True)
    discount_price = models.CharField(max_length=50,null=True,blank=True)
    files = models.FileField(upload_to=get_restaurant_file_path)
    uploaded_on = models.DateTimeField('createdonrestmenus', auto_now_add=True)
    uploaded_by = models.ForeignKey(User,null=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ['title']        
        
       
class Cuisines(Basetable):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    description = models.CharField(max_length=2000,null=True,blank=True)
    def __unicode__(self):
        return self.name
    
    def get_active_restaurant_count(self):
        return Restaurants.objects.filter(cuisines = self,status='P').count()
    
    class Meta:
        ordering = ['name']
 

class PaymentOptions(models.Model):
    name = models.CharField(max_length=100)
    image_position=models.CharField(max_length=200,null=True,blank=True)
    
    def __unicode__(self):
        return self.name
        
    class Meta:
        ordering = ['name']

class Reviews(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    parent = models.ForeignKey("Reviews",null=True)
    subject = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=60)
    email = models.EmailField(max_length=300)
    review = models.TextField()
    rating = models.IntegerField(default=0, null=True)
    food_rating = models.IntegerField(default=0, null=True)
    service_rating = models.IntegerField(default=0, null=True)
    ambiance_rating = models.IntegerField(default=0, null=True)
    value_rating = models.IntegerField(default=0, null=True)
    
    abuse_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=1,default='N')#N=new    B=blocked    A=approved
    approved_on = models.DateTimeField("approvedonrestreview", auto_now_add=True)
    created_by = models.ForeignKey(User,null=True,blank=True)
    created_on = models.DateTimeField('Createdon',auto_now_add=True)
    
    

class RestaurantPrice(models.Model):
    level = models.CharField(max_length=10,null=True)
    level_visibility = models.BooleanField(default=True)
    level_label = models.CharField(max_length=50,null=True)   
    is_paid = models.BooleanField(default=True)
    exposure = models.CharField(max_length=2,null=True)
    images = models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    videos = models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    share_buttons = models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    comments = models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    newsletter = models.CharField(max_length=1,null=True)#Y=Yes N=No E=None
    socialmedia = models.CharField(max_length=1)
    price_month = models.FloatField(default=0.0)
    price_year = models.FloatField(default=0.0)
        
    def get_exposure(self):
        if self.exposure=='1':
            return _('5X') 
        elif self.exposure=='2':
            return _('10X') 
        elif self.exposure=='3':
            return _('15X') 
        elif self.exposure=='4':
            return _('20X') 
        elif self.exposure=='5':
            return _('25X') 
        else:
            return _('Standard')
    










    
    
