from hashlib import md5
import urllib
import time
from django.utils import simplejson
import datetime
from django.conf import settings
from common.models import SignupSettings

REST_SERVER = 'http://api.facebook.com/restserver.php'


def facebook_getuserinfo(uid):
     try:
            fb_setting=SignupSettings.objects.filter(facebook=True)[:1][0]
     except:
            return HttpResponse('Sorry. Facebook login not enabled.')
        
     API_KEY = fb_setting.facebook_app_id
     user_info_params = {
        'method': 'Users.getInfo',
        'api_key': API_KEY,
        'call_id': time.time(),
        'v': '1.0',
        'uids': uid,
        'fields': 'first_name,last_name,pic_square_with_logo,profile_url,uid,name,username',
        'format': 'json',
     }

     user_info_hash = facebook_getsignature(user_info_params)
     user_info_params['sig'] = user_info_hash
     user_info_params = urllib.urlencode(user_info_params)
     user_info_response  = simplejson.load(urllib.urlopen(REST_SERVER, user_info_params))
     return user_info_response
def facebook_getcomments(uid):
     try:
            fb_setting=SignupSettings.objects.filter(facebook=True)[:1][0]
     except:
            return HttpResponse('Sorry. Facebook login not enabled.')
        
     API_KEY = fb_setting.facebook_app_id
     user_info_params = {
        'method': 'stream.getComments',
        'api_key': API_KEY,
        'call_id': time.time(),
        'v': '1.0',
        'post_id': uid,
        'format': 'json',
     }

     user_info_hash = facebook_getsignature(user_info_params)
     user_info_params['sig'] = user_info_hash
     user_info_params = urllib.urlencode(user_info_params)
     user_info_response  = simplejson.load(urllib.urlopen(REST_SERVER, user_info_params))
     return user_info_response
 

# Generates signatures for FB requests/cookies
def facebook_getsignature(values_dict, is_cookie_check=False):

    try:
            fb_setting=SignupSettings.objects.filter(facebook=True)[:1][0]
    except:
            return HttpResponse('Sorry. Facebook login not enabled.')
        
    API_KEY = fb_setting.facebook_app_id
    API_SECRET = fb_setting.facebook_secret_key
    signature_keys = []
    for key in sorted(values_dict.keys()):
        if (is_cookie_check and key.startswith(API_KEY + '_')):
            signature_keys.append(key)
        elif (is_cookie_check is False):
            signature_keys.append(key)
    if (is_cookie_check):
        signature_string = ''.join(['%s=%s' % (x.replace(API_KEY + '_',''), values_dict[x]) for x in signature_keys])
    else:
        signature_string = ''.join(['%s=%s' % (x, values_dict[x]) for x in signature_keys])
    signature_string = signature_string + API_SECRET
    return md5(signature_string).hexdigest()

def facebook_getidfromcookie(request):
    try:
            fb_setting=SignupSettings.objects.filter(facebook=True)[:1][0]
    except:
            return HttpResponse('Sorry. Facebook login not enabled.')
        
    API_KEY = fb_setting.facebook_app_id
    signature_hash = ''
    if API_KEY in request.COOKIES:
            signature_hash = facebook_getsignature(request.COOKIES, True)

# The hash of the values in the cookie to make sure they're not forged
    try:
        if(signature_hash == request.COOKIES[API_KEY]):
      
    # If session hasn't expired
            if(datetime.datetime.fromtimestamp(float(request.COOKIES[API_KEY+'_expires'])) > datetime.datetime.now()):
                 return request.COOKIES[API_KEY + '_user']
            else:
                 return request.COOKIES[API_KEY + '_user']
    except:
         pass
    return None
