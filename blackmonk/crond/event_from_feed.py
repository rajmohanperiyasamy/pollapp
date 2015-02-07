import getsettings
from django.conf import settings

import datetime,time,urllib
from time import strptime
from datetime import timedelta
import ftplib
import os
from os import path
from xml.dom import minidom
from xml.dom.minidom import Node,parse,parseString

from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.template.defaultfilters import slugify
from common.models import Address as EventVenue
from common.models import VenueType

from events.models import * 
from common.getunique import getUniqueValue
#from events import settings as msg_settings
from common import feedparser

def getText(nodelist):
   rc = ""
   for node in nodelist:
       if node.nodeType == node.TEXT_NODE:
           rc = rc + node.data
   return rc  

#EventFeedPhotos.objects.all().delete()
#EventSchedule.objects.all().delete()

xml_dir='.'
#/home/longisland/webapps/mybangalore/media/xml/events/'

server_name='ftp.cinema-source.com'


"""ftp = ftplib.FTP(server_name)
ftp.login('nylic','1oNi5And')#New
ftp.cwd('events/')
"""
xmls = ['venues.xml', 'perfs.xml', 'events.xml' , 'photos.xml']#New

"""for xml in xmls:
    ftp.retrbinary('RETR ' + xml,open(xml_dir+'%s' %xml,"w").write)
ftp.close()
"""
# path : /home/longisland/webapps/mybangalore/media/xml/events/
venues_xml = open('venues.xml')
perf_xml = open('perfs.xml')
events_xml = open('events.xml')
photos_xml = open('photos.xml')

vendom = parse(venues_xml)
perfdom = parse(perf_xml)
evdom = parse(events_xml)
phdom = parse(photos_xml)

admin = User.objects.get(id=1)
art_and_culture = EventCategory.objects.get(id=32)
education_and_learning = EventCategory.objects.get(id=33)
near_by_nyc = EventCategory.objects.get(id=34)


if evdom != []:
    ''' Adding Event Venues '''
    for vnode in vendom.getElementsByTagName('venue'):
        id = getText(vnode.getElementsByTagName("venue_id")[0].childNodes)
        try:
            venue = EventVenue.objects.get(id=id)
        except:
            venue=EventVenue(id=id)
            
        venue.venue = getText(vnode.getElementsByTagName("venue_name")[0].childNodes)
        
        try:venue.slug = getUniqueValue(EventVenue,slugify(venue.venue),instance_pk=venue.id)
        except:venue.slug = getUniqueValue(EventVenue,slugify(venue.venue))
        
        venue.address1 =  getText(vnode.getElementsByTagName("venue_address")[0].childNodes)
        venue.city = getText(vnode.getElementsByTagName("venue_city")[0].childNodes)
        
        venue.state = getText(vnode.getElementsByTagName("venue_state")[0].childNodes)
        venue.zip = getText(vnode.getElementsByTagName("venue_zip")[0].childNodes)
        #venue.cross_street = getText(vnode.getElementsByTagName("cross_street")[0].childNodes)
        #venue.neighborhood = getText(vnode.getElementsByTagName("venue_neighborhood")[0].childNodes)
        venue.telephone1 = getText(vnode.getElementsByTagName("venue_phone")[0].childNodes)
        #venue.fax = getText(vnode.getElementsByTagName("venue_fax")[0].childNodes)
        venue.email = getText(vnode.getElementsByTagName("venue_email")[0].childNodes)
        venue.website = getText(vnode.getElementsByTagName("venue_website")[0].childNodes)
        #venue.venue_hours = getText(vnode.getElementsByTagName("venue_hours")[0].childNodes)
        #venue.seating = getText(vnode.getElementsByTagName("venue_seating")[0].childNodes)
        #venue.payment = getText(vnode.getElementsByTagName("venue_payment_options")[0].childNodes)
        #venue.parking = getText(vnode.getElementsByTagName("venue_parking")[0].childNodes)
        #venue.parking_desc = getText(vnode.getElementsByTagName("venue_parking_desc")[0].childNodes)
        #venue.accessibility = getText(vnode.getElementsByTagName("venue_accessibility")[0].childNodes)
        #venue.accessibility_desc = getText(vnode.getElementsByTagName("venue_accessibility_desc")[0].childNodes)
        #venue.smoking = getText(vnode.getElementsByTagName("venue_smoking")[0].childNodes)
        #venue.smoking_desc = getText(vnode.getElementsByTagName("venue_smoking_desc")[0].childNodes)
        #venue.age_restriction = getText(vnode.getElementsByTagName("venue_agerestrict")[0].childNodes)
        #venue.age_restriction_desc = getText(vnode.getElementsByTagName("venue_agerestrict_desc")[0].childNodes)
        #venue.alcohol_served = getText(vnode.getElementsByTagName("venue_alcohol")[0].childNodes)
        vt = getText(vnode.getElementsByTagName("venue_type")[0].childNodes)
        try:
            venue_type = VenueType.objects.get(title=getText(vnode.getElementsByTagName("venue_type")[0].childNodes))
        except:
            venue_type = VenueType(title=vt, slug=slugify(vt), seo_title=vt, seo_description=vt)
            venue_type.save()
        venue.type = venue_type
        #venue.venue_area = getText(vnode.getElementsByTagName("venue_area")[0].childNodes)
        try:
            venue.lat = getText(vnode.getElementsByTagName("venue_lat")[0].childNodes)
            venue.lon = getText(vnode.getElementsByTagName("venue_lon")[0].childNodes)
            venue.zoom = 12
        except:
            pass     
        venue.created_by = admin
        venue.modified_by = admin
        venue.save()
    
    ''' Adding Event Performers '''        
    """for pfnode in perfdom.getElementsByTagName('performer'): 
        perfid = getText(pfnode.getElementsByTagName("perf_id")[0].childNodes)
        try:
            performer = Performer.objects.get(id=perfid)
        except:
            performer=Performer(id=perfid)
        performer.name = getText(pfnode.getElementsByTagName("perf_name")[0].childNodes)
        performer.description = getText(pfnode.getElementsByTagName("perf_description")[0].childNodes)
        performer.performer_url = getText(pfnode.getElementsByTagName("perf_website")[0].childNodes)
        #performer.performer_genre = getText(pfnode.getElementsByTagName("perf_genre")[0].childNodes)
        #performer.performer_keywords = getText(pfnode.getElementsByTagName("perf_keywords")[0].childNodes)
        performer.save()"""
        
    ''' Adding Event Informations '''  
    for evntnode in evdom.getElementsByTagName('event'):
        event_id = getText(evntnode.getElementsByTagName("event_id")[0].childNodes)
        
        try:
            event = Event.objects.get(id=event_id)
        except:
            event=Event(id=event_id)
            
        event.is_feed = True
        """try:
            ev_perf=Performer.objects.get(id=getText(evntnode.getElementsByTagName("perf_id")[0].childNodes))
            event.performer = ev_perf
        except:
            pass"""
        try:
            ev_ven=EventVenue.objects.get(id=getText(evntnode.getElementsByTagName("venue_id")[0].childNodes))
            event.event_venue = ev_ven
            event.venue = ev_ven.venue
            event.address1 = ev_ven.address1
            event.address2 = ev_ven.address2
            event.zip = ev_ven.zip
            event.city = ev_ven.city
            #event.name = ev_ven.city
            event.phone = ev_ven.telephone
            event.mobile = ev_ven.mobile
            event.contact_email = ev_ven.email
            event.lat = ev_ven.lat
            event.lon = ev_ven.lon
            event.zoom = 12
        except:
            ev_ven = False
            pass
        if ev_ven:
            event.title = getText(evntnode.getElementsByTagName("event_name")[0].childNodes)     
            event.slug = getUniqueValue(Event,slugify(event.title[:150]))
            event.summary = getText(evntnode.getElementsByTagName("event_desc")[0].childNodes) 
            event.description = getText(evntnode.getElementsByTagName("event_desc")[0].childNodes)
            event.created_by = admin
            event.is_check = True
            event.is_draft = False
            event.update_status = 'P'
            event.tkt_prize = getText(evntnode.getElementsByTagName("prices")[0].childNodes)
            event.ticket_info = getText(evntnode.getElementsByTagName("ticket_info")[0].childNodes)
            event.ticket_sale_date = getText(evntnode.getElementsByTagName("ticket_sale_date")[0].childNodes)
            event.payment_options = getText(evntnode.getElementsByTagName("payment_options")[0].childNodes)
            event.event_showtimes = getText(evntnode.getElementsByTagName("showtimes")[0].childNodes) 
            
            event_cat = getText(evntnode.getElementsByTagName("event_type")[0].childNodes)
            
            if event.event_venue and event.event_venue.venue_area == 'NYC':
                event.categories.add(near_by_nyc)
            elif event_cat == 'Dance':
                event.categories.add(art_and_culture)
            elif event_cat == 'Art':
                event.categories.add(art_and_culture)
            elif slugify(event_cat) == 'talks-readings':
                event.categories.add(education_and_learning)
            else:
                try:
                    evcat=EventCategory.objects.get(type=slugify(event_cat))
                except:
                    evcat=EventCategory(name=event_cat)
                    evcat.slug=getUniqueValue(EventCategory,slugify(event_cat))
                    evcat.type = evcat.slug
                    evcat.save()  
                event.category = evcat         
            """
            if event_cat != 'Dance':
                try:
                    evcat=EventCategory.objects.get(type=slugify(event_cat))
                except:
                    evcat=EventCategory(name=event_cat)
                    evcat.slug=getUniqueValue(EventCategory,slugify(event_cat))
                    evcat.type = evcat.slug
                    evcat.save()   
                event.category = evcat
            else:
                event.category = art_and_culture
            """           
            event.save()
                
            try:
                for nod in evntnode.getElementsByTagName("genres"):
                    for gnod in nod.getElementsByTagName("genre"):
                        newnod=getText(gnod.childNodes)
                        try:
                            evgnre = EventGenre.objects.get(name=newnod)
                        except:
                            evgnre = EventGenre(name=newnod)    
                            evgnre.save()
                        event.genre.add(evgnre)
            except:pass
                
            try:
                shedules = evntnode.getElementsByTagName("schedule")
                for snod in evntnode.getElementsByTagName("schedule"):
                    for idx, tnod in enumerate(snod.getElementsByTagName('performance')):
                        evnt_schdle = EventSchedule(event=event)
                        try:
                            ndate = datetime.datetime.strptime(tnod.getAttribute('date'),"%m/%d/%y")
                            evnt_schdle.date = ndate.date()
                        except:
                            pass    
                        evnt_schdle.time = getText(tnod.childNodes)
                        evnt_schdle.save()
                        if idx==0:
                            event.start_date=ndate.date()
                        if idx==len(evntnode.getElementsByTagName("performance"))-1:
                            event.end_date= ndate.date()
                        #if forloop.first:
                event.save()            
            except:pass
            
    ''' Adding Venue Photos and Performers Photos '''        
    for pnod in phdom.getElementsByTagName('photos'):
        v_id=None
        p_id=None
        for vpnod in pnod.getElementsByTagName('venuephoto'): 
            try:
                id=getText(vpnod.getElementsByTagName("venue_id")[0].childNodes)
                feed_photos=EventFeedPhotos()
                venue=EventVenue.objects.get(id=id)
                feed_photos.venue=venue
                feed_photos.photo = getText(vpnod.getElementsByTagName("photo_file")[0].childNodes)
                feed_photos.photo_caption = getText(vpnod.getElementsByTagName("photo_caption")[0].childNodes)
                feed_photos.photo_res = getText(vpnod.getElementsByTagName("perf_res")[0].childNodes)
                feed_photos.save()
                v_id=venue.id
                       
            except:pass
        
        for ppnod in pnod.getElementsByTagName('perfphoto'):
            try:
                feed_photos=EventFeedPhotos()
                performer=Performer.objects.get(id=getText(ppnod.getElementsByTagName("perf_id")[0].childNodes))
                feed_photos.performer=performer
                feed_photos.photo = getText(ppnod.getElementsByTagName("photo_file")[0].childNodes)
                feed_photos.photo_caption = getText(ppnod.getElementsByTagName("photo_caption")[0].childNodes)
                feed_photos.photo_res = getText(vpnod.getElementsByTagName("perf_res")[0].childNodes)
                feed_photos.save()
                p_id=performer.id
            except:pass
            
else:
    pass
