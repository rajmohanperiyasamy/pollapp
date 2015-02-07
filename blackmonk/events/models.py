import datetime
from time import strptime

from django.db import models
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.translation import ugettext as _
from gallery.models import PhotoAlbum
from common.models import Basetable,Address
from common.utils import getCoverPhoto
from audit_log.models.managers import AuditLog
from django.contrib.contenttypes.models import ContentType

import uuid
import os
from django.conf import settings
User = settings.AUTH_USER_MODEL

def get_eventlogo_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('event/logo', filename)
def get_eventgallery_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('event/images', filename)

class Tag(models.Model):
    tag = models.CharField(max_length=150)  
    def __unicode__(self):
        return self.tag

# TABLE: EVENTS
class Event(Basetable):
    title = models.CharField(max_length=150)
    event_description = models.TextField()
    image = ThumbnailerImageField(upload_to=get_eventlogo_path, resize_source=dict(size=(700, 0), crop='smart'),)
    category = models.ManyToManyField("EventCategory")
    venue = models.ForeignKey(Address,null=True)
    slug = models.CharField(max_length=150)
    
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(max_length=25, null=True)
    end_time = models.TimeField(max_length=25, null=True)
    is_reoccuring = models.BooleanField(default=False)
    repeat_summary = models.CharField(max_length=400, null=True)
    rule = models.ForeignKey("EventRule",null=True,on_delete=models.SET_NULL)
    
    tkt_prize = models.CharField(max_length=350, null=True, default='0')
    ticket_site = models.URLField(null=True) #changed
    tkt_phone = models.CharField(max_length=40, null=True, blank=True)
    
    event_website = models.URLField(null=True)
    facebook = models.URLField(null=True,)
    googleplus = models.URLField(null=True)
    
    visits = models.IntegerField(default=0)
    visitors = models.IntegerField(default=0)    # For I_M_GOING
    
    contact_email = models.EmailField(null=True)
    phone = models.CharField(max_length=40, null=True, blank=True)
    mobile = models.CharField(max_length=40, null=True, blank=True)
    
    
    tdate = models.DateField(null=True)
    tags = models.ManyToManyField(Tag, null=True)
    forder = models.IntegerField(default=1)
    
    album = models.ForeignKey(PhotoAlbum, blank=True, null=True, on_delete=models.SET_NULL)
    seo_title = models.CharField(max_length=200, null=True)
    seo_description = models.CharField(max_length=400, null=True)
    
    members = models.ManyToManyField(User,null=True,blank=True,through='EventRsvp')
    
    # Payment and listing properties
    listing_type = models.CharField(max_length=1, null=True, blank=True) # F= Featured , S = Sponsored, B = Basic
    payment = models.ForeignKey("EventPrice", null=True, blank=True)
    listing_start = models.DateField(null=True) # Featured or Sponsored Start Date
    listing_end = models.DateField(null=True) # Featured or Sponsored End Date
    listing_duration = models.CharField(max_length=30, null=True)
    listing_price = models.CharField(max_length=10, null=True)
    is_paid = models.BooleanField(default = False)
    audit_log = AuditLog()
    
    def __unicode__(self):
        return self.title
     
    def get_visits(self):
        return self.visits
    
    def get_action_type(self):
        if self.status=='P':return 'update'
        else:return 'delete'
        
    def get_offline_payment_object(self):
        ctype = ContentType.objects.get_for_model(self)
        try:
            from payments.models import OfflinePayment
            payobj = OfflinePayment.objects.filter(
                content_type=ctype,
                object_id=self.id,
            ).order_by('-posted_date')[0]
            return payobj
        except:
            return False
        
    def get_preview_url(self):
        return reverse('staff_events_preview', args=[self.id])
     
    def get_modified_time(self):
        return self.modified_on
    
    def get_absolute_url(self):
        url = '/events/' + self.slug + '.html'
        return url
    
    def get_staff_url(self):
        url = '/staff/events/' + self.slug + '.html'
        return url
    
    def is_featured_sponsored(self):
        today = datetime.date.today()
        if self.listing_type == 'S': return 'S'
        elif self.listing_type == 'F' and self.listing_end >= today: return 'F'
        else: return 'B'
    
    #Notification
    def get_staff_preview_url(self):
        url = reverse('staff_events_preview',args=[self.id])
        return url
    def get_staff_listing_url(self):
        url = reverse('staff_event_home')
        return url
    #Notification
    
    def get_current_date(self):
        today = datetime.datetime.now().date()
        if self.is_reoccuring:
            occ_objs = EventOccurence.objects.filter(event=self).order_by('id')
            for occ_obj in occ_objs:
                if occ_obj.date >= today:
                    return occ_obj.date
            return self.start_date 
        
    def get_first_event_photo(self):
        return self.get_cover_image()
        
    def get_photo_gallery(self):
        if self.album:
            return self.album.get_gallery_uploaded_images()
        else:return False
    
    def get_first_photo_gallery(self):
        return self.get_cover_image()
        
    def get_cover_image(self):
        photo = getCoverPhoto(self)
        if photo:
            return photo.photo
        else:
            if self.album:
                return self.album.get_cover_image()
            else:
                return False
        
    def get_default_image(self):
        return settings.STATIC_URL+"ui/images/global/img-none.png"        
    
    def can_delete_event(self, user):
        if user.is_superuser:
            return True
        elif user.has_perm('events.delete_event'):
            return True
        elif self.is_check == True and self.created_by == user and user.has_perm('events.can_delete_published'):
            return True
        elif self.created_by == user and self.is_check == False and user.has_perm('events.can_delete_owned'):
            return True
        else:
            return False
     
    def can_change_event(self, user):
        if user.is_superuser:
            return True
        elif user.has_perm('events.change_event'):
            return True
        elif self.is_check == True and self.created_by == user and user.has_perm('events.can_change_published'):
            return True
        elif self.created_by == user and self.is_check == False and user.has_perm('events.can_change_owned'):
            return True
        else:
            return False    
    
    def get_lat_lang(self):
        venue = Address.objects.get(pk=self.venue_id)
        data = {}
        if venue.lat: data['lat']= venue.lat
        else:data['lat']=None
        if venue.lon:data['lon']= venue.lon
        else:data['lon']=None
        if venue.venue:data['venue']= venue.venue
        else:data['venue']="Calagary"       
        return data
    
    def can_manage_status(self, user):
        if user.is_superuser:
            return True
        elif user.has_perm('events.can_manage_status'):
            return True
        else:
            return False
        
    def can_manage_featured(self, user):
        if user.is_superuser:
            return True
        elif user.has_perm('events.can_manage_featured'):
            return True
        else:
            return False
    
    def check_occured(self):
        endDate = datetime.datetime(*strptime(str(self.end_date), "%Y-%m-%d")[0:5])
        today = datetime.datetime.now()
        result = endDate - today
        if (result.days < -1):
            return True
        return False
    
    def gettags(self):
         return self.tags.all()
    def get_event_total_count(self):
        return Event.objects.filter(~Q(status='D')).count()
   
    def get_search_result_html(self):
        template = 'search/r_events.html'
        data = { 'object': self }
        return render_to_string(template, data)
    
    def get_scheduled_days(self):
        return EventScheduleDay.objects.filter(event=self)
    
    def get_payment_photo(self):
        return self.get_cover_image()
        
    def get_payment_title(self):
        return self.title   
    
    def get_payment_description(self):
        if self.event_description:
            return self.event_description
        else:
            return self.title

    def get_payment_duration_type(self):
        return "Day"  
    def get_payment_listing_type(self):
        return self.payment.level_label   
    def get_payment_listing_price(self):
        return self.listing_price
    def get_payment_listing_duration(self):
        return self.listing_duration
    def get_payment_listing_start_date(self):
        return self.listing_start
    def get_payment_listing_end_date(self):
        return self.listing_end
     # Payment confirmation page info ends
     
    def get_rsvp_maybe_count(self):
        return EventRsvp.objects.filter(event=self,status='M').count()
    
    def get_rsvp_going_count(self):
        return EventRsvp.objects.filter(event=self,status='Y').count() 
    
    def event_iso_start_datetime(self):
        start = self.start_date
        try:start = datetime.datetime.combine(self.start_date,self.start_time)
        except:pass
        return start.isoformat()
    
    def event_iso_end_datetime(self):
        end = self.end_date
        try:end = datetime.datetime.combine(self.end_date, self.end_time)
        except:pass
        return end.isoformat()
    
    class Meta:
        permissions = (("publish_events", "Can Publish Events"),("promote_events", "Can Promote Events"),)

# TABLE: CATEGORY
class EventCategory(models.Model):
    name = models.CharField(max_length=50)
    #keyword = models.CharField(max_length=25,null=True,blank=True)
    slug = models.SlugField()
    seo_title = models.CharField(max_length=200, null=True)
    seo_description = models.CharField(max_length=400, null=True)
    def __unicode__(self):
         return self.name
   
    def get_absolute_url(self):
        return '/events/%s/' % (self.slug)
    def get_category_count(self):
        return Event.objects.filter(category__id=self.id, status='P').count()
    def get_event_count(self):
        return Event.objects.filter(category__id=self.id).count()
    def get_free_category_count(self):
        return Event.objects.filter(category__id=self.id, status='P', tkt_prize='FREE').count()
    def get_modules(self):
        return self.module.all()
    @classmethod
    def get_half_count(cls): # Used for Event Alerts To split cat in 2 columns
        #return int(round(EventCategory.objects.all().count()/2.0))
        return 8
    
    def get_expired_count(self):
        today = datetime.datetime.now()
        count = Event.objects.filter(category__id=self.id, is_draft=False, end_date__lt=today).count()
        return count

#class EventPhoto(models.Model):    
#    event = models.ForeignKey("Event",null=True,related_name="eventphotos")
#    title = models.CharField(max_length=200, null=True)
#    photo = ThumbnailerImageField(upload_to=get_eventgallery_path, resize_source=dict(size=(700, 0), crop='smart'),)
#    uploaded_on = models.DateTimeField('createdoneventphoto', auto_now_add=True)
#    uploaded_by = models.ForeignKey(User)
#    
#    def get_delete_url(self):
#        return reverse('events_ajax_delete_photos', args=[self.id])
        
# Report Problem
class EventReport(models.Model):
    report = models.CharField(max_length=1)#Offensive=O Spam=S oldEvent=E 
    report_by = models.ForeignKey(User)
    event = models.ForeignKey("Event")

class EventRule(models.Model):
    repeat = models.CharField(max_length=2, null=True)
    repeat_every = models.CharField(max_length=2, null=True)
    repeat_on_wk = models.CharField(max_length=500, null=True)
    repeat_on_mnth = models.CharField(max_length=2, null=True)
    ends = models.CharField(max_length=6, null=True)
    ends_occurence = models.CharField(max_length=5, null=True)
    ends_on = models.DateField(null=True)

class EventOccurence(models.Model):
    event = models.ForeignKey('Event',null=True)
    date = models.DateField(max_length=20, null=True)
    
class EventPrice(models.Model):
    level = models.CharField(max_length=10, null=True)
    level_visibility = models.BooleanField(default=True)
    level_label = models.CharField(max_length=50, null=True)   
    is_paid = models.BooleanField(default=True)
    exposure = models.CharField(max_length=2, null=True)
    images = models.CharField(max_length=1, null=True) #Y=yes N=No E=None
    ticket_info = models.CharField(max_length=1, null=True) #Y=yes N=No E=None
    comments = models.CharField(max_length=1, null=True) #Y=yes N=No E=None
    share_buttons = models.CharField(max_length=1, null=True) #Y=yes N=No E=None
    sms = models.CharField(max_length=1, null=True) #Y=yes N=No E=None
    social_media = models.CharField(max_length=1, null=True)#F=Facebook T=Twitter B=Both N=No
    newsletter = models.CharField(max_length=1, null=True)#Y=yes N=No E=None
    price = models.FloatField(default=0.0)
    
    def get_exposure(self):
        if self.exposure=='1':return _('1X') 
        elif self.exposure=='2':return _('5X') 
        elif self.exposure=='3':return _('10X') 
        elif self.exposure=='4':return _('15X') 
        elif self.exposure=='5':return _('20X')
        elif self.exposure=='6':return _('25X')
        else:return _('Standard')
    
class EventRsvp(models.Model):
    event = models.ForeignKey('Event')
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,default='N')
    past_status = models.CharField(max_length=2,default='DG')
    notes = models.CharField(max_length=100,null=True,blank=True)
