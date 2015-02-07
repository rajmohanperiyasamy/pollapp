from django.db import models
from common.models import Basetable

from django.template.loader import render_to_string
from common.utils import get_global_settings
from django.core.urlresolvers import reverse
from django.conf import settings

from audit_log.models.managers import AuditLog

User = settings.AUTH_USER_MODEL

class VideoCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    label = models.CharField(max_length=200)
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return '/videos/'+self.slug+'/'
    def get_videos(self):
        return Videos.objects.filter(category=self,is_active=True)#retreive active videos
    def get_videos_count(self):
        return Videos.objects.filter(category=self).count()#retreive count of active videos
    def get_latest_video(self):
        videos=Videos.objects.filter(category=self,is_active=True).order_by('-id')[:1]#retreive latest active videos
        for v in videos:
            return v.get_thumb()

class Keywords(models.Model):    
    keyword = models.CharField(max_length=150)
    total_ref = models.IntegerField(blank=True, default=0)
    font_size = models.IntegerField(blank=True, default=0)
    def __unicode__(self):
        return self.keyword
    def get_videos(self):
        return Videos.objects.filter(keywords__keyword=self.keyword)
    def get_videos_count(self):
        return Videos.objects.filter(keywords__keyword=self.keyword).count()

def get_default_category():
    return VideoCategory.objects.get_or_create(name="Uncategorized", slug='uncategorized')[0]

class Videos(Basetable):
    #N=New    #D=Draft
    category = models.ForeignKey('VideoCategory', default=get_default_category, on_delete=models.SET_DEFAULT)  
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=255)
    video_id = models.CharField(max_length=200)
    video_view = models.PositiveIntegerField(default=0)
    votes = models.PositiveIntegerField(default=0)
    ratings = models.PositiveIntegerField(default=0)
    duration = models.CharField(max_length=150)
    keywords = models.ManyToManyField("Keywords",null=True)
    description = models.TextField()
    featured=models.BooleanField(default=False)
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    is_vimeo=models.BooleanField(default=False)
    vimeo_image = models.CharField(max_length=300,null=True,blank=True)
    published_on = models.DateTimeField(null=True,blank=True)
    audit_log = AuditLog()
    
    def __unicode__(self):
        return self.title
    def get_visits(self):
        return self.video_view
    def get_action_type(self):
        if self.status=='P':return 'update'
        else:return 'delete'
    def get_preview_url(self):
        return reverse('staff_video_home') 
    def get_modified_time(self):
        return self.modified_on
    def get_thumb(self):
        return 'http://i2.ytimg.com/vi/%s/default.jpg'%(self.video_id)
    def get_hq_thumb(self):
        return 'http://i2.ytimg.com/vi/%s/hqdefault.jpg'%(self.video_id)  
    def get_video_hq_image(self):
        if self.is_vimeo:return self.vimeo_image
        else:return 'http://i2.ytimg.com/vi/%s/hqdefault.jpg'%(self.video_id)   
    def get_video_url(self):
        if self.is_vimeo:vp_url = 'http://player.vimeo.com/video/%s'%(self.video_id) 
        else:vp_url =  'http://www.youtube.com/v/%s'%(self.video_id) 
        return vp_url
    def get_comments_count(self):
        return VideoComments.objects.filter(video=self).count()
    def get_comments(self):
        return VideoComments.objects.filter(video=self,status='A').order_by('-id') #-created_on
    def get_total_comments_count(self):
        return VideoComments.objects.filter(video=self).count()
    def get_pending_comments_count(self):
        return VideoComments.objects.filter(video=self,status='N').count()
    def get_rejected_comments_count(self):
        return VideoComments.objects.filter(video=self,status='B').count()
    def get_approved_comments_count(self):
        return VideoComments.objects.filter(video=self,status='A').count()
    def get_absolute_url(self):
        return '/videos/'+self.slug + '.html' #?vid=%d'%(self.id)# Removed gallery from this line  
    
    def get_url(self):
        url = get_global_settings().website_url+'videos/'+self.slug + '.html'
        return url
   
     #Notification
    def get_staff_preview_url(self):
        url = reverse('staff_video_home')
        return url
    def get_staff_listing_url(self):
        url = reverse('staff_video_home')
        return url
    #Notification
    
    def get_search_result_html( self ):
        template = 'search/r_videos.html'
        data = { 'object': self }
        return render_to_string( template, data )
    
    def get_video_status(self):
        if self.status =='P':
            sts = 'active'
        elif self.status =='N':
            sts = 'pending' 
        elif self.status =='B':
            sts = 'blocked' 
        elif self.status =='R':
            sts = 'rejected' 
        else: sts = 'expired' 
        return sts 
    
    def get_embed_video_player(self):
        if self.is_vimeo:append_video_player = '<iframe width="100%" height="450" frameborder="0"  src="http://player.vimeo.com/video/'+self.video_id+'?theme=light&amp;rel=0&amp;autoplay=1" allowfullscreen></iframe>'
        else:append_video_player = '<iframe width="100%" height="450" frameborder="0" src="http://www.youtube.com/embed/'+self.video_id+'?theme=light&amp;rel=0&amp;autoplay=1" allowfullscreen></iframe>'
        return append_video_player
    
    def get_twitter_share_url(self):
        if self.is_vimeo:share_url = 'https://player.vimeo.com/video/%s'%(self.video_id) 
        else:share_url =  'https://www.youtube.com/embed/%s'%(self.video_id) 
        return share_url
    
    def get_fb_share_url(self):
        if self.is_vimeo:vp_url = 'http://vimeo.com/moogaloop.swf?clip_id=%s'%(self.video_id) 
        else:vp_url =  'http://www.youtube.com/v/%s?autohide=1&amp;version=3'%(self.video_id) 
        return vp_url
    
    def get_embed_video_src(self):
        if self.is_vimeo:embed_src = 'http://player.vimeo.com/video/'+self.video_id+'?theme=light&amp;rel=0&amp;autoplay=1'
        else:embed_src = 'http://www.youtube.com/embed/'+self.video_id+'?theme=light&amp;rel=0&amp;autoplay=1'
        return embed_src
    
    class Meta:
        permissions = (("publish_videos", "Can Publish Videos"),)
        
class VideoComments(models.Model):
    video = models.ForeignKey("Videos")
    title = models.CharField(max_length=120)
    name = models.CharField(max_length=60,null=True)
    email = models.EmailField(max_length=300)
    comment = models.TextField()
    abuse_count = models.PositiveIntegerField(default=0)
    like_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=1,default='N')#N=new    B=blocked    A=approved
    approved_on = models.DateTimeField("VC_approvedoncomment", auto_now = True)
    created_by = models.ForeignKey(User, related_name='createdbyvideocomment',null=True)
    created_on  = models.DateTimeField('VC_Created_On', auto_now_add = True)
    
    def get_comments_count(self):
        return VideoComments.objects.filter(video=self).count()
    def get_video_coments(self):
        return VideoComments.objects.filter(video=self,status='A').order_by('-id')
    

    
    

    
    
