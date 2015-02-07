from django.db import models
from django.conf import settings
from common.models import Basetable,Address
from common.utils import *
from locality.models import Locality

from django.utils.translation import ugettext as _
import datetime,time
from datetime import timedelta
from django.template.loader import render_to_string
import os
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.urlresolvers import reverse
from gallery.models import PhotoAlbum

from audit_log.models.managers import AuditLog

import uuid
import os
User = settings.AUTH_USER_MODEL

def get_moviegallery_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('movies', filename)  

def get_theatregallery_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('movies/theatre', filename)  

class Theatres(models.Model):
    name = models.CharField(max_length=300)
    slug = models.CharField(max_length=250)
    image = models.ImageField(upload_to=get_theatregallery_path,null=True)    
    tkt_url = models.CharField(max_length=300)
    boxoffice_no = models.CharField(max_length=300)
    address = models.ForeignKey(Address)
    theatreseo_title = models.CharField(max_length=200,null=True)
    theatreseo_description = models.CharField(max_length=400,null=True) 
    
    def __unicode__(self):
        return _("%s") % self.name
    
    def get_search_result_html( self ):
        template = 'search/r_theater.html'
        data = { 'object': self }
        return render_to_string( template, data )
    def get_action_type(self):
        return 'update'
        
    def get_screens_count(self):
        return MovieTime.objects.filter(theatre=self).count()
    def get_movies_count(self):
        return MovieTime.objects.filter(theatre=self).count()
    def get_movies(self):
        return MovieTime.objects.filter(theatre=self).distinct()
    def get_active_theatres(self):
        return ShowTime.objects.filter(movietime__theatre=self).distinct()[:1]
        
    def get_screens(self):    
        return Screens.objects.filter(theatre=self)

    def get_movie_status(self):
        if self.status =='P':
            sts = 'active'
        elif self.status =='B':
            sts = 'inactive' 
        else: sts = 'expired' 
        return sts          
    
    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return settings.STATIC_URL+'images/defaultmovie.gif'
    
    def get_absolute_url(self):
        url = reverse('movies_home_page')+'theater/'+self.address.slug+'.html'
        return url 
    
    def comment_get_absolute_url(self):
        url = '/movies/theatre/'
        url = url +self.address.slug+'.html'
        return url 
    
    def get_phone_number(self):
        item = self.address.phone.split(',')
        return item[0]
        
class MovieType(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    seo_title = models.CharField(max_length=300,null=True)
    seo_description = models.TextField(null=True)
    
    def __unicode__(self):
        return self.name
    
    def get_movies_count(self):
        return Movies.objects.filter(movie_type=self).count()

class Screens(models.Model):
    theatre = models.ForeignKey('Theatres')
    screens = models.CharField(max_length=20)
    show_times = models.TextField(null=True)

class Movies(Basetable):
    language = models.ForeignKey("MovieLanguage",null=True)
    title = models.CharField(max_length=300)
    movie_type = models.ManyToManyField("MovieType", related_name="genre",null=True)
    image = models.ImageField(upload_to=get_moviegallery_path,null=True)
    movie_url=models.CharField(max_length=200,null=True,blank=True)
    #display_image = models.ImageField(upload_to=get_moviegallery_path,null=True)
    #original_image = models.ImageField(upload_to=get_moviegallery_path,null=True)
    slug = models.CharField(max_length=350)    
    release_date = models.DateField(null=True)
    duration_minutes = models.CharField(max_length=100)
    duration_hours = models.CharField(max_length=100)
    web = models.CharField(max_length=300,null=True)
    writer = models.CharField(max_length=100,null=True)
    facebook_url = models.URLField(max_length=200,null=True)
    googleplus = models.URLField(max_length=200,null=True)
    twitter_hash = models.CharField(max_length=100,null=True)
    director = models.TextField() 
    cast = models.TextField()
    synopsis = models.TextField()
    votes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    ratings = models.FloatField(default=0)
    certification = models.CharField(max_length=50,null=True,blank=True)
    photo_id = models.CharField(max_length=100,null=True)
    photo_key = models.CharField(max_length=100,null=True)
    #seo_title = models.CharField(max_length=150,default='movie showtime')
    #seo_description = models.CharField(max_length=150,default='movie showtime')  
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    is_vimeo=models.BooleanField(default=False)
    album = models.ForeignKey(PhotoAlbum, blank=True, null=True, on_delete=models.SET_NULL,related_name='movie_photos')
    audit_log = AuditLog()
    
    def __unicode__(self):
        return _("%s") % self.title
    
    def get_visits(self):
        return self.views
    
    def get_action_type(self):
        if self.status=='P':return 'update'
        else:return 'delete'
    def get_absolute_url(self):
        url = '/movies/' +self.slug+'.html'
        return url
    
    def get_lang_split(self):
        try:
            temp=self.language.split(',')
            return temp
        except:return list[self.language]
        
    def get_language(self):
        return self.language
                
    def get_movie_url(self):
        return 'http://www.youtube.com/v/%s'%(self.movie_url)
    
    def get_video_poster(self):
        return 'http://i2.ytimg.com/vi/%s/hqdefault.jpg'%(self.movie_url)
    
    def get_video_url(self):
        if self.is_vimeo:vp_url = 'http://player.vimeo.com/video/%s'%(self.movie_url) 
        else:vp_url =  'http://www.youtube.com/watch?v=%s'%(self.movie_url)+'&autoplay=1' 
        return vp_url
    
    def get_critic_reviews(self):
        return CriticReview.objects.filter(movie__id=self.id)
    def get_movie_photo(self):
        if self.album:
            return self.album.get_gallery_uploaded_images()
        return None
    
    def get_active_movies(self):
        return ShowTime.objects.filter(movietime__movie=self).distinct()[:1]
        
    def check_show_times(self):
        if self.release_date:
            return ShowTime.objects.filter(movietime__movie=self,date__lte = datetime.datetime.now()+timedelta(days=6),date__gte = self.release_date)
        else:
            return ShowTime.objects.filter(movietime__movie=self,date__lte = datetime.datetime.now()+timedelta(days=6),date__gte = datetime.datetime.now())
    def get_movie_status(self):
        if self.status =='P':
            sts = 'active'
        elif self.status =='B':
            sts = 'inactive' 
        else: sts = 'expired' 
        return sts 
    
    def getrating(self):
        try:
            r= self.ratings / self.votes
        except:
            r=0
        return r
    
    def get_image(self):
        if self.album:return self.album.get_absolute_url()
        else:return settings.STATIC_URL+"ui/images/global/img-none.png"        
    

    def is_boxoffice(self):
        try:
            BoxOffice.objects.get(movie=self)
            return True
        except:
            return False
    def get_first_photo(self):
        photos= MoviesPhoto.objects.filter(movie=self).order_by('id')[:1]
        return photos[0]
    def get_photo_gallery(self):
        if self.album:
            return self.album.get_gallery_uploaded_images()
        return None
    def get_theatres(self):
        return MovieTime.objects.filter(movie=self).distinct()
    def get_genre(self):
        return self.movie_type.all()
    def get_search_result_html( self ):
        template = 'search/r_movies.html'
        data = { 'object': self }
        return render_to_string( template, data )
    class META:
        get_latest_by = 'id'
        permissions = (("publish_movies", "Can Publish Movies"),)
   
class MovieTime(models.Model):
    theatre = models.ForeignKey('Theatres')
    movie = models.ForeignKey('Movies',related_name='movie_showtimes')
    def get_shows(self):
        return ShowTime.objects.filter(movietime=self).order_by('date')
    def get_shows_user(self):
        if self.movie.release_date:
            return ShowTime.objects.filter(movietime=self,date = datetime.datetime.now()).order_by('date')
        else:
            return ShowTime.objects.filter(movietime=self,date = datetime.datetime.now()).order_by('date')
        

class ShowTime(models.Model):
    movietime = models.ForeignKey("MovieTime",related_name='mvt_showtimes')
    date = models.DateField(null=True)
    show_times = models.CharField(max_length=300,null=True)
    
class FeaturedList(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField()
    url = models.URLField()
  
# class MoviesPhoto(models.Model):    
#     movie = models.ForeignKey("Movies",null=True,related_name="movie_images")
#     title = models.CharField(max_length=200,null=True)
#     photo = ThumbnailerImageField(upload_to=get_moviegallery_path)
#     uploaded_by = models.ForeignKey(User)
#     created_on = models.DateTimeField('createdonmoviephoto', auto_now_add=True)
#     
#     def get_delete_url(self):
#         return reverse('movies_ajax_delete_photos', args=[self.id])


class CriticReview(models.Model):
    title = models.CharField(max_length=200)
    movie = models.ForeignKey("Movies")
    source = models.ForeignKey("CriticSource")
    rating =  models.IntegerField(blank=True, default=0)
    reviewed_by = models.CharField(max_length=30)
    published_on = models.DateTimeField(auto_now_add=True) 
    review = models.TextField()
    
class CriticSource(models.Model):
    source_title =  models.CharField(max_length=100)
    url = models.URLField()
    logo = models.ImageField(upload_to=get_moviegallery_path,null=True)
    copyright = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.source_title
    
    def get_source_image(self):
            image = self.logo        
            return image
        

class MovieLanguage(models.Model):
    
    name = models.CharField(max_length=40,null=True)
    def __unicode__(self):
        return self.name 
