from xml.etree import ElementTree 
from urllib2 import urlopen
from meetup.models import Meetup,MeetupSettings
from common.templatetags.ds_utils import get_misc_attribute
from django.http import Http404
#from django.views.decorators.cache import cache_page
from django.core.cache import cache
import datetime
import urllib

def __get_meetup_url():
    try:
        params={}
        ms = MeetupSettings.objects.all()[:1][0]
        params['city']=ms.city
        params['state']=ms.state
        params['country']=ms.country
        params['zip']=ms.zip
        params['key']=ms.api_key
       # params['lat']=ms.lat
       # params['lon']=ms.lon
        params['status']='upcoming'
        url="https://api.meetup.com/2/open_events/?format=xml&"
        aurl=url+urllib.urlencode(params)
        return aurl
    except:
        return None
    
def get_meetup_validate(url):
    tree = ElementTree.parse(urlopen(url))
    rootElem = tree.getroot()
    next = rootElem.findtext("head/next").replace("https://api.meetup.com/2/open_events.xml?",'')
    items = rootElem.findall("items/item")
    return True

def get_all_meetups(category=None):
    from bs4 import BeautifulSoup
    try:
        URL=__get_meetup_url()
        if not URL:return [],None
        target_url=URL
        if category:
            target_url = URL+"&topic=%s" %(category)
            
        tree = ElementTree.parse(urlopen(target_url))
        rootElem = tree.getroot()
        next = rootElem.findtext("head/next").replace("https://api.meetup.com/2/open_events.xml?",'')
        items = rootElem.findall("items/item")
        names = []
        meetups = []
        count =0
        for item  in items:
             m = Meetup()
             m.url = item.findtext("event_url")
             
             photo_url = item.findtext("photo_url")
             if not photo_url:
                 try:
                     soup = BeautifulSoup(item.findtext("description").encode("UTF-8"))
                     imgs = [x.attrs['src'] for x in soup.find_all('img')]
                     photo_url = imgs[0]
                 except:photo_url = ''    
             
             m.photo=photo_url
             #if not m.photo:
             #    continue
             m.name = item.findtext("name")
             if m.name in names:
                 continue
             else:
                names.append(m.name)
                
             venue = item.find("venue")
             
             
             if venue:
                 state=venue.findtext("state")
                 m.state=state
                 m.city=venue.findtext("city")
                 
                 if state:
                     m.venue = venue.findtext("address_1") 
                     meetups.append(m)                   
                     count += 1
                 else:
                     continue
             else:
                  meetups.append(m)
             m.description= item.findtext("description")
             if m.description:
                m.description = m.description.encode("UTF-8")
             e_date= item.findtext("time")
             date = datetime.datetime.fromtimestamp(int(e_date)/1000)
             m.event_date=date+datetime.timedelta(hours=2)
    
             
             m.rsvp= item.findtext("yes_rsvp_count")
             
             group = item.find("group")
           
             if group:
                 m.group_name=group.findtext("name")
                 m.group_url=group.findtext("urlname")
        
        return meetups,next
    except:
        return [],[]

def get_more_meetups(target_url,category):
    from bs4 import BeautifulSoup
    try:
        '''if category:
            target_url = target_url+"&topic=%s" %(category)'''
        
        tree = ElementTree.parse(urlopen(target_url))
        
        rootElem = tree.getroot()
        next = rootElem.findtext("head/next").replace("https://api.meetup.com/2/open_events.xml?",'')
        items = rootElem.findall("items/item")
        names = []
        meetups = []
        count =0
        for item  in items:
             m = Meetup()
             m.url = item.findtext("event_url")
             photo_url = item.findtext("photo_url")
             if not photo_url:
                 try:
                     soup = BeautifulSoup(item.findtext("description").encode("UTF-8"))
                     imgs = [x.attrs['src'] for x in soup.find_all('img')]
                     photo_url = imgs[0]
                 except:photo_url = ''    
             
             m.photo=photo_url
             #if not m.photo:
             #    continue
             m.name = item.findtext("name")
             if m.name in names:
                 continue
             else:
                names.append(m.name)
                
             venue = item.find("venue")
             if venue:
                 state=venue.findtext("state")
                 m.state=state
                 m.city=venue.findtext("city")
                 
                 if state:
                     m.venue = venue.findtext("address_1") 
                     meetups.append(m)                   
                     count += 1
                 else:
                     continue
             else:
                  meetups.append(m)
             m.description= item.findtext("description")
             if m.description:
                m.description = m.description.encode("UTF-8")
             e_date= item.findtext("time")
             date = datetime.datetime.fromtimestamp(int(e_date)/1000)
             m.event_date=date+datetime.timedelta(hours=2)
    
             
             m.rsvp= item.findtext("yes_rsvp_count")
             
             group = item.find("group")
           
             if group:
                 m.group_name=group.findtext("name")
                 m.group_url=group.findtext("urlname")
        
        return meetups,next
    except:
        return [],[]

def get_meetups():
    try:
        URL=get_misc_attribute('MEETUP_API')
    except:
        return []
    if URL:URL_TOPICS=URL+"&topic=%s"
    else:
        return []
    if cache.get('meetups'):
        return cache.get('meetups')
    else:
        tree = ElementTree.parse(urlopen(URL))
        
        rootElem = tree.getroot()
        items = rootElem.findall("items/item")
        names = []
        meetups = []
        count =0
        for item  in items:
             m = Meetup()
             m.url = item.findtext("event_url")
             m.photo=item.findtext("photo_url")
             if not m.photo:
                 continue
             m.name = item.findtext("name")
             if m.name in names:
                 continue
             else:
                names.append(m.name)
            # m.description= item.findtext("description").encode("UTF-8")
             venue = item.find("venue")
             if venue:
                 state=venue.findtext("state")
                 if state:
                     m.venue = venue.findtext("address_1") +" " + state
                     meetups.append(m)
                     count += 1
             if count == 5:
                 break
        cache.set('meetups', meetups, 60*60)
        return meetups