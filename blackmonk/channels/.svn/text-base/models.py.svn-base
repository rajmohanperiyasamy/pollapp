from django.db import models
from django.core.urlresolvers import reverse

from article.models import ArticleCategory
from business.models import BusinessCategory
from attraction.models import AttractionCategory
from classifieds.models import ClassifiedCategory
from deal.models import DealCategory
from events.models import EventCategory
from gallery.models import PhotoCategory
from videos.models import VideoCategory
from common.models import Basetable
from audit_log.models.managers import AuditLog


class Channel(Basetable):
    title = models.CharField(max_length=100,null=True)
    slug = models.CharField(max_length=100,null=True)
    description = models.TextField(blank=True, null=True)
    seo_title = models.CharField(max_length=70, null=True)
    seo_description = models.CharField(max_length=160, null=True)
    template_name = models.CharField(max_length=100, null=True)
    audit_log = AuditLog()
    
    def __unicode__(self):
        return self.title

    def get_selected_artcatids(self):
        try: return self.articlewidget.categories.values_list('id', flat=True)
        except: return []
    
    def get_selected_bizcatids(self):
        try: return self.businesswidget.categories.values_list('id', flat=True)
        except: return []
    
    def get_selected_evecatids(self):
        try: return self.eventwidget.categories.values_list('id', flat=True)
        except: return []
    
    def get_selected_vidcatids(self):
        try: return self.videowidget.categories.values_list('id', flat=True)
        except: return []
    
    def get_selected_galcatids(self):
        try: return self.gallerywidget.categories.values_list('id', flat=True)
        except: return []
        
    def get_selected_dealcatids(self):
        try: return self.dealwidget.categories.values_list('id', flat=True)
        except: return []
    
    def get_selected_attractioncatids(self):
        try: return self.attractionwidget.categories.values_list('id', flat=True)
        except: return []
    
    def get_absolute_url(self):
        url = reverse('site_home') + self.slug + '/'
        return url    

class ArticleWidget(models.Model):
    channel = models.OneToOneField(Channel)
    categories = models.ManyToManyField(ArticleCategory)

class EventWidget(models.Model):
    channel = models.OneToOneField(Channel)
    categories = models.ManyToManyField(EventCategory)
    
class BusinessWidget(models.Model):
    channel = models.OneToOneField(Channel)
    categories = models.ManyToManyField(BusinessCategory)
    
class GalleryWidget(models.Model):
    channel = models.OneToOneField(Channel)
    categories = models.ManyToManyField(PhotoCategory)

class VideoWidget(models.Model):
    channel = models.OneToOneField(Channel)
    categories = models.ManyToManyField(VideoCategory)
    
class DealWidget(models.Model):
    channel = models.OneToOneField(Channel)
    categories = models.ManyToManyField(DealCategory)
    
class AttractionWidget(models.Model):
    channel = models.OneToOneField(Channel)
    categories = models.ManyToManyField(AttractionCategory)