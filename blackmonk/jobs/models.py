from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL
from common.models import Basetable

class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=100)
    seo_title = models.CharField(max_length=100)
    seo_description = models.CharField(max_length=400)
    slug = models.SlugField(max_length=150)

    def __unicode__(self):
        return self.name
    def get_jobs(self):
        return JobDetail.objects.filter(category=self)
    def get_absolute_url(self):
        return '/jobs/search/?skw=%s&lkw='%self.slug

class JobTitle(models.Model):
    title = models.CharField(max_length=200)
    count = models.PositiveIntegerField(default=0)
    def __unicode__(self):
        return self.title
    def get_jobs(self):
        return JobDetail.objects.filter(title=self)

class JobCompany(models.Model):
    company = models.CharField(max_length=100)
    count = models.PositiveIntegerField(default=0)
    def get_jobs(self):
        return JobDetail.objects.filter(company=self)
    
class JobDetail(Basetable):
    title = models.ForeignKey("JobTitle" , null=True)
    category = models.ForeignKey("JobCategory" , null=True)
    company = models.ForeignKey("JobCompany" , null=True)
    source = models.CharField(max_length=100)
    source_url = models.CharField(max_length=400)
    detail = models.CharField(max_length=600)
    location = models.CharField(max_length=70)
    type = models.CharField(max_length=50)
    active_on = models.DateTimeField(null=True)
    seo_title = models.CharField(max_length=100)
    seo_description = models.CharField(max_length=400)
    slug = models.SlugField(max_length=255)
    def get_absolute_url(self):
        return self.source_url
                            

class JobSettings(models.Model):
    jurl = models.CharField(max_length=300)
    jbd = models.CharField(max_length=200)
    pshid = models.CharField(max_length=50)
    ssty = models.CharField(max_length=10)
    cflg = models.CharField(max_length=10)
    location = models.CharField(max_length=100,null=True,blank=True)
    post_buttonurl = models.CharField(max_length=500,null=True,blank=True)      
    miles = models.FloatField(null=True, blank=True)
    
    def __unicode__(self):
        return self.jbd                      
