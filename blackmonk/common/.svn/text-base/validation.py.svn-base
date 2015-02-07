from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import urllib
import urllib2
import re
from django.conf import settings
from common.exception import AppException 

def _get_url_info(url):
    d = urllib2.urlopen(url)
    return d.info()


def validate_url(url):
    validate = URLValidator()  # verify_exists=True
    try:
        validate(url)
    except ValidationError, e:
        raise AppException("Invalid  Url")

def validate_imgurl(url):
    validate_url(url)
    info=_get_url_info(url)
    if info['Content-Type'] not in settings.IMG_UPLOAD_FILE_TYPES:
       raise AppException("Invalid Image Type")
    elif int(info['Content-Length']) > settings.MAX_UPLOAD_SIZE:
         raise AppException("Image Size Shouldn't exceed 5MB")
    else:
         return True
   


'''
headers = {
                    "Accept": "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5",
                    "Accept-Language": "en-us,en;q=0.5",
                    "Accept-Charset": "ISO-8859-1,utf-8;q=0.7,*;q=0.7",
                    "Connection": "close",
                    "User-Agent": None,
                }
regex = re.compile(
          r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
def _get_content_type(url):
    d = urllib.urlopen(url)
    #print d.info()
    return d.info()['Content-Type']

def _get_content_size(url):
    d = urllib.urlopen(url)
   # print d.info()
    return d.info()['Content-Type']
'''
