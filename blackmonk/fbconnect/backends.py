from django.contrib.auth import get_user_model
User = get_user_model()
from fbconnect.models import FBUser #AppUser has User as foreign key and facebookid field
from django.conf import settings
from fbconnect.utils import *

class FacebookConnectBackend:

    @staticmethod
    def authenticate(request):
        try:
            facebookId = request.session['fb_id']
        except:
            return None    
    
        if facebookId is None:
            return None
    
        try:
            appUser = FBUser.objects.get(fbid= facebookId )
            appUser.user.backend='fbconnect.backends.FacebookConnectBackend'
            return appUser.user
        except FBUser.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
