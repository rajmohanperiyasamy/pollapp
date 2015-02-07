import datetime,time,urllib
from time import strptime
from django.conf import settings as my_settings
from events.models import Event,EventCategory
from events.models import Tag as Etag

from django.core.mail import EmailMessage
from common.utils import get_global_settings
from django.template import  Template,Context
from usermgmt.adminviews import  *
from common.staff_messages import EVENT_MSG

import dateutil
from dateutil.relativedelta import *
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
import commands
from googlemaps import GoogleMaps
from pygeocoder import Geocoder

MNTH = {'0':DAILY,'1':WEEKLY,'2':MONTHLY,'3':YEARLY}
WEEK = {'MO':MO,'TU':TU,'WE':WE,'TH':TH,'FR':FR,'SA':SA,'SU':SU}
MNTH_NM = {'Sunday':SU,'Monday':MO,'Tuesday':TU,'Wednesday':WE,'Thursday':TH,'Friday':FR,'Saturday':SU}

def get_week_no(date):
   d = date.day
   res = d / 7
   if d % 7:
       res += 1
   return res
# def get_venue_map_settings(venue,ven,add1,add2,zip,latt,lon,zoom):
#     globalsettings = get_global_settings()
#     try:
#         try:
#             venue.lat=float(latt)
#             venue.lon=float(lon)
#             venue.zoom=int(zoom)
#         except: 
#             gmaps = GoogleMaps()
#             address = add1+','+add2+','+zip+','+globalsettings.city
#             lat, lng = Geocoder.geocode(address)[0].coordinates
#             venue.lat=lat
#             venue.lon=lng
#             venue.zoom=11
#     except:       
#         venue.lat=globalsettings.google_map_lat
#         venue.lon=globalsettings.google_map_lon
#         venue.zoom=11
#     return venue

def from_eventurl_to_object(eventurl):
    try:
        slug = eventurl.split('/events/')[1].split('.html')[0]
        return Event.objects.get(slug=slug)
    except:
        return False

def co_add_categories(event,categories):
    if event.category:event.category.clear()
    for cid in categories:
        category = EventCategory.objects.get(id=cid)
        event.category.add(category)

def co_add_tags(event,taglist):
    try:taglist=taglist.split(',')
    except:taglist=taglist
    event.tags.clear()
    for nx in taglist:
        nx = nx.strip()
        if nx:
            try:
                objtag = Etag.objects.get(tag = nx)
            except:
                objtag = Etag(tag=nx)
                objtag.save()
            event.tags.add(objtag)

def event_repeat_save(request,event,evnt_rule):
    try:evnt_rule.repeat = request.POST['repeat_store']
    except:pass
    try:evnt_rule.repeat_every = request.POST['repeat_every_store']
    except:pass 
    try:evnt_rule.repeat_on_wk = request.POST['repeat_on_wk_store']
    except:pass 
    try:evnt_rule.repeat_on_mnth = request.POST['repeat_on_mnth_store']
    except:pass
    try:evnt_rule.ends = request.POST['ends_store']
    except:pass 
    try:evnt_rule.ends_occurence = request.POST['ends_occurence_store']
    except:pass
    try: evnt_rule.ends_on = datetime.datetime(*strptime(request.POST['ends_on_store'],"%m/%d/%Y")[0:5])
    except:pass                                    
    
    event.repeat_summary =  request.POST['repeat_summary']
    
    if evnt_rule.repeat:repeat_val= MNTH[evnt_rule.repeat]
    if evnt_rule.repeat_every:
        repeat_every_val = evnt_rule.repeat_every  
    if evnt_rule.ends_occurence:ends_occurence_val = evnt_rule.ends_occurence
    if evnt_rule.ends_on:ends_on_val = evnt_rule.ends_on
    
    if evnt_rule.repeat =='1':
        weak_vls = evnt_rule.repeat_on_wk.split(',')
        weak_v=[]
        for s in weak_vls:weak_v.append(WEEK[s])
        weak_v=tuple(weak_v)    
        if evnt_rule.ends == 'AFT':
            rslt = list(rrule(repeat_val, count=int(ends_occurence_val) ,interval=int(repeat_every_val),byweekday=(weak_v),dtstart=event.start_date))    
        else:
            rslt = list(rrule(repeat_val, interval=int(repeat_every_val),byweekday=(weak_v),dtstart=event.start_date,until=ends_on_val))        
    elif evnt_rule.repeat =='2':
        if evnt_rule.ends == 'AFT':
            if evnt_rule.repeat_on_mnth == 'M':
                
                rslt = list(rrule(repeat_val, count=int(ends_occurence_val) ,interval=int(repeat_every_val),dtstart=event.start_date))    
            else:
                wknme = MNTH_NM[event.start_date.strftime("%A")]
                rslt = list(rrule(repeat_val, count=int(ends_occurence_val),bysetpos=get_week_no(event.start_date),byweekday=(wknme),interval=int(repeat_every_val),dtstart=event.start_date)) 
        else:
            if evnt_rule.repeat_on_mnth == 'M':
                rslt = list(rrule(repeat_val, interval=int(repeat_every_val),dtstart=event.start_date,until=ends_on_val))        
            else:
                wknme = MNTH_NM[event.start_date.strftime("%A")]
                rslt = list(rrule(repeat_val, interval=int(repeat_every_val),bysetpos=get_week_no(event.start_date),byweekday=(wknme),dtstart=event.start_date,until=ends_on_val))  
    else:
        if evnt_rule.ends == 'AFT':
            rslt = list(rrule(repeat_val, count=int(ends_occurence_val) ,interval=int(repeat_every_val),dtstart=event.start_date))    
        else:
            rslt = list(rrule(repeat_val, interval=int(repeat_every_val),dtstart=event.start_date,until=ends_on_val))        
     
    return evnt_rule,rslt,event
     


def publish_event_mail(event):
    global_settings=get_global_settings()
    try:
        if event.listing_type =='F':
            type = "featured"
        elif event.listing_type =='S':
            type = "sponsored"
        else:
            type = "free"     
        to_emailids = [event.created_by.email]
        email_temp = EmailTemplates.objects.get(code='epe')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": event.created_by.display_name,"EVENT_TITLE": event.title,"EVENT_TYPE": type,
                    "EVENT_URL": event.get_absolute_url(),"WEBSITE": global_settings.domain,"ADD_URL":global_settings.website_url+'/events/addevent/'})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass

"""    
def upgrade_event_mail(event):
    try:
        if event.listing_type =='F':
            type = "featured"
        elif event.listing_type =='S':
            type = "sponsored"
        else:
            type = "free"     
        to_emailids = [event.created_by.email]
        email_temp = EmailTemplates.objects.get(code='eue')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": event.created_by.display_name,"EVENT_TITLE": event.title,"EVENT_TYPE": type,
                    "EVENT_URL": event.get_absolute_url(),"WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass
        
def reject_event_mail(event):
    try:
        if event.listing_type =='F':
            type = "featured"
        elif event.listing_type =='S':
            type = "sponsored"
        else:
            type = "free"     
        to_emailids = [event.created_by.email]
        email_temp = EmailTemplates.objects.get(code='ere')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": event.created_by.display_name,"EVENT_TITLE": event.title,"EVENT_TYPE": type,
                    "EVENT_URL": event.get_absolute_url(),"WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass    

"""
