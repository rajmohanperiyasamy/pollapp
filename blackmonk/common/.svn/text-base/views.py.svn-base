# Python Libs and methods
import datetime
import os
import urllib2
    
# Django Libs
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.db.models import Count
from django.template import Template, Context
from django.contrib import messages
from dateutil import rrule
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required

#Application Libs and Common Methods
from django.conf import settings as my_settings
from django.template.response import TemplateResponse

#Module Files(models,forms etc...)
from common.utils import get_global_settings
from common.user_messages import CONTACT_MSG
from common.weather import get_weather_network, get_weather_online
from common.forms import AdvertiseForm, ContactForm
from common.models import CommonFaq
from common.models import BannerAdds, WeatherApiSettings, ModuleNames, Pages, Views_Reports, Feedback, MiscAttribute, AvailableApps, AvailableModules

from community.models import Topic
from article.models import ArticleCategory
from attraction.models import AttractionCategory
from business.models import BusinessCategory
from classifieds.models import ClassifiedCategory
from classifieds.models import Classifieds
from events.models import EventCategory
from channels.models import Channel
#from forum.models import Category as DiscussionCategory
from gallery.models import PhotoCategory
from polls.models import Poll, Choices
from usermgmt.models import EmailTemplates
from videos.models import VideoCategory
from banners.models import HeroBanners
try:
    from collections import Counter
except:
    from common.utils import Counter
from django.db.models import get_model

project_path = lambda a: os.path.join(my_settings.PROJECT_PATH, a)

def __getpoll(request):
    import math,sys
    today = datetime.datetime.now()
    data = {}
    try:
        poll = Poll.objects.get(status="P")
        try:
            request.session['poll%s' % (poll.id)]
            data['status'] = 'voted'
        except:
            data['status'] = 'notvoted'
        data['choice'] = choice = Choices.objects.filter(poll=poll).order_by('id')
        total_votes = 0
        for c in choice:
            total_votes = total_votes + int(c.vote)
        data['total_votes'] = total_votes
        #if poll.expiry_date >= today.date():
        if poll.status == 'P':
            try:
                perc = []
                for c in choice:
                    vote_prcnt = (int(c.vote) * 1.0 / int(total_votes)) * 100
                    perc.append(int(vote_prcnt))

                results = []
                i = 0
                for c in choice:
                    results.append({'choice': c.choice, 'votes': c.vote, 'perc': perc[i]})
                    i += 1
                data['results'] = results
                data['poll_expire'] = True
            except:
                pass
        else:
            pass
    except:
        poll = False
    data['poll'] = poll
    return data


def get_poll_details(request):
    return __getpoll(request)

def favicon(request):
    global_settings = get_global_settings() 
    image_data =  global_settings.fav_ico
    return HttpResponse(image_data, mimetype="image/png")

def robot_txt(request):
    try:
        robot = MiscAttribute.objects.get(attr_key='ROBOT_TXT')
        robot = robot.attr_value
    except:
        global_settings = get_global_settings()
        robot = global_settings.domain
    return HttpResponse(robot, content_type="text/plain")

@cache_page(60 * 20)
def home(request, template="default/common/home.html"):
    ''' index page methods '''
    data = {}
    try:
        data['seo'] = ModuleNames.get_module_seo(name='home')
    except:
        pass
    polldata = __getpoll(request)
    banners = HeroBanners.objects.filter(status='P').order_by('display_order')
    data['hero_banners'] = banners 
    data.update(polldata)
    return TemplateResponse(request, template, data)


def get_banner_ads(request):
    ''' method for displaying banner ads for each module '''
    try:
        module = request.GET['url'].split('/')[3]
    except:
        module = 'home'

    try:
        if module == '':
            module = 'home'
    except:
        pass

    try:
        add_obj = BannerAdds.objects.get(name=module)
        data = {'right': add_obj.right, 'top': add_obj.top}
    except:
        data = {'right': False, 'top': False}
    return HttpResponse(simplejson.dumps(data))


#@cache_page(60 * 20)
def weather(request):
    ''' method for displaying weather conditions '''
    data = {}
    try:
        wx_api_obj = WeatherApiSettings.objects.all()[:1][0]
        if wx_api_obj.option == 'WO':
            return get_weather_online(request, wx_api_obj)
        else:
            return get_weather_network(request, wx_api_obj)
    except:
        wx_api_obj = False
        data['error']=True
        return render_to_response('default/common/world-weather.html',data,context_instance=RequestContext(request))


def coming_soon(request):
    return render_to_response('default/common/coming-soon.html', context_instance=RequestContext(request))

def things_to_do(request,template="default/common/places-to-see.html"):
    ''' viator partner things to do page iframe'''
    data = {}
    data['seo'] = ModuleNames.get_module_seo(name='thingstodo')
    #return TemplateResponse(request, template,data)
    return render_to_response(template, data, context_instance=RequestContext(request))


def golf(request,template="common/golf.html"):
    ''' GolfNow.com golf page iframe'''
    data = {}
    data['seo'] = ModuleNames.get_module_seo(name='golf')
    return TemplateResponse(request, template, data)


def resources(request, slug, template='default/common/resources.html'):
    data = {}
    try:
        page = Pages.objects.get(slug=slug, is_active=True)
    except:
        raise Http404
    data['page'] = page
    return render_to_response(template, data, context_instance=RequestContext(request))

def favicon(request, slug, template='default/common/resources.html'):
    global_settings = get_global_settings()
    file_name, file = None, None
    if slug=="favicon" and global_settings.fav_ico:
        file_name = project_path( global_settings.fav_ico.url[1:].replace('site_media', 'media') )
    elif slug=="apple-touch-icon" and global_settings.iphone_logo:
        file_name = project_path( global_settings.iphone_logo.url[1:].replace('site_media', 'media') )
    elif slug=="sitelogo" and global_settings.logo:
        file_name = project_path( global_settings.logo.url[1:].replace('site_media', 'media') )
    if file_name:
        file = open(file_name,'rb')
    response = HttpResponse(file, mimetype="image/gif")
    return response

def advertise(request, template='default/common/advertisewithus.html'):
    data = {}
    global_settings = get_global_settings()
    try:
        data['msg'] = CONTACT_MSG[request.GET['msg']]
    except:
        data['msg'] = False

    if not request.POST:
        try:
            data['form'] = AdvertiseForm(initial={'email': request.user.email})
        except:
            data['form'] = AdvertiseForm()
    else:
        form = AdvertiseForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.type = 'A'
            contact.save()
            data['contact'] = contact
            global_settings = get_global_settings()
            try:
                subject = "[Advertise with us] "
                to_emailids = []
                to_emailids.append(global_settings.info_email)
                email_message = render_to_string("default/common/contact-email.html", data,context_instance=RequestContext(request))
                email = EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
                email.content_subtype = "html"
                email.send()
            except:pass
            try:
                to_emailid = contact.email
                email_temp = EmailTemplates.objects.get(code='adv')
                s = Template(email_temp.subject)
                t = Template(email_temp.template)
                c = Context({ "USERNAME": contact.name, "WEBSITE": global_settings.domain})
                email_message = t.render(c)
                subject = s.render(c)
                to_emailids = []
                to_emailids.append(to_emailid)
                email = EmailMessage(subject, email_message, my_settings.DEFAULT_FROM_EMAIL, to_emailids)
                email.content_subtype = "html"
                email.send()
            except:
                pass
            messages.success(request, str(CONTACT_MSG['ADWS']))
            return HttpResponseRedirect(reverse('common_advertise'))
        else:
            data['form'] = form
    return render_to_response(template, data, context_instance=RequestContext(request))


def contact(request, template='default/common/contactus.html'):
    data = {}
    global_settings = get_global_settings()
    if request.method == 'GET':
        if request.user.is_authenticated():
            data['form'] = ContactForm(initial={
                'email': request.user.useremail,
                'name': request.user.display_name,
                'phone': request.user.phone,
            })
        else:
            data['form'] = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.type = 'C'
            contact.save()
            data['contact'] = contact
            try:
                subject = "Customer Enquiry / Feedback"
                to_emailids = [global_settings.info_email, ]
                email_message = render_to_string("default/common/contact-email.html", data, context_instance=RequestContext(request))
                email = EmailMessage(subject, email_message, my_settings.DEFAULT_FROM_EMAIL, to_emailids)
                email.content_subtype = "html"
                email.send()
            except:
                pass
            try:
                to_emailid = contact.email
                email_temp = EmailTemplates.objects.get(code='cnt')
                s = Template(email_temp.subject)
                t = Template(email_temp.template)
                c = Context({ "USERNAME": contact.name, "WEBSITE": global_settings.domain})
                email_message = t.render(c)
                subject = s.render(c)
                to_emailids = []
                to_emailids.append(to_emailid)
                email = EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL, to_emailids)
                email.content_subtype = "html"
                email.send()
            except:
                pass
            messages.success(request, str(CONTACT_MSG['CNAS']))
            return HttpResponseRedirect(reverse('common_contact'))
        else:
            data['form'] = form
    return render_to_response(template, data, context_instance=RequestContext(request))


def weddings(request, template='default/common/weddings-comingsoon.html'):
    return render_to_response(template, context_instance=RequestContext(request))


def restaurants(request, template='default/common/restaurants-comingsoon.html'):
    return render_to_response(template, context_instance=RequestContext(request))


def modules_elements_views(request):
    listing_types = {}
    Id = request.GET.get('bids', False)
    category = request.GET.get('category', False)
    pathname = request.GET.get('pathname', False)
    org_path = request.GET.get('org_path', False)
    clicks = request.GET.get('clicks', False)
    if clicks == 'false':
        click = False
    else:
        click = True
    if Id:
        Id_array = Id.split(',')
    else:
        Id_array = ['none']
    if category:
        category = category.split(',')
    else:
        category = "none"
    if pathname:
        pathname_split = pathname.split('/')
        module = pathname_split[1]
    if module == "articles":
        module = "article"
    elif module == 'photos':
        module = 'gallery'
    ip_addr = request.META.get('REMOTE_ADDR')
    url_pathnames = request.META.get('HTTP_REFERER')
    if org_path == '/' or org_path == '/business/':
        if module == 'business':
                listing_types = {}
                table_fields = {'business': ['name', 'featured_sponsored']}
                model_name = {'business': 'business'}
                model = get_model(module, model_name[module])
                for id in Id_array:
                    bis = model.objects.values_list(table_fields[module][0], table_fields[module][1]).get(id=id)
                    listing_types[id] = bis[1]
        else:
            listing_types = {}
            for id in Id_array:
                listing_types[id] = 'Normal'
    else:
            listing_types = {}
            for id in Id_array:
                listing_types[id] = 'Normal'

    object_list = []
    for id, listing in listing_types.items():
        report_obj = Views_Reports(element_id=id, module_name=module, referral_url=url_pathnames, viewed_on=datetime.datetime.now(), ip_address=ip_addr, listing_type=listing , clicks=click)
        object_list.append(report_obj)
    Views_Reports.objects.bulk_create(object_list)
    return HttpResponse('1')


def unique(list):
    output = []
    for x in list:
        if x not in output:
            output.append(x)
    else:
        pass
    return output

"""
def get_detailed_views(module, id):
    table_fields = {'videos': ['title', 'video_view'], 'events': ['title', 'visits'], 'deal': ['title', 'most_viewed'], 'business': ['name', 'most_viewed'], 'gallery': ['title', 'most_viewed'], 'article': ['title', 'most_viewed'], 'news': ['title', 'most_viewed']}
    model_name = {'events': 'event', 'article': 'article', 'videos': 'videos', 'deal': 'deal', 'business': 'business', 'galleries': 'photoAlbum', 'news': 'news'}
    model = get_model(module, model_name[module])
    bis = model.objects.values_list(table_fields[module][0], table_fields[module][1]).get(id=id)
    return bis
"""

def get_detail(module, id):
    model_name = {'events': 'event', 'article': 'article', 'videos': 'videos', 'movies': 'movies', 'business': 'business', 'gallery': 'photoalbum', 'classifieds':'classifieds'}
    model = get_model(module, model_name[module])
    bis = model.objects.get(id=id)
    return bis

@login_required
def get_modules_elements_views(request, id, modules,year):
    date=datetime.datetime.now()
    if year == '0' or int(year) == date.year:
        year = date.year
        month = date.month 
    else:
        year=year
        month = 12
    month_names = {}
    months_choices = {}
    start_date =  datetime.date(2012, 1, 1)
    end_date = date
    for i in range(1,month+1):
        month_names[i]=datetime.date(2008, i, 1).strftime('%B')
        months_choices[i]=""
    referral_url = []
    ip_address = []
    list_clicks=[]
    list_imp=[]
    for key in months_choices.keys():
        impression_list = Views_Reports.objects.filter(element_id=id, module_name=modules , viewed_on__year = year , viewed_on__month = key , clicks=False)
        clicks_list = Views_Reports.objects.filter(element_id=id, module_name=modules , viewed_on__year = year , viewed_on__month = key , clicks=True)
        months_choices[key] = {impression_list.count():clicks_list.count()}
        list_clicks.append(clicks_list.count())
        list_imp.append(impression_list.count())
    element = get_detail(modules,int(id))
    #start_date = element.created_on
    max_value = max([max(list_clicks),max(list_imp)])
    scaleStepWidth = float(float(max_value)/10)
    link=''
    if modules == 'article':
        link='article'
    data = {}
    data['modules'] = modules
    data['month_list'] = months_choices
    data['month_names']=month_names
    data['year'] = int(year)
    data['element'] = element  
    data['scaleStepWidth'] = scaleStepWidth  
    data['id']=id
    if link:data['link']=link
    data['modules']=modules
    years = list(rrule.rrule(rrule.YEARLY,dtstart=start_date,until=end_date))
    data['years'] = list(reversed(years))
    return render_to_response('default/view_reports.html', data, context_instance=RequestContext(request))


def get_traffic_sources(request, id, modules,year,month,type):
    data={}
    referral_url=[]
    ip_address=[]
    ip_address_click=[]
    counter=Counter()
    org_path=type
    if 'impression' in type:
        type="click"
        org_type="impression"
        impression_list = Views_Reports.objects.filter(element_id=id, module_name=modules , viewed_on__year = year , viewed_on__month = month,clicks=False)
    else:
        org_type='click'
        type="impression"
        impression_list = Views_Reports.objects.filter(element_id=id, module_name=modules , viewed_on__year = year , viewed_on__month = month,clicks=True)
    for buz in impression_list:
        refer_url = ""
        refer_url = buz.referral_url
        refer_url = str(refer_url)
        referral_url.append(refer_url)
        ip_addr = ""
        ip_addr = buz.ip_address
        ip_addr = str(ip_addr)
        ip_address.append(ip_addr)
    #ip_address = unique(ip_address)
    for url in ip_address:
        counter[url] += 1
    a = []
    b = []
    for k, v in counter.items():
        a.append(k)
        b.append(v)
    result=[]
    Referr = dict(zip(a, b))
    result.append(Referr)
    NO_OF_ITEMS_PER_PAGE=10
    data['Referr'] = Referr
    data['id']=id
    data['modules']=modules
    data['year']=year
    data['type']=type
    data['month']=month
    data['org_path']=org_path
    return render_to_response('default/view_sources.html', data, context_instance=RequestContext(request))

def google_verify(request, code=None):
    if code:
        gc = ''.join(['google-site-verification: google', code, '.html'])
        return HttpResponse(gc)
    else:
        return HttpResponse('Error')


def feedback(request):
    try:
        data = {
          'topic': request.POST['topic'],
          'fdbk_name': request.POST['fdbk_name'],
          'type': request.POST['type'],
          'fdbk_to_email': request.POST['fdbk_to_email'],
          'fdbk_msg': request.POST['fdbk_msg']
          }
        feedback = Feedback(name=data['fdbk_name'], email=data['fdbk_to_email'], message=data['fdbk_msg'], type=data['type'], module=data['topic'], user=request.user)
        feedback.save()
        global_settings = get_global_settings()
        subject = "[Feedback] "
        to_emailids = []
        to_emailids.append(global_settings.info_email)
        email_message = render_to_string("default/common/feedback.html", data, context_instance=RequestContext(request))
        email= EmailMessage(subject, email_message, my_settings.DEFAULT_FROM_EMAIL, to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass
    try:
        to_emailid = data['fdbk_to_email']
        email_temp = EmailTemplates.objects.get(code='fdb')
        s = Template(email_temp.subject)
        t = Template(email_temp.template)
        c = Context({ "USERNAME": data['fdbk_name'],"WEBSITE": global_settings.domain})
        email_message = t.render(c)
        subject = s.render(c)
        to_emailids = []
        to_emailids.append(to_emailid)
        email = EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
        return HttpResponse('1')
    except:
        return HttpResponse('0')


def sitemap(request):
    apps = AvailableApps.objects.filter(sitemap='A', status='A').order_by('name')
    sitemaps = []

    general_linkes = []
    general_linkes.append({'name': 'Home', 'url': '/'})
    for app in apps:
        general_linkes.append({'name': app.name, 'url': '/' + str(app.slug)})
    general = {'name': 'General', 'slug': 'general', 'links': general_linkes}
    sitemaps.append(general)

    for app in apps:
        x = {}
        if app.slug == 'movies':
            x = {
             'name': 'Movies', 'slug': 'movies',
             'links': [
                        {'name': 'Home', 'url': '/movies/'},
                        {'name': 'All Movies', 'url': '/movies/all/'},
                        {'name': 'Now Playing', 'url': '/movies/nowplaying/'},
                        {'name': 'Upcoming', 'url': '/movies/upcoming/'},
                        {'name': 'Showtimes', 'url': '/movies/showtimes/'},
                        {'name': 'Theatre Showtimes', 'url': '/movies/theatre-showtimes/'}
                    ]
             }
        elif app.slug == 'deals':
            x = {
             'name': 'Deals', 'slug': 'deals',
             'links': [
                        {'name': 'Home', 'url': '/deals/'},
                        {'name': 'All Deals', 'url': '/deals/all/'},
                        {'name': 'How it Works', 'url': '/deals/how_it_works/'},
                        {'name': "FAQ's", 'url': '/deals/faqs/'},
                        {'name': 'Contact', 'url': '/deals/contact/'}
                    ]
             }
        else:
            links = []
            if app.slug !='channel':
                links.append({'name': 'Home', 'url': '/' + app.slug})

            if app.slug == 'community':
                category = Topic.objects.all().order_by('name')

            elif app.slug == 'articles':
                category = ArticleCategory.objects.all().order_by('name')

            elif app.slug == 'attractions':
                category = AttractionCategory.objects.all().order_by('name')

            elif app.slug == 'business':
                category = BusinessCategory.objects.filter(parent_cat__isnull=True).order_by('name')

            elif app.slug == 'classifieds':
                category = ClassifiedCategory.objects.filter(parent__isnull=True).order_by('name')

            #elif app.slug == 'discussions':
                #category = DiscussionCategory.objects.all().order_by('name')

            elif app.slug == 'events':
                category = EventCategory.objects.all().order_by('name')

            elif app.slug == 'photos':
                category = PhotoCategory.objects.all().order_by('name')

            elif app.slug == 'videos':
                category = VideoCategory.objects.all().order_by('name')
                
            elif app.slug == 'channel':
                category = Channel.objects.filter(status = 'P').order_by('title')    

            if category:
                for cat in category:
                    links.append({'name': cat, 'url': cat.get_absolute_url()})

            x = {'name': app.name, 'slug': app.slug, 'links': links}

        if x:
            sitemaps.append(x)

    accounts = {
             'name': 'Account', 'slug': 'account',
             'links': [{'name': 'Sign In', 'url': '/account/signin/'}, {'name': 'Register', 'url': '/account/signup/'}]
             }
    sitemaps.append(accounts)

    legal = {
             'name': 'Legal', 'slug': 'legal',
             'links': [
                      {'name': 'Terms and Service', 'url': '/terms-of-use.html'},
                      {'name': 'Privacy Policy', 'url': '/privacy-policy.html'},
                      {'name': 'Disclaimer', 'url': '/disclaimer.html'}
                    ]
             }
    sitemaps.append(legal)

    data={'sitemaps': sitemaps}
    return render_to_response('default/sitemap.html', data, context_instance=RequestContext(request))

def get_google_plus_count(request):
    ''' used for getting the google plus count for a particular url'''
    result = {}
    try:
        check_url = request.GET['url']
        gplus_url = "https://plusone.google.com/u/0/_/+1/fastbutton?url="+check_url
        response_html = urllib2.urlopen(gplus_url)
        soup = BeautifulSoup(response_html)
        total_count = soup.find("div", {"id": "aggregateCount"}).string
        
        if 'k' in total_count:
            total_count = total_count.split('k')[0]
            total_count = 1000*float(total_count)
        elif 'M' in total_count:
            total_count = total_count.split('M')[0]
            total_count = 1000000*float(total_count)
        
        result['count'] = total_count
    except:
        result['count'] = 0
            
    return HttpResponse(simplejson.dumps(result))

def get_menu_id(request):
    url = request.GET['url']
    try:
        m = AvailableModules.objects.get(base_url=url, level__in=["header", "submenu"])
        return HttpResponse(str(m.parent_id if m.parent_id else m.id))
    except:
        url = url.split("//")[1]
        url = url[url.index('/'):]
        try:
            m = AvailableModules.objects.get(base_url=url, level__in=["header", "submenu"])
        except:
            try: 
                m = AvailableModules.objects.get(base_url = "/"+url.split('/')[1]+'/', level__in=["header", "submenu"])
            except:
                from sys import exc_info 
                return HttpResponse(exc_info())
    return HttpResponse(str(m.parent_id if m.parent_id else m.id))

def load_fb_box(request):
    """ Loads the facebook like box for new templates """
    data={}
    send_data={}
    width = request.GET.get('window_width',False)
    data['globalsettings']  = get_global_settings()
    try:
        if width>=767:
            html = render_to_string("minimal/likebox.html", data, context_instance=RequestContext(request))
            send_data['html'] = html
            send_data['status'] = True
        else:
            send_data['status'] = False
    except:
        send_data['status'] = False
    return HttpResponse(simplejson.dumps(send_data))

def faq(request, template='default/common/faqs.html'):
    try:
        faq_obj = CommonFaq.objects.all()
    except:
        faq_obj = False
    data = {'faq_list': faq_obj}
    return render_to_response(template, data, context_instance=RequestContext(request))


