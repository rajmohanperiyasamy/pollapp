#! /home/blackmonk/virtualenvs/bm/bin/python

import getsettings
from urllib import urlencode, urlopen
from xml.dom import minidom
import hashlib
import os
from datetime import timedelta, datetime,date
from django.contrib.auth import get_user_model
User = get_user_model()
from classifieds.models  import Classifieds,TPClassifiedsImages,TPClassifiedsAttribute,ClassifiedCategory,OodleSettings
from common.utils import get_global_settings
from django.template.defaultfilters import slugify
from common.getunique import *
from django.db import connection
from domains import *
OODLE_BM_DICT={'Single-Family Houses':'Houses for sale','Media, Journalism & Newspaper Jobs':'Writing Jobs',
               'Condos, Townhouses & Apts for Sale':'Apartments & Townhouses for Sale','Media, Journalism & Newspaper Jobs':'Writing Jobs',
               'Health & Beauty Services':'Health and Beauty','Apartments for Rent':'Apartments & Townhouses for Rent',
               } 
def load_data(url):
    _doget(url)
    
       
def _doget(url):
    xml =  minidom.parse(urlopen(url))
    data = unmarshal(xml)
    classfds=[]
    try:
        if data.oodle_response.listings.__dict__.has_key('element'):
            if isinstance(data.oodle_response.listings.element, list):
                for classfd in data.oodle_response.listings.element:
                    classfds.append(_parse_data(classfd))
            else:
                classfds = [_parse_data(data.oodle_response.listings.element)]
    except:
        print "not valid url %s" %(url)
    return classfds
          
def _parse_data(element):
    global_settings = get_global_settings()
    id=element.id.text
    user=User.objects.get(username='admin')
    try:
        clfd=Classifieds.objects.get(tp_id=id)
        return
    except:
        clfd=Classifieds()
    clfd.title=element.title.text
    clfd.description=element.body.text
    clfd.source_url=element.url.text
    clfd.data_src='oodle'
   
    #clfd.latitude=element.location.latitude.text
    #clfd.longitude=element.location.longitude.text
    try:
        cat= element.category.name.text
        try:cat=OODLE_BM_DICT[cat]
        except:pass
        category=ClassifiedCategory.objects.get(name__iexact=cat)
    except:
        print cat
        return
    clfd.category=category
    clfd.created_by=user
    clfd.created_on=datetime.fromtimestamp(int(element.ctime.text))
    clfd.action='S'
    clfd.status='P'
    clfd.listing_start_date=datetime.now()
    clfd.listing_end_date=datetime.now() + timedelta(days = 30)
    clfd.tp_id=element.id.text
    clfd.is_active=True
    clfd.slug=getUniqueValue(Classifieds, slugify(getSlugData(clfd.tp_id)))
    #SEO
    clfd.seo_title= "%s | %s | %s" %(clfd.title,category.name,global_settings.domain)
    clfd.seo_description= clfd.description[:30]
    clfd.tp_save()
    print "%s saved" %(clfd.title)
    #clfd.classifiedsaddress_set.add(addr)
    
    if element.__dict__.has_key('attributes'):
        for attrname,attrval in  element.attributes.__dict__.items():
            if attrname == 'price':
                try:
                    clfd.price=attrval.text
                    clfd.tp_save()
                except:
                    pass
            clsattr= TPClassifiedsAttribute()
            clsattr.attr_name=attrname
            clsattr.attr_val=attrval.text
            clsattr.classified = clfd
            clsattr.save()
            #clfd.tpclassifiedsattribute_set.add(clsattr)    
            
    if element.images.__dict__.has_key('element'):
        for img in  element.images.element:
            clsimg=TPClassifiedsImages()
            clsimg.img_width=img.width.text
            clsimg.img_height=img.height.text
            clsimg.img_alt=img.alt.text
            clsimg.img_size=img.size.text
            clsimg.img_url=img.src.text
            clsimg.classified=clfd
            clsimg.save()
            clfd.tpclassifiedsimages_set.add(clsimg)
    return clfd

   
class Bag: pass

def unmarshal(element):
    rc = Bag()
    if isinstance(element, minidom.Element):
        for key in element.attributes.keys():
            setattr(rc, key, element.attributes[key].value)
            
    childElements = [e for e in element.childNodes \
                     if isinstance(e, minidom.Element)]
    if childElements:
        for child in childElements:
            key = child.tagName
        
            if hasattr(rc, key):
                if type(getattr(rc, key)) <> type([]):
                    setattr(rc, key, [getattr(rc, key)])
                setattr(rc, key, getattr(rc, key) + [unmarshal(child)])
            elif isinstance(child, minidom.Element)and \
                     (child.tagName == 'element'):
                
                setattr(rc,key,[unmarshal(child)])
              
            else:
                setattr(rc, key, unmarshal(child))
    else:
       
        text = "".join([e.data for e in element.childNodes \
                        if isinstance(e, minidom.Text)])
        setattr(rc, 'text', text)
    return rc
OODLE_DICT={'Jobs':'job','Community':'community','Property For Rent':'housing/rent','Real Estate':'housing/sale','Personals':'personals','Merchandise':'sale','Pets':'sale/pet','Tickets':'sale/tickets','Services':'service','Cars & Vehicles':'vehicle'}
OODLE_LIST=['vehicle/car','community/announcements','community/groups',
'housing/rent/apartment','housing/rent/home','housing/sale/home',
'housing/sale/condo','job/hospitality','job/writing','job/fitness',
'job/restaurant','job/domestic_help','sale/pet/dog','sale/pet/cat',
'personals/women_seeking_men','personals/women_seeking_women','personals/men_seeking_women',
'personals/men_seeking_men','sale/health','sale/furniture','sale/appliance','service/care/child',
'service/care/child/babysitter','service/cleaning','service/education/tutor','service/health']
def load_cls_data(oodle_s):
    key = oodle_s.api_key
    radius = oodle_s.radius
    location=oodle_s.location
    citycode=oodle_s.region
    categories=ClassifiedCategory.objects.filter(parent__isnull=True)    
    url_set = []
    for category in OODLE_LIST:
        try:
            api_url='http://api.oodle.com/api/v2/listings?key=%s&radius=%s&location=%s&region=%s&category=%s&num=25'%(key,radius,location, citycode,category)
            url_set.append(api_url)
        except:
            print "Category %s not foound"%(category.name)
   
    for url in url_set:
        print url
        load_data(url)

SCHEMATA_DOMAINS = {
    'yourbondi.com.au': {
        'schema_name': 'yourbondi',
    }
}        
for domain_name in SCHEMATA_DOMAINS:
    connection.set_schemata_domain(domain_name)   
    print domain_name
    print oodle_s.radius
    print oodle_s.location
    print oodle_s.region
    date= datetime.now() + timedelta(days = -29)
    Classifieds.objects.filter(created_on__lte=date).delete()  
    try:oodle_s = OodleSettings.objects.all()[:1][0]
    except:continue
    load_cls_data(oodle_s)

