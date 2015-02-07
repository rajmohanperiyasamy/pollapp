from django.db.models import Count
from django.template import Library
from movies.models import Movies,ShowTime, MovieTime, Theatres
import time, datetime
from django.core.cache import cache
CACHE_TIMEOUT=60*10

register = Library()

@register.assignment_tag
def get_movie_trailers(limit='all'):
    cache_key='ttag_movie_trailers'+str(limit)
    movie_trailers=cache.get(cache_key)
    if movie_trailers is None:
        if limit != 'all':movie_trailers = Movies.objects.only('title','slug','movie_url','created_on').filter(status='P').exclude(movie_url=u'').order_by('-release_date')[:limit]
        else:movie_trailers = Movies.objects.only('title','slug','movie_url','created_on').filter(status='P').exclude(movie_url=u'').order_by('-release_date')
        cache.set(cache_key,movie_trailers,CACHE_TIMEOUT)
    return movie_trailers    

@register.assignment_tag
def get_movie_galleries(limit=4):
    #movie_galleries = Movies.objects.only('title','slug','created_on').filter(status='P').prefetch_related('movie_images').order_by('-release_date')[:limit]
    cache_key='ttag_movie_galleries'+str(4)
    movie_galleries=cache.get(cache_key)
    if movie_galleries is None:
        movie_galleries = Movies.objects.annotate(num_images = Count('title') ).only('title','slug','created_on').filter(status='P', num_images__gt=1).order_by('-release_date')[:limit]
        cache.set(cache_key,movie_galleries,CACHE_TIMEOUT)
    return movie_galleries 


@register.assignment_tag
def get_top_theatres(limit):
    selected_date = datetime.date.today()
    fetched_values=['name','slug','address']
    cache_key='ttag_theatres'+str(limit)
    theatres=cache.get(cache_key)
    if theatres is None:
        try:
            show_times = ShowTime.objects.filter(date = selected_date).distinct('movietime')
            movie_times = MovieTime.objects.filter(id__in = [st.movietime.id for st in show_times]).distinct('theatre')
            theatres = Theatres.objects.filter(id__in = [mt.theatre.id for mt in movie_times]).order_by('name')[:limit]
        except:theatres = False    
        cache.set(cache_key,theatres,CACHE_TIMEOUT)
    return theatres


@register.assignment_tag
def get_home_page_movies(limit=4):
    today = datetime.datetime.now()
    fetched_values = ['title','slug','image','release_date','certification']
    cache_key='ttag_moviepack'+str(limit)
    movies_pack=cache.get(cache_key)
    if movies_pack is None:
        movies_pack = {}
        movies_pack['theatres'] = Theatres.objects.all().order_by('name')
        movies_pack['upcoming_movies'] = Movies.objects.only(*fetched_values).filter(release_date__gt=today, status='P').order_by('-release_date')
        movies_pack['released_movies'] = Movies.objects.only(*fetched_values).filter(release_date__lte=today, status='P').order_by('-release_date')
        movies_pack['datelist'] = [ today + datetime.timedelta(days=x) for x in range(0,7) ]
        cache.set(cache_key,movies_pack,CACHE_TIMEOUT)
    return movies_pack 

def convert_to24Hrs(t):
    try:
        x = time.strptime(t.replace(' ',''),'%I:%M%p')
    except:
        return '0.0'
    return time.strftime('%H.%M',x)

def convert_to12Hrs(t):
    x = time.strptime(t,'%H.%M')
    return time.strftime('%I.%M',x)  
 
@register.filter
def get_showtime_format(showtimes):
    data = []
    try:
        show_times = showtimes.split(',')
    except:
        show_times = showtimes   
    for s in show_times:
        if s.strip() == '':
            continue
        st=float(convert_to24Hrs(s))
        position = (st-6)*100/18
        st=convert_to12Hrs(str(st))
        data.append({'position':position,'showtime':st})
    return data
    