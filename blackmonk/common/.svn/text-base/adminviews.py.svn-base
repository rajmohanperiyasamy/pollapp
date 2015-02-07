#Python
from datetime import date, timedelta, datetime
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson, timezone
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt
import smtplib
from socket import gaierror
import sys
import urllib

from article.models import Article
from attraction.models import Attraction
from banners.models import BannerAdvertisements
from bookmarks.models import Bookmark
from business.models import Business
from classifieds.models import Classifieds
from common.admin_utils import error_response
from common.fileupload import config_upload_logo, config_delete_logo, \
    config_delete_fav, config_delete_iphone
from common.forms import GeneralSettings, GeneralMapMarker, GeneralPayment, \
    UpdateBannerContents, SEOForm, GeneralReport, SignupSettingsForm, \
    MiscAttributeForm, SmtpConfigForm, UploadEditorImageForm
from common.models import CommentSettings, BannerAdds, Pages, AvailableApps, \
    MiscAttribute, ModuleNames, SocialSettings, AvailableModules, CommonConfigure, \
    NewsLetterApiSettings, PaymentConfigure, SignupSettings, Advertisement, \
    SmtpConfigurations
from common.static_msg import CONFIG_MSG, DEALS_MSG, API_MSG, MISC_MSG, HOME_MSG, \
    UTILITY_MSG
from common.templatetags.ds_utils import get_msg_class_name
from common.utils import ds_pagination, get_global_settings
from deal.models import Deal
from events.models import Event
from gallery.models import PhotoAlbum, Photos
from movies.models import Movies
from usermgmt.decorators import admin_required
from usermgmt.models import EmailTemplates
from videos.models import Videos


User = get_user_model()


#Django
#from django.conf import settings as my_settings
@admin_required
def dashboard(request, template='admin/portal/dashboard.html'):
    apps = AvailableApps.objects.all().exclude(status='N').order_by('name')
    affiliates = apps.filter(type='A')
    data = {'apps': apps, 'affiliates':affiliates, 'pages': Pages.objects.filter(is_static=True).order_by('name')}
    return render_to_response(template, data, context_instance=RequestContext(request))


@admin_required
def home_seo_update(request, template='admin/portal/update_seo.html'):
    try:
        seo = ModuleNames.get_module_seo(name='home')
    except:
        seo = None
    form = None
    if request.method == 'POST':
        try:
            form = SEOForm(request.POST)
            try:
                seo = ModuleNames.get_module_seo(name='home')
            except:
                seo = ModuleNames(name='home')
            if form.is_valid():
                title = form.cleaned_data.get('meta_title')
                description = form.cleaned_data.get('meta_description')
                seo.seo_title = title
                seo.seo_description = description
                seo.modified_by = request.user
                seo.save()
                data = {'status': 1, 'msg': str(HOME_MSG['HSUS']), 'mtype': get_msg_class_name('s')}
                return HttpResponse(simplejson.dumps(data))
            else:
                data = {'seo': seo, 'form': form}
                return error_response(data, template, HOME_MSG)
        except:
            pass
    data = {'seo': seo, 'form': form}
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def configuration_analytics(request, template='admin/configuration/analytics.html'):
    data = {}
    return render_to_response (template, data, context_instance=RequestContext(request))


################# ADMIN SETTINGS #################
@admin_required
def configuration(request):
    return HttpResponseRedirect(reverse('admin_configuration_general'))

ds_site_dateformats = [
    {'format': '%B %d, %Y', 'sample': datetime.now().strftime('%B %d, %Y')},
    {'format': '%Y/%m/%d', 'sample': datetime.now().strftime('%Y/%m/%d')},
    {'format': '%m/%d/%Y', 'sample': datetime.now().strftime('%m/%d/%Y')},
    {'format': '%d/%m/%Y', 'sample': datetime.now().strftime('%d/%m/%Y')},
]
ds_default_date = "%d/%b/%Y"
ds_site_timeformats = [
    {'format': '%I:%M %p', 'sample': datetime.now().strftime('%I:%M %p')},
    {'format': '%H:%M', 'sample': datetime.now().strftime('%H:%M')},
]
ds_default_time = "%I:%M %p"

@admin_required
def configuration_general(request, template='admin/configuration/basic_info.html'):
    general = CommonConfigure.objects.all()[:1]
    if general:
        general = general[0]
    else:
        general = None
    form = GeneralSettings(instance=general)
    data = {'form': form, 'general': general}
    try:
        data['seo'] = ModuleNames.get_module_seo(name='home')
    except:
        data['seo'] = None
    data['ds_site_dateformats'] = ds_site_dateformats
    data['custom_date'] = {"format": ds_default_date, "sample": datetime.now().strftime(ds_default_date)}
    data['ds_site_timeformats'] = ds_site_timeformats
    data['custom_time'] = {"format": ds_default_time, "sample": datetime.now().strftime(ds_default_time)}
    try:
        if general.site_dateformat not in ['%B %d, %Y', '%Y/%m/%d', '%m/%d/%Y', '%d/%m/%Y']:
            data['custom_dateformat'] = True
            data['custom_date'] = {"format": general.site_dateformat, "sample": datetime.now().strftime(general.site_dateformat)}
    except: pass 
    try:
        if general.site_timeformat not in ['%I:%M %p', '%H:%M']:
            data['custom_timeformat'] = True
            data['custom_time'] = {"format": general.site_timeformat, "sample": datetime.now().strftime(general.site_timeformat)}
    except: pass
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def configuration_general_update(request, template='admin/configuration/include_basic_info.html'):
    general = CommonConfigure.objects.all()[:1]
    if general:
        general = general[0]
    else:
        general = None
    form = GeneralSettings(request.POST, instance=general)
    if form.is_valid():
        general_x = form.save()
    seoform = SEOForm(request.POST)
    try:
        seo = ModuleNames.get_module_seo(name='home')
    except:
        seo = ModuleNames(name='home')
    if seoform.is_valid():
        title = seoform.cleaned_data.get('meta_title')
        description = seoform.cleaned_data.get('meta_description')
        seo.seo_title = title
        seo.seo_description = description
        seo.modified_by = request.user
        seo.save()
    try:
        site_logo = general.logo.url
    except:
        site_logo = ''
    
    html_data = {'form': GeneralSettings(instance=general), 'general': general, 'seo': seo}
    html_data['ds_site_dateformats'] = ds_site_dateformats
    html_data['custom_date'] = {"format": ds_default_date, "sample": datetime.now().strftime(ds_default_date)}
    html_data['ds_site_timeformats'] = ds_site_timeformats
    html_data['custom_time'] = {"format": ds_default_time, "sample": datetime.now().strftime(ds_default_time)}
    try:
        if general.site_dateformat not in ['%B %d, %Y', '%Y/%m/%d', '%m/%d/%Y', '%d/%m/%Y']:
            html_data['custom_dateformat'] = True
            html_data['custom_date'] = {"format": general.site_dateformat, "sample": datetime.now().strftime(general.site_dateformat)}
    except: pass
    try:
        if general.site_timeformat not in ['%I:%M %p', '%H:%M']:
            html_data['custom_timeformat'] = True
            html_data['custom_time'] = {"format": general.site_timeformat, "sample": datetime.now().strftime(general.site_timeformat)}
    except: pass
    html = render_to_string(template, html_data, context_instance=RequestContext(request))
    data = {'html': html, 'msg': str(CONFIG_MSG['BIUS']), 'mtype': get_msg_class_name('s'), 'site_name': general.site_title, 'logo': site_logo}
    
    return HttpResponse(simplejson.dumps(data))

def load_customdate(request):
    return HttpResponse(datetime.now().strftime(request.POST.get("format_str", ds_default_date)))

def load_customtime(request):
    return HttpResponse(datetime.now().strftime(request.POST.get("format_str", ds_default_time)))


@admin_required
def configuration_social_url_update(request):
    try:
        general = CommonConfigure.objects.all()[:1][0]
        obj=request.POST['obj']
        action=request.POST['action']
        value=request.POST.get('value',None)
        if action=='add':
            if obj == 'facebook_page_url':general.facebook_page_url=value
            elif obj == 'twitter_url':general.twitter_url=value
            elif obj == 'googleplus_url':general.googleplus_url=value
            elif obj == 'pinterest':general.pinterest=value
            else:return HttpResponse('0')
            general.save()
            return HttpResponse('1')
        elif action=='remove':
            if obj == 'facebook_page_url':general.facebook_page_url=''
            elif obj == 'twitter_url':general.twitter_url=''
            elif obj == 'googleplus_url':general.googleplus_url=''
            elif obj == 'pinterest':general.pinterest=''
            else:return HttpResponse('0')
            general.save()
            return HttpResponse('1')
        else:return HttpResponse('0')
    except:return HttpResponse('0')
    
@admin_required
def config_ajax_upload_logo(request):
    general = CommonConfigure.objects.all()[:1]
    general = general[0]
    return config_upload_logo(request, CommonConfigure, general, 'logo')


@admin_required
def config_ajax_upload_fav(request):
    general = CommonConfigure.objects.all()[:1]
    general = general[0]
    return config_upload_logo(request, CommonConfigure, general, 'fav')


@admin_required
def config_ajax_upload_iphonelogo(request):
    general = CommonConfigure.objects.all()[:1]
    general = general[0]
    return config_upload_logo(request, CommonConfigure, general, 'iphone')


@admin_required
def config_ajax_delete_logo(request):
    general = CommonConfigure.objects.all()[:1]
    general = general[0]
    return config_delete_logo(request, general)


@admin_required
def config_ajax_delete_fav(request):
    general = CommonConfigure.objects.all()[:1]
    general = general[0]
    return config_delete_fav(request, general)


@admin_required
def config_ajax_delete_iphonelogo(request):
    general = CommonConfigure.objects.all()[:1]
    general = general[0]
    return config_delete_iphone(request, general)


@admin_required
def configuration_general_signup(request, template='admin/configuration/signup_option.html'):
    signup = SignupSettings.objects.all()[:1]
    if signup:
        signup = signup[0]
    else:
        signup = None
    form = SignupSettingsForm(instance=signup)
    data = {'form': form, 'signup': signup}
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required
def configuration_general_signup_update(request, template='admin/configuration/include_signup_settings.html'):
    signup = SignupSettings.objects.all()[:1]
    if signup:
        signup = signup[0]
    else:
        signup = None
    form = SignupSettingsForm(request.POST, instance=signup)
    if form.is_valid():
        signup = form.save()
    html = render_to_string(template, {'form': form, 'signup': signup})
    data = {'html': html, 'msg': str(CONFIG_MSG['SSUS']), 'mtype': get_msg_class_name('s')}
    return HttpResponse(simplejson.dumps(data))


@admin_required
def share_buttons(request, template='admin/configuration/share_buttons.html'):
    socail = SocialSettings.get_or_create_obj()
    data = {'socail': socail}
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required
def ajax_share_buttons(request):
    try:
        Id = request.POST['id']
        val = request.POST['val']
        socail = SocialSettings.get_or_create_obj()
        if Id == 'facebook':
            socail.fb_like = int(val)
        elif Id == 'twitter':
            socail.twitter = int(val)
        elif Id == 'googleplus':
            socail.google_plus = int(val)
        elif Id == 'pinterest':
            socail.pinterest = int(val)
        socail.save()
        return HttpResponse('1')
    except:
        return HttpResponse('0')


####### AVAILABLE APPS #####
@admin_required
def configuration_available_apps(request, template='admin/configuration/availableapps.html'):
    apps = AvailableApps.objects.all().exclude(status='N').order_by('name')
    data = {'apps': apps}
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required
def configuration_available_apps_change_status(request):
    try:
        app = AvailableApps.objects.get(id=request.GET['id'])
        if app.status == 'A':
            app.status = 'I'
            status = '1'
        else:
            app.status = 'A'
            status = '2'
        app.save()
        process_menuitems(app)
        try: cache.clear()
        except: pass
        return HttpResponse(status)
    except:
        return HttpResponse('0')

def process_menuitems(app):
    try:
        slug = '/' + app.slug + '/'
        menus = AvailableModules.objects.filter(base_url__icontains=slug)
        if app.status == 'A':
            menus.update(is_active=True)
        else:
            menus.update(is_active=False)
        cache.delete('inactive_apps')
        return None
    except:
        return None


@admin_required
def configuration_general_advertisement(request, template='admin/configuration/advertisement.html'):
    advertisement = Advertisement.objects.all()[:1]
    if advertisement:
        advertisement = advertisement[0]
    else:
        advertisement = None
    data = {'advertisement': advertisement}
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required
def configuration_general_advertisement_update(request, template='admin/configuration/include_advertisement.html'):
    advertisement = Advertisement.objects.all()[:1]
    if advertisement:
        advertisement = advertisement[0]
    else:
        advertisement = Advertisement()
    advertisement.adoption = request.POST['adoption']
    advertisement.header_section = request.POST['header_section']
    advertisement.save()
    html = render_to_string(template, {'advertisement': advertisement})
    data = {'html': html, 'msg': str(CONFIG_MSG['ASUS']), 'mtype': get_msg_class_name('s')}
    return HttpResponse(simplejson.dumps(data))


@admin_required
def configuration_map_marker(request, template='admin/configuration/map_marker.html'):
    general = CommonConfigure.objects.all()[:1]
    if general:
        general = general[0]
    else:
        general = None
    form = GeneralMapMarker(instance=general)
    data = {'form': form}
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required
def configuration_map_marker_update(request, template='admin/configuration/include_map_marker.html'):
    general = CommonConfigure.objects.all()[:1]
    if general:
        general = general[0]
    else:
        general = None
    form = GeneralMapMarker(request.POST, instance=general)
    if form.is_valid():general = form.save()
    html = render_to_string(template, {'form':form, 'general':general}, context_instance=RequestContext(request))
    data = {'html': html, 'msg': str(CONFIG_MSG['MMUS']), 'mtype': get_msg_class_name('s')}
    return HttpResponse(simplejson.dumps(data))


@admin_required
def configuration_report(request, template='admin/configuration/reports.html'):
    general = CommonConfigure.objects.all()[:1]
    if general:
        general = general[0]
    else:
        general = None
    form = GeneralReport(instance=general)
    data = {'form': form}
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required
def configuration_report_update(request, template='admin/configuration/include_reports.html'):
    general = CommonConfigure.objects.all()[:1]
    if general:
        general = general[0]
    else:
        general = None
    form = GeneralReport(request.POST, instance=general)
    if form.is_valid():
        general = form.save()
    html = render_to_string(template, {'form': form, 'general': general})
    data = {'html': html, 'msg': str(CONFIG_MSG['RSUS']), 'mtype': get_msg_class_name('s')}
    return HttpResponse(simplejson.dumps(data))


@admin_required
def configuration_social(request, template='admin/configuration/social.html'):
    general = CommonConfigure.objects.all()[:1]
    if general:
        general = general[0]
    else:
        general = None
    form = GeneralSocial(instance=general)
    data = {'form': form}
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required
def configuration_social_update(request, template='admin/configuration/include_social.html'):
    general = CommonConfigure.objects.all()[:1]
    if general:
        general = general[0]
    else:
        general = None
    form = GeneralSocial(request.POST, instance=general)
    if form.is_valid():
        general = form.save()
    html = render_to_string(template, {'form': form, 'general': general})
    data = {'html': html, 'msg': str(CONFIG_MSG['SOSUS']), 'mtype': get_msg_class_name('s')}
    return HttpResponse(simplejson.dumps(data))


@admin_required
def configuration_payment(request, template='admin/configuration/payment.html'):
    payment = PaymentConfigure.objects.all()[:1]
    if payment:
        payment = payment[0]
    else:
        payment = None
    form = GeneralPayment(instance=payment)
    data = {'form': form, 'payment': payment}
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required
def configuration_payment_update(request, template='admin/configuration/include_payment.html'):
    payment = PaymentConfigure.objects.all()[:1]
    if payment:
        payment = payment[0]
    else:
        payment = None
    form = GeneralPayment(request.POST, instance=payment)
    if form.is_valid():
        general = form.save()
        try:
            common = CommonConfigure.objects.all()[:1][0]
            common.currency = general.currency_symbol
            common.save()
        except:
            pass
    html = render_to_string(template, {'form': form, 'payment': payment})
    data = {'html': html, 'msg': str(CONFIG_MSG['PSUS']), 'mtype': get_msg_class_name('s')}
    return HttpResponse(simplejson.dumps(data))


#################### EMAIL TEMPLATES #######################
@admin_required
def emailtemplates(request, template='admin/configuration/emailtemplates.html'):
    data = {}
    try:
        email_templist = EmailTemplates.objects.all().order_by('name')
    except:
        email_templist = False
    
    data['email_templist'] = email_templist
    return render_to_response(template, data, context_instance=RequestContext(request))


@admin_required
def change_email_status(request):
    try:
        email_temp = EmailTemplates.objects.get(id=request.GET['id'])
        if email_temp.active:
            email_temp.active = False
            status = '1'
        else:
            email_temp.active = True
            status = '2'
        email_temp.save()
        return HttpResponse(status)
    except:
        return HttpResponse('0')

ALL_EMAIL_KEY = {
              'BUYER_NAME': '{{BUYER_NAME}}',
               #'BUSINESS': '{{BUSINESS}}',
              'REMAINING_DAYS': '{{REMAINING_DAYS}}',
              'VALID_DATE': '{{VALID_DATE}}',
              'VALID_NO': '{{VALID_NO}}',
              'VOUCHER_NO': '{{VOUCHER_NO}}',
              'WEBSITE': '{{WEBSITE}}',
              'FRIEND_NAME': '{{FRIEND_NAME}}',


              'USERNAME': '{{USERNAME}}',
              'ADD_URL': '{{ADD_URL}}',
              'ARTICLE_TYPE': '{{ARTICLE_TYPE}}',
              'ARTICLE_URL': '{{ARTICLE_URL}}',
              'ARTICLE_TITLE': '{{ARTICLE_TITLE}}',

              'CLASSIFIED_TITLE': '{{CLASSIFIED_TITLE}}',
              'CLASSIFIED_TYPE': '{{CLASSIFIED_TYPE}}',
              'CLASSIFIED_URL': '{{CLASSIFIED_URL}}',
              'RENEW_URL': '{{RENEW_URL}}',

              'RETRIEVE_URL': '{{RETRIEVE_URL}}',

              'BUSINESS_NAME': '{{BUSINESS_NAME}}',
              'BUSINESS_URL': '{{BUSINESS_URL}}',
              'BUSINESS_TYPE': '{{BUSINESS_TYPE}}',

               "EVENT_TITLE": '{{EVENT_TITLE}}',
               "EVENT_TYPE": '{{EVENT_TYPE}}',
               "EVENT_URL": '{{EVENT_URL}}',
              'ADD_URL': '{{ADD_URL}}',

               "GALLERY_NAME": '{{GALLERY_NAME}}',
               "GALLERY_URL": '{{GALLERY_URL}}',
               "ADD_GALLERY_URL": '{{ADD_GALLERY_URL}}',

               "ADD_VIDEO_URL": "{{ADD_VIDEO_URL}}",

              'WEBSITE_URL': '{{WEBSITE_URL}}',

              'PASSWORD': '{{PASSWORD}}',
              'LOGIN_URL': '{{LOGIN_URL}}',
              'SITE_URL': '{{SITE_URL}}',

              'CONTEST_TITLE': '{{CONTEST_TITLE}}',
              'CONTEST_ID': '{{CONTEST_ID}}',
              'CONTEST_URL': '{{CONTEST_URL}}',
              'CONTEST_HOME_URL': '{{CONTEST_HOME_URL}}',
              
              'ORDER_ID': '{{ORDER_ID}}',
              'PRICE': '{{PRICE}}',
              'ITEMS': '{{ITEMS}}',
              'DELIVERY_ADDRESS': '{{DELIVERY_ADDRESS}}',
              'SHIPPING_METHOD': '{{SHIPPING_METHOD}}',
              'ORDER_URL': '{{ORDER_URL}}',
              'STATUS':'{{STATUS}}',
              
              'ENTRY_NAME':'{{ENTRY_NAME}}',
              'ENTRY_URL':'{{ENTRY_URL}}',
              'ENTRY_TYPE':'{{ENTRY_TYPE}}',
              
              'BANNER_TITLE':'{{BANNER_TITLE}}',
              'BANNER_TYPE':'{{BANNER_TYPE}}',
              
}


@admin_required
def view_template(request, template='admin/configuration/email-edit.html'):
    data = {}
    code = request.GET['id']
    discription = {
                  'dbf': {
                         'Buyer name': 'BUYER_NAME',
                         'Name of the domain': 'BUSINESS',
                         'Remaining days left to redeem': 'REMAINING_DAYS',
                         'Voucher Valid Date': 'VALID_DATE',
                         'Voucher no': 'VOUCHER_NO',
                         'Business Outlet': 'WEBSITE',
                         'Friend name': 'FRIEND_NAME',
                          },
                  'dbs': {
                         'Username of the account owner': 'USERNAME',
                         'Business Outlet': 'BUSINESS',
                         'Remaining days left to reedem': 'REMAINING_DAYS',
                         'Voucher Valid Date': 'VALID_DATE',
                         'Voucher no': 'VOUCHER_NO',
                         'Website Name': 'WEBSITE',
                          },
                  'cec': {
                         'Username of the account owner': 'USERNAME',
                         'Classified Title': 'CLASSIFIED_TITLE',
                         'Website Name': 'WEBSITE',
                         'Classified listing type': 'CLASSIFIED_TYPE',
                         'Renew Url of the expired classified': 'RENEW_URL',
                         'Add more classified Url': 'ADD_URL'
                          },
                  'ufp': {
                         'Username of the account owner': 'USERNAME',
                         'Retrive Password Url': 'RETRIEVE_URL',
                         'Website Name': 'WEBSITE'
                          },
                  'apa': {
                         'Username of the account owner': 'USERNAME',
                         'Article title': 'ARTICLE_TITLE',
                         'Article listing type': 'ARTICLE_TYPE',
                         'Article url': 'ARTICLE_URL',
                         'Add more article Url': 'ADD_URL',
                         'Website Name': 'WEBSITE'
                    },
                  'cpc': {
                         'Username of the account owner': 'USERNAME',
                         'Classified Title': 'CLASSIFIED_TITLE',
                         'Website Name': 'WEBSITE',
                         'Classified listing type': 'CLASSIFIED_TYPE',
                         'Url of the classified': 'CLASSIFIED_URL'
                          },
                  'bpb': {
                         'Username of the account owner': 'USERNAME',
                         'Name of the business ': 'BUSINESS_NAME',
                         'Business Url': 'BUSINESS_URL',
                         'Business listing type': 'BUSINESS_TYPE',
                         'Website Name': 'WEBSITE'
                          },
                  'epe': {
                         'Username of the account owner': 'USERNAME',
                         'Event Title': 'EVENT_TITLE',
                         'Event listing type': 'EVENT_TYPE',
                         'Url of the event': 'EVENT_URL',
                         'Website Name': 'WEBSITE',
                         'Add more event Url': 'ADD_URL'
                          },
                  'gpg': {
                         'Username of the account owner': 'USERNAME',
                         'Gallery Name': 'GALLERY_NAME',
                         'Gallery Url': 'GALLERY_URL',
                         'Website Name': 'WEBSITE',
                         'Add more gallery Url': 'ADD_GALLERY_URL'
                          },
                  'vpv': {
                         'Username of the account owner': 'USERNAME',
                         'Website Name': 'WEBSITE',
                         'Add more video Url': 'ADD_VIDEO_URL',
                          },
                  'uui': {
                         'Site URL': 'SITE_URL',
                         'Username of the account owner': 'USERNAME',
                         'Website Name': 'WEBSITE'
                    },
                  'usu': {
                         'Username of the account owner': 'USERNAME',
                         'Login Password': 'PASSWORD',
                         'Login Url': 'LOGIN_URL',
                         'Website Name': 'WEBSITE'
                    },
                   'cwm': {
                          'Username of the account owner': 'USERNAME',
                          'Contest title':'CONTEST_TITLE',
                          'Contest Unique ID':'CONTEST_ID',
                          'Contest detail page URL':'CONTEST_URL',
                          'Contest home page URL':'CONTEST_HOME_URL',
                          'Website Name': 'WEBSITE'
                    },
                   'soc': {
                          'Username of the account owner': 'USERNAME',
                          'Order Id':'ORDER_ID',
                          'Price':'PRICE',
                          'Ordered Items':'ITEMS',
                          'Delivery Address':'DELIVERY_ADDRESS',
                          'Order Page URL':'ORDER_URL',
                          'Website Name': 'WEBSITE'
                    },
                   'sdc': {
                          'Username of the account owner': 'USERNAME',
                          'Order Id':'ORDER_ID',
                          'Ordered Items':'ITEMS',
                          'Website Name': 'WEBSITE'
                    },
                   'ssc': {
                          'Username of the account owner': 'USERNAME',
                          'Order Id':'ORDER_ID',
                          'Price':'PRICE',
                          'Ordered Items':'ITEMS',
                          'Shipping Method':'SHIPPING_METHOD',
                          'Delivery Address':'DELIVERY_ADDRESS',
                          'Order Page URL':'ORDER_URL',
                          'Website Name': 'WEBSITE'
                    },
                    'cpe': {
                          'Username of the account owner': 'USERNAME',
                          'Question, Answer or Post': 'ENTRY_TYPE',
                          'Name of Question, Answer or Post': 'ENTRY_NAME',
                          'Question, Answer or Post Url': 'ENTRY_URL',
                          'Add more Question, Answer or Post': 'ADD_URL',
                          'Website Name': 'WEBSITE'
                    },
                    'sun':{
                          'Username of the account owner': 'USERNAME',
                          'Name of the Business':'BUSINESS_NAME',
                          'Status of the request':'STATUS',
                          'Website Name': 'WEBSITE',
                       },
                   'ssn':{
                          'Username of the business owner': 'USERNAME',
                          'Name of the Business':'BUSINESS_NAME',
                          'Website Name': 'WEBSITE',
                      },
                   'ban':{
                          'Username of the account owner': 'USERNAME',
                          'Title of the banner ': 'BANNER_TITLE',
                          'Banner Type(Top, Bottom or Right)': 'BANNER_TYPE',
                          'Add more banners URL': 'ADD_URL',
                          'Website Name': 'WEBSITE'
                      }
    }

    try:data['dcrip'] = discription[code]
    except: data['dcrip'] = False
    try:email_temp = EmailTemplates.objects.get(code=code)
    except:email_temp = False
    data['code'] = code
    data['email_temp'] = email_temp

    templates = email_temp.template
    subject = email_temp.subject

    for aek in ALL_EMAIL_KEY:
        templates = templates.replace(ALL_EMAIL_KEY[aek], aek)
        subject = subject.replace(ALL_EMAIL_KEY[aek], aek)

    data['template'] = templates
    data['subject'] = subject
    return render_to_response(template, data, context_instance=RequestContext(request))

@admin_required
def email_savetemplate(request):
    try:
        emailtemp = EmailTemplates.objects.get(code=request.POST['template_code'])
        templates = request.POST['temp_content']
        subject = request.POST['subject']

        for aek in ALL_EMAIL_KEY:
            templates = templates.replace(aek, ALL_EMAIL_KEY[aek])
            subject = subject.replace(aek, ALL_EMAIL_KEY[aek])

        emailtemp.template = templates
        emailtemp.subject = subject
        emailtemp.save()
        messages.success(request, str(DEALS_MSG['ETS'])) 
        return HttpResponseRedirect(reverse('admin_configuration_emailtemplates'))
    except:
        messages.success(request, str(DEALS_MSG['ETNU'])) 
        return HttpResponseRedirect(reverse('admin_configuration_emailtemplates'))

####################Banner Ads ##################

@admin_required
def configuration_get_ads_content(request, template='admin/configuration/ajax-update-ads-content.html'):
    ''' ajax method for retrieving and updating module based banner info '''
    try:
        try: add_obj = BannerAdds.objects.get(name=request.REQUEST['module'])
        except: 
            add_obj = BannerAdds(name=request.REQUEST['module'], top="", right="", bottom="")
            add_obj.save()
        if request.POST:
            form = UpdateBannerContents(request.POST, instance=add_obj)
            if form.is_valid():
                form.save()
            else:
                data = {'add_obj':add_obj, 'form':form}
        else:form = UpdateBannerContents(instance=add_obj)
        data = {'add_obj':add_obj, 'form':form}
        html = render_to_string(template, data, context_instance=RequestContext(request))
        return_data = {'html':html, 'msg':str(CONFIG_MSG['BAUS']), 'mtype':get_msg_class_name('s')}
        return HttpResponse(simplejson.dumps(return_data))
    except:
        messages.success(request, str(HOME_MSG['OOPS'])) 
        return HttpResponseRedirect(reverse('admin_configuration_advertisement'))




########################Comments API Configurations ############

@admin_required
def configuration_general_comments(request, template='admin/configuration/comments-config.html'):
    ''' method for displaying the comments API config information '''
    try:comments_obj = CommonConfigure.objects.all()[:1][0]
    except:comments_obj = False
    data = {'comments_obj':comments_obj}
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required
def configuration_general_comments_update(request, template='admin/configuration/comments-api-settings.html'):
    ''' method for updating the comments API settings information '''
    comments_obj = CommonConfigure.objects.all()[:1][0]
    comments_obj.disqus_forum_name = request.POST['forum_name']
    comments_obj.save()

    data = {'comments_obj':comments_obj}
    html = render_to_string(template, data, context_instance=RequestContext(request))
    return_data = {'html':html, 'msg':str(API_MSG['CAUS']), 'mtype':get_msg_class_name('s')}
    return HttpResponse(simplejson.dumps(return_data))


######################## Misc Configurations ########################
@admin_required
def manage_misc(request, template='admin/configuration/manage-misc.html'):
    miscs = MiscAttribute.objects.all().order_by('-id')
    data = {'miscs':miscs}
    return render_to_response(template, data, context_instance=RequestContext(request))

@admin_required
def manage_things_to_do(request, template='admin/configuration/manage_things_to_do.html'):
    try:
        misc = MiscAttribute.objects.get(attr_key='VIATOR_URL')
        form = MiscAttributeForm(instance=misc)
    except:
        misc = False
        form = MiscAttributeForm()
    seoform = SEOForm()
    try:seo = ModuleNames.get_module_seo(name='thingstodo')
    except:seo = None
    if request.method == 'POST':
        if misc:
            form = MiscAttributeForm(request.POST, instance=misc)
        else:form = MiscAttributeForm(request.POST)
        if form.is_valid():
            form.save()
            if misc:msg_tp = 'TUS'
            else:msg_tp = 'TAS'
        seoform = SEOForm(request.POST)
        try:seo = ModuleNames.get_module_seo(name='thingstodo')
        except:seo = ModuleNames(name='thingstodo')
        if seoform.is_valid():
            title = seoform.cleaned_data.get('meta_title')
            description = seoform.cleaned_data.get('meta_description')
            seo.seo_title = title
            seo.seo_description = description
            seo.modified_by = request.user
            seo.save()
        if form.is_valid() and seoform.is_valid():
            messages.success(request, str(MISC_MSG[msg_tp])) 
            return HttpResponseRedirect(reverse('admin_config_manage_things_to_do'))
    data = {'form':form, 'misc':misc, 'seoform':seoform, 'seo':seo}
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required
def manage_golf(request, template='admin/configuration/manage_golf.html'):
    try:
        misc = MiscAttribute.objects.get(attr_key='GOLF_LINK')
        form = MiscAttributeForm(instance=misc)
    except:
        misc = False
        form = MiscAttributeForm()
    seoform = SEOForm()
    try:seo = ModuleNames.get_module_seo(name='golf')
    except:seo = None
    if request.method == 'POST':
        if misc:
            form = MiscAttributeForm(request.POST, instance=misc)
        else:form = MiscAttributeForm(request.POST)
        if form.is_valid():
            form.save()
            if misc:msg_tp = 'GUS'
            else:msg_tp = 'GAS'

        seoform = SEOForm(request.POST)
        try:seo = ModuleNames.get_module_seo(name='golf')
        except:seo = ModuleNames(name='golf')
        if seoform.is_valid():
            title = seoform.cleaned_data.get('meta_title')
            description = seoform.cleaned_data.get('meta_description')
            seo.seo_title = title
            seo.seo_description = description
            seo.modified_by = request.user
            seo.save()
        if form.is_valid() and seoform.is_valid():
            messages.success(request, str(MISC_MSG[msg_tp])) 
            return HttpResponseRedirect(reverse('admin_config_manage_golf'))
    data = {'form':form, 'misc':misc, 'seo':seo, 'seoform':seoform}
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required
def api_check_url_exist(request):
    try:
        test = urllib.urlopen(request.GET['url']).read()
        return HttpResponse('1')
    except:
        return HttpResponse('0')
    return HttpResponse()

@admin_required
def misc_add(request, id=False, template='admin/configuration/add-misc.html'):
    try:
        misc = MiscAttribute.objects.get(id=id)
        form = MiscAttributeForm(instance=misc)
    except:
        misc = False
        form = MiscAttributeForm()
    if request.method == 'POST':
        if misc:
            form = MiscAttributeForm(request.POST, instance=misc)
        else:
            form = MiscAttributeForm(request.POST)
        if form.is_valid():
            form.save()
            if misc:
                msg_tp = 'MUS'
            else:
                msg_tp = 'MAS'
            messages.success(request, str(MISC_MSG[msg_tp]))     
            return HttpResponseRedirect(reverse('admin_config_manage_misc'))
    data = {'form': form, 'misc': misc}
    return render_to_response (template, data, context_instance=RequestContext(request))


def misc_delete(request, id):
    try:
        misc = MiscAttribute.objects.get(id=id)
        misc.delete()
        messages.success(request, str(MISC_MSG['MDS'])) 
        return HttpResponseRedirect(reverse('admin_config_manage_misc'))
    except:
        messages.error(request, str(MISC_MSG['OOPS']))
        return HttpResponseRedirect(reverse('admin_config_manage_misc'))


@admin_required
def newsletter_configuration(request, template='admin/configuration/newsletter-config.html'):
    try:
        nwsltr_obj = NewsLetterApiSettings.objects.all()[:1][0]
    except:
        nwsltr_obj = False
    data = {'nwsltr_obj': nwsltr_obj}
    return render_to_response (template, data, context_instance=RequestContext(request))


@admin_required
def update_newsletter_api_settings(request, template='admin/configuration/include_newsletter_config.html'):
    try:
        nwsltr_obj = NewsLetterApiSettings.objects.all()[:1][0]
    except:
        nwsltr_obj = NewsLetterApiSettings()

    nwsltr_obj.option = request.POST['option']
    nwsltr_obj.api_key = request.POST['api_key']
    nwsltr_obj.list_id = request.POST['list_id']
    nwsltr_obj.subscribe_url = request.POST['sub_url']
    nwsltr_obj.save()

    data = {'nwsltr_obj': nwsltr_obj}
    html = render_to_string(template, data, context_instance=RequestContext(request))
    return_data = {'html': html, 'msg': str(API_MSG['NAUS']), 'mtype': get_msg_class_name('s')}
    return HttpResponse(simplejson.dumps(return_data))


@admin_required
def manage_comment_settings(request, template='admin/configuration/commentsettings.html'):
    data = {
         'apps': AvailableApps.objects.filter(status='A').exclude(comment='N').order_by('name'),
          }
    data['settings'] = CommentSettings.get_or_create_obj()

    try:
        data['msg'] = CONFIG_MSG[request.REQUEST['msg']]
    except:
        pass

    try:
        data['mtype'] = get_msg_class_name(request.REQUEST['mtype'])
    except:
        data['mtype'] = None

    return render_to_response(template, data, context_instance=RequestContext(request))


@admin_required
def update_comment_settings(request, template='admin/configuration/include_commentsettings.html'):
    apps = AvailableApps.objects.filter(status='A').exclude(comment='N').order_by('name')
    try:
        for a in apps:
            try:
                request.POST['app_%d' % (a.id)]
                a.comment = 'A'
            except:
                a.comment = "I"
            a.save()

        settings = CommentSettings.get_or_create_obj()


        settings.discuss_comment = request.POST.get('discuss_comment', False)
        if settings.discuss_comment:
            settings.discuss_shortcut = request.POST.get('discuss_shortcut', '')

        settings.like_dislike = request.POST.get('like_dislike', False)
        settings.flag = request.POST.get('flag', False)
        settings.approval = request.POST.get('approval', False)
        settings.threaded = request.POST.get('threaded', False)
        settings.anonymous = request.POST.get('anonymous', False)
        settings.avatar = request.POST.get('avatar', False)
        settings.rating = request.POST.get('rating', False)
        #settings.sort               = request.POST.get('sort','N')
        settings.save()
        msg = str(CONFIG_MSG['CSUS'])
        mtype = get_msg_class_name('s')
    except:
        msg = str(CONFIG_MSG['OOPS'])
        mtype = get_msg_class_name('e')

    data = {
         'apps': AvailableApps.objects.filter(status='A').exclude(comment='N').order_by('name'),
          }
    data['settings'] = CommentSettings.get_or_create_obj()

    html = render_to_string(template, data, context_instance=RequestContext(request))
    data = {'html': html, 'msg': msg, 'mtype': mtype}
    return HttpResponse(simplejson.dumps(data))

@admin_required
def configuration_site_email_settings(request, template='admin/configuration/site-email-settings.html'):
    try:
        smtp_settings_obj = SmtpConfigurations.objects.all()[:1][0]
    except:
        smtp_settings_obj = None
            
    form = SmtpConfigForm(instance = smtp_settings_obj)
    data = {'form':form}
    return render_to_response(template, data, context_instance=RequestContext(request))

@admin_required
def update_smtp_email_settings(request):
    try:
        smtp_settings_obj = SmtpConfigurations.objects.all()[:1][0]
    except:
        smtp_settings_obj = None
        
    form = SmtpConfigForm(instance = smtp_settings_obj)
    if request.method == "POST":
        form = SmtpConfigForm(request.POST, instance = smtp_settings_obj)
        if form.is_valid():
            update_smtp = form.save(commit = False)
            update_smtp.created_by = request.user
            update_smtp.default_from_mail = update_smtp.email_host_user
            update_smtp.save()
            status = True
        else:
            status = False   
    data = {'status':status, 'mtype':get_msg_class_name('s'), 'msg':str(UTILITY_MSG['SMTPSS'])}
    return HttpResponse(simplejson.dumps(data))

@admin_required
def test_smtp_connection(request):
    global_settings = get_global_settings()
    data = {}
    try:
        smtp_server = request.POST['email_host']
        port = int(request.POST['email_port'])
        secure_type = request.POST['secure_type']
        username = request.POST['email_host_user']
        passwd = request.POST['email_host_password']
        
        try:
            if secure_type == 'SSL':
                smptp_connection = smtplib.SMTP_SSL(smtp_server,port)
            else:
                smptp_connection = smtplib.SMTP(smtp_server,port)
            smptp_connection.ehlo()
            if secure_type == 'TLS':
                smptp_connection.starttls()
                smptp_connection.ehlo
            smptp_connection.login(username, passwd)
            
            subject = _('SMTP Email Config')
            email_message = global_settings.domain + _(' - Successful SMTP Email Configurations')
            header = 'To:' + username + '\n' + 'From: ' + username + '\n' + 'Subject: ' +subject + '\n'
            msg = header + '\n' + email_message + ' \n\n'
            smptp_connection.sendmail(username, [username,request.user.useremail,'shahanar@doublespring.com'], msg)
            smptp_connection.close()
            result_msg = _('Connected successfully!')
            status = True
            
        except (smtplib.SMTPException, gaierror), error:
            result_msg = 'Error while test connection ' +str(error)
            status = False
            
    except:
        status = False
        result_msg = 'Error while test connection ' +str(sys.exc_info())
        
    data['result_msg'] = result_msg
    data['status'] = status
    return HttpResponse(simplejson.dumps(data))
    
@admin_required
def clear_website_cache(request):
    try:
        cache.clear()
        status = True
        msg_cls = 's'
        msg = 'AUCCS'
    except:
        msg_cls = 'e'
        status = False
        msg = 'ERROR'
    return HttpResponse(simplejson.dumps({'status':status, 'mtype':get_msg_class_name(msg_cls), 'msg':str(UTILITY_MSG[msg])})) 

@admin_required
def update_global_search_index(request):
    from haystack.tasks import celery_rebuild_index
    try:
        result=celery_rebuild_index.delay()
        msg_cls = 's'
        msg = 'GSIS'
    except:
        msg_cls = 'e'
        msg = 'OOPS'
    """
    from haystack.management.commands import update_index
    try:
        update_index.Command().handle(using='default')
        msg_cls = 's'
        msg = 'GSIS'
    except:
        msg_cls = 'e'
        msg = 'OOPS'
    """
    return HttpResponse(simplejson.dumps({'mtype':get_msg_class_name(msg_cls), 'msg':str(UTILITY_MSG[msg])}))    


#from common.models import AvailableApps, Notification
#from hotels.models import Hotels
#from news.models import News

module_dict = {
    'article': Article,
    'event': Event,
    'videos': Videos,
    'movies': Movies,
    'attraction':Attraction,
    'banner':BannerAdvertisements,
    'bookmark':Bookmark,
    'business':Business,
    'classified':Classifieds,
    'deal':Deal,
    'photos':PhotoAlbum
}

def content_counts(useremail=None, usergroup="all", startdate=None, enddate=None, module=None, status='all'):
    counts = []
    module_obj_list = None
    if startdate and enddate:
        startdate = datetime.strptime(startdate, '%d/%m/%Y')
        enddate = datetime.strptime(enddate, '%d/%m/%Y')
    def get_status_list():
        if modulename != 'photos':
            obj_list = modelclass.objects.all()
        else:
            obj_list = modelclass.objects.filter(category__is_editable=True)
        if startdate and enddate:
            obj_list = obj_list.filter(created_on__range=(startdate, enddate))
        if usergroup != 'all':
            if useremail:
                obj_list = obj_list.filter(created_by__useremail=useremail)
            elif usergroup == 'user':
                obj_list = obj_list.filter(created_by__is_staff=False)
            elif usergroup == 'staff':
                obj_list = obj_list.filter(created_by__is_staff=True)
        
        obj_list = obj_list.order_by("-created_on")
        status_list = list(obj_list.values_list('status', flat=True))
        
        return (status_list, obj_list)
    
    for modulename, modelclass in module_dict.items():
        status_list, obj_list = get_status_list()
        if modulename == module:
            module_obj_list = obj_list
            if status != 'all':
                module_obj_list = module_obj_list.filter(status={
                    'drafted': 'D',
                    'pending': 'N',
                    'published': 'P',
                    'rejected': 'R',
                    'blocked': 'B',
                    'expired': 'E',
                    'scheduled': 'S'
                }[status])
        counts.append(
            {   'modulename': modulename,
                'count': [{
                    'total': len(status_list),
                    'drafted': status_list.count(u'D'),
                    'pending': status_list.count(u'N'),
                    'published': status_list.count(u'P'),
                    'rejected': status_list.count(u'R'),
                    'blocked': status_list.count(u'B'),
                    'expired': status_list.count(u'E'),
                    'scheduled': status_list.count(u'S'),
                },]
            }
        )
    return (counts, module_obj_list)

User = get_user_model()
ITEM_PER_PAGE=10

@admin_required
def admin_reports(request, template="admin/reports/index.html"):
    data = {}
    usergroup = request.GET.get("usergroup", "all")
    useremail = request.GET.get("useremail") if usergroup == "singleuser" else None
    data['content_counts'], data['object_list'] = content_counts(
        startdate=request.GET.get("startdate"),
        enddate=request.GET.get("enddate"),
        useremail=useremail,
        usergroup=usergroup,
        module=request.GET.get("module"),
        status=request.GET.get("status", "all"),
    )
    page = int(request.GET.get('page',1))
    data['page'] = page
    if data['object_list']:
        data['object_count'] = data['object_list'].count()
        pgdata = ds_pagination(data['object_list'], page, 'object_list',ITEM_PER_PAGE)
        data.update(pgdata)
    data['users'] = User.objects.all()
    data.update({
        'startdate': request.GET.get("startdate", ""),
        'enddate': request.GET.get("enddate", ""),
        'useremail': useremail,
        'module': request.GET.get("module", ""),
        'usergroup': usergroup,
        'status': request.GET.get("status", "all"), 
    })
    return render_to_response(template,data, context_instance=RequestContext(request))


def auto_suggest_user(request):
    try:
        data = User.objects.filter(display_name__icontains=request.GET['term'])
    except:
        data = User.objects.all()
    response_dict = {}
    child_dict = []
    response_dict.update({'results':child_dict})
    myfriends=[]
    for friend in data[:10]:
        b={'label':friend.display_name+" (%s)"%(friend.useremail),
           'id':friend.id,
           'value':friend.useremail,}
        myfriends.append(b)
    return HttpResponse(simplejson.dumps(myfriends))
        
@csrf_exempt
@admin_required
def upload_image_from_editor(request):
    form = UploadEditorImageForm(request.POST, request.FILES)
    
    if form.is_valid():
        photo = form.cleaned_data.get('upload')
    else:
        result = [{'error': form.non_field_errors()}]
        return HttpResponse(simplejson.dumps(result), mimetype='application/javascript')
    '''
    file_name = get_tempimg_path(photo.name)
    destination = open(settings.MEDIA_ROOT+file_name, 'wb+')
    
    for chunk in photo.chunks(): 
        destination.write(chunk)
    destination.close()
    '''
    
    photos = Photos()
    photos.photo = photo
    photos.caption = str(timezone.now())
    photos.created_by = request.user
    photos.save()
    
    return HttpResponse("""
    <script type='text/javascript'>
        window.parent.CKEDITOR.tools.callFunction(%s, '%s');
    </script>""" % (request.GET['CKEditorFuncNum'], photos.photo.url))
