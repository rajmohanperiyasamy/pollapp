import re
import math
from datetime import date
import datetime

from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson
from django.db.models import Count
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.html import strip_tags


from tastypie.resources import ModelResource,ALL,ALL_WITH_RELATIONS
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.utils import trailing_slash
from tastypie.api import Api

from easy_thumbnails.files import get_thumbnailer
from bs4 import BeautifulSoup

from common.utils import get_global_settings
from locality.models import Venue,VenuePhoto
from events.models import Event,EventPhoto,EventCategory
from attraction.models import Attraction,AttractionCategory,AttractionPhotos


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'last_login']
        allowed_methods = ['get']
        filtering = {
            'username': ALL,
            'created': ['exact'],
        }
    
###################### Event ########################
class EventCategoryResource(ModelResource):
    class Meta:
        queryset = EventCategory.objects.all().order_by('name')
        resource_name = 'eventscategorylist'
        fields = ['name','resource_uri','id','slug']
    
    def dehydrate(self,bundle):
        bundle.data['resource_uri'] = 'mobapp/api/v1/events_by_cat/?format=json&category='+str(bundle.obj.id)
        return bundle
          
class VenueResource(ModelResource):
    class Meta:
        queryset = Venue.objects.all().order_by('venue')
        resource_name = 'venue'
        fields = ['venue','description','address1','telephone','website','type','slug','lat','lon']
        filtering = {
            'zip':ALL
        }
    def dehydrate(self,bundle):
        image = bundle.obj.get_first_venue_photo()
        if image:bundle.data['image'] = get_thumbnail_image(image,'320','107')
        else:bundle.data['image'] = ''    
        event_list = Event.objects.filter(venue=bundle.obj,status='P').order_by('end_date','-tdate','-start_date').distinct()
        events = []
        for event in event_list:
            events.append({
                 'id':event.id,          
                 'title':event.title,
                 'image':get_thumbnail_image(event.get_cover_image()),          
                 'resource_uri': '/mobapp/api/v1/eventlist/%s/?format=json'%(event.id)  ,      
                           })
        bundle.data['events'] = events
        return bundle   
   
       
class EventResource(ModelResource):
    created_by = fields.ForeignKey(UserResource, 'created_by')
    venue      = fields.ForeignKey(VenueResource, 'venue')    
    category   = fields.ToManyField(EventCategoryResource, 'category',related_name='event') 
    
    class Meta:
        queryset = Event.objects.filter(status='P').order_by('-id').distinct()
        resource_name = 'eventlist'
      
    
    def dehydrate(self,bundle):
        global_settings = get_global_settings()
        
        bundle.data['event_description'] = filter_content(bundle.data['event_description'])
        category=bundle.obj.category.all()[:1][0]
        bundle.data['cat']=category.name
        bundle.data['currency'] = global_settings.currency
        
        try:venue=Venue.objects.get(event__id=int(bundle.data['id']))
        except:venue = None
        if bundle.obj.start_time:
            bundle.data['date_time'] = bundle.obj.start_date.strftime("%a, %b %d,")+' '+bundle.obj.start_time.strftime("%I:%M%p")
        else:
            bundle.data['date_time'] = bundle.obj.start_date.strftime("%a, %b %d")
        
        try:bundle.data['created_by'] = bundle.obj.created_by.profile.get_full_name()
        except:bundle.data['created_by'] =  bundle.obj.created_by
        
        image = bundle.obj.get_cover_image()
        bundle.data['image'] = get_thumbnail_image(image,'300','80')
        
        images=[]
        image_list = bundle.obj.get_photo_gallery()
        bundle.data['image_count'] = image_list.count()
        if image_list:
            image_list=image_list[:3]
            for img in image_list:
                croped_img=get_thumbnail_image(img.photo,'95','70')
                images.append(croped_img)
        bundle.data['imagelist'] = images       
        
        if venue:
            bundle.data['venue'] = venue.venue
            
            if venue.lat:bundle.data['lat'] = venue.lat
            else:bundle.data['lat'] = ''
            
            if venue.lon:bundle.data['lon'] = venue.lon 
            else:bundle.data['lon'] = '' 
            
            if venue.address1:bundle.data['address1'] = venue.address1 
            else:bundle.data['address1'] = '' 
            if venue.address2:bundle.data['address2'] = venue.address2
            else:bundle.data['address2'] = '' 
            if venue.zip:bundle.data['zip'] = venue.zip
            else:bundle.data['zip'] = '' 
            if venue.telephone:bundle.data['telephone'] = venue.telephone
            else:bundle.data['telephone'] = '' 
            if venue.email:bundle.data['email'] = venue.email
            else:bundle.data['email'] = '' 
           
                
        return bundle

class EventPhotoResource(ModelResource):
    event      = fields.ForeignKey(EventResource, 'event')  
    class Meta:
        queryset = EventPhoto.objects.all()
        resource_name = 'event_gallery'
        filtering={
                   'event':ALL
                   }
        


class EventsListResource(ModelResource):
    category   = fields.ToManyField(EventCategoryResource, 'category',related_name='events_by_cat') 
    venue      = fields.ForeignKey(VenueResource, 'venue') 
    
    class Meta:
        queryset = Event.objects.filter(status='P').order_by('end_date','-tdate','-start_date')
        resource_name = 'events_by_cat'
        fields = ['title','resource_uri','venue','listing_type','start_date','event_description']
        filtering = {
            'title':ALL_WITH_RELATIONS,
            'category': ALL,
            'listing_type':['exact'],
            'start_date':ALL,
            'venue':ALL,
            'zip':ALL
            
        }
     
    def dehydrate(self,bundle):
        bundle.data['resource_uri'] = bundle.data['resource_uri'].replace("events_by_cat", "eventlist");
        bundle.data['event_description'] = filter_content(bundle.data['event_description'])
        image = bundle.obj.get_cover_image()
        bundle.data['image'] = get_thumbnail_image(image)
        
        bundle.data['venuename'] = bundle.obj.venue
        bundle.data['zip'] = bundle.obj.venue.zip
        
        if bundle.obj.start_time:
            bundle.data['date_time'] = bundle.obj.start_date.strftime("%a, %b %d,")+' '+bundle.obj.start_time.strftime("%I:%M%p")
        else:
            bundle.data['date_time'] = bundle.obj.start_date.strftime("%a, %b %d")
            
        return bundle  
   




##################### Photos ###########################
from gallery.models import PhotoCategory,PhotoAlbum,Photos

class PhotoCategoryResource(ModelResource):
    class Meta:
        queryset = PhotoCategory.objects.all().order_by('name')
        resource_name = 'photocategorylist'
        fields = ['name','resource_uri','id']
    
    def dehydrate(self,bundle):
        bundle.data['resource_uri'] = 'mobapp/api/v1/photo_album_list/?format=json&category='+str(bundle.obj.id)
        return bundle

class PhotoAlbumListResource(ModelResource):
    category   = fields.ForeignKey(PhotoCategoryResource, 'category',related_name='photoalbum_by_cat') 
    
    class Meta:
        queryset = PhotoAlbum.objects.filter(status='P').order_by('-id')
        resource_name = 'photos_list_detail'
        fields = ['title','resource_uri','summary','listing_type','created_on','id']
        filtering = {
            'title':ALL_WITH_RELATIONS,
            'category': ALL,
            'listing_type':['exact'],
        }
    def dehydrate(self,bundle):
        bundle.data['category_name'] = bundle.obj.category.name        
        
        bundle.data['created_date'] = bundle.obj.created_on.strftime("%b %d, %Y")
        
        if bundle.obj.get_cover_image():
            bundle.data['image'] = get_thumbnail_image(bundle.obj.get_cover_image(),100,100)
            bundle.data['image_count'] = bundle.obj.get_gallery_uploaded_images().count()
        elif bundle.obj.get_cover_url():
            bundle.data['image'] = bundle.obj.get_cover_url()
            bundle.data['image_count'] = bundle.obj.get_gallery_flicker_images().count()
        
        images = []
        if bundle.obj.get_gallery_uploaded_images():
            for photos in bundle.obj.get_gallery_uploaded_images():
                 images.append(photos.photo)
        elif bundle.obj.get_gallery_flicker_images():
            for photos in bundle.obj.get_gallery_flicker_images():
                images.append(photos.get_image())
        bundle.data['images'] = images    
            
        return bundle 
class SPhotoAlbumListResource(ModelResource):
    category   = fields.ForeignKey(PhotoCategoryResource, 'category',related_name='photoalbum_by_cat') 
    
    class Meta:
        queryset = PhotoAlbum.objects.filter(status='P').order_by('-id')
        resource_name = 'sphotos_list_detail'
        fields = ['title','resource_uri','summary','listing_type']
        filtering = {
            'title':ALL_WITH_RELATIONS,
            'category': ALL,
            'listing_type':['exact'],
        }
    def dehydrate(self,bundle):
        bundle.data['resource_uri'] = bundle.data['resource_uri'].replace("sphotos_list_detail", "photos_list_detail");
        bundle.data['category_name'] = bundle.obj.category.name        
        
        bundle.data['created_date'] = bundle.obj.created_on.strftime("%b %d, %Y")
        
        if bundle.obj.get_cover_image():
            bundle.data['image'] = get_thumbnail_image(bundle.obj.get_cover_image(),100,100)
            bundle.data['image_count'] = bundle.obj.get_gallery_uploaded_images().count()
        elif bundle.obj.get_cover_url():
            bundle.data['image'] = bundle.obj.get_cover_url()
            bundle.data['image_count'] = bundle.obj.get_gallery_flicker_images().count()
        
        images = []
        if bundle.obj.get_gallery_uploaded_images():
            for photos in bundle.obj.get_gallery_uploaded_images():
                 images.append(get_thumbnail_image(photos.photo,100,100))
        elif bundle.obj.get_gallery_flicker_images():
            for photos in bundle.obj.get_gallery_flicker_images():
                images.append(photos.photo_url)
        bundle.data['images'] = images    
            
        return bundle  
 

class PhotosResource(ModelResource):
    album   = fields.ForeignKey(PhotoAlbumListResource, 'album',related_name='photos') 
    
    class Meta:
        queryset = Photos.objects.all()
        resource_name = 'photos'
        fields = ['photo','photo_url','title','caption']
        filtering = {
            'title':ALL_WITH_RELATIONS,
            'album':['exact'],
        }
        
    def dehydrate(self,bundle):
        
            
        
        return bundle


##################### Articles ###########################
from article.models import Article,ArticleCategory,ArticlePhotos

class ArticleCategoryResource(ModelResource):
    class Meta:
        queryset = ArticleCategory.objects.all().order_by('name')
        resource_name = 'articlecategorylist'
        fields = ['name','resource_uri','id','slug']
    
    def dehydrate(self,bundle):
        bundle.data['resource_uri'] = 'mobapp/api/v1/articlelist/?format=json&category='+str(bundle.obj.id)
        return bundle

class ArticleRes(ModelResource):
    category   = fields.ForeignKey(ArticleCategoryResource, 'category',related_name='articlelist') 
    class Meta:
        queryset = Article.objects.all()
        resource_name = 'article1'
        
   

class ArticleResource(ModelResource):
    category   = fields.ForeignKey(ArticleCategoryResource, 'category',related_name='articlelist') 
    class Meta:
        queryset = Article.objects.filter(status='P').order_by('-id').distinct()
        resource_name = 'article'
        filtering = {
            'title':ALL_WITH_RELATIONS,
            'category': ALL,
            'listing_type':['exact'],
        }
   
        
    def dehydrate(self,bundle):
        global_settings = get_global_settings()
        bundle.data['cat'] = bundle.obj.category.name
        bundle.data['content'] = filter_content(bundle.data['content'])
        try:bundle.data['author'] = bundle.obj.created_by.profile.get_full_name()
        except:bundle.data['author'] =  bundle.obj.created_by
        bundle.data['published_on'] = bundle.obj.published_on.strftime("%B %d, %Y")
        bundle.data['start_date'] = bundle.obj.published_on
        
        if bundle.obj.published_on:
            bundle.data['date_time'] = bundle.obj.published_on.strftime("%a, %b %d,")+' '+bundle.obj.published_on.strftime("%I:%M%p")
        else:
            bundle.data['date_time'] = bundle.obj.published_on.strftime("%a, %b %d")
        image = bundle.obj.get_featured_image()
        if image:bundle.data['image'] = get_thumbnail_image(image,'360','175')
        else:
            try:bundle.data['image'] = soup.img['src']
            except:bundle.data['image'] ="" 
                
        bundle.data['share_url'] = global_settings.website_url+bundle.obj.get_absolute_url()
        
        return bundle  

class ArtcleListResource(ModelResource):
    category   = fields.ForeignKey(ArticleCategoryResource, 'category',related_name='articlelist') 
    class Meta:
        queryset = Article.objects.defer('content').filter(status='P').order_by('-id')
        resource_name = 'articlelist'
        fields = ['title','summary','resource_uri','published_on','featured']
        filtering = {
            'title': ALL,         
            'published_on': ALL_WITH_RELATIONS,
            'featured':['exact'],
            'category':['exact']
        }
    def dehydrate(self, bundle):
        bundle.data['resource_uri'] = bundle.data['resource_uri'].replace("articlelist", "article");
        soup = BeautifulSoup(bundle.obj.content)
        bundle.data['category_name'] = bundle.obj.category.name
        try:bundle.data['author'] = bundle.obj.created_by.profile.get_full_name()
        except:bundle.data['author'] =  bundle.obj.created_by
        
        bundle.data['published_date'] = bundle.obj.published_on.strftime("%B %d, %Y")
        
        image = bundle.obj.get_featured_image()
        if image:bundle.data['image'] = get_thumbnail_image(image)
        else:
            try:bundle.data['image'] = soup.img['src']
            except: pass
        '''
        for img in soup.findAll(lambda tag: tag.name=="img"):
                image_url = img['src']
                print image_url
        '''      
        return bundle
        
       
################# Business #########################
from business.models import Business,BusinessCategory,BusinessPhoto

class BusinessCategoryResource(ModelResource):
    class Meta:
        queryset = BusinessCategory.objects.filter(parent_cat__isnull=True).order_by('name')
        resource_name = 'businesscategorylist'
        fields = ['name','resource_uri','id','slug']
    
    def dehydrate(self,bundle):
        bundle.data['resource_uri'] = 'mobapp/api/v1/businesslist/?format=json&category='+str(bundle.obj.id)
        return bundle

class BusinessResource(ModelResource):
    class Meta:
        queryset = Business.objects.filter(status='P').order_by('-id')
        resource_name = 'business'
        #fields = ['name','ratings','resource_uri','featured_sponsored','description','fb_url','twitter_url','gooleplus_url']
    
    def dehydrate(self,bundle):
        bundle.data['logo'] = get_thumbnail_image(bundle.obj.get_payment_photo())
        bundle.data['description'] = filter_content(bundle.data['description'])
        try:
            image = bundle.obj.get_photos()[:1]
            img = image[0].photo
            bundle.data['image'] = get_thumbnail_image(img,'360','107')
        except:bundle.data['image'] = ''
        
        images=[]
        image_list = bundle.obj.get_photos()
        bundle.data['image_count'] = image_list.count()
        if image_list:
            image_list=image_list[:3]
            for img in image_list:
                croped_img=get_thumbnail_image(img.photo,'95','70')
                images.append(croped_img)
        bundle.data['imagelist'] = images       
        
        if bundle.obj.operating_hours:
            if bundle.obj.workinghours:
                wrkin_hrs=bundle.obj.workinghours
                if wrkin_hrs.sun_start:
                    sun = '%s - %s'%(wrkin_hrs.sun_start,wrkin_hrs.sun_end)
                else:sun = "Closed"   
                if wrkin_hrs.mon_start:
                    mon = '%s - %s'%(wrkin_hrs.mon_start,wrkin_hrs.mon_end)
                else:mon = "Closed"    
                if wrkin_hrs.tue_start:
                    tue = '%s - %s'%(wrkin_hrs.tue_start,wrkin_hrs.tue_end)
                else:tue = "Closed"    
                if wrkin_hrs.wed_start:
                    wed = '%s - %s'%(wrkin_hrs.wed_start,wrkin_hrs.wed_end)
                else:wed = "Closed"    
                if wrkin_hrs.thu_start:
                    thu = '%s - %s'%(wrkin_hrs.thu_start,wrkin_hrs.thu_end)
                else:thu = "Closed"    
                if wrkin_hrs.fri_start:
                    fri = '%s - %s'%(wrkin_hrs.fri_start,wrkin_hrs.fri_end)
                else:fri = "Closed"    
                if wrkin_hrs.sat_start:
                    sat = '%s - %s'%(wrkin_hrs.sat_start,wrkin_hrs.sat_end)
                else:sat = "Closed"    
                
                wrk_hrs = [ sun,mon,tue,wed,thu,fri,sat ]
                bundle.data['workig_hrs'] = wrk_hrs
            else: bundle.data['workig_hrs'] =""
        
        buss_address = bundle.obj.getaddress()[:1][0]
        if buss_address:
            if buss_address.pointer_lat:bundle.data['lat'] = buss_address.pointer_lat
            else:bundle.data['lat'] = ''
            if buss_address.pointer_lng :bundle.data['lon'] = buss_address.pointer_lng 
            else:bundle.data['lon'] = '' 
            if buss_address.address1 and buss_address.address2:
                bundle.data['address'] = buss_address.address1+', '+buss_address.address2 
            elif buss_address.address1:bundle.data['address'] = buss_address.address1    
            else:bundle.data['address'] = ''
            if buss_address.city:bundle.data['city'] = buss_address.city
            else:bundle.data['city'] = '' 
            if buss_address.mobile_no:bundle.data['phone'] = buss_address.mobile_no
            elif  buss_address.telephone:bundle.data['phone'] = buss_address.telephone
            else:bundle.data['phone'] = ''
            if buss_address.email:bundle.data['email'] = buss_address.email
            else:bundle.data['email'] = '' 
            if buss_address.website:bundle.data['website'] = buss_address.website
            else:bundle.data['website'] = '' 

        return bundle 

def business_list(request):
    gbl_settings = get_global_settings()
    data = []
    old_data = []
    key = {}
    name_search = request.GET.get('name_icontains',None)
    type = request.GET.get('featured_sponsored',None)
    try:category = BusinessCategory.objects.get(id=request.GET['category'])
    except:category = None
    if category:key['categories'] = category
    if type:key['featured_sponsored'] = type
    if name_search:key['name__icontains'] = name_search
   
    
    business=Business.objects.filter(status='P',**key)
   
    range=int(request.GET.get('range',36000))
    limit = int(request.GET.get('limit',100))
    offset = int(request.GET.get('offset',0))
    try:
        lant=float(request.GET['lat'])
        long=float(request.GET['lon'])
        for bus in business:
            addrs_list=bus.get_lat_lang()
            x=math.cos( math.radians(lant) ) * math.cos( math.radians( addrs_list['lat']  ) ) * math.cos( math.radians( addrs_list['lon'] ) - math.radians(long) ) + math.sin( math.radians(lant) ) * math.sin( math.radians( addrs_list['lat'] ) ) 
            distance = 3959 * (math.acos(x))
            if distance <= range:
                buss_address = bus.getaddress()[:1][0]
                if buss_address:
                    if buss_address.address1 and buss_address.address2:
                        address = buss_address.address1+', '+buss_address.address2 
                    elif buss_address.address1:address = buss_address.address1    
                    else:address = ''
                    try:
                        city = buss_address.city
                        if not city:city = gbl_settings.city
                    except:city = gbl_settings.city
                old_data.append({'resource_uri':'/mobapp/api/v1/business/'+str(bus.id)+'/','name':bus.name,
                             'logo':get_thumbnail_image(bus.get_payment_photo()),'lat': buss_address.pointer_lat,
                             'lon':buss_address.pointer_lng ,'address':address,'city':city,'distance':round(distance, 1)
                             })  
        sort_data  = [ d['distance'] for d in old_data ]
        unsort_data = sort_data[:]
        sort_data.sort()
        data = []
        for val in sort_data:
            ind = unsort_data.index(val)
            data.append(old_data[ind])
            unsort_data[ind] = ''
        
    except:
        for bus in business:
            buss_address = bus.getaddress()[:1][0]
            if buss_address:
                if buss_address.address1 and buss_address.address2:
                    address = buss_address.address1+', '+buss_address.address2 
                elif buss_address.address1:address = buss_address.address1    
                else:address = ''
                try:city = buss_address.city
                except:city = gbl_settings.city
            data.append({'resource_uri':'/mobapp/api/v1/business/'+str(bus.id)+'/','name':bus.name,
                         'logo':get_thumbnail_image(bus.get_payment_photo()),'lat': buss_address.pointer_lat,
                         'lon':buss_address.pointer_lng ,'address':address,'city':city
                         })     
    
                   
    constant_val={'limit':limit,'offset':offset,'total_count':len(data)}   
    objects = {'meta':constant_val,'objects':data[offset:offset+limit]}
    return HttpResponse(simplejson.dumps(objects))


######################### VIDEOS ##############################
from movies.models import MovieType,MovieLanguage,Theatres,Movies,CriticSource,MoviesPhoto,MovieType
class MovieLanguageResources(ModelResource):
    
    class Meta:
        queryset = MovieLanguage.objects.all().order_by('name')
        resource_name = 'movie_language'
    
    def dehydrate(self,bundle):
        bundle.data['resource_uri'] = 'mobapp/api/v1/movies/?format=json&language='+str(bundle.obj.id)
        return bundle

class MoviesCategoryResource(ModelResource):
    class Meta:
        queryset = MovieType.objects.all().order_by('name')
        resource_name = 'movies_cat'
        fields = ['name','resource_uri','id','slug']
    
    def dehydrate(self,bundle):
        bundle.data['resource_uri'] = 'mobapp/api/v1/movies/?format=json&category='+str(bundle.obj.id)
        return bundle

           
class MoviesResources(ModelResource):
    language   = fields.ForeignKey(MovieLanguageResources, 'language',related_name='movie_language') 
    class Meta:
        queryset = Movies.objects.filter(status='P').select_related('language').prefetch_related('movie_type').order_by('-release_date')
        resource_name = 'movies'
        fields = ['title','director','cast','movie_url','synopsis']
        filtering = {
            'title':ALL_WITH_RELATIONS,
            'language': ALL,
            'release_date': ALL
        }
    def dehydrate(self,bundle):
        bundle.data['synopsis'] = filter_content(bundle.data['synopsis'])
        if bundle.obj.release_date:
            if bundle.obj.release_date > datetime.datetime.now().date():
                bundle.data['release_date'] = bundle.obj.release_date.strftime("%B %d, %Y")
                bundle.data['released_on'] = ''
            else:
                bundle.data['released_on'] = bundle.obj.release_date.strftime("%B %d, %Y")
                bundle.data['release_date'] = ''
        else:
            bundle.data['release_date'] = 'Not Avaliable'
            
        bundle.data['language'] = bundle.obj.language.name
        bundle.data['poster'] = get_thumbnail_image(bundle.obj.image)
        bundle.data['poster1'] = get_thumbnail_image(bundle.obj.image,'102','151')
        genre = []
        for gnr in bundle.obj.movie_type.all():
            genre.append(gnr.name)
        bundle.data['genre'] = genre
        #bundle.data['trailer'] = bundle.obj.get_movie_url()
        if bundle.obj.movie_url:bundle.data['trailer'] = 'http://www.youtube.com/watch?v=%s'%(bundle.obj.movie_url)
        casting = []
        total_casts = bundle.obj.cast
        casting = total_casts.split(',')
        if bundle.obj.cast:bundle.data['cast'] = casting[:5]
        images = []
        image_list = bundle.obj.get_movie_photo()
        bundle.data['images_count'] = image_list.count()
        for img in image_list:
            images.append(get_thumbnail_image(img.photo))
        bundle.data['images'] = images
        if bundle.obj.duration_hours:bundle.data['duration'] = bundle.obj.duration_hours
        else:bundle.data['duration'] = ''
            
        return bundle



def get_thumbnail_image(image,w=90,h=90):
    thumbnail_options = dict(size=(w, h), crop=True)
    try:
        img = get_thumbnailer(image).get_thumbnail(thumbnail_options)
        return settings.MEDIA_URL+str(img)
    except:return ''

def filter_content(content):
       import HTMLParser
       parse = HTMLParser.HTMLParser()
       custom_html = content.replace('<br />','@@').replace('@@+','')
       gen_string = parse.unescape(re.sub('\s+', ' ',strip_tags(custom_html)))
       return  re.sub('@@', '\n',gen_string)   

###################### Attraction ################################

class AttractionResource(ModelResource):
    class Meta:
        queryset = Attraction.objects.filter(status='P').order_by('-id')
        resource_name = 'attraction'
        
    
    def dehydrate(self,bundle):
        bundle.data['logo'] = get_thumbnail_image(bundle.obj.get_payment_photo())
        bundle.data['description'] = filter_content(bundle.data['description'])
        try:
            image = bundle.obj.get_cover_image()[:1]
            img = image[0].photo
            bundle.data['image'] = get_thumbnail_image(img,'360','107')
        except:bundle.data['image'] = ''
        
           
        
        attr_address = bundle.obj.get_attr_venue()[:1][0]
        if attr_address:
            if attr_address.lat:bundle.data['lat'] = attr_address.lat
            else:bundle.data['lat'] = ''
            if attr_address.lon :bundle.data['lon'] = attr_address.lon 
            else:bundle.data['lon'] = '' 
            if attr_address.address1 and attr_address.address2:
                bundle.data['address'] = attr_address.address1+', '+attr_address.address2 
            elif attr_address.address1:bundle.data['address'] = attr_address.address1    
            else:bundle.data['address'] = ''
            
            if attr_address.mobile:bundle.data['phone'] = attr_address.mobile
            elif  attr_address.telephone:bundle.data['phone'] = attr_address.telephone
            else:bundle.data['phone'] = ''
            if attr_address.email:bundle.data['email'] = attr_address.email
            else:bundle.data['email'] = '' 
            if attr_address.website:bundle.data['website'] = attr_address.website
            else:bundle.data['website'] = '' 

        return bundle 



class AttractionCategoryResource(ModelResource):
    class Meta:
        queryset = AttractionCategory.objects.all().order_by('name')
        resource_name = 'attractioncategorylist'
        fields = ['name','resource_uri','id','slug']
    
    def dehydrate(self,bundle):
        bundle.data['resource_uri'] = 'mobapp/api/v1/attraction_list/?format=json&category='+str(bundle.obj.id)
        return bundle



def attraction_list(request):
    gbl_settings = get_global_settings()
    data = []
    old_data = []
    key = {}
    name_search = request.GET.get('name_icontains',None)
    type = request.GET.get('featured_sponsored',None)
    try:category = AttractionCategory.objects.get(id=request.GET['category'])
    except:category = None
    if category:key['category'] = category
    if type:key['is_featured'] = type
    if name_search:key['name__icontains'] = name_search
   
    
    attraction=Attraction.objects.filter(status='P',**key)
   
    range=int(request.GET.get('range',36000))
    limit = int(request.GET.get('limit',100))
    offset = int(request.GET.get('offset',0))
    try:
        lant=float(request.GET['lat'])
        long=float(request.GET['lon'])
        for attr in attraction:
            addrs_list=attr.get_lat_lang()
            x=math.cos( math.radians(lant) ) * math.cos( math.radians( addrs_list['lat']  ) ) * math.cos( math.radians( addrs_list['lon'] ) - math.radians(long) ) + math.sin( math.radians(lant) ) * math.sin( math.radians( addrs_list['lat'] ) ) 
            distance = 3959 * (math.acos(x))
            if distance <= range:
                attr_address = attr.get_attr_venue()[:1][0]
                if attr_address:
                    if attr_address.address1 and attr_address.address2:
                        address = attr_address.address1+', '+attr_address.address2 
                    elif attr_address.address1:address = attr_address.address1    
                    else:address = ''
                    try:
                        city = attr_address.city
                        if not city:city = gbl_settings.city
                    except:city = gbl_settings.city
                old_data.append({'resource_uri':'/mobapp/api/v1/attraction/'+str(attr.id)+'/','name':attr.name,
                             'logo':get_thumbnail_image(attr.get_cover_image()),'lat': attr_address.pointer_lat,
                             'lon':attr_address.pointer_lng ,'address':address,'city':city,'distance':round(distance, 1)
                             })  
        sort_data = [ d['distance'] for d in old_data ]
        unsort_data = sort_data[:]
        sort_data.sort()
        data = []
        for val in sort_data:
            ind = unsort_data.index(val)
            data.append(old_data[ind])
            unsort_data[ind] = ''
        
    except:
        for attr in attraction:
            attr_address = attr.get_attr_venue()[:1][0]
            if attr_address:
                if attr_address.address1 and attr_address.address2:
                    address = attr_address.address1+', '+attr_address.address2 
                elif attr_address.address1:address = attr_address.address1    
                else:address = ''
                try:city = attr_address.city
                except:city = gbl_settings.city
            try:
                latitude = attr_address.pointer_lat
                longitude = attr_address.pointer_lng
            except:
                latitude = 44.09
                longitude = 10.11
            data.append({'resource_uri':'/mobapp/api/v1/attraction/'+str(attr.id)+'/','name':attr.name,
                         'logo':get_thumbnail_image(attr.get_payment_photo()),'lat': latitude,
                         'lon':longitude ,'address':address,'city':city
                         })     
    
                   
    constant_val={'limit':limit,'offset':offset,'total_count':len(data)}   
    objects = {'meta':constant_val,'objects':data[offset:offset+limit]}
    return HttpResponse(simplejson.dumps(objects))      
   
#########################################GlOBAL NEAR BY########################################### 
def near_by_locations_events(request):
        data = []
        
        lant=float(request.GET['lat'])
        long=float(request.GET['lon'])
        range=int(request.GET.get('range',36000))
        limit = int(request.GET.get('limit',100))
        offset = int(request.GET.get('offset',0))
        events=Event.objects.all()
        for event in events:
            venue_list=event.get_lat_lang()
            x=math.cos( math.radians(lant) ) * math.cos( math.radians( venue_list['lat']  ) ) * math.cos( math.radians( venue_list['lon'] ) - math.radians(long) ) + math.sin( math.radians(lant) ) * math.sin( math.radians( venue_list['lat'] ) ) 
            distance = 3959 * (math.acos(x))
            if distance <= range:
                data.append({'type':"events",
                             'resource_uri':'/mobapp/api/v1/eventlist/'+str(event.id)+'/',
                             'title':event.title,
                             'venuename':venue_list['venue'],
                             'distance':round(distance, 1),
                             'latitude':venue_list['lat'],
                             'longitude':venue_list['lon'],
                             'image':get_thumbnail_image(event.get_cover_image())})
        
        old_data = data[:] 
        sort_data = [ d['distance'] for d in old_data ]
        unsort_data = sort_data[:]
        sort_data.sort()
        data = []
        for val in sort_data:
            ind = unsort_data.index(val)
            data.append(old_data[ind])
            unsort_data[ind] = ''
                    
        constant_val={'limit':limit,'offset':offset,'total_count':len(data)}   
        objects = {'meta':constant_val,'objects':data[offset:offset+limit]}
        return HttpResponse(simplejson.dumps(objects))   
    
def near_by_locations_attractions(request):
        data = []
        attraction=Attraction.objects.all()
        lant=float(request.GET['lat'])
        long=float(request.GET['lon'])
        range=int(request.GET.get('range',36000))
        limit = int(request.GET.get('limit',100))
        offset = int(request.GET.get('offset',0))
        for event in attraction:
            x=math.cos( math.radians(lant) ) * math.cos( math.radians( event.venue.lat  ) ) * math.cos( math.radians( event.venue.lon ) - math.radians(long) ) + math.sin( math.radians(lant) ) * math.sin( math.radians( event.venue.lat ) ) 
            distance = 3959 * (math.acos(x))
            if distance <= range:
                data.append({'resource_uri':'/mobapp/api/v1/eventlist/'+str(event.id)+'/',
                             'title':event.name,
                             'distance':round(distance, 1),
                             'latitude':event.venue.lat,
                             'longitude':event.venue.lon,
                             'image':get_thumbnail_image(event.get_cover_image())})
                
        constant_val={'limit':limit,'offset':offset,'total_count':len(data)}   
        objects = {'meta':constant_val,'objects':data[offset:offset+limit]}
        return HttpResponse(simplejson.dumps(objects))   

def gloabal_nearby(request):
        data = []        
        lant=float(request.GET['lat'])
        long=float(request.GET['lon'])
        range=int(request.GET.get('range',36000))
        limit = int(request.GET.get('limit',100))
        offset = int(request.GET.get('offset',0))
        events=Event.objects.all()
        for event in events:
            venue_list=event.get_lat_lang()
            x=math.cos( math.radians(lant) ) * math.cos( math.radians( venue_list['lat']  ) ) * math.cos( math.radians( venue_list['lon'] ) - math.radians(long) ) + math.sin( math.radians(lant) ) * math.sin( math.radians( venue_list['lat'] ) ) 
            distance = 3959 * (math.acos(x))
            if distance <= range:
                data.append({'type':"events",'resource_uri':'/mobapp/api/v1/eventlist/'+str(event.id)+'/','title':event.title,'distance':round(distance, 3),'latitude':venue_list['lat'],'longitude':venue_list['lon'],
                             'image':get_thumbnail_image(event.get_cover_image(),'40','40')})
        
        attraction=Attraction.objects.all()
        for event in attraction:
            x=math.cos( math.radians(lant) ) * math.cos( math.radians( event.venue.lat  ) ) * math.cos( math.radians( event.venue.lon ) - math.radians(long) ) + math.sin( math.radians(lant) ) * math.sin( math.radians( event.venue.lat ) ) 
            distance = 3959 * (math.acos(x))
            if distance <= range:
                data.append({'type':"attraction",'resource_uri':'/mobapp/api/v1/eventlist/'+str(event.id)+'/','title':event.name,'distance':round(distance, 3),'latitude':event.venue.lat,'longitude':event.venue.lon,
                             'image':get_thumbnail_image(event.get_cover_image(),'40','40')})
        business=Business.objects.all()
        for bus in business:
            addrs_list=bus.get_lat_lang()
            x=math.cos( math.radians(lant) ) * math.cos( math.radians( addrs_list['lat']  ) ) * math.cos( math.radians( addrs_list['lon'] ) - math.radians(long) ) + math.sin( math.radians(lant) ) * math.sin( math.radians( addrs_list['lat'] ) ) 
            distance = 3959 * (math.acos(x))
            if distance <= range:
                buss_address = bus.getaddress()[:1][0]                   
                data.append({'type':"Business",'resource_uri':'/mobapp/api/v1/business/'+str(bus.id)+'/','title':bus.name,
                             'image':get_thumbnail_image(bus.get_payment_photo(),'40','40'),'latitude': buss_address.pointer_lat,
                             'longitude':buss_address.pointer_lng ,'distance':round(distance, 3)
                             })
        old_data = data[:] 
        sort_data = [ d['distance'] for d in old_data ]
        unsort_data = sort_data[:]
        sort_data.sort()
        data = []
        for val in sort_data:
            ind = unsort_data.index(val)
            data.append(old_data[ind])
            unsort_data[ind] = ''
                
        constant_val={'limit':limit,'offset':offset,'total_count':len(data)}   
        objects = {'meta':constant_val,'objects':data[offset:offset+limit]}
        return HttpResponse(simplejson.dumps(objects))   



############################### Gallery Listing ################################

class BusinessPhotoResource(ModelResource):
    business = fields.ForeignKey(BusinessResource, 'business')  
    class Meta:
        queryset = BusinessPhoto.objects.all()
        resource_name = 'bus_gallery'
        filtering={
                   'business':ALL
                   }
class ArticlePhotoResource(ModelResource):
    article = fields.ForeignKey(ArticleResource, 'article')  
    class Meta:
        queryset = ArticlePhotos.objects.all()
        resource_name = 'article_gallery'
        filtering={
                   'article':ALL
                   }

class MoviePhotoResource(ModelResource):
    movie = fields.ForeignKey(MoviesResources, 'movie')  
    class Meta:
        queryset = MoviesPhoto.objects.all()
        resource_name = 'movie_gallery'
        filtering={
                   'movie':ALL
                   }
class AttractionPhotoResource(ModelResource):
    attraction = fields.ForeignKey(AttractionResource, 'attraction')  
    class Meta:
        queryset = AttractionPhotos.objects.all()
        resource_name = 'attraction_gallery'
        filtering={
                   'attraction':ALL
                   }
        











            
v1_api = Api(api_name='v1')
v1_api.register(UserResource())

#Events
v1_api.register(EventsListResource())
v1_api.register(EventPhotoResource())
v1_api.register(VenueResource())
v1_api.register(EventResource())    
v1_api.register(EventCategoryResource()) 

#Photos
v1_api.register(PhotoCategoryResource())  
v1_api.register(PhotoAlbumListResource())  
v1_api.register(PhotosResource()) 
v1_api.register(SPhotoAlbumListResource()) 
#Articles
v1_api.register(ArticleCategoryResource())  
v1_api.register(ArticleResource())  
v1_api.register(ArtcleListResource()) 
v1_api.register(ArticleRes()) 
v1_api.register(ArticlePhotoResource()) 

#attraction

v1_api.register(AttractionResource()) 
v1_api.register(AttractionPhotoResource()) 
v1_api.register(AttractionCategoryResource()) 

#Business
v1_api.register(BusinessCategoryResource()) 
#v1_api.register(BusinessleListResource()) 
v1_api.register(BusinessResource()) 
v1_api.register(BusinessPhotoResource()) 


v1_api.register(MovieLanguageResources()) 
v1_api.register(MoviesResources()) 
v1_api.register(MoviePhotoResource()) 
v1_api.register(MoviesCategoryResource())


