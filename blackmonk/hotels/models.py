from django.db import models
from django.conf import settings

from common.utils import get_global_settings

User = settings.AUTH_USER_MODEL
API_OPTIONS=(('E','Expedia'),('O','Others'))

class ApiSettings(models.Model):
    option = models.CharField(max_length=1,choices=API_OPTIONS)   # E=>Expedia  O=>Others
    city = models.CharField(max_length=200,null=True,blank=True)
    api_key = models.CharField(max_length=400,null=True,blank=True)
    customer_id = models.CharField(max_length=400,null=True,blank=True)
    tripadvisor_key = models.CharField(max_length=400,null=True,blank=True)

class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    catid = models.IntegerField(null=True,blank=True)
    
    def get_hotels_count(self):
        return Hotels.objects.filter(category=self).count()
    def get_absolute_url(self):
        return '/hotels/%s/' %(self.slug)     
   
class Amenities(models.Model):
    name = models.CharField(max_length=300,null=True)
    
class HotelDetails(models.Model):
    number_of_rooms = models.CharField(max_length=200,null=True,blank=True)
    number_of_floors = models.CharField(max_length=200,null=True,blank=True)
    checkin_time = models.CharField(max_length=200,null=True,blank=True)
    checkout_time = models.CharField(max_length=200,null=True,blank=True)
    property_information = models.TextField(null=True,blank=True)
    area_information = models.TextField(null=True,blank=True)
    property_description = models.TextField(null=True,blank=True)
    hotel_policy = models.TextField(null=True,blank=True)
    room_information = models.TextField(null=True,blank=True)
    driving_directions = models.TextField(null=True,blank=True)
    checkin_instructions= models.TextField(null=True,blank=True)


class Hotels(models.Model):
    hotelid = models.IntegerField(null=True,blank=True)
    name = models.CharField(max_length=250)
    slug = models.CharField(max_length=250)
    created_by = models.ForeignKey(User)  
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=400,null=True,blank=True)
    city = models.CharField(max_length=200,null=True,blank=True)
    state_province_code = models.CharField(max_length=100,null=True,blank=True)
    postal_code = models.CharField(max_length=50,null=True,blank=True)
    country_code = models.CharField(max_length=200,null=True,blank=True)
    airport_code = models.CharField(max_length=200,null=True,blank=True)
    category = models.ManyToManyField("Category",null=True)
    amenities = models.ManyToManyField("Amenities",null=True)
    details = models.ForeignKey('HotelDetails',null=True)
    hotel_rating = models.CharField(max_length=200,null=True,blank=True)
    confidence_rating = models.CharField(max_length=200,null=True,blank=True)
    tripadvisor_rating = models.CharField(max_length=200,null=True,blank=True)
    tripadvisor_review_count = models.CharField(max_length=100,null=True,blank=True)
    tripadvisor_rating_url = models.URLField(max_length=400,null=True,blank=True,)  # verify_exists=False)
    location_description = models.CharField(max_length=1500,null=True,blank=True)
    short_description = models.TextField(null=True,blank=True)
    highrate = models.FloatField(null=True,blank=True)
    lowrate = models.FloatField(null=True,blank=True)
    currency_code = models.CharField(max_length=100,null=True,blank=True)
    latitude =  models.FloatField(null=True,blank=True)
    longitude =  models.FloatField(null=True,blank=True)
    zoom =  models.SmallIntegerField(default=13)
    proximity_distance = models.CharField(max_length=300,null=True,blank=True)
    proximity_unit = models.CharField(max_length=300,null=True,blank=True)
    deeplink = models.URLField(max_length=1000,null=True,blank=True,)  # verify_exists=False)
    is_active = models.BooleanField(default=False)
    
    def get_absolute_url(self):
        return '/hotels/%s' %(self.slug)+'.html'     
    
class HotelImages(models.Model):
    hotel = models.ForeignKey('Hotels',related_name='hotel_images')
    imageid = models.IntegerField(null=True,blank=True)
    caption = models.CharField(max_length=500,null=True,blank=True)
    image_thumbnail = models.CharField(max_length=600,null=True,blank=True)
    image_big = models.CharField(max_length=600,null=True,blank=True)    
    
class RoomAmenities(models.Model):
    name = models.CharField(max_length=500,null=True)
        
class HotelRoomDetails(models.Model):
    hotel = models.ForeignKey('Hotels',related_name='hotel_rooms')
    type = models.CharField(max_length=500,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    amenities = models.ManyToManyField("RoomAmenities",null=True)    
    
