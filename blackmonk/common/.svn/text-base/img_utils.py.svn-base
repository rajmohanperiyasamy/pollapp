from easy_thumbnails.files import get_thumbnailer
from django.core.files import File
from common.validation import validate_imgurl
from common.exception import *
import urlparse
import urllib
import os

def custom_thumbnail(source,width,height):
    thumbnail_options = dict(size=(width, height), crop=True, bw=True)
    return get_thumbnailer(source).get_thumbnail(thumbnail_options)

def download_from_url(url):
     try:
         result = urllib.urlretrieve(url)
         filename = os.path.basename(urlparse.urlparse(url).path) 
         file = File(open(result[0]))
         return filename ,file
     except:
          raise AppException("Error in download Url Data")
 
def validate_download_img(url):
    validate_imgurl(url)
    return download_from_url(url)
    
        