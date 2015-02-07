import urllib2
from xml.dom import minidom
from xml.dom.minidom import Node
import socket
from django.core.cache import cache
from common.utils import get_global_settings,get_ad_settings
from common.models import WeatherApiSettings

from django.conf import settings


def getText(nodelist):
   rc = ""
   for node in nodelist:
       if node.nodeType == node.TEXT_NODE:
           rc = rc + node.data
   return rc


def get_weather_online(request,wx_api_obj,global_settings):
    """
    google_result = pywapi.get_weather_from_google('regina,ca')
    temp_c=google_result['current_conditions']['temp_f']   
    icon=google_result['current_conditions']['icon'] 
    w_condition=google_result['current_conditions']['condition']
    """ 
    if cache.get('w_temp'):
        return {
                'w_temp': cache.get('w_temp'),
                'w_unit': cache.get('w_unit'),
                'w_icon': cache.get('w_icon'),
                'w_condition': cache.get('w_condition')
            }
    else:
        url = wx_api_obj.weather_xml
        try:
            timeout = 3
            socket.setdefaulttimeout(timeout)
            dom = minidom.parse(urllib2.urlopen(url))
            
            w_unit = wx_api_obj.weather_unit
            for node in dom.getElementsByTagName("data"):
                '''Current Weather '''
                for cc in dom.getElementsByTagName("current_condition"):
                    cw_image = cc.getElementsByTagName('weatherIconUrl')[0].childNodes[0].data
                    if w_unit == 'cel':
                        cw_temp = getText(cc.getElementsByTagName('temp_C')[0].childNodes)
                    else:
                        cw_temp = getText(cc.getElementsByTagName('temp_F')[0].childNodes)
                    cw_desc = cc.getElementsByTagName('weatherDesc')[0].childNodes[0].data
            
            cache.set('w_temp', cw_temp, 60*30)
            cache.set('w_unit', w_unit, 60*30)
            cache.set('w_icon', cw_image, 60*30)
            cache.set('w_condition', cw_desc, 60*30)
            socket.setdefaulttimeout(30)
            return {
                'w_temp': cw_temp,
                'w_unit': w_unit,
                'w_icon': cw_image,
                'w_condition': cw_desc
            }         
            
        except:
            return {}

def get_weather_network(request,wx_api_obj,global_settings):

    if cache.get('w_temp'):
        return {
                'w_temp': cache.get('w_temp'),
                'w_icon': cache.get('w_icon'),
                'w_unit': cache.get('w_unit'),
                'w_condition': cache.get('w_condition')
            }
    else:
        url = wx_api_obj.weather_xml
        try:
            timeout = 3
            socket.setdefaulttimeout(timeout)
            dom = minidom.parse(urllib2.urlopen(url))
              
            for node in dom.getElementsByTagName("SITE"):
                current_condition_list=node.getElementsByTagName("OBS")
                '''Current Weather '''
                for list in current_condition_list:
                    forcast=list.getAttribute('FORECAST_TEXT_EN')
                    temperature=list.getAttribute('TEMPERATURE')
                    cur_weather_icon=settings.STATIC_URL+'images/weather/new/'+list.getAttribute('ICON')+'.jpg' 
            w_unit=wx_api_obj.weather_unit
            cache.set('w_temp', temperature, 60*30)
            cache.set('w_icon', cur_weather_icon, 60*30)
            cache.set('w_unit', w_unit, 60*30)
            cache.set('w_condition', forcast, 60*30)
            socket.setdefaulttimeout(30)        
            return {
                    'w_temp': temperature,
                    'w_icon':cur_weather_icon,
                    'w_unit':w_unit,
                    'w_condition':forcast
        
                   }
        except:
            return {}


def weather(request,gsettings):
    try: wx_api_obj = WeatherApiSettings.objects.all()[:1][0]
    except:return {}
    if wx_api_obj.option == 'WO':
        return get_weather_online(request,wx_api_obj,gsettings)
    else:
        return get_weather_network(request,wx_api_obj,gsettings)


def getsettings(request):
    gsettings = get_global_settings()
    ad_obj = None
    data= {'globalsettings':gsettings,
           'adsettings':ad_obj,
           'base':settings.TEMPLATE_THEME_PATH+"base.html"
          }    
    weather_data=weather(request,gsettings)
    data.update(weather_data)
    return data


