from xml.dom import minidom
import urllib2
import random
import cPickle as pickle
import base64
import urllib
import os
import datetime
from random import random
try:
    from hashlib import sha1
except ImportError:
    import sha
from django.template import  Template,Context
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse ,Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist , ImproperlyConfigured
from django.core.mail import EmailMessage,send_mail
import pycurl
import cStringIO
import urllib
from xml.dom import minidom

from django.template.loader import render_to_string
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth import authenticate, login ,REDIRECT_FIELD_NAME
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import *
from django.views.decorators.cache import never_cache
from django.utils import simplejson
from django.utils.http import urlquote_plus
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _
from django.core.cache import cache
from django.conf import settings as my_settings
from django.template.defaultfilters import slugify
from common.getunique import getUniqueValue

from common.utils import  *
from common.forms import  *
from usermgmt.models import  *
from usermgmt.forms import *
from locality.models import  Locality
from usermgmt.adminviews import  *
from usermgmt.newsletter import ajax_subscripe_newsletter
from django.db.models import Count
from business.models import Business
from article.models import Article
from attraction.models import Attraction
from classifieds.models import Classifieds
from deal.models import Deal
from events.models import Event
#from forum.models import Forum
from gallery.models import PhotoAlbum
from hotels.models import Hotels
from common.models import HomeFeatureContent,Notification,AvailableApps,SignupSettings
from movies.models import Movies
from news.models import News
from bookmarks.models import Bookmark
from videos.models import Videos

from common.templatetags.ds_utils import get_msg_class_name
from common.user_messages import USERMGMT_MSG

from random import choice
from string import letters
from common import signals
try:
    from openid.yadis import xri
except ImportError:
    from yadis import xri

def ajax_auth_close_popup(request):
    data={'auth_compleated':True}
    return render_to_response('account/ajax_signin_other.html',data,context_instance=RequestContext(request))

def ajax_newsletter(request):
    data = {}
    if request.method=='POST':
        try:name=request.POST['name']
        except:
            try:name=request.user.display_name
            except:name=''
        try:mailtype=request.POST['mailtype']
        except:mailtype='html'
        return ajax_subscripe_newsletter(name,request.POST['email'],mailtype)
    #else:return HttpResponse('0')
    return render_to_response('general/newsletter.html',data,context_instance=RequestContext(request))
        
def ajax_signup(request):
    if request.method == 'POST':
        data = request.POST.copy() # so we can manipulate data
        try:
            name=request.POST['useremail'].split('@')[0]
            data['username']=getUniqueValue(User,slugify(name),field_name='useremail')
        except:
            data['username'] = ''.join([choice(letters) for i in xrange(20)])
        form = SignUpForm(data)
        if form.is_valid():
            email = form.cleaned_data.get('useremail')
            username = form.cleaned_data.get('useremail')
            password = form.cleaned_data.get('password1')
            newuser = form.save()
            privacy = ProfilePrivacy(profile=newuser)
            privacy.save()
            user=authenticate(username=email, password=password)
            login(request, user)
            try:signup_mail(email,password,form.cleaned_data.get('useremail'))
            except:pass
            signals.create_notification.send(sender=None,user=newuser, obj=newuser, not_type='joined')
            return HttpResponse('1')
        else:
            return HttpResponse('0')
    else:
        data = {
            'form': SignUpForm(),
            'type': request.GET.get('type'),
            'val': request.GET.get('val'),
            'next': request.GET.get('next'),
        }
        return render_to_response('default/account/ajax_signup.html', data,
                              context_instance=RequestContext(request))
    
def ajax_signin(request):
    if request.method=='POST':
        try:
            user = authenticate(username=request.POST['email'],password=request.POST['password'])
            if user:
                login(request, user)
                return HttpResponse('1')
            else:return HttpResponse('0')
        except:
            return HttpResponse('0')
    else:
        data = {
            'type': request.GET.get('type'),
            
            'next': request.GET.get('next'),
        }
        val = request.GET.get('val')
        data['val'] = val if val else False
        return render_to_response('default/account/ajax_signin.html',data,context_instance=RequestContext(request))


def signup_mail(username,password,email):
    global_settings = get_global_settings()
    to_emailid = [email]
    email_temp = EmailTemplates.objects.get(code='usu')
    s = Template(email_temp.subject)
    sub = Context({"WEBSITE": global_settings.domain})
    subject = s.render(sub)
    t= Template(email_temp.template)
    c= Context({ "USERNAME": username,"PASSWORD": password,"LOGIN_URL": global_settings.website_url+my_settings.LOGIN_URL,"WEBSITE": global_settings.domain})
    email_message=t.render(c)
    email= EmailMessage(subject,email_message,my_settings.DEFAULT_FROM_EMAIL,to_emailid)
    email.content_subtype = "html"
    email.send()


def sign_up(request):
    """ User sign up form """
    redirect_to = request.REQUEST.get('next', '')
    if request.method == 'POST':
        data = request.POST.copy() # so we can manipulate data
        try:
            name=request.POST['useremail'].split('@')[0]
            data['username']=getUniqueValue(User,slugify(name),field_name='useremail')
        except:
            data['username'] = ''.join([choice(letters) for i in xrange(20)])
        form = SignUpForm(data)
        if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
            redirect_to = my_settings.LOGIN_REDIRECT_URL
        if form.is_valid():
            email = form.cleaned_data.get('useremail')
            username = form.cleaned_data.get('useremail')
            password = form.cleaned_data.get('password1')
            newuser = form.save()
            privacy = ProfilePrivacy(profile=newuser)
            privacy.save()
            user=authenticate(username=email, password=password)
            login(request, user)
            try:signup_mail(email,password,form.cleaned_data.get('useremail'))
            except:pass
            signals.create_notification.send(sender=None,user=newuser, obj=newuser, not_type='joined')
            return HttpResponseRedirect(redirect_to)
    else:
        form = SignUpForm()
    return render_to_response('account/signup.html', {'form':form,'next':redirect_to},
                              context_instance=RequestContext(request))

################################################################################################################################
#                                                INVITE FRIENDS                                                                #
################################################################################################################################

@login_required
def user_invite(request,template="account/invite.html"):
    data={}
    code=request.GET.get('code',None)
    if code:
        try:
            data['contacts']=get_contact(code)
        except:
            data['msg']=USERMGMT_MSG['OOPS']
            data['mtype'] =get_msg_class_name('e')
    data['signup'] = SignupSettings.get_or_create_obj() 
    data['clientid'] = my_settings.GC_CLIENT_ID
    data['load_more'] = 1
    return render_to_response(template, data,context_instance=RequestContext(request))

def get_contact(code):
    authcode= code
    clientid=my_settings.GC_CLIENT_ID;
    clientsecret=my_settings.GC_CLIENT_SECRET;
    
    #redirecturi='http://localhost/account/profile/invite/';
    global_settings = get_global_settings()
    redirecturi=global_settings.website_url+'/account/profile/invite/';
    
    response = cStringIO.StringIO()
    c = pycurl.Curl() 
    c.setopt(c.URL,"https://accounts.google.com/o/oauth2/token")
    c.setopt(c.POST, 5)
    request={'code':code,'client_id':clientid,'client_secret':clientsecret,'redirect_uri':redirecturi,'grant_type':'authorization_code'}
    request=urllib.urlencode(request)
    c.setopt(c.POSTFIELDS, request);
    c.setopt(c.SSL_VERIFYPEER,False);
    c.setopt(c.WRITEFUNCTION, response.write)
    c.perform()
    c.close()
    result=eval(response.getvalue())
    request.session['REQUEST_TOKEN']=result['access_token']
    contacts=minidom.parse(urllib.urlopen('https://www.google.com/m8/feeds/contacts/default/full?start-index=1&max-results=200&oauth_token='+request.session['REQUEST_TOKEN']))
    contacts=contacts.getElementsByTagName('entry')
    data_list=[]
    for contact in contacts:
        try:
            #id=contact.getElementsByTagName("id")[0].firstChild.nodeValue.splat('/base/')[1]
            try:name=contact.getElementsByTagName("title")[0].firstChild.nodeValue
            except:name=''
            email=contact.getElementsByTagName("gd:email")[0].attributes["address"].value
            data={'name':name,'email':email}
            data_list.append(data)
        except:pass
    return data_list

def get_contact_more(count):
    contacts=minidom.parse(urllib.urlopen('https://www.google.com/m8/feeds/contacts/default/full?start-index='+str(count)+'&max-results=200&oauth_token='+request.session['REQUEST_TOKEN']))
    contacts=contacts.getElementsByTagName('entry')
    data_list=[]
    for contact in contacts:
        try:
            try:name=contact.getElementsByTagName("title")[0].firstChild.nodeValue
            except:name=''
            email=contact.getElementsByTagName("gd:email")[0].attributes["address"].value
            data={'name':name,'email':email}
            data_list.append(data)
        except:pass
    return data_list

@login_required
def user_invite_google_more(request,template="account/google_more.html"):
    data={}
    try:
        sdata={}
        count=int(request.GET.get('count',1))
        sdata['contacts']=get_contact_more(count)
        sdata['length']=len(sdata['contacts'])
        data['length']= sdata['length']
        data['count']=count+200
        data['html']=render_to_string(template,sdata,context_instance=RequestContext(request))
        data['status']=1
    except:
        data['status']=0
    return HttpResponse(simplejson.dumps(data))


@login_required
def user_invite_google(request,template="account/google_contact.html"):
    data={}
    try:
        from usermgmt.google_contacts import ContactsSample
        obj=ContactsSample(request.POST['email'],request.POST['password'])
        clist=obj.AllContacts()
        data['html']=render_to_string(template,{'clist':clist},context_instance=RequestContext(request))
        data['status']=1
    except:
        data['status']=0
    return HttpResponse(simplejson.dumps(data))

@login_required
def user_invite_mail(request):
    import re
    global_settings=get_global_settings()
    valid = []
    invalid = []
    try:
        try:to_emailids=request.POST['mails'].split(',')
        except:to_emailids=[request.POST['mails']]
        total = len(to_emailids)
        for emil in to_emailids:
            if re.match(r'[\w.-]+@[\w.-]+', emil):
                valid.append(emil)
            else:
                invalid.append(emil)
        email_temp = EmailTemplates.objects.get(code='uui')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        
        c= Context({ 
            "USERNAME": request.user.display_name,
            "WEBSITE": global_settings.domain,
            "SITE_URL": "<a href='%s'>%s</a>" % (
                 global_settings.website_url,
                 global_settings.website_url
             ),
        })
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,valid)
        email.content_subtype = "html"
        email.send()
        if total == len(valid):
            return HttpResponse('1')
        else:
            return HttpResponse(len(valid))
    except:
        return HttpResponse('0')


@login_required
def user_profile(request,template="account/profile.html"):
    data = {}
    form = ProfileEditForm()
    try:
        profile = request.user
        form = ProfileEditForm(instance=profile)
    except:
        profile = None
        form = ProfileEditForm()
        messages.error(request, str(USERMGMT_MSG['OOPS']))
    if request.method == 'POST':
        form = ProfileEditForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, str(USERMGMT_MSG['PSU']))
        else:
            messages.error(request, str(USERMGMT_MSG['OOPS']))
    return render_to_response(template, {'form':form,'profile':profile,},context_instance=RequestContext(request))

from common.fileupload import upload_profile_pic,delete_profile_photo

@login_required
def update_profile(request):
    try:
        profile = request.user
        profile.display_name = request.POST.get("name",None)
        profile.about = request.POST['bio']
        profile.save()
        signals.create_notification.send(sender=None,user=profile, obj=profile, not_type='updated his profile in')
        data = {'status':1,'name':profile.display_name,'bio':profile.about,'msg':str(USERMGMT_MSG['PSU']),'mtype':get_msg_class_name('s') }
    except:
        data = {'msg':str(USERMGMT_MSG['OOPS']),'mtype':get_msg_class_name('e') }    
    return HttpResponse(simplejson.dumps(data))

@login_required
def update_email(request):
    try:
        user=User.objects.get(id=request.POST['id'])
        email = request.POST['email']
    except:
        data = {'msg':str(USERMGMT_MSG['OOPS']),'mtype':get_msg_class_name('e') }  
        return HttpResponse(simplejson.dumps(data))      
    if not email== request.user.email:
        users = User.objects.filter(email = email)
        if users:
            data = {'msg':str(USERMGMT_MSG['EAU']),'mtype':get_msg_class_name('e') }  
            return HttpResponse(simplejson.dumps(data))      
        else:
            user.email = email 
            user.save()
        
    data = {'status':1,'email':email}                         
    return HttpResponse(simplejson.dumps(data))

@login_required
def add_social_profiles(request,template='account/ajax_social_profiles.html'):
    try:
        profile=Profile.objects.get(user=request.POST['id'])
        social_profile = SocialProfiles()
        social_profile.media = request.POST['media']
        social_profile.media_url = request.POST['url']
        social_profile.label = request.POST.get("label",None)
        social_profile.profile = profile
        social_profile.save()
        html=render_to_string(template,{'profile':profile})
        data = {'status':1,'html':html}  
        return HttpResponse(simplejson.dumps(data)) 
    except:
        data = {'msg':str(USERMGMT_MSG['OOPS']),'mtype':get_msg_class_name('e') }  
    return HttpResponse(simplejson.dumps(data))

@login_required
def delete_social_profiles(request,template='account/ajax_social_profiles.html'):
    try:
        profile=Profile.objects.get(user=request.POST['pid'])
        social = SocialProfiles.objects.get(id=request.POST['id'])
        social.delete()
        html=render_to_string(template,{'profile':profile})
        data = {'status':1,'html':html}  
        return HttpResponse(simplejson.dumps(data)) 
    except:
        data = {'msg':str(USERMGMT_MSG['OOPS']),'mtype':get_msg_class_name('e') }  
    return HttpResponse(simplejson.dumps(data))

@login_required
def update_social_profiles(request,template='account/ajax_social_profiles.html'):
    try:
        profile=Profile.objects.get(user=request.POST['pid'])
        social = SocialProfiles.objects.get(id=request.POST['id'])
        social.media_url = request.POST['url']
        social.label = request.POST['label']
        social.save()
        html=render_to_string(template,{'profile':profile})
        data = {'status':1,'html':html}  
        return HttpResponse(simplejson.dumps(data)) 
    except:
        data = {'msg':str(USERMGMT_MSG['OOPS']),'mtype':get_msg_class_name('e') }  
    return HttpResponse(simplejson.dumps(data))

@login_required
def ajax_upload_photos(request):  
    profile = request.user
    return upload_profile_pic(request,profile)

@login_required
def ajax_delete_photos(request,pk):
    try:
        photo_obj = request.user
        return delete_profile_photo(request,photo_obj)
    except: return HttpResponse("Error in delete photo")    


@login_required
def change_password(request,template="account/change-password.html"):
    data = {}
    form = PasswordReset(request.user)
    if request.method == "POST":
        form = PasswordReset(request.user,request.POST)
        if form.is_valid():
            user=User.objects.get(id=request.user.id)
            user.set_password(form.cleaned_data.get('password2'))
            user.save()
            messages.success(request, str(USERMGMT_MSG['UPS']))
            return HttpResponseRedirect(reverse('usermgmt_viewprofile'))
        else:
            data['form'] = form
            return render_to_response(template ,data,context_instance=RequestContext(request))
    else:
        data['form'] = form
        return render_to_response(template,data,context_instance=RequestContext(request))

def  forgotpwd(request,template="default/account/forgotpwd.html"):
    data={}
    if request.method == 'POST':
        error=success=False
        global_settings = get_global_settings()
        email=request.POST['email'].lower()
        try:
            user=User.objects.get(useremail=email)
            success=True
        except:error=True
        try:  
            try:code = sha1(str(random())).hexdigest()[:16]
            except:code = sha.new(str(random())).hexdigest()[:16]
            
            try:
                retivepwd=RetivePwd.objects.get(user=user)
                date=datetime.datetime.now()+datetime.timedelta(days=7)
                if retivepwd.date.date() > date.date():
                    retivepwd.code=code
                    retivepwd.date=datetime.datetime.now()
                    retivepwd.save()
                else:pass
            except:
                retivepwd=RetivePwd(user=user,code=code)
                retivepwd.save()
            slug_email=slugify(user.useremail)
                    
            to_emailid = [email]
            email_temp = EmailTemplates.objects.get(code='ufp')
            s = Template(email_temp.subject)
            sub = Context({"WEBSITE": global_settings.domain})
            subject = s.render(sub)
            t= Template(email_temp.template)
            c= Context({"USERNAME": user.display_name,"RETRIEVE_URL": str(global_settings.website_url)+"/account/retrivepwd/"+str(retivepwd.code)+"/"+str(slug_email)+"/"+str(retivepwd.id),
                        "WEBSITE": global_settings.domain})
            email_message=t.render(c)
            email= EmailMessage(subject,email_message,my_settings.DEFAULT_FROM_EMAIL,to_emailid)
            email.content_subtype = "html"
            email.send()
        except:
            pass    
        data={'success':success,'error':error}
        return render_to_response(template,data,context_instance=RequestContext(request))
    else:
        try:
            if request.GET['msg']=='INVDLINK':data['msg']='Oops!!! Invalid link.'
            elif request.GET['msg']=='EXPLINK':data['msg']='Oops!!! Link expired.'
        except:pass
        return render_to_response(template,data,context_instance=RequestContext(request))


def retrive_password(request,code,email,id,template="default/account/retrive-password.html"):
    try:
        retivepwd=RetivePwd.objects.get(code=code,id=id)
        rdate=retivepwd.date
        date=datetime.datetime.now()+datetime.timedelta(days=+7)
        if date.date()<rdate.date():return HttpResponseRedirect(reverse('usermgmt_forgotpwd')+'?msg=EXPLINK')
    except:
        return HttpResponseRedirect(reverse('usermgmt_forgotpwd')+'?msg=INVDLINK')
    if slugify(retivepwd.user.useremail)!=email:
        return HttpResponseRedirect(reverse('usermgmt_forgotpwd')+'?msg=INVDLINK')
    form = RetrivePassword(request.user)
    if request.method == "POST":
        form = RetrivePassword(request.user,request.POST)
        if form.is_valid():
            user=User.objects.get(id=retivepwd.user.id)
            user.set_password(form.cleaned_data.get('password2'))
            user.save()
            retivepwd.delete()
            return HttpResponseRedirect(reverse('usermgmt_viewprofile')+'?msg=UPS&mtype=s')
        else:
            data={'code':code,'id':id,'email':email,'form':form}
            return render_to_response(template ,data,context_instance=RequestContext(request))
    else:
        data={'code':code,'id':id,'email':email,'form':form}
        return render_to_response(template,data,context_instance=RequestContext(request))
 
    
@never_cache
def user_status(request):
    
    context = {}
    context['is_authenticated'] = request.user.is_authenticated()
    
    if request.GET.get('notices'):
        context['messages'] = request.messages.get_and_clear()
 
    if context['is_authenticated']:
        context['username'] = request.user.display_name
        context['user_id'] = request.user.id 
    context['mob_html'] = render_to_string('default/mobile_user_status.html',{'user':request.user,}, context_instance=RequestContext(request))
    context['status_html'] = render_to_string('default/user_status.html',{'user':request.user,}, context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps(context))


@login_required
def modules_data(request):
    user = request.user
    dict_list = []
    list_dict = {}
    total_modules={}
    apps=[app.module_name for app in AvailableApps.get_active_apps_module_name()]
    tb_list_dict = {}
    
    if 'events' in apps:
        tb_list_dict['Events']=Event
    if 'article' in apps:
        tb_list_dict['Articles']=Article
    if 'videos' in apps:
        tb_list_dict['Videos']=Videos
    if 'classifieds' in apps:
        tb_list_dict['Classifieds']=Classifieds
    if 'business' in apps: 
        tb_list_dict['Business']=Business
    if 'gallery' in apps:
        tb_list_dict['Galleries']=PhotoAlbum

    for module,tb_name in tb_list_dict.items():
        data_a= total_posts_by_users(tb_name,user)
        list_dict[module] = data_a
    for module,value in list_dict.items():
        value['Published'] = value.pop('P')
        value['Draft'] = value.pop('D')
        value['Rejected'] = value.pop('R')
        value['Pending'] = value.pop('N')
        value['Blocked'] = value.pop('B')
        value['Expired'] = value.pop('E')
        total_modules[module] = value['total']
        del value['total']
    return_data = {}
    return_data['list_dict']=list_dict
    return_data['total_modules']=total_modules
    return_data['recent_activity']=recent_activity(user,apps)
    return_data['user']=user
    return_data['apps']=apps
    return render_to_response('default/common/user-dashboard.html',return_data, context_instance=RequestContext(request)) 
    

def total_posts_by_users(tb_name,user):
    try:
        if tb_name.__name__ == "PhotoAlbum":
            users_data=tb_name.objects.values('status').filter(created_by=user, category__is_editable=True).annotate(s_count=Count('status'))
        else:
            users_data=tb_name.objects.values('status').filter(created_by=user).annotate(s_count=Count('status'))
        total = 0
        status_counts={'P':0,'N':0,'S':0,'R':0,'B':0,'D':0,'E':0,'total':0}
        for st in users_data:
            status_counts[st['status']]+=st['s_count']
            total+=st['s_count']
        status_counts['total'] = total
    except:
        if tb_name.__name__ == "PhotoAlbum":
            users_data=tb_name.objects.filter(created_by=user, category__is_editable=True)
        else:
            users_data=tb_name.objects.filter(created_by=user)
        status_counts={'P':0,'N':0,'S':0,'R':0,'B':0,'D':0,'E':0,'total':0}
        status_counts['total'] = users_data.count()
    return status_counts


def recent_activity(user,apps):
    recent_activity = Notification.objects.filter(user_id = user.id,content_type__app_label__in=apps).order_by('-id')[:10]
    return recent_activity

@login_required
def contact_info(request,template="account/contact_info.html"):
    form = ContactEditForm()
    try:
        profile = request.user
        form = ContactEditForm(instance=profile)
    except:
        profile = None
        form = ContactEditForm()
        messages.error(request, str(USERMGMT_MSG['OOPS']))
    if request.method == 'POST':
        form = ContactEditForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, str(USERMGMT_MSG['CSU']))
    return render_to_response(template, {'form':form,'profile':profile,},context_instance=RequestContext(request))

@login_required
def profile_privacy(request,template="account/profile_privacy.html"):
    form = ProfilePrivacyForm()
    try:
        profile, created = ProfilePrivacy.objects.get_or_create(profile_id=request.user.id)
        form = ProfilePrivacyForm(instance=profile)
    except:
        profile = None
        form = ProfilePrivacyForm()
        messages.error(request, str(USERMGMT_MSG['OOPS']))
    if request.method == 'POST':
        form = ProfilePrivacyForm(request.POST,instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, str(USERMGMT_MSG['PPU']))
    return render_to_response(template, {'form':form,'profile':profile,},context_instance=RequestContext(request))
    
    