from django.db import models
from common.models import Basetable,Address
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.conf import settings as my_settings
from django.conf import settings
from gallery.models import PhotoAlbum

from audit_log.models.managers import AuditLog

import uuid
import os
User = settings.AUTH_USER_MODEL

def get_attraction_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('attractions', filename)

class AttractionTag(models.Model):    
    tag = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.tag
    
class AttractionCategory(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255)
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    created_on = models.DateTimeField(auto_now_add = True)
    modified_on = models.DateTimeField(auto_now = True)
    created_by = models.ForeignKey(User,related_name='attraction_category_createdby')
    modified_by = models.ForeignKey(User,related_name='attraction_category_modifiedby',null=True)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return '/attractions/'+self.slug
    
    def get_attractions_count(self):
        return Attraction.objects.filter(category = self, status = 'P').count()

class Attraction(Basetable):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255)
    alias= models.CharField(max_length=350,null=True)
    category = models.ManyToManyField("AttractionCategory",related_name="attractions")
    venue = models.ForeignKey(Address,related_name="attraction_venu")
    tag = models.ManyToManyField("AttractionTag",null=True)
    description= models.TextField()
    ticket_url = models.CharField(max_length=150,null=True)
    website_url= models.CharField(max_length=150,null=True)
    fb_url = models.CharField(max_length=150,null=True)
    twitter_url= models.CharField(max_length=150,null=True)
    gooleplus_url = models.CharField(max_length=150,null=True)
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    is_featured=models.BooleanField(default=False)
    allow_user_photo=models.BooleanField(default=False)
    view_count = models.PositiveIntegerField(default=0)
    ticket_cost_adult= models.DecimalField(max_digits=10,decimal_places=2,null=True)
    ticket_cost_child= models.DecimalField(max_digits=10,decimal_places=2,null=True)
    ticket_cost_free= models.BooleanField(default=False)
    start_time=models.TimeField(null=True)
    end_time=models.TimeField(null=True)
    rating = models.FloatField(default=0)
    votes = models.IntegerField(default=0)
    activities = models.CharField(max_length=2000, null=True, blank=True)
    time_of_activity = models.CharField(max_length=1000, null=True, blank=True)
    admission_notes = models.CharField(max_length=1000, null=True, blank=True)
    notes=models.CharField(max_length=250,null=True)
    album = models.ForeignKey(PhotoAlbum, blank=True, null=True, on_delete=models.SET_NULL)
    audit_log = AuditLog()
    
    def __unicode__(self):
        return self.name
    
    def get_action_type(self):
        if self.status=='P':return 'update'
        else:return 'delete'
    def get_visits(self):
        return self.view_count
    def get_absolute_url(self):
        return '/attractions/'+self.slug+'.html'
    def get_attraction_photos(self):
        if self.album:
            return self.album.get_gallery_uploaded_images()
        return None
    def get_photos(self):
        if self.album:
            return self.album.get_gallery_uploaded_images()
        return None
    def get_cover_image(self):
        if self.album:
            return self.album.get_cover_image()
        else:
            return None
    def get_attraction_video(self):#only one video allowed
        return AttractionVideos.objects.get(attraction=self.id)
    def get_status(self):
        if self.status =='P':
            sts = 'published'
        elif self.status =='N':
            sts = 'pending' 
        elif self.status =='B':
            sts = 'blocked'
        elif self.status =='R':
            sts = 'rejected' 
        else: sts = 'blocked' 
        return sts   
    def get_search_result_html( self ):
        template = 'search/r_attractions.html'
        data = { 'object': self }
        return render_to_string( template, data )
    
    def get_lat_lang(self):
        venue = Address.objects.get(pk=self.venue_id)
        data = {}
        if venue.lat: data['lat']= venue.lat
        else:data['lat']=None
        if venue.lon:data['lon']= venue.lon
        else:data['lon']=None
        data['venue']= venue.venue
        return data
    def get_attr_venue(self):
        venue = Address.objects.filter(pk=self.venue_id).order_by('id')
        return venue
    def get_payment_photo(self):
        if self.album:
            if self.album.get_gallery_uploaded_images():
                for photo in self.album.get_gallery_uploaded_images():
                    return photo.photo
            else:return False
    
    class Meta:
        permissions = (("publish_attraction", "Can Publish Attractions"),("promote_attractions", "Can Promote Attractions"),)
    
# class AttractionPhotos(models.Model):
#     title = models.CharField(max_length=200)
#     attraction = models.ForeignKey("Attraction",null=True,related_name="attraction_photo")
#     photo = ThumbnailerImageField(upload_to=get_attraction_path,null=True)
#     photo_url = models.CharField(max_length=255,null=True)
#     uploaded_by = models.ForeignKey(User,related_name='uploaded_by',null=True)
#     uploaded_on  = models.DateTimeField( auto_now_add = True)
#     is_approved=models.BooleanField(default=False)
    
#     def __unicode__(self):
#         return self.title
#     
#     def get_delete_url(self):
#         return reverse('staff_attraction_ajax_delete_photos', args=[self.id])
    
class AttractionVideos(models.Model):
    title = models.CharField(max_length=200)
    attraction = models.ForeignKey("Attraction",related_name="attraction_video")
    video_url = models.CharField(max_length=255,null=True)
    added_by = models.ForeignKey(User,related_name='added_by',null=True)
    added_on  = models.DateTimeField( auto_now_add = True)
    is_vimeo = models.BooleanField(default=False)
    vimeo_image = models.CharField(max_length=300, null=True, blank=True)
    
    def __unicode__(self):
        return self.title
    
    def get_hq_thumb(self):
        if self.is_vimeo:return self.vimeo_image
        else:return 'http://i2.ytimg.com/vi/%s/hqdefault.jpg'%(self.video_url)
        
    def get_video_player(self):
        if self.is_vimeo:player_url = 'http://vimeo.com/%s'%(self.video_url) 
        else:player_url =  'http://www.youtube.com/watch?v=%s'%(self.video_url) 
        return player_url     
