from classifieds.models import Classifieds,ClassifiedCategory,ClassifiedAttribute,ClassifiedAttributevalue,Tag
from classifieds.models import ClassifiedReport,ClassifiedPrice,Address
import datetime
from time import strptime
from common.getunique import getUniqueValue,getSlugData
from django.template.defaultfilters import slugify
from django.core.mail import EmailMessage
from common.utils import get_global_settings,get_lat_lng
from django.template import  Template,Context
from googlemaps import GoogleMaps
from pygeocoder import Geocoder
#from usermgmt.adminviews import  *

"""

def publish_classified_mail(classified):
    try:
        global_settings=get_global_settings()
        if classified.listing_type =='F':
            type = "featured"
        elif classified.listing_type =='S':
            classified = "sponsored"
        else:
            type = "free"     
        to_emailids = [classified.created_by.email]
        email_temp = EmailTemplates.objects.get(code='cpc')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": classified.created_by.display_name,"CLASSIFIED_TITLE": classified.title,"CLASSIFIED_TYPE": type,
                    "CLASSIFIED_URL": classified.get_absolute_url(),"WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass
    
def reject_classified_mail(classified):
    try:
        global_settings=get_global_settings()
        if classified.listing_type =='F':
            type = "featured"
        elif classified.listing_type =='S':
            classified = "sponsored"
        else:
            type = "free"     
        to_emailids = [classified.created_by.email]
        email_temp = EmailTemplates.objects.get(code='crc')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": classified.created_by.display_name,"CLASSIFIED_TITLE": classified.title,"CLASSIFIED_TYPE": type,
                    "CLASSIFIED_URL": classified.get_absolute_url(),"WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass    

def expire_classified_mail(classified):
    try:
        global_settings=get_global_settings()
        if classified.listing_type =='F':
            type = "featured"
        elif classified.listing_type =='S':
            classified = "sponsored"
        else:
            type = "free"     
        to_emailids = [classified.created_by.email]
        email_temp = EmailTemplates.objects.get(code='cec')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": classified.created_by.display_name,"CLASSIFIED_TITLE": classified.title,"CLASSIFIED_TYPE": type,
                    "RENEW_URL": classified.get_absolute_url(),"WEBSITE": global_settings.domain,"ADD_URL":global_settings.website_url+'/classifieds/dashboard/addclassified_details/'})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass 

def set_comment_session(request,comment,v):        
    if v == 'comment':
        flag = 'clascommentlike'
        try:
            if request.session['%s%s'%(flag,comment.id)] != comment.id:
                request.session['%s%s'%(flag,comment.id)] = comment.id
                comment.like_count = comment.like_count + 1
                comment.save()
                return True
            else:
                return False
        except:
            request.session['%s%s'%(flag,comment.id)] = comment.id 
            comment.like_count = comment.like_count + 1
            comment.save()
            return True
    elif v == 'abuse':
        flag = 'clascommentabuse'
        try:
            if request.session['%s%s'%(flag,comment.id)] != comment.id:
                request.session['%s%s'%(flag,comment.id)] = comment.id
                comment.abuse_count = comment.abuse_count + 1
                comment.save()
                return True
            else:
                return False
        except:
            request.session['%s%s'%(flag,comment.id)] = comment.id 
            comment.abuse_count = comment.abuse_count + 1
            comment.save()
            return True
"""

def get_classified_map_settings(add,latt,lon,zoom):
    globalsettings = get_global_settings()
    try:
        try:
            add.lat=float(latt)
            add.lon=float(lon)
            add.zoom=int(zoom)
        except:
            gmaps = GoogleMaps()
            address = add.address1+','+add.address2+','+add.zip+','+add.city
            lat, lng = Geocoder.geocode(address)[0].coordinates
            add.lat=lat
            add.lon=lng
            add.zoom=11
    except:
        add.lat=globalsettings.google_map_lat
        add.lon=globalsettings.google_map_lon
        add.zoom=11
    return add


def save_classified_address(request, address, form):
    global_settings = get_global_settings()
    address.status='P' 
    address.created_by = request.user
    address.modified_by = request.user
    address.seo_title = None
    address.venue = form.title
    address.address_type="classified"
    address.slug=getUniqueValue(Address,slugify(form.title),instance_pk=address.id)
    try:
        address.lat, address.lon, address.zoom = get_lat_lng(request.POST['lat_lng'])
        try:address.zoom = int(request.POST['zoom'])
        except:pass
    except:
        address.lat, address.lon, address.zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
    address.save()
    return address
    
    
    
def save_classified_tags(classified, tags):
    try:tags=tags.split(',')
    except:tags=tags
    try:classified.tags.clear()
    except:pass
    for tag in tags:
        tag = tag.strip()
        try:
            objtag = Tag.objects.get(tag = tag)
        except:
            objtag = Tag(tag = tag)
            objtag.save()
        classified.tags.add(objtag)
        
def save_classifieds_photos(classified,photos):
    photo_obj=ClassifiedPhoto.objects.filter(id__in=photos).exclude(classified__isnull=False).update(classified=classified)
   
        
def save_classified_attribute(classified, select_dict):
    att_v = ClassifiedAttributevalue.objects.filter(classified=classified)
    att_v.delete()
    for n in select_dict:
        clasatt = ClassifiedAttribute.objects.get(id=n)
        attvalue = ClassifiedAttributevalue(classified=classified, attribute_id=clasatt, attribute=clasatt.name)
        if type(select_dict[n]) == list:
            attvalue.value = ','.join(select_dict[n])
        else:
            attvalue.value = select_dict[n]
        attvalue.save()

