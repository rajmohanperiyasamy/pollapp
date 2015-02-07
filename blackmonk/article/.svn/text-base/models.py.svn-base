import datetime

from django.template.loader import render_to_string
from django.db import models

from common.models import ModuleNames,Basetable
from common.utils import get_global_settings
from common.utils import getCoverPhoto
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.urlresolvers import reverse
from gallery.models import PhotoAlbum
from django.core.validators import MinValueValidator, MaxValueValidator


from audit_log.models.managers import AuditLog

import uuid
import os


from django.conf import settings
User = settings.AUTH_USER_MODEL


def get_article_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('article', filename)

class Tag(models.Model):
    tag = models.CharField(max_length=150)  
    def __unicode__(self):
        return self.tag
    class Admin:pass

class ArticleCategory(models.Model):
    name = models.CharField(max_length=150,unique=True)
    slug = models.CharField(max_length=200,null=True)
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        url = reverse('article_list') + self.slug + '/'
        return url
    
def get_default_category():
    return ArticleCategory.objects.get_or_create(name="Uncategorized", slug='uncategorized')[0]

class Article(Basetable):
    title = models.CharField(max_length=200)
    article_type=models.CharField(max_length=50,null=True,blank=True) #Own Story=FR, Pressrelease=PR , Advertorial=A , Review Request=RR
    slug = models.CharField(max_length=250)
    seo_title = models.CharField(max_length=200,null=True,blank=True)
    seo_description = models.CharField(max_length=400,null=True,blank=True)
    summary = models.TextField(null=True,blank=True)
    content = models.TextField()
    featured = models.BooleanField(default=False,blank=True)
    payment_mode = models.CharField(max_length=20,null=True,blank=True)
    category = models.ForeignKey("ArticleCategory", default=get_default_category, on_delete=models.SET_DEFAULT)
    tags = models.ManyToManyField("Tag",null=True,blank=True)
    most_viewed = models.PositiveIntegerField(default=0)
    published_on = models.DateTimeField(null=True,blank=True)
    album = models.ForeignKey(PhotoAlbum, blank=True, null=True, on_delete=models.SET_NULL, related_name='articlephotos')
    audit_log = AuditLog()
    
#     venues = models.ManyToManyField(Venue,null=True,blank=True)
#     album_url = models.URLField(null=True,blank=True)
#     gallery_url = models.URLField(null=True)
    
    def __unicode__(self):
        return self.title
    
    def get_visits(self):
        return self.most_viewed
    
    def get_action_type(self):
        if self.status=='P':return 'update'
        else:return 'delete'
        
    def articlephotos(self):
        if self.album:
            return self.album.get_gallery_uploaded_images()
        return None
    
    def get_payment_state(self):
        try:
            payment_option=ArticlePrice.objects.all()[0]
            if self.article_type =="FR": 
                return payment_option.ownstory_is_paid
            elif self.article_type =="PR": 
                return payment_option.pressrelease_is_paid
            elif self.article_type =="A": 
                return payment_option.advertorial_is_paid
            elif self.article_type =="RR": 
                return payment_option.requestreview_is_paid
            else:return False
        except:return False
        return 
    def get_preview_url(self):
        return reverse('staff_article_preview', args=[self.id]) 
    def get_modified_time(self):
        return self.modified_on
    def gettags(self):
         return self.tags.all()
    #Notification
    def get_staff_preview_url(self):
        url = reverse('staff_article_preview',args=[self.id])
        return url
    def get_staff_listing_url(self):
        url = reverse('staff_article_home')
        return url
    #Notification
    def get_absolute_url(self):
        url = reverse('article_list') + str(self.created_on.strftime("%m%y"))+'/'
        url = url +self.slug+'.html'
        return url
    
    def get_cover_photo(self):
        photo = getCoverPhoto(self)
        if photo:
            return photo.photo
        else:
            if self.album:
                return self.album.get_cover_image()
            else:
                return False
    
    def get_first_article_photo(self):
        return self.get_cover_photo()
    
    def get_img_from_html(self):
        from bs4 import BeautifulSoup
        try:
            soup = BeautifulSoup(self.content)
            image = soup.img['src']
            return image
        except:return False    
    
    def get_featured_image(self):
        return self.get_cover_photo()
     
    def get_photos(self):
        if self.album:
            return self.album.get_gallery_uploaded_images()
        return None   
    
    def get_default_image(self):
        return settings.STATIC_URL+"ui/images/global/img-none.png" 
    
    def get_search_result_html( self ):
        template = 'search/r_article.html'
        data = { 'object': self }
        return render_to_string( template, data )
    
    def get_payment_photo(self):
        return self.get_cover_photo()
        
    def get_payment_title(self):
        return self.title   
    def get_payment_description(self):
        if self.summary:return self.summary
        else:return self.title
    def get_payment_listing_type(self):
        type = self.article_type
        if type == 'FR':
            return 'Own Story'
        elif type == 'PR':
            return 'Press Release'
        elif type == 'A':
            return 'Advertorial'
        else:
            return 'Review Request'
    class Meta:
        permissions = (("publish_article", "Can Publish Article"),("promote_articles", "Can Promote Articles"),)


class ArticlePrice(models.Model): 
    ownstory_price      =  models.FloatField(default=0.0)
    pressrelease_price  =  models.FloatField(default=0.0,validators=[MinValueValidator(0.0),MaxValueValidator(9999999999.0)])
    advertorial_price   =  models.FloatField(default=0.0,validators=[MinValueValidator(0.0),MaxValueValidator(9999999999.0)])
    requestreview_price =  models.FloatField(default=0.0,validators=[MinValueValidator(0.0),MaxValueValidator(9999999999.0)])
    ownstory_is_paid       =  models.BooleanField(default=False)
    pressrelease_is_paid   =  models.BooleanField(default=False)
    advertorial_is_paid    =  models.BooleanField(default=False)
    requestreview_is_paid  =  models.BooleanField(default=False)
