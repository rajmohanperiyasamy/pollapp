from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.gis.geoip import GeoIP
from googlemaps import GoogleMaps

from common.models import ModuleNames, Address as Venues

from business.models import Business
from events.models import Event
from classifieds.models import Classifieds
from attraction.models import Attraction
from movies.models import Theatres

geoip_obj = GeoIP()

CONTENT_MODELS = {'business':Business, 'events':Event, 'classifieds':Classifieds, 'attractions':Attraction, 'cinemas':Theatres, 'venues':Venues}

def __get_location_from_ip(request):
    from common.utils import get_global_settings
    global_settings = get_global_settings()
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for: ip = x_forwarded_for.split(',')[0]
        else:ip = request.META.get('REMOTE_ADDR')
        location = geoip_obj.city(ip)['city']
    except:
        location = global_settings.city
    location = global_settings.city
    return location    

def __get_map_info_window_contents(module,objid):
    try:content_obj = CONTENT_MODELS[module].objects.get(id = objid)
    except:content_obj = None
    return content_obj   
    
