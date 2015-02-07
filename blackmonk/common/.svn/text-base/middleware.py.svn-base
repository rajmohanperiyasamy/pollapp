from django.contrib.auth.views import logout_then_login, login
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from common import utils
from django.core.exceptions import MiddlewareNotUsed
from django.shortcuts import render_to_response
    
class SiteLogin:
    def process_request(self, request):
        if settings.MAINTENANCE_MODE:
           return render_to_response("unavailable.html")
        if not settings.LIVE:
            if request.META['PATH_INFO'].find('site_media') != -1:
                pass
            elif request.user.is_anonymous() and request.META['PATH_INFO'] != '/account/signin/' and request.META['PATH_INFO'] != '/account/savepassword/':
                if not request.user.is_anonymous():
                    return HttpResponseRedirect('/account/signin/')
                else:
                    return HttpResponseRedirect('/account/signin/')
        else:
            pass

"""

class DetectTheme(object):

    
    def process_request(self, request):
        utils._init_theme(request)
        
        #get from POST and GET
        actual_theme = utils.get_theme_from_request(request)
        
        #set the theme in the local thread
        #utils.set_theme_in_local_thread(actual_theme)
        
        #set the cookie
        utils.set_theme_in_cookie(request, actual_theme)
        
        
   """     

class ThemeTemplate(object):
    
    def process_template_response(self, request, response):
        try:
            actual_theme = response.template_name
        except:
            return response
        if isinstance(actual_theme,basestring):
            new_template = settings.TEMPLATE_THEME_PATH + actual_theme
        elif actual_theme and isinstance(actual_theme,list):
            new_template = actual_theme[0]
        else:
            new_template="500.html"
        try:
            response.resolve_template(new_template) # template exception if the template doesnt exist
        except:
            new_template = actual_theme
            response.resolve_template(new_template)
        response.template_name = new_template
        return response

