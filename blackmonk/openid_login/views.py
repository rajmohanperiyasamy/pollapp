from openid.consumer.consumer import (Consumer, SUCCESS, CANCEL, FAILURE,
                                      SETUP_NEEDED)
from openid.consumer.discover import DiscoveryFailure
from openid.extensions import sreg, ax

from django.shortcuts import redirect
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _

from .versioncheck import generic

from .forms import OpenIDForm
from .middleware import OpenIDMiddleware
from .store import DjangoOpenIDStore
from .utils import get_url_host, discover_extensions, from_openid_response
from django.core.urlresolvers import reverse

from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from random import choice
from string import letters
from django.contrib.auth import authenticate, login 

from common.models import SignupSettings
from openid_login.models import UserAssociation
from common.utils import get_global_settings
from django.template import RequestContext
class ReturnUrlMixin(object):
    return_url = None

    def get_return_url(self):
        if self.return_url is None:
            raise NotImplementedError("Either set the return_url or "
                                      "implement get_return_url()")
        return get_url_host(self.request) + self.return_url


class Begin(generic.FormView, ReturnUrlMixin):
    form_class = OpenIDForm
    sreg_attrs = {}
    ax_attrs = []
    store_class = DjangoOpenIDStore
    trust_root = '/'
    template_name='openid.html'
    def get(self, request, *args, **kwargs):
        next = request.GET.get('next','/')
        request.session["next_page"] = next 
        return render_to_response('openid.html',{},context_instance=RequestContext(request))
    def form_valid(self, form):
        
        openid_url = form.cleaned_data['openid_url']
        return_url = self.get_return_url()
        return self.ask_openid(openid_url, return_url)

    def get_trust_root(self):
        return get_url_host(self.request) + self.trust_root

    def get_sreg_attrs(self):
        return self.sreg_attrs

    def get_ax_attrs(self):
        return self.ax_attrs

    def ask_openid(self, openid_url, return_url):
      
        trust_root = self.get_trust_root()
        consumer = Consumer(self.request.session, self.store_class())

        try:
            auth_request = consumer.begin(openid_url)
        except DiscoveryFailure:
            message = _('The OpenID %(url)s was invalid')
            return self.failure(message % {'url': openid_url})

        use_ax, use_sreg = discover_extensions(openid_url)
        sreg_request = None
        ax_request = None
        if use_sreg:
            sreg_attrs = self.get_sreg_attrs()
            if 'optional' not in sreg_attrs:
                sreg_attrs.update({'optional': ['nickname', 'email']})
            sreg_request = sreg.SRegRequest(**sreg_attrs)
        if use_ax:
            ax_request = ax.FetchRequest()
            ax_request.add(
                ax.AttrInfo('http://schema.openid.net/contact/email',
                            alias='email', required=True),
            )
            ax_request.add(
                ax.AttrInfo('http://schema.openid.net/namePerson/friendly',
                            alias='nickname', required=True),
            )
            ax_attrs = self.get_ax_attrs()
            for attr in ax_attrs:
                if len(attr) == 2:
                    ax_request.add(ax.AttrInfo(attr[0], required=attr[1]))
                else:
                    ax_request.add(ax.AttrInfo(attr[0]))

        if sreg_request is not None:
            auth_request.addExtension(sreg_request)
        if ax_request is not None:
            auth_request.addExtension(ax_request)
        redirect_url = auth_request.redirectURL(trust_root, return_url)
        return redirect(redirect_url)
    def get_return_url(self):
        #return reverse('openid_callback')
        global_settings = get_global_settings()
        return "%s/openid/openid/complete/" %(global_settings.website_url)

   
    def failure(self, message):

        return HttpResponse('Error while login with openid!')


class BadOpenIDStatus(Exception):
    pass


class Callback(generic.View, ReturnUrlMixin):
    def success(self,request):
        next = request.session.get('next_page','/')
        if not next:
            next='/'
        openid_=request.openids[0]
        if not openid_:
            return HttpResponse('Error while login with openid!!')
        if openid_.sreg is not None:
            nickname = openid_.sreg.get('nickname', '')
            email = openid_.sreg.get('email', '')
            email = email.lower()
        if openid_.ax is not None and not nickname or not email:
            if openid_.ax.get('http://schema.openid.net/namePerson/friendly', False):
                nickname = openid_.ax.get('http://schema.openid.net/namePerson/friendly')[0]
            if openid_.ax.get('http://schema.openid.net/contact/email', False):
                email = openid_.ax.get('http://schema.openid.net/contact/email')[0]
        try:
            assoc = UserAssociation.objects.get(openid=openid_)
            user=assoc.user
            user.backend='django.contrib.auth.backends.ModelBackend' 
            login(request, user)
            return HttpResponseRedirect(next)
        except:
            try:
                user=User.objects.get(email=email)
                user.backend='django.contrib.auth.backends.ModelBackend' 
                UserAssociation(openid=openid_,user=user).save()
                login(request, user)
                return HttpResponseRedirect(next)
            except User.MultipleObjectsReturned:
                return HttpResponse("Couldn't login, Error while login with openid!")
            except:
                password=User.objects.make_random_password(length=6, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
                try:
                    username = email.split('@')[0].replace('.',' ')
                except:
                    username=getuniqueusername()
                user = User.objects.create_user(email, username[:25], password)
                if not nickname:
                    nickname=username[:25]
                user.display_name=nickname
                user.is_active=True
                user.save()
                UserAssociation(openid=openid_,user=user).save()
                user.backend='django.contrib.auth.backends.ModelBackend' 
                login(request, user)
                return HttpResponseRedirect(next)
            

    def failure(self, message):
        """
        Gets called when the OpenID authentication fails.
        """
        return HttpResponse('Error while login with openid!')
    
    def get_return_url(self):
        global_settings = get_global_settings()
        return "%s/openid/openid/complete/" %(global_settings.website_url)
    def get(self, request, *args, **kwargs):
        consumer = Consumer(request.session, DjangoOpenIDStore())
        query = dict((k, smart_unicode(v)) for k, v in request.GET.items())
        openid_response = consumer.complete(query, self.get_return_url())
        self.openid_response = openid_response

        if openid_response.status == SUCCESS:
            if 'openids' not in request.session.keys():
                request.session['openids'] = []
            request.session['openids'] = filter(
                lambda o: o.openid != openid_response.identity_url,
                request.session['openids'],
            )
            request.session['openids'].append(
                from_openid_response(openid_response),
            )
            OpenIDMiddleware().process_request(request)
            return self.success(request)
        elif openid_response.status == CANCEL:
            return self.failure(_('The request was cancelled'))
        elif openid_response.status == FAILURE:
            return self.failure(openid_response.message)
        elif openid_response.status == SETUP_NEEDED:
            return self.failure(_('Setup needed'))
        else:
            raise BadOpenIDStatus(openid_response.status)
def getuniqueusername():
    name=''.join([choice(letters) for i in xrange(20)])
    try:
        User.objects.get(username=name)
        getuniqueusername()
    except:
        return name