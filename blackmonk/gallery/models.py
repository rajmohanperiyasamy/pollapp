from django.db import models
import datetime
from django.db.models import Q
import os
from django.conf import settings
from django.template.loader import render_to_string
from easy_thumbnails.fields import ThumbnailerImageField
from django.core.urlresolvers import reverse

from common.models import ModuleNames,Basetable
from common.utils import get_global_settings

from locality.models import Locality

from django.conf import settings

from audit_log.models.managers import AuditLog

User = settings.AUTH_USER_MODEL
#P=published    H=not published    D=draft
import uuid
def get_photosgallery_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('photos/gallery', filename)
class Tag(models.Model):    
    tag = models.CharField(max_length=150)
    total_ref = models.IntegerField(blank=True, default=0)
    font_size = models.IntegerField(blank=True, default=0)
    def __unicode__(self):
        return self.tag
    def get_album_count(self):
        return PhotoAlbum.objects.filter(tags__tag=self.tag).count()


class PhotoCategory(models.Model):
    name = models.CharField(max_length=150)
    #caption = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255)
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    is_editable = models.BooleanField(default=True) 
    def __unicode__(self):
        return self.name
    def get_main_categories(self):
        return PhotoCategory.objects.filter(parent_cat__isnull=True).order_by('name')
    def get_gallery_count(self):
        return PhotoAlbum.objects.filter(is_active=True, status='P', category=self).count()
    def get_all_gallery_count(self):
        return PhotoAlbum.objects.filter(category=self).count()
    def get_all_photo_count(self):
        return Photos.objects.filter(album__category=self).count()
    def get_absolute_url(self):
        url = '/photos/' + self.slug + '/'
        return url
    def get_latest_photo(self):
        photos = Photos.objects.filter(album__category=self).order_by('-published_on')[:1]
        for photo in photos:
            return photo.photo_url.split('_m.jpg')[:1][0]
    
    class Meta:
        ordering = ['-is_editable', 'name']

def get_default_category():
    return PhotoCategory.objects.get_or_create(name="Uncategorized", slug='uncategorized', is_editable=False)[0]

class PhotoAlbum(Basetable):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=2000,null=True)
    category = models.ForeignKey("PhotoCategory", default=get_default_category)
    flickr_date = models.DateTimeField("flickr_date",null=True)
    slug = models.SlugField(max_length=255)
    tags = models.ManyToManyField("Tag",null=True)
    most_viewed = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    is_featured=models.BooleanField(default=False)
    published_on = models.DateTimeField(null=True,blank=True)
    is_editable = models.BooleanField(default=True)
    audit_log = AuditLog()
    def __unicode__(self):
        return self.title
    def get_visits(self):
        return self.most_viewed
    def get_action_type(self):
        if self.status=='P':return 'update'
        else:return 'delete'
    def get_preview_url(self):
        return reverse('staff_gallery_detail', args=[self.id]) 
    def get_modified_time(self):
        return self.modified_on
    #method to show random image
    def new_cover_image(self):
        photo = Photos.objects.filter(album=self, featured=True)
        if not photo.exists():
            photo = Photos.objects.filter(album=self).order_by('?')
        if photo.exists():
            img = photo[0]
            return img.photo_url if img.photo_url else img
        else:
            return self.get_default_image()
        
    def get_random_image(self):
        try:
            photo = Photos.objects.filter(album=self).order_by('?')[:1][0]
            return photo.photo
        except:
            return False
        
    def get_cover_image(self):
        photo = Photos.objects.filter(album=self, featured=True)
        if photo.exists():
            if photo.count() > 1:
                Photos.objects.exclude(id=photo[0].id).update(featured=False)
            return photo[0].photo
        else:
            return self.get_random_image()
    def get_cover_url(self):
        photos = Photos.objects.filter(album=self).order_by('?')[:1]
        if photos:
            for photo in photos:
                return photo.photo_url
        else:return False
    
    #Notification
    def get_staff_preview_url(self):
        url = reverse('staff_gallery_detail',args=[self.id])
        return url
    def get_staff_listing_url(self):
        url = reverse('staff_manage_gallery')
        return url
    #Notification
    
    def get_status(self):
        if self.status =='P':
            sts = 'published'
        elif self.status =='N':
            sts = 'pending' 
        elif self.status =='B':
            sts = 'blocked'
        elif self.status =='R':
            sts = 'rejected' 
        elif self.status =='D':
            sts = 'drafted' 
        else: sts = 'expired' 
        return sts             
    
    def get_default_image(self):
        return settings.STATIC_URL+"ui/images/global/img-none.png"        
    
    def cover_image(self):
        photos = Photos.objects.filter(album=self).order_by('?')[:1]
        for photo in photos:
            if photo.photo_url:
                return photo.photo_url.split('_m.jpg')[:1][0]
    
    def get_gallery_image(self):
        return Photos.objects.filter(album=self).order_by('id')
    
    def get_gallery_flicker_images(self):
        return Photos.objects.filter(album=self,photo_url__isnull=False).order_by('id')
    
    def get_gallery_uploaded_images(self):
        return Photos.objects.filter(album=self,photo_url__isnull=True).order_by('id') 
    
    def get_photo_gallery(self):
        return Photos.objects.filter(album=self).order_by('id')
            
    def cover_imageM(self):
        photos = Photos.objects.filter(album=self).order_by('?')[:1]
        if photos:
            for photo in photos:
                if photo.photo_url:
                    return photo.photo_url
                else:
                    return photo.photo.url
        else:
            return settings.STATIC_URL+"themes/green/images/global/nophoto_90.jpg"
        
    def get_MobThumb(self):
        photos = Photos.objects.filter(album=self).order_by('?')[:1]
        if photos:
            for photo in photos:
                if photo.photo_url:
                    return photo.photo_url
                else:
                    return photo.photo.url
        else:
            return False
            
    def get_last_uploaded(self):
        photos = Photos.objects.filter(album=self).order_by('-published_on')[:1]
        for photo in photos:
            return photo
    def get_image_count(self):
        return Photos.objects.filter(album=self).count()
    def get_absolute_url(self):
        url = '/photos/'+ self.slug + '.html'
        return url
    def get_album_url(self):
        global_settings = get_global_settings()
        url = global_settings.website_url+'/photos/'+ self.slug + '.html'
        return url
    def get_limited_photos(self):
        return Photos.objects.filter(album=self).order_by('?')[:5]
    def gettags(self):
        return self.tags.all()
    def get_comments(self):
        return AlbumComment.objects.filter(album=self,status='A').order_by('-created_on')
    def get_comment_count(self):
        return AlbumComment.objects.filter(album=self,status='A').count()
    def get_total_comments(self):
        return AlbumComment.objects.filter(album=self).order_by('-id')
    def get_total_comment_count(self):
        return AlbumComment.objects.filter(album=self).count()
    def get_pending_comments_count(self):
        return AlbumComment.objects.filter(album=self,status='N').count()
    def get_rejected_comments_count(self):
        return AlbumComment.objects.filter(album=self,status='B').count()
    def get_search_result_html( self ):
        template = 'search/r_photos.html'
        data = { 'object': self }
        return render_to_string( template, data )
    def show_cover_image(self):
        photos = Photos.objects.filter(album=self).order_by('?')[:1]
        for photo in photos:
            if photo.photo_url:
                return photo.photo_url
    class Meta:
        permissions = (("publish_photoalbum", "Can Publish PhotoAlbum"),("promote_photoalbum", "Can Promote PhotoAlbum"),)
        
class Photos(Basetable):
    album = models.ForeignKey("PhotoAlbum",related_name='album_photos', null=True, blank=True)
    photo = ThumbnailerImageField(upload_to=get_photosgallery_path)
    photo_url = models.CharField(max_length=255,null=True)
    owner_name = models.CharField(max_length=100,null=True)
    caption = models.CharField(max_length=200, default="")
    published_on = models.DateTimeField(null=True)
    votes = models.PositiveIntegerField(default=0)
    ratings = models.PositiveIntegerField(default=0)
    most_viewed = models.PositiveIntegerField(default=0)#now not using
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)
    
    
    def __unicode__(self):
        return self.caption
    
    def get_flickr_id(self):
        if self.photo_url:
            return self.photo_url.split('/')[-1].split('_')[0]
        else:
            return ''
    
    def get_flickr_thumbnail(self):
        if self.photo_url:
            a = self.photo_url.split('/')
            b = a[-1].split('_')
            b[-1] = '.'.join(['t', b[-1].split('.')[-1]])
            a[-1] = '_'.join(b)
            return '/'.join(a)
        else:
            return ''
    
    def get_image(self):
        if self.photo_url:
            url= self.photo_url.split('_m.jpg')[:1][0]
            return url+".jpg"
        else:
            return self.photo.url
        
    def get_large_image(self):
        url= self.photo_url.split('_m.jpg')[:1][0]
        return url+"_z.jpg"
    def get_small_image(self):
        url= self.photo_url.split('_m.jpg')[:1][0]
        return url+"_t.jpg"
        
    def get_imageL(self):
        if self.photo_url:
            url= self.photo_url.split('_m.jpg')[:1][0]
            return url+"_z.jpg"
        else:
            global_settings = get_global_settings()
            url = '%s/photos/%s_%s-M.jpg' % (global_settings.smugmug_url, self.photo_id, self.photo_key)
            return url
    
    def get_absolute_url(self):
        url = '/photos/'+ self.album.slug + '.html?pid=%d' % (self.id)
        return url
    def get_photo_name(self):
        return os.path.basename(self.photo.url)
    
    def get_delete_url(self):
        return reverse('gallery_ajax_delete_photo', args=[self.id])
    
    def get_twitter_card_image(self):
        url= self.photo_url.split('_m.jpg')[:1][0]
        return url+"_b.jpg"
    
class AlbumComment(models.Model):
    album = models.ForeignKey("PhotoAlbum")
    name = models.CharField(max_length=60,null=True)
    email = models.EmailField(max_length=300,null=True)
    title = models.CharField(max_length=120,null=True)
    comment = models.TextField()
    abuse_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=1,default='N')#N=new    B=blocked    A=approved
    approved_on = models.DateTimeField("approvedalbumcomment", auto_now = True)
    created_by = models.ForeignKey(User, related_name='createdbyalbumcomment',null=True)
    created_on  = models.DateTimeField('Created', auto_now_add = True)

