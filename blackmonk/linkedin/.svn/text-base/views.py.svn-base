import oauth2 as oauth
import cgi
import simplejson as json
from random import choice
from string import letters

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.template import RequestContext
from django.contrib.auth import login
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate as simpleauthenticate

from linkedin.models import LinkedInUser
from common.models import SignupSettings

from common.utils import get_global_settings
from usermgmt.views import signup_mail
from usermgmt.newsletter import subscripe_newsletter

access_token_url = 'https://api.linkedin.com/uas/oauth/accessToken'
authenticate_url = 'https://www.linkedin.com/uas/oauth/authenticate'

#                                                Points Remember
#  1) we have to create API for Site in Linkedin
#  2) add them into common-social
#

def getLinkedInClient():
    try:
        global_settings = get_global_settings()
        signupsetting=SignupSettings.objects.all()[0]
        consumer = oauth.Consumer(signupsetting.linkedin_app_id, signupsetting.linkedin_secret_key)
        client = oauth.Client(consumer)
        return global_settings,client,consumer
    except:
        raise Http404("Invalid request")

def oauth_login(request):
    try:request.session["next"] =request.GET['next']
    except:pass
    global_settings,client,consumer=getLinkedInClient()
    request_token_url = 'https://api.linkedin.com/uas/oauth/requestToken?oauth_callback='+global_settings.website_url+reverse('linkedin_authenticated')#http://localhost/linkedin/login/authenticated/
    resp, content = client.request(request_token_url, "GET")
    
    if resp['status'] != '200':
        raise Exception("Invalid response from Provider.")
    request.session['request_token'] = dict(cgi.parse_qsl(content))
   
    url = "%s?oauth_token=%s" % (authenticate_url,
        request.session['request_token']['oauth_token'])
    return HttpResponseRedirect(url)

def oauth_authenticated(request):
    global_settings,client,consumer=getLinkedInClient()
    token = oauth.Token(request.session['request_token']['oauth_token'],request.session['request_token']['oauth_token_secret'])
    if 'oauth_verifier' in request.GET:
        token.set_verifier(request.GET['oauth_verifier'])
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response from Provider.")
    
    access_token = dict(cgi.parse_qsl(content))
    headers = {'x-li-format':'json'}
    url = "http://api.linkedin.com/v1/people/~:(id,first-name,last-name,pictureUrl)"
    
    token = oauth.Token(access_token['oauth_token'],access_token['oauth_token_secret'])
    client = oauth.Client(consumer,token)
    
    resp, content = client.request(url, "GET", headers=headers)
    profile = json.loads(content)
    
    lnid = profile['id']
    try:
        luser=LinkedInUser.objects.get(lnid=lnid)
        luser.user.backend='django.contrib.auth.backends.ModelBackend' 
        login(request, luser.user)
        return HttpResponseRedirect(request.session.get('next','/'))
    except:
        request.session["lnid"] = lnid
        request.session["lnname"] = profile['firstName']+' '+profile['lastName']
        request.session["lnfname"] = profile['firstName']
        request.session["lnlname"] = profile['lastName']
        try:
            request.session["lnimg"] = profile['pictureUrl']
        except:
            request.session["lnimg"]="http://www.nasa.gov/images/content/297522main_image_1244_946-710.jpg"
        request.session["oauth_token"] = access_token['oauth_token']
        request.session["oauth_secret"] = access_token['oauth_token_secret']
        return HttpResponseRedirect(reverse('linkedin_complete'))  
    
def complete(request):
    profile=""
    try:
        if not request.session.get("lnid",False):
            if request.user.is_authenticated:return HttpResponseRedirect('/account/profile/')
            else:return HttpResponseRedirect('/account/signin/')
        else:
            try:
                ln_user=LinkedInUser.objects.get(lnid=request.POST['id'])
                return HttpResponseRedirect(request.GET.get('next','/'))
            except:
                if request.method=='POST':
                    email=request.POST['email'].lower()
                    if request.POST.get('ex_user',False):
                        password=request.POST['password']
                        user=simpleauthenticate(useremail=email, password=password)
                        if user:pass
                        else:
                            data={'name':request.session["lnname"],'img':request.session["lnimg"],'login':True,'loginerror':True,'email':request.POST['email']}
                            return render_to_response('linkedin/complete.html',data,context_instance=RequestContext(request))
                    else:
                        try:
                            user=User.objects.get(useremail=email)
                            data={'name':request.session["lnname"],'img':request.session["lnimg"],'errmsg':True,'email':email}
                            data['next']=request.POST.get('next',None)
                            return render_to_response('linkedin/complete.html',data,context_instance=RequestContext(request))
                        except:
                            password=User.objects.make_random_password(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
#                             username=getuniqueusername()
                            
#                             user = User.objects.create_user(email, username, password)
                            user = User()
                            user.useremail = email
                            user.email = email
                            user.set_password(password)
#                             user.first_name=request.session["lnfname"]
#                             user.last_name=request.session["lnlname"]
                            user.status='A'
                            user.display_name=request.session["lnname"]
                            user.image=request.session["lnimg"]
                            user.save()
                            try:signup_mail(user.display_name,password,email)
                            except:pass
                            subscripe_newsletter(user.display_name,email)
                    ln_user=LinkedInUser(lnid=request.session["lnid"],user=user)
                    ln_user.oauth_token=request.session["oauth_token"]
                    ln_user.oauth_secret=request.session["oauth_secret"]
                    ln_user.save()
                    user.backend='django.contrib.auth.backends.ModelBackend' 
                    login(request, user)
                    request.session["lnid"] = None 
                    request.session["lnname"] = None 
                    request.session["lnimg"] = None 
                    request.session["oauth_token"] = None
                    request.session["oauth_secret"] = None
                    return HttpResponseRedirect(request.session.get('next','/account/profile/'))
                else:
                    data={'name':request.session["lnname"],'img':request.session["lnimg"]}
                    return render_to_response('linkedin/complete.html',data,context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect('/account/signin/')
        
def getuniqueusername():
    name=''.join([choice(letters) for i in xrange(20)])
    try:
        User.objects.get(username=name)
        getuniqueusername()
    except:
        return name 