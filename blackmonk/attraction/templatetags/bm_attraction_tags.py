import datetime
from django.template import Library
from django.core.cache import cache
from attraction.models import AttractionCategory, Attraction
from common.utils import get_global_settings
from django.core.cache import cache
CACHE_TIMEOUT=60*10
register = Library()

@register.assignment_tag
def get_featured_attractions(**kwargs):
    fetched_values = ['name','slug','category','rating','album']
    limit = kwargs.get('limit', 20)
    category = kwargs.get('category', False)
    if category:
        attractions =  Attraction.objects.only(*fetched_values).filter(category = category, is_featured = True, status = 'P').select_related('album').prefetch_related('category').order_by('-id')[:limit] 
    else:
        attractions =  Attraction.objects.only(*fetched_values).filter(is_featured = True, status = 'P').select_related('album').prefetch_related('category').order_by('-id')[:limit]
    return attractions 

@register.assignment_tag
def get_attraction_categories():
    return AttractionCategory.objects.all().order_by('name')

@register.assignment_tag
def get_total_attractions_count():
    return Attraction.objects.filter(status = 'P').count()

@register.assignment_tag
def get_near_by_attractions(**kwargs):
    fetched_values = ['name','venue','category','slug','rating']
    key = {'status':'P'}
    limit = kwargs.get('limit', 6)
    attraction = kwargs.get('attraction', None)
    try:venue = attraction.venue
    except:venue = False
    if venue:
        key['venue'] = venue
    
    attractions =  Attraction.objects.only(*fetched_values).filter(**key).exclude(id = attraction.id).select_related('category','venue').order_by('-id')[:limit]
    return attractions

@register.assignment_tag
def get_near_by_restaurants(**kwargs):
    from restaurants.models import Restaurants, RestaurantAddress
    fetched_values = ['name','slug','ratings','logo','cuisines']
    limit = kwargs.get('limit', 6)
    venue = kwargs.get('venue', False)
    try:
        restaurant_ids = RestaurantAddress.objects.filter(pin__iexact = venue.zip).values_list('restaurant_id', flat=True).distinct()
        restaurants =  Restaurants.objects.only(*fetched_values).filter(id__in = restaurant_ids, status='P').prefetch_related('cuisines','restaurant_address').select_related('logo').order_by('-id')[:limit]
    except:
        restaurants = False
    return restaurants

@register.assignment_tag
def get_near_by_hotels(**kwargs):
    from business.models import Business, Address
    fetched_values = ['name','slug','ratings','logo','categories']
    cat_slug = 'hotels'
    limit = kwargs.get('limit', 6)
    venue = kwargs.get('venue', False)
    
    try:
        business_ids = Address.objects.filter(pin__iexact = venue.zip).values_list('business_id', flat=True).distinct()
        business_list =  Business.objects.only(*fetched_values).filter(id__in = business_ids, categories__slug = cat_slug, status='P').prefetch_related('categories').select_related('logo').order_by('-id')[:limit]
    except:
        business_list = False
    
    return business_list    
    
@register.assignment_tag
def get_attraction_weather_info(**kwargs): 
    global_settings = get_global_settings()
    country = global_settings.country.lower()
    attraction = kwargs.get('attraction', False)   
    if cache.get('weather_datas'+str(attraction.id)):
        weather_datas = cache.get('weather_datas'+str(attraction.id))
        return weather_datas
    else:
        weather_datas = []
        try:
            import socket,urllib2,json
            timeout = 3
            weather_url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q=%s,%s&mode=json&units=metric&cnt=5'%(attraction.venue.zip,country)
            socket.setdefaulttimeout(timeout)
            weather_info = urllib2.urlopen(weather_url)
            weather_info = json.loads(weather_info.read())
            for weather in weather_info['list']:
                wdate = datetime.datetime.utcfromtimestamp(weather['dt'])
                if wdate.date() >= datetime.datetime.today().date():
                    try:
                        temp_min = str(weather['temp']['min']).split('.')[0]
                    except:
                        temp_min = weather['temp']['min']
                    try:
                        temp_max = str(weather['temp']['max']).split('.')[0]
                    except:
                        temp_max = weather['temp']['max']    
                    weather_datas.append({'temp_min':temp_min, 'temp_max':temp_max, 'wdate':datetime.datetime.utcfromtimestamp(weather['dt']).date()})
            weather_datas = weather_datas[:3]
        except:
            weather_datas = False
        
        cache.set('weather_datas'+str(attraction.id), weather_datas, 60*60)
        socket.setdefaulttimeout(30)
        return weather_datas
