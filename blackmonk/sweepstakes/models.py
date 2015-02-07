import uuid
import os

from django.db import models

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from common.models import Basetable,Pages,AvailableApps
from easy_thumbnails.fields import ThumbnailerImageField
from django.conf import settings
User = settings.AUTH_USER_MODEL

WEEK_DIST={'SU':'Sunday','MO':'Monday','TU':'Tuesday','WE':'Wednesday','TH':'Thursday','FR':'Friday','SA':'Saturday'}

def get_sweepstakes_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('sweepstakes', filename)

class SweepstakesSettings(models.Model):
    email = models.CharField(max_length=150)
    
    def __unicode__(self):
       return self.email
   
class SweepstakesQandA(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(null=True)
    position = models.IntegerField(default=1,null=True)
    
    def __unicode__(self):
       return self.title

class SweepstakesImages(models.Model):
    image = ThumbnailerImageField(upload_to=get_sweepstakes_path, resize_source=dict(size=(700, 0), crop='smart'),)
    uploaded_on = models.DateTimeField('createdonbusinesslogo', auto_now_add=True)
    uploaded_by=models.ForeignKey(User,null=True)
    
    def get_delete_url(self):
        return reverse('staff_sweepstakes_ajax_delete_photos', args=[self.id])
    
    def __unicode__(self):
        return _('SweepstakesImage')

    
class Sweepstakes(Basetable):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)
    description = models.TextField()
    image = models.ForeignKey("SweepstakesImages", related_name='sweepstakesimage')
    duration = models.CharField(max_length=1, default='W')  # W:Weekly    M:Monthly
    start_date = models.DateTimeField("sweepstakesstart",null=True)
    end_date = models.DateTimeField("sweepstakesend",null=True)
    current_end_date = models.DateTimeField("currentsweepstakesend",null=True)
    winner = models.ManyToManyField("SweepstakesParticipant", related_name='sweepstakeswinner',null=True)
    sweepstakes_id = models.CharField(max_length=20)
    contest_id = models.CharField(max_length=20)
    total_winners = models.IntegerField(default=1)
    select_winners_on = models.CharField(max_length=10,null=True)
    seo_title = models.CharField(max_length=200,null=True)
    seo_description = models.CharField(max_length=400,null=True)
    settings = models.ManyToManyField(AvailableApps, through='SweepstakesPoints')
    
    reg_point = models.PositiveIntegerField(default=0,null=True)
    fb_point = models.PositiveIntegerField(default=0,null=True)
    friend_point = models.PositiveIntegerField(default=0,null=True)
    comments = models.PositiveIntegerField(default=0,null=True)
    advice_e = models.PositiveIntegerField(default=0,null=True)
    discussions_e = models.PositiveIntegerField(default=0,null=True)
    static_page=models.ForeignKey(Pages,null=True)
    
    def __unicode__(self):
       return self.title
    def get_cover_image(self):
       try:return self.image.image
       except:return False
    def get_duration_text(self):
        if self.duration=='W':
            return _("Every week on ")+WEEK_DIST[self.select_winners_on]
        elif self.duration=='M':
            try:
                select_winners_on=int(self.select_winners_on)
                text=str(select_winners_on)+" th"
                if select_winners_on not in [1,2,3]:text=str(select_winners_on)+" th"
                elif select_winners_on==1:text=str(select_winners_on)+" st"
                elif select_winners_on==2:text=str(select_winners_on)+" nd"
                elif select_winners_on==3:text=str(select_winners_on)+" rd"
                return _("Every month on ")+ text
            except:return None
        else:
            return None
    def get_absolute_url(self):
        return '/'#'/attractions/'+self.slug+'.html'
    
    def get_status(self):
        if self.status =='P':
            sts = 'published'
        elif self.status =='N':
            sts = 'pending' 
        elif self.status =='B':
            sts = 'blocked'
        elif self.status =='E':
            sts = 'expired' 
        else: sts = 'blocked' 
        return sts   
    
    def get_participant(self):
        return SweepstakesParticipant.objects.filter(sweepstakes=self)
    def get_participant_count(self):
        return SweepstakesParticipant.objects.filter(sweepstakes=self).count()
    def get_offers(self):
       return SweepstakesOffers.objects.filter(sweepstakes=self)    
   
class SweepstakesPoints(models.Model):
    app = models.ForeignKey(AvailableApps)
    sweepstake = models.ForeignKey(Sweepstakes)
    app_point = models.PositiveIntegerField(default=0)
    
    def get_points(self,user,mobj):
        c_type = ContentType.objects.filter(model=mobj)
        points=SweepstakesParticipantPoints.objects.filter(sweepstakes=self.sweepstake,sweepstakes__participant=user,content_type__in=c_type).aggregate(models.Sum('user_point'))
        return points['user_point__sum']
    
    
class SweepstakesOffers(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(null=True)
    description = models.TextField()
    image = models.ForeignKey("SweepstakesImages", related_name='sweepstakesofferimage',null=True)
    sweepstakes = models.ForeignKey("Sweepstakes", related_name='sweepstakesoffer')
    
    def __unicode__(self):
       return self.title

class SweepstakesParticipant(models.Model):
    sweepstakes = models.ForeignKey("Sweepstakes", related_name='sweepstakesname')
    participant = models.ForeignKey(User)
    status = models.CharField(max_length=1,default='A')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=400)
    zip = models.CharField(max_length=16,null=True)
    phone = models.CharField(max_length=25,null=True)
    city = models.CharField(max_length=80,null=True)
    
    reg_point = models.PositiveIntegerField(default=0,null=True)
    fb_point = models.PositiveIntegerField(default=0,null=True)
    friend_point = models.PositiveIntegerField(default=0,null=True)
    comments = models.PositiveIntegerField(default=0,null=True)
    total = models.IntegerField(default=0,null=True)
    
    def __unicode__(self):
       return str(self.first_name)+str(self.last_name)  
   
class SweepstakesParticipantPoints(models.Model):
    sweepstakes = models.ForeignKey("SweepstakesParticipant", related_name='sweepstakesparticipant')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    user_point = models.PositiveIntegerField(default=0,null=True)
    
    def __unicode__(self):
       return self.action

from sweepstakes.signals import * 
