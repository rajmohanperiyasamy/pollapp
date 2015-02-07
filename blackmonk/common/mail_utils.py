from django.conf import settings as my_settings
from django.core.mail import EmailMessage
from django.template import  Template,Context

from usermgmt.models import EmailTemplates
from common.utils import get_global_settings


def mail_publish_article(article):
    global_settings=get_global_settings()
    type = {
        'FR':'Article Own Story',
        'PR':'Article Pressrelease',
        'A':'Article Advertorial',
        'RR':'Article Review Request',
    }[article.article_type]
        
    to_emailids = [article.created_by.email]
    email_temp = EmailTemplates.objects.get(code='apa')
    s = Template(email_temp.subject)
    t= Template(email_temp.template)
    try:
        c= Context({"USERNAME": article.created_by.display_name,"ARTICLE_TITLE": article.title,"ARTICLE_TYPE": type,
                "ARTICLE_URL": global_settings.website_url+article.get_absolute_url(),"WEBSITE": global_settings.domain,"ADD_URL":global_settings.website_url+'/user/articles/'})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass
    
def mail_publish_community(entry):
    global_settings=get_global_settings()

    to_emailids = [entry.created_by.email]
    email_temp = EmailTemplates.objects.get(code='cpe')
    s = Template(email_temp.subject)
    t= Template(email_temp.template)
    
    entry_type={'Q':'Question','A':'Answer','P':'Post'}[entry.entry_type]
    try:
        c= Context({"USERNAME": entry.created_by.display_name,"ENTRY_NAME": entry.title,"ENTRY_TYPE": entry_type,
                "ENTRY_URL": global_settings.website_url+entry.get_absolute_url(),"WEBSITE": global_settings.domain,"ADD_URL":global_settings.website_url+'/community/'})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass

def mail_publish_banner(banner):
    global_settings=get_global_settings()
    try:
        banner_type=banner.zones.get_slot_display()
        to_emailids = [banner.created_by.email]
        email_temp = EmailTemplates.objects.get(code='ban')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": banner.created_by.display_name,"BANNER_TITLE": banner.caption,"BANNER_TYPE": banner_type,
                    "WEBSITE": global_settings.domain,"ADD_URL":global_settings.website_url+'/user/banners/'})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass
    

def mail_publish_event(event):
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
                    "EVENT_URL": global_settings.website_url+event.get_absolute_url(),"WEBSITE": global_settings.domain,"ADD_URL":global_settings.website_url+'/user/events/addevent/'})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass
    
def mail_publish_classifieds(classifieds):
    global_settings=get_global_settings()
    try:
        if classifieds.listing_type =='F':
            type = "featured"
        elif classifieds.listing_type =='S':
            type = "sponsored"
        else:
            type = "free"     
        to_emailids = [classifieds.created_by.email]
        email_temp = EmailTemplates.objects.get(code='cpc')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": classifieds.created_by.display_name,"CLASSIFIED_TITLE": classifieds.title,"CLASSIFIED_TYPE": type,
                    "CLASSIFIED_URL": global_settings.website_url+classifieds.get_absolute_url(),"WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass  
    
def mail_expire_classifieds(classifieds):
    global_settings=get_global_settings()
    try:
        if classifieds.listing_type =='F':
            type = "featured"
        elif classifieds.listing_type =='S':
            type = "sponsored"
        else:
            type = "free"     
        to_emailids = [classifieds.created_by.email]
        email_temp = EmailTemplates.objects.get(code='cec')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": classifieds.created_by.display_name,"CLASSIFIED_TITLE": classifieds.title,"CLASSIFIED_TYPE": type,"RENEW_URL":global_settings.website_url+'/user/classifieds/',
                    "WEBSITE": global_settings.domain,"ADD_URL":global_settings.website_url+'/user/classifieds/add/'})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:pass  
   
def mail_publish_business(business):
    global_settings=get_global_settings()
    try:
        if business.featured_sponsored =='F':
            type = "featured"
        elif business.featured_sponsored =='S':
            type = "sponsored"
        else:
            type = "free"     
        to_emailids = [business.created_by.email]
        email_temp = EmailTemplates.objects.get(code='bpb')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": business.created_by.display_name,"BUSINESS_NAME": business.name,"BUSINESS_TYPE": type,
                    "BUSINESS_URL": global_settings.website_url+business.get_absolute_url(),"WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass 
    
def mail_publish_gallery(gallery):
    global_settings=get_global_settings()
    try:
        to_emailids = [gallery.created_by.email]
        email_temp = EmailTemplates.objects.get(code='gpg')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": gallery.created_by.display_name,"GALLERY_NAME": gallery.title,"ADD_GALLERY_URL": global_settings.website_url+'/user/photos/',
                    "GALLERY_URL": global_settings.website_url+gallery.get_absolute_url(),"WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:pass  
    
def mail_publish_videos(videos):
    global_settings=get_global_settings()
    try:
        to_emailids = [videos.created_by.email]
        email_temp = EmailTemplates.objects.get(code='vpv')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": videos.created_by.display_name,"ADD_VIDEO_URL": global_settings.website_url+'/user/videos/',
                   "WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:pass 
    
def mail_publish_restaurant(restaurant):
    global_settings=get_global_settings()
    try:
        if restaurant.featured_sponsored =='F':
            type = "featured"
        elif restaurant.featured_sponsored =='S':
            type = "sponsored"
        else:
            type = "free"     
        to_emailids = [restaurant.created_by.email]
        email_temp = EmailTemplates.objects.get(code='mpr')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": restaurant.created_by.display_name,"RESTAURANT_NAME": restaurant.name,"RESTAURANT_TYPE": type,
                    "RESTAURANT_URL": global_settings.website_url+restaurant.get_absolute_url(),"WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:pass     

from payments.stripes.models import StripePaymentDetails,StripeUnsubscribers
from business.models import Business
from common.models import StaffEmailSettings
def business_unsubscribe_staff_notification(id):
    global_settings=get_global_settings()
    try:
        stripe_object = StripePaymentDetails.objects.get(id=id)
        business = Business.objects.get(id = stripe_object.object_id)
        to_emailids = [StaffEmailSettings.objects.get(availableapps__name__iexact='business',action='C').emails,]
        email_temp = EmailTemplates.objects.get(code='ssn')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c = Context({"USERNAME":stripe_object.user.display_name,"BUSINESS_NAME":business.name,"WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass

def business_unsubscribe_user_notification(id,email):
    global_settings=get_global_settings()
    try:
        stripe_object = StripePaymentDetails.objects.get(id=id)
        business = Business.objects.get(id = stripe_object.object_id)
        to_emailids = [email]
        email_temp = EmailTemplates.objects.get(code='sun')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        if stripe_object.subscription_status == 'inactive':
            status = 'processed successfully'
        elif stripe_object.subscription_status == 'active':
            status = 'rejected'
        c = Context({"USERNAME":stripe_object.user.display_name,"BUSINESS_NAME":business.name,'STATUS':status,"WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:pass
      
    

