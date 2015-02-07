import tweepy
from django.template import RequestContext
from django.conf import settings
from django.shortcuts import redirect
from django.views import generic
from twitter_login.models import TwitterUser
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from random import choice
from string import letters
from django.contrib.auth import authenticate, login 
from django.contrib.auth import get_user_model
User = get_user_model()
from common.models import SignupSettings
from django.utils.translation import ugettext as _
from django.core.validators import email_re
class Authorize(generic.View):
    """
    A base class for the authorize view. Just sets the request token
    in the session and redirects to twitter.
    """
    def get(self, request, *args, **kwargs):
        try:
            twitter_setting=SignupSettings.objects.filter(twitter=True)[:1][0]
        except:
            return HttpResponse('Sorry. Twitter login not enabled.')
        
        next = request.GET.get('next',None)
        request.session["next_page"] = next
        
        auth = tweepy.OAuthHandler(twitter_setting.twitter_consumer_key,
                                   twitter_setting.twitter_consumer_secret, secure=True)
        url = auth.get_authorization_url(signin_with_twitter=True)
        request.session['request_token'] = (auth.request_token.key,
                                            auth.request_token.secret)
        return redirect(url)


class Return(generic.View):
    """
    A base class for the return callback. Subclasses must define:

        - handle_error(error_msg, exception=None): what to do when
          something goes wrong? Must return an HttpResponse

        - handle_success(auth): what to do on successful auth? Do
          some stuff with the tweepy.OAuth object and return
          an HttpResponse
    """
    def get(self, request, *args, **kwargs):
        verifier = request.GET.get('oauth_verifier', None)
        if verifier is None:
            return self.handle_error('No verifier code')

        if not 'request_token' in request.session:
            return self.handle_error('No request token found in the session')

        request_token = request.session.pop('request_token')
        request.session.modified = True
        try:
            twitter_setting=SignupSettings.objects.filter(twitter=True)[:1][0]
        except:
            return HttpResponse('Sorry. Twitter login not enabled.')
        auth = tweepy.OAuthHandler(twitter_setting.twitter_consumer_key,
                                   twitter_setting.twitter_consumer_secret, secure=True)
        auth.set_request_token(request_token[0], request_token[1])
        try:
            auth.get_access_token(verifier=verifier)
        except tweepy.TweepError as e:
            return self.handle_error(_('Failed to get an access token'))

        return self.handle_success(auth,request)

    def handle_success(self, auth,request):
        next = request.session.get('next_page','/')
        if not next:
            next = '/'
        api = tweepy.API(auth)
        tname=api.me().screen_name
        try:
            tuser=TwitterUser.objects.get(screen_name=tname)
            user=tuser.user
            user.backend='django.contrib.auth.backends.ModelBackend' 
            login(request, user)
            return HttpResponseRedirect(next)
        except:
           
            data={'screen_name':tname}
            return render_to_response('twitter/associate.html',data,context_instance=RequestContext(request))
            
        

    def handle_error(self, error_msg, exception=None):
        return HttpResponse(_('Error while login with twitter!'))
def associate(request):
    next = request.session.get('next_page','/')
    if not next:
        next = '/'
    if request.method =='POST':
        name=request.POST['screen_name']
        email=request.POST['email'].lower()
        try:
            password=request.POST['password']
        except:is_new=True
        try:
            display_name=request.POST['display_name']
        except:
            display_name=name
            is_new=False
        
        if not email or not email_re.match(email):
            data={'screen_name':name,'error':'enter valid email address'}
            return render_to_response('twitter/associate.html',data,context_instance=RequestContext(request))
        if is_new:
            try:
                User.objects.get(useremail=email)
                data={'name':name,'email':email,'error':'Email already exists,If you holds this account please connect with your existing account','next':next}
                return render_to_response('fbconnect/complete.html',data,context_instance=RequestContext(request))
            except User.MultipleObjectsReturned:
                data={'name':name,'email':email,'error':'Email already exists,If you holds this account please connect with your existing account','next':next}
                return render_to_response('twitter/associate.html',data,context_instance=RequestContext(request))
            except:
                pass
            password = User.objects.make_random_password(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
            username = getuniqueusername()
            user = User.objects.create_user(email, display_name, password)
            user.save()
            tuser=TwitterUser(user=user,screen_name=name)
            tuser.save()
            user.backend='django.contrib.auth.backends.ModelBackend' 
            login(request, user)
            return HttpResponseRedirect(next)
        else:
            try:
                user=authenticate(username=email, password=password)
            except:
                data={'name':name,'error':'login failure','next':next}
                return render_to_response('twitter/associate.html',data,context_instance=RequestContext(request))
            if user:
                tuser=TwitterUser(user=user,screen_name=name)
                tuser.save()
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                data={'name':name,'error':'login failure','next':next}
                return render_to_response('twitter/associate.html',data,context_instance=RequestContext(request))
    
def getuniqueusername():
    name=''.join([choice(letters) for i in xrange(20)])
    try:
        User.objects.get(username=name)
        getuniqueusername()
    except:
        return name
    