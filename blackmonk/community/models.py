from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
from common.utils import get_global_settings
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.conf import settings
from common.models import Basetable
from audit_log.models.managers import AuditLog
from bs4 import BeautifulSoup
User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    tag = models.CharField(max_length=150)  

class Topic(models.Model):
    name = models.CharField(max_length=150,unique=True)
    slug = models.CharField(max_length=200,null=True)
    seo_title = models.CharField(max_length=70,null=True)
    seo_description = models.CharField(max_length=160,null=True)
    subscriber = models.ManyToManyField(User,null=True,blank=True)
    
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('community_listing',args=[self.slug])
    
def get_default_topic():
    return Topic.objects.get_or_create(name="Uncategorized", slug='uncategorized')[0]


class Entry(Basetable):
    topic = models.ForeignKey("Topic",default=get_default_topic, on_delete=models.SET_DEFAULT)
    entry_type = models.CharField(max_length=1)# 'Q'=question, 'P'=post, 'A' =Answer
    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=160)
    content = models.TextField(null=True)
    tags = models.ManyToManyField("Tag",null=True)
    is_featured =  models.BooleanField(default=False) 
    rateplus = models.PositiveIntegerField(default=0)
    rateminus = models.PositiveIntegerField(default=0)
    spam = models.PositiveIntegerField(default=0)
    viewed = models.PositiveIntegerField(default=0)
    question = models.ForeignKey("Entry",null=True,blank=True,related_name="question_answer")
    subscriber = models.ManyToManyField(User,null=True,blank=True,related_name="subscriber_list")
    
    def __unicode__(self):
        return self.title if self.title else ""
    
    def get_absolute_url(self):
        if not self.entry_type == 'A':
            return '/community/'+self.topic.slug+'/'+self.slug+'.html'
        else:
            return '/community/'+self.topic.slug+'/'+self.question.slug+'.html'
    
    def get_preview_url(self):
        if not self.entry_type == 'A':
            return '/community/'+self.topic.slug+'/'+self.slug+'.html'
        else:
            return '/community/'+self.topic.slug+'/'+self.question.slug+'.html'

    def get_modified_time(self):
        return self.created_on
    
    def get_answer_count(self):
        answer_count = Entry.objects.filter(entry_type='A',question__id=self.id).count()
        return answer_count
    
    def check_answer_latest(self):
        entry = Entry.objects.filter(entry_type='A',question__id=self.id)
        answer = entry.latest('created_on')
        if self.id == answer.id:
            return True
        else:
            return False
        
    def get_entry_date(self):
        today = timezone.now()
        week = today-timedelta(7)
        if self.created_on.date() == today.date():
            res = today - self.created_on
            hours = res.seconds / (3600)
            rem_seconds = res.seconds - (hours * 3600)
            minutes = rem_seconds / (60)
            if hours < 1:
                return str(minutes)+"m ago"
            else:
                return str(hours)+"h ago"
        elif self.created_on.date()>week.date():
            return self.created_on.strftime('%a')
        else:
            return self.created_on.strftime('%d %b')


    def get_search_result_html( self ):
        template = 'search/r_community.html'
        data = { 'object': self }
        return render_to_string( template, data )

    def get_autoescaped_content(self):
        return BeautifulSoup(self.content).getText()




