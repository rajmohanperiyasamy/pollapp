from fbconnect.models import *
from django.contrib.auth import login
from fbconnect.backends import *

def facebook_authenticate(request):
    
    user = FacebookConnectBackend.authenticate(request)
    message = ''
    if user is not None:
        if user.is_active:
            login(request, user)
            #return HttpResponseRedirect('/')
            return True
        else:
           # message = 'Account for this Facebook Account is Inactive.'
           return False
    else:
    #Login failed
        #message = 'Facebook Account is not associated to any of our members.'
        return False
    
    return False
