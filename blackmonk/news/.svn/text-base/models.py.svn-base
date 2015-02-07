from django.db import models
from common.models import Basetable
from common.utils import get_global_settings


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    
    def __unicode__(self):
        return self.name
    
    def get_active_count(self):
        return News.objects.filter(category=self,is_active=True).count()
    def get_expired_count(self):
        return News.objects.filter(category=self,is_active=False).count()

        
class Provider(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=260)
    is_active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name
    def news_count(self):
        return News.objects.filter(provider=self).count()
    
    
class News(Basetable):
    title = models.CharField(max_length=450)
    category = models.ForeignKey("Category")
    provider = models.ForeignKey("Provider")
    url = models.URLField(max_length=800,null=True)
    image_url = models.URLField(max_length=800,null=True)
    summary = models.TextField(null=True)
    seo_title = models.CharField(max_length=600,null=True)
    seo_description = models.CharField(max_length=800,null=True)
    slug = models.SlugField(max_length=255)
    is_feed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.title
    def get_absolute_url(self):
        global_settings = get_global_settings()
        url = global_settings.website_url+'/news/'
        url = url +self.slug+'.html'
        return url
    def get_sitemap_url(self):
        url = '/news/' + self.slug + '.html'
        return url
    def can_delete_news(self,user):
        if user.is_superuser:
            return True
        elif user.has_perm('news.delete_news'):
            return True
        else:
            return False
    
    def can_manage_status(self,user):
        if user.is_superuser:
            return True
        elif user.has_perm('news.can_manage_status'):
            return True
        else:
            return False
    
    class Meta:
        permissions = (
            ("can_manage_status", "Can Manage News Status"),
            )

