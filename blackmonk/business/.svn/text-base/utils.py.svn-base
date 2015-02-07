import datetime

from django.conf import settings as mysettings
from business.models import BusinessCategory,AttributeGroup,Attributes,AttributeValues,BizAttributes,Tag as BusinessTags
from business.models import WorkingHours,BusinessLogo,Business,Address,PaymentOptions,BusinessClaimSettings
from business.models import ContactDetails,BusinessCoupons,BusinessProducts,BusinessPrice,BusinessClaim
      
from django.core.mail import EmailMessage
from common.utils import get_global_settings
from django.template import  Template,Context
from django.utils import timezone
from usermgmt.adminviews import  *
# from googlemaps import GoogleMaps
# from pygeocoder import Geocoder

# def get_business_map_settings(latt,lon,zoom, add1, add2, zip, city):
#     globalsettings = get_global_settings()
#     LAT, LON, ZOOM = 0,0,0
#     try:
#         LAT = float(latt)
#         LON = float(lon)
#         ZOOM = int(zoom)
#     except:
#         try:
#             gmaps = GoogleMaps()
#             address = add1+','+add2+','+zip+','+city
#             LAT, LON = Geocoder.geocode(address)[0].coordinates
#             ZOOM = 11
#         except:
#             LAT = globalsettings.google_map_lat
#             LON = globalsettings.google_map_lon
#             ZOOM = 11
#     return (LAT, LON, ZOOM)

def co_add_categories(business,cid):
    if business.categories:business.categories.clear()
    categories = BusinessCategory.objects.filter(id__in=cid)
    for category in categories:
        if category.parent_cat:
            business.categories.add(category)

def save_to_claim_business(user=None, business=None, approve=False, paid=False, level='level0'):
    level_letter = {
        'level0': 'B',
        'level1': 'S',
        'level2': 'F',
    }[level]
    try:
        claim = BusinessClaim.objects.get(business=business)
        if user is not None and claim.user != user:
            claim.delete()
            claim = False
    except:
        claim = False
    if not claim:
        claim = BusinessClaim(
            business=business,
            payment_status=level_letter,
            staff=business.created_by,
            user=user,
        )
    claim.is_approved = approve
    claim.is_paid = business.is_paid = paid
    if approve:
        claim.approved_on = datetime.datetime.now()
        business.status = 'P'
        business.featured_sponsored = claim.payment_status
        business.created_by = claim.user
        business.created_on = timezone.now()
    elif paid:
        business.is_claimable = False
        business.status = 'N'
    business.save()
    claim.save()
    return True
   
def publish_business_mail(business):
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
                    "BUSINESS_URL": business.get_absolute_url(),"WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, mysettings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass  
   
def upgrade_business_mail(business):
    global_settings=get_global_settings()
    try:
        if business.featured_sponsored =='F':
            type = "featured"
        elif business.featured_sponsored =='S':
            type = "sponsored"
        else:
            type = "free"        
        to_emailids = [business.created_by.email]
        email_temp = EmailTemplates.objects.get(code='bub')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": business.created_by.display_name,"BUSINESS_NAME": business.name,"BUSINESS_TYPE": type,
                    "BUSINESS_URL": business.get_absolute_url(),"WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, mysettings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass       

def reject_business_mail(business):
    global_settings=get_global_settings()
    try:
        if business.featured_sponsored =='F':
            type = "featured"
        elif business.featured_sponsored =='S':
            type = "sponsored"
        else:
            type = "free"        
        to_emailids = [business.created_by.email]
        email_temp = EmailTemplates.objects.get(code='brb')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": business.created_by.display_name,"BUSINESS_NAME": business.name,"BUSINESS_TYPE": type,
                    "BUSINESS_URL": business.get_absolute_url(),"WEBSITE": global_settings.domain})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, mysettings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass    


def co_get_business_attribute(business):
    attr = []
    common_attributes = business.get_attributes(style='A')
    for attribute in common_attributes:
        keys = attribute.get_sub_attributes_all()
        k=[]
        for key in keys:
            try:
                ba = BizAttributes.objects.get(business=business,attribute=attribute,key=key)
            except:ba=[]
            l_k = {'key':key,'business_attribute':ba}
            k.append(l_k)
        l_a = {'attribute':attribute,'value':k}
        attr.append(l_a)
    return attr

def co_get_business_service(business):
    attr = []
    common_attributes = business.get_attributes(style='S')
    for attribute in common_attributes:
        try:bs = BizServices.objects.filter(business=business,attribute=attribute)
        except:bs=[]
        l_o = {'attribute':attribute,'business_services':bs}
        attr.append(l_o)
    return attr

def co_add_tags(business,taglist):
    try:taglist=taglist.split(',')
    except:taglist=taglist
    business.tags.clear()
    for tag in taglist:
        tag = tag.strip()[:50]
        try:
            objtag = BusinessTags.objects.get(tag__iexact = tag)
            business.tags.add(objtag)
        except:
            if tag!="":
                objtag = BusinessTags(tag=tag)
                objtag.save()
                business.tags.add(objtag)
        

def co_add_workinghours(business, request):
    wh = WorkingHours.objects.filter(business=business)
    wh.delete()
    for n in request.POST:
        if "att_name_id_" == n[:12]:
            attid=n[12:]
            if request.POST['att_style_'+attid] == 'W':
                main_att = Attributes.objects.get(id=int(attid))
                try:
                    request.POST['hours'+attid]
                except:
                    return False
                if request.POST['hours'+attid]=='f':
                    wstat=False
                    wh = WorkingHours(business=business,attribute=main_att)
                    try:
                        request.POST['c0'+attid]
                        wh.mon_start=None
                        wh.mon_end=None
                    except:
                        wstat=True
                        wh.mon_start = request.POST['hts0'+attid]
                        wh.mon_end = request.POST['hte0'+attid]
                    try:
                        request.POST['c1'+attid]
                        wh.tue_start = None
                        wh.tue_end = None
                    except:
                        wstat=True
                        wh.tue_start = request.POST['hts1'+attid]
                        wh.tue_end = request.POST['hte1'+attid]
                    try:
                        request.POST['c2'+attid]
                        wh.wed_start = None
                        wh.wed_end = None
                    except:
                        wstat=True
                        wh.wed_start = request.POST['hts2'+attid]
                        wh.wed_end = request.POST['hte2'+attid]
                    try:
                        request.POST['c3'+attid]
                        wh.thu_start = None
                        wh.thu_end = None
                    except:
                        wstat=True
                        wh.thu_start = request.POST['hts3'+attid]
                        wh.thu_end = request.POST['hte3'+attid]
                    try:
                        request.POST['c4'+attid]
                        wh.fri_start = None
                        wh.fri_end = None
                    except:
                        wstat=True
                        wh.fri_start = request.POST['hts4'+attid]
                        wh.fri_end = request.POST['hte4'+attid]
                    try:
                        request.POST['c5'+attid]
                        wh.sat_start = None
                        wh.sat_end = None
                    except:
                        wstat=True
                        wh.sat_start = request.POST['hts5'+attid]
                        wh.sat_end = request.POST['hte5'+attid]
                    try:
                        request.POST['c6'+attid]
                        wh.sun_start = None
                        wh.sun_end = None
                    except:
                        wstat=True
                        wh.sun_start = request.POST['hts6'+attid]
                        wh.sun_end = request.POST['hte6'+attid]
                    try:
                        wstat=True
                        wh.notes = request.POST['wh_notes'+attid]
                    except:
                        wh.notes = ''
                    if wstat:
                        wh.save()

def co_add_paymentoption(business, paymentoptions):
    business.paymentoptions.clear()
    for paymentoption in paymentoptions:
        try:
            po = PaymentOptions.objects.get(id=paymentoption)
            business.paymentoptions.add(po)
        except:pass

def co_add_services(business, request):
    bs = BizServices.objects.filter(business=business)
    bs.delete()
    for n in request.POST:
        if "att_name_id_" == n[:12]:
            main_att = Attributes.objects.get(id=int(n[12:]))
            s_list = request.POST.getlist('service_'+n[12:])
            for s in s_list:
                s= s.strip()
                if s:
                    bs = BizServices(business=business, attribute=main_att, value=s)
                    bs.save()

def co_add_attributes(business, request):
    ba = BizAttributes.objects.filter(business=business)#.exclude(key__type='I')
    ba.delete()
    for n in request.POST:
        if "att_name_id_" == n[:12]:
            main_att = Attributes.objects.get(id=int(n[12:]))
            a_id_list = request.POST.getlist('attribute_name_'+n[12:])
            for a_id in a_id_list:
                ak = AttributeKey.objects.get(id=a_id)
                ba = BizAttributes(business=business,attribute=main_att,key = ak)
                ba.save()
                try:
                    file = request.FILES['attr_file_'+n[12:]+'_'+a_id]
                    ba.value.clear()
                    file_data = file.read()
                    filename = file.name
                    sf_base, sf_filename = os.path.split(filename)
                    sf_name, sf_extension = os.path.splitext(sf_filename)
                    sf_extension_f = sf_extension.upper()
                    if sf_extension_f in ['.JPEG','.JPG','.JPE','.PNG','.BMP','.GIF','.PDF','.DOC','.XDOC','.PPT','.CSV','.XLS','.ODT','.RTF','.TXT','.ODS','.XLT']:
                        absolute_file_name = 'images/business/file/%d_%s%s'%(business.id,n[12],sf_extension)
                        fullabsolute_file_name = '%s%s'%(mysettings.MEDIA_ROOT,absolute_file_name)
                        #from __future__ import with_statement
                        fileobj = open(fullabsolute_file_name,"w")
                        fileobj.write(file_data)
                        fileobj.close()
                        v = absolute_file_name
                        try:
                            av = AttributeValue.objects.get(attribute_key=ak,name__iexact=v)
                        except:
                            av = AttributeValue(attribute_key=ak,name=v)
                            av.save()
                        ba.value.add(av)
                except:
                    ba.value.clear()
                    try:
                        v =request.POST['attr_file_exist_'+n[12:]+'_'+a_id]
                        if v:
                            try:
                                av = AttributeValue.objects.get(attribute_key=ak,name__iexact=v)
                            except:
                                av = AttributeValue(attribute_key=ak,name=v)
                                av.save()
                            ba.value.add(av)
                    except:
                        value_list = request.POST.getlist('attribute_'+n[12:]+'_'+a_id)
                        for v in value_list:
                            if v:
                                try:
                                    av = AttributeValue.objects.get(attribute_key=ak,name__iexact=v)
                                except:
                                    av = AttributeValue(attribute_key=ak,name=v[:150])
                                    av.save()
                                ba.value.add(av)
            
            a_kid_list = request.POST.getlist('extra_attribute_key_'+n[12:])
            a_vid_list = request.POST.getlist('extra_attribute_value_'+n[12:])
            i=0
            for k_value in a_kid_list:
                k_value = k_value.strip()
                v_value = a_vid_list[i].strip()
                if k_value and v_value:
                    try:
                        ak = AttributeKey.objects.get(name__iexact=k_value,attribute=main_att)
                    except:
                        ak = AttributeKey(name=k_value,attribute=main_att,type='C')
                        ak.save()
                    ba = BizAttributes(business=business,attribute=main_att,key = ak)
                    ba.save()
                    ba.value.clear()
                    try:
                        av = AttributeValue.objects.get(attribute_key=ak,name__iexact=v_value)
                    except:
                        av = AttributeValue(attribute_key=ak,name=v_value)
                        av.save()
                    ba.value.add(av)
                i = i + 1
                
from common.models import PaymentConfigure
from payments.stripes.models import StripePaymentDetails
import stripe
def business_stripe_unsubscribe(id):
    try:
        stripe_list = StripePaymentDetails.objects.filter(object_id = id)
        currency=PaymentConfigure.get_payment_settings()
        stripe.api_key = currency.stripe_private_key
        for s in stripe_list:
            cust = str(s.customer_id)
            customer = stripe.Customer.retrieve(cust)
            customer.delete()
        stripe_list.update(subscription_status ='Inactive')
    except:pass
    
    
    
        