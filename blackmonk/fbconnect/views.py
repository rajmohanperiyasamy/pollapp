import os
from urlparse import urlparse
import urllib, cgi,urllib2

from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.utils.http import urlquote
from django.contrib.auth import get_user_model 
from django.views.decorators.csrf import csrf_protect
User = get_user_model()

from django.conf import settings

from fbconnect.utils import *
from fbconnect.facebook import *
from fbconnect.models import FBUser
from django.template.response import TemplateResponse

from common.utils import  get_global_settings
from common.models import SignupSettings
from random import choice
from string import letters
from django.contrib.auth import  login ,REDIRECT_FIELD_NAME
from django.contrib.auth import authenticate as simpleauthenticate
from django.core.validators import email_re

def _clear_fbsession():
    try:del request.session["fb_id"]
    except: pass
    try:del request.session["fb_name"]
    except: pass
    try:del request.session["fb_email"]
    except: pass
    try:del request.session["next_page"]
    except: pass
    
def _fbconnect_user_info(request,code):
    global_settings = get_global_settings()
    try:
            fb_setting=SignupSettings.objects.filter(facebook=True)[:1][0]
    except:
            return HttpResponse('Sorry. Facebook login not enabled.')
        
    APP_ID = fb_setting.facebook_app_id
    APP_SECRET = fb_setting.facebook_secret_key
    args = dict(client_id=APP_ID, redirect_uri="%s/fbconnect/authenticate/"%(global_settings.website_url))
    args["client_secret"] = APP_SECRET
    args["code"] = code 
    args["scope"]="email"
    res_data=urllib2.urlopen("https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args)).read()
    access_token =res_data.split("&")[0].split("=")[1]
    user_data_json = urllib2.urlopen("https://graph.facebook.com/me?" + urllib.urlencode(dict(access_token=access_token)))
    profile = simplejson.load(user_data_json)
    request.session["fb_id"] = fid = profile["id"] 
    request.session["fb_name"] = user_name = profile["name"]
    try:
        request.session["fb_email"] = email = profile["email"].lower()
    except:
        email=None
    return fid,user_name,email

def _facebook_authenticate(facebookId):
    if facebookId is None:
            return None
    try:
        appUser = FBUser.objects.get(fbid= facebookId )
        return appUser.user
    except FBUser.DoesNotExist:
        return None


@csrf_protect
def authenticate(request):
    global_settings = get_global_settings()
    try:
            fb_setting=SignupSettings.objects.filter(facebook=True)[:1][0]
    except:
            return HttpResponse('Sorry. Facebook login not enabled.')
    APP_ID = fb_setting.facebook_app_id
    code = request.GET.get("code",None)
    args = dict(client_id=APP_ID, redirect_uri="%s/fbconnect/authenticate/"%(global_settings.website_url),scope="email")
    if code != None:
        next = request.session.get('next_page','/')
        if not next:
            next = '/'
        fbid,firstname,email = _fbconnect_user_info(request,code)
        data = {}
        data['is_authenticated'] = facebook_authenticate(request)
        if data['is_authenticated']:
            _clear_fbsession()
            return HttpResponseRedirect(next)
        else:
           try:
               if not email:
                   resdata={'name':firstname,'next':next}
                   return render_to_response('fbconnect/complete.html',resdata,context_instance=RequestContext(request))
               else:
                   User.objects.get(useremail=email)
                   resdata={'name':firstname,'email':email,'next':next}
                   return render_to_response('account/signin_registered.html',resdata,context_instance=RequestContext(request))
           except User.DoesNotExist:
                logo="http://static.ak.fbcdn.net/pics/q_silhouette.gif"
                password=User.objects.make_random_password(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                username=email.split('@')[0].replace('.',' ')
                user = User.objects.create_user(email, username, password)
                fuser=FBUser(user=user,fbid=fbid,logo=logo)
                fuser.save()
                user.backend='django.contrib.auth.backends.ModelBackend' 
                login(request, user)
                _clear_fbsession()
                return HttpResponseRedirect(next)
           except:return HttpResponseRedirect('/fbconnect/complete/?next='+next)
    else:
        next = request.GET.get('next',None)
        request.session["next_page"] = next
        return HttpResponseRedirect("https://www.facebook.com/dialog/oauth?" + urllib.urlencode(args))
    
def _build_context(request, extra_context=None):
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return context    



def associate_fbaccount(request,template="fbconnect/complete.html"):
    #id=facebook_getidfromcookie(request)
    try:
        id=request.session['fb_id']
    except:
        raise Http404 
    userinfo = facebook_getuserinfo(id)
    data={}
    fbusername=''
    next = request.session.get('next_page','/')
    if not next:
            next = '/'
    try:
        fbusername=request.session["fb_name"]
    except:
        pass
    data['logo']="http://static.ak.fbcdn.net/pics/q_silhouette.gif"
    try:
        name=request.session["fb_name"]
        name=name.replace(' ','.');
        data['username']= name
    except:
        name=''
        data['username']= ''
    try:
        email=request.session["fb_email"]
        data['email']= email
    except:
        pass
        
    if name:
         data['name'] = name
    else:
         data['name'] = fbusername
    try:
        data['profile_url'] = userinfo[0]['profile_url']
    except:
        data['profile_url'] = ''
    data['next']= next
    return render_to_response(template,data,context_instance=RequestContext(request))

def register(request,redirect_field_name=REDIRECT_FIELD_NAME,template_name='fbconnect/complete.html',extra_context=None):
    is_redirect = False
    redirect_to = request.REQUEST.get(redirect_field_name, '')
    id=request.session['fb_id']
    logo=request.POST['logo']
    email = ''
    next = request.session.get('next_page','/')
    if not next:
            next = '/'
    if request.POST:
        name=display_name=request.POST.get('display_name','')
        email=request.POST['email'].lower()
        is_new=False
        try:password=request.POST['password']
        except:is_new=True
        if not email or not email_re.match(email):
            data={'name':name,'email':email,'error':'Enter a valid email address','next':next}
            return render_to_response('fbconnect/complete.html',data,context_instance=RequestContext(request))
       
        if is_new:
            try:
                User.objects.get(email=email)
                data={'name':name,'email':email,'error':'Email already exists,If you holds this account please connect with your existing account','next':next}
                return render_to_response('fbconnect/complete.html',data,context_instance=RequestContext(request))
            except User.MultipleObjectsReturned:
                data={'name':name,'email':email,'error':'Email already exists,If you holds this account please connect with your existing account','next':next}
                return render_to_response('fbconnect/complete.html',data,context_instance=RequestContext(request))
            except:
                pass
            password=User.objects.make_random_password(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
            username=email.split('@')[0].replace('.',' ')
            user = User.objects.create_user(email, username, password)
            fuser = FBUser(user=user,fbid=id,logo=logo)
            fuser.save()
            user.backend='django.contrib.auth.backends.ModelBackend' 
            login(request, user)
            _clear_fbsession()
            return HttpResponseRedirect(next)
        else:
            try:
                user=simpleauthenticate(username=email, password=password)
            except:
                data={'name':name,'error':'login failure','next':next}
                return render_to_response('fbconnect/complete.html',data,context_instance=RequestContext(request))
            if user:
                tuser=FBUser(user=user,fbid=id,logo=logo)
                tuser.save()
                login(request, user)
                _clear_fbsession()
                return HttpResponseRedirect(next)
            else:
                
                data={'name':name,'error':'login failure','next':next}
                return render_to_response('fbconnect/complete.html',data,context_instance=RequestContext(request))
    
    return render_to_response(template_name, {
        redirect_field_name: redirect_to,
        'email': email,
        'logo':logo,
        'next':next
    }, context_instance=_build_context(request, extra_context=extra_context))  
    
def register_account(form):
    user = User.objects.create_user(
        form.cleaned_data['email'],
        form.cleaned_data['username'], 
        form.password)
    user.backend = "django.contrib.auth.backends.ModelBackend"
    return user

def getuniqueusername():
    name=''.join([choice(letters) for i in xrange(20)])
    try:
        User.objects.get(username=name)
        getuniqueusername()
    except:
        return name    
