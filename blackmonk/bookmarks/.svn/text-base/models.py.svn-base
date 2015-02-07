from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
User = settings.AUTH_USER_MODEL

class BookmarkCategory(models.Model):
    name = models.CharField(max_length=150)
    slug = models.CharField(max_length=200, null=True)
    seo_title = models.CharField(max_length=200, null=True)
    seo_description = models.CharField(max_length=400, null=True)
    def __unicode__(self):
        return self.name
    
  
class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=250)
    summary = models.TextField(null=True)
    source_url = models.URLField(null=True)
    status = models.CharField(max_length=1, default='N')
    featured = models.BooleanField(default=False)
    category = models.ForeignKey("BookmarkCategory")
    most_viewed = models.PositiveIntegerField(default=0)
    published_on = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='createdbybookmark')
    created_on = models.DateTimeField('Createdonbookmark', auto_now_add=True)
    modified_by = models.ForeignKey(User, related_name='modifiedbybookmark')
    modified_on = models.DateTimeField("modifiedonbookmark", auto_now=True)
    image_url = models.URLField(null=True)
    seo_title = models.CharField(max_length=200, null=True)
    seo_description = models.CharField(max_length=400, null=True)
    
    def __unicode__(self):
        return self.title
    
    def get_visits(self):
        return self.most_viewed
    
    def get_preview_url(self):
        return reverse('staff_bookmark_preview')+"?id="+str(self.id) 
    
    def get_absolute_url(self):
        return reverse("bookmark_details", args=[self.slug, '.html'])
    
    def get_default_image(self):
        return settings.STATIC_URL+"ui/images/global/img-none.png" 
    
    def get_modified_time(self):
        return self.modified_on
    
    def get_staff_preview_url(self):
        url = reverse('staff_bookmark_preview')+"?id="+str(self.id)
        return url
    
    class META:
        permissions = (("publish_bookmark", "Can Publish Bookmark"),)
    
