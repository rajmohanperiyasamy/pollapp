import datetime
from time import strptime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template import RequestContext
from deal.models import Deal,DealPayment
from business.models import Business,Address
from django.conf import settings as my_settings
from common.utils import get_global_settings


from django.template import  Template,Context
from usermgmt.adminviews import EmailTemplates
from business.models import Address
from usermgmt.models import BmUser
from PIL import Image
from xml.dom import minidom
import os



def get_next_alpha(key):
    t=ord(key[0])
    h=ord(key[1])
    o=ord(key[2])
    if o == 90:
        o=65
        if h == 90:
            t = t + 1
            h = 65
        else:
            h = h + 1
    else:
        o = o + 1
    return chr(t)+chr(h)+chr(o)

def get_rem_seconds(deal,today):
    now = datetime.datetime.now()
    rem_seconds = 0
    if deal:
        if deal.end_date >= today:
            rem_seconds = 86400-((now.hour*60*60)+(now.minute*60)+(now.second))
    days = deal.end_date - today
    rem_seconds = rem_seconds + (days.days*60*60*24)
    return rem_seconds

def get_seconds(today):
    now = datetime.datetime.now()
    rem_seconds = 0
    rem_seconds = 86400-((now.hour*60*60)+(now.minute*60)+(now.second))
    return rem_seconds

def set_numberof_views(deal,request):
    try:
        if request.session['dealcount%s'%(deal.id)] != deal.id:
            request.session['dealcount%s'%(deal.id)] = deal.id
            deal.most_viewed = deal.most_viewed + 1
            deal.save()
    except:
        request.session['dealcount%s'%(deal.id)] = deal.id
        deal.most_viewed = deal.most_viewed + 1
        deal.save()

def get_todays_deals(today):
    return Deal.objects.filter(status='P', end_date__gte=today ,start_date__lte=today).order_by('-created_on')

def get_voucher_key(deal):
    from random import choice,randint
    key = deal.dealkey
    while True:
        a = ''.join([choice('1234567890') for i in range(3)])
        a = key + a
        try:DealPayment.objects.get(dealkey=a)
        except:return a
            
def buy_success_mail(deal_payment,deal):
    global_settings=get_global_settings()
    to_emailids = [deal_payment.email]
    email_temp = EmailTemplates.objects.get(code='dbs')
    s = Template(email_temp.subject)
    t= Template(email_temp.template)
    c= Context({ "USERNAME": deal_payment.created_by.display_name,"REMAINING_DAYS": deal.get_remaining_second(),
                "VALID_DATE": deal.voucher_valid,"VOUCHER_NO": deal_payment.dealkey,"WEBSITE": global_settings.domain})
    email_message=t.render(c)
    subject = s.render(c)
    email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
    email.content_subtype = "html"
    email.send()

def buy_success_gift_mail(deal_payment,deal):
    global_settings=get_global_settings()
    to_emailids = [deal_payment.gift_addr.g_email]
    email_temp = EmailTemplates.objects.get(code='dbf')
    s = Template(email_temp.subject)
    t= Template(email_temp.template)
    c= Context({ "BUYER_NAME": deal_payment.created_by.profile.get_full_name(),"REMAINING_DAYS": deal.get_remaining_second(),"VALID_DATE": deal.voucher_valid,
                "VOUCHER_NO": deal_payment.dealkey,"WEBSITE": global_settings.domain,"FRIEND_NAME":deal_payment.gift_addr.g_name})
    email_message=t.render(c)
    subject = s.render(c)
    email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
    email.content_subtype = "html"
    email.send()

def send_voucher_mail(deal_payment,deal,to_email):
    to_emailids = [to_email]
    user=BmUser.objects.get(display_name = deal_payment.address)
    globalsettings=get_global_settings()
    subject = globalsettings.domain+" Gift Voucher"
    email_message = render_to_string(
        "default/deals/voucher.html",
        {'deal': deal,
         'payment': deal_payment,
         'globalsettings': globalsettings}
    )
    email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
    email.content_subtype = "html"
    email.send()
    
def send_mail_contact(request,name,mobile,email, message):
    global_settings=get_global_settings()
    subject = "Deal Contact from "+name
    to_emailids = [global_settings.info_email]
    try:
        email_message = render_to_string("default/deals/mail_contactus.html", {"name": name,'mobile':mobile,'email':email,'message':message}, context_instance=RequestContext(request))
        email = EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL, to_emailids)
        email.content_subtype = "html"
        email.send()
    except:pass

