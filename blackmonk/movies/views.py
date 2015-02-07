#Python Libs 
import datetime,time
from time import strptime
from datetime import timedelta

#Django Libs 
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings as my_settings
from mptt_comments.models import MpttComment
#Application Libs and Common Methods
from common.utils import ds_pagination, get_global_settings
from common.models import ModuleNames
from gallery.models import PhotoAlbum
from usermgmt.models import Favorite
from usermgmt.favoriteviews import add_remove_fav,get_fav

#Module Files(models,forms etc...)
from movies.models import Movies, Theatres, CriticReview, MovieLanguage, MovieTime, ShowTime

GET_SORT_ORDER = {'ratings':'-ratings', 'title':'title', 'release-date':'-release_date', 'runtime':'-duration_hours'}
ITEMS_PER_PAGE = 20

def movies_home(request, template='default/movies/home.html'):
    today = datetime.datetime.now()
    data = {}
    data['datelist'] = [ today + datetime.timedelta(days=x) for x in range(0,7) ]
    data['theatres'] = Theatres.objects.all().order_by('name')
    data['featured_movies'] = Movies.objects.only('title','slug','movie_url','release_date','duration_hours','certification','album').filter(status='P').order_by('-ratings')[:8]
    data['released_movies'] = Movies.objects.only('title','slug','release_date','certification','album').filter(release_date__lte=today, status='P').order_by('-release_date')[:20]
    data['upcoming_movies'] = Movies.objects.only('title','slug','release_date','certification','album').filter(release_date__gt=today, status='P').order_by('release_date')[:20]
    return render_to_response(template,data,context_instance=RequestContext(request))

def movies_recent_reviews(request, template='default/movies/recent-reviews.html'):
    ''' home page ajax method for retrieving all recent movie reviews'''
    from django.contrib.contenttypes.models import ContentType
    from mptt_comments.models import MpttComment
    data={}
    send_data = {}
    try:
        c_type = ContentType.objects.get(model='movies')
        movie_ids = Movies.objects.values_list('id')
        data['recent_reviews'] = MpttComment.objects.filter(content_type=c_type,level__gte=1,is_public=True,is_removed=False).order_by('-submit_date')[:4]
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        send_data['status'] = True
    except:send_data['status'] = False
    return HttpResponse(simplejson.dumps(send_data)) 

def movies_listing(request, movietype='all', template='default/movies/movie-listing.html'):
    today = datetime.datetime.now()
    fetched_values=['title','slug','movie_url','movie_type','release_date','duration_hours','certification','director','cast','synopsis','ratings']
    sort = request.GET.get('sort','release-date')
    sorder = GET_SORT_ORDER[sort]
    
    if movietype == 'nowplaying':movies = Movies.objects.only(*fetched_values).filter(release_date__lte=today, status='P').prefetch_related('movie_type').order_by(sorder)
    elif movietype == 'upcoming':movies = Movies.objects.only(*fetched_values).filter(release_date__gt=today, status='P').prefetch_related('movie_type').order_by(sorder)
    else:movies = Movies.objects.only(*fetched_values).filter(status='P').prefetch_related('movie_type').order_by(sorder)      
    
    page = int(request.GET.get('page',1))
    data = ds_pagination(movies,page,'movies',ITEMS_PER_PAGE)
    data['movietype'] = movietype
    data['url'] = reverse('movies_listing',args=[movietype])
    data['view_type'] = request.GET.get('view','grid')
    data['sort'] = sort
    return render_to_response(template,data,context_instance=RequestContext(request)) 

def movies_trailer_list(request, template='default/movies/movies-trailer-list.html'):
    fetched_values = ['title','slug','movie_url','movie_type','release_date','duration_hours','certification','director','cast','synopsis','ratings']
    trailer_type = request.GET.get('type','latest')
    
    if trailer_type == 'latest':
        movies = Movies.objects.only(*fetched_values).filter(status='P').prefetch_related('movie_type').exclude(movie_url=u'').order_by('-id')
    else:
        movies = Movies.objects.only(*fetched_values).filter(status='P').prefetch_related('movie_type').exclude(movie_url=u'').order_by('-views')
            
    page = int(request.GET.get('page',1))
    data = ds_pagination(movies,page,'movies',21)
    data['url'] = reverse('movies_movies_trailer_list')
    data['view_type'] = request.GET.get('view','grid')
    data['trailer_type'] = trailer_type
    #data['seo'] = get_movie_seo('trailer-list')
    return render_to_response(template,data,context_instance=RequestContext(request)) 

def movies_galleries_list(request, template='default/movies/movies-galleries-list.html'):
    fetched_values = ['title','slug','movie_url','movie_type','release_date','duration_hours','certification','director','cast','synopsis','ratings']
    gallery_type = request.GET.get('type','latest')
    
    if gallery_type == 'latest':
        movies = Movies.objects.only(*fetched_values).filter(status='P').select_related('movie_photos').prefetch_related('movie_type').order_by('-id')
    else:
        movies = Movies.objects.only(*fetched_values).filter(status='P').select_related('movie_photos').prefetch_related('movie_type').order_by('-views')
   
    page = int(request.GET.get('page',1))
    data = ds_pagination(movies,page,'movies',21)
    data['url'] = reverse('movies_movies_galleries_list')
    data['view_type'] = request.GET.get('view','grid')
    data['gallery_type'] = gallery_type
    #data['seo'] = get_movie_seo('trailer-list')
    return render_to_response(template,data,context_instance=RequestContext(request)) 

def oldmovies_search(request, template='default/movies/movies-search-listing.html'):
    fetched_values=['title','slug','movie_url','movie_type','release_date','duration_hours','certification','director','cast','synopsis','ratings']
    q_text=()
    sort = request.GET.get('sort','release-date')
    sorder = GET_SORT_ORDER[sort]
    q = request.GET.get('q','')
    try:
        movie = Movies.objects.get(title=q,status='P')
        redirect_url = movie.get_absolute_url()
        return HttpResponseRedirect(redirect_url)
    except:
        q_text = (Q(title__icontains=q) | Q(synopsis__icontains=q) | Q( director__icontains = q ) | Q( cast__icontains = q ))
        movies = Movies.objects.only(*fetched_values).filter(q_text,status='P').order_by(sorder).distinct()
    page = int(request.GET.get('page',1))
    data = ds_pagination(movies,page,'movies',ITEMS_PER_PAGE)
    data['url'] = reverse('movies_movies_search')
    data['view_type'] = request.GET.get('view','grid')
    data['sort'] = sort
    data['search'] = True
    data['kw'] = q
    return render_to_response(template,data,context_instance=RequestContext(request)) 

def auto_suggest_movies(request):
    from movies.utils import get_suggested_movies
    
    ''' calling method wriitn in movies utils '''
    return_data = get_suggested_movies(request) 
    return HttpResponse(simplejson.dumps(return_data), content_type="application/json")

def showtime_search(request):
    keyword = request.GET.get('keyword')
    selected_date = request.GET.get('date')
    search = request.GET.get('search',False)
    type = request.GET.get('type')
    page = int(request.GET.get('page',1))
    try:selected_date = datetime.datetime(*strptime(request.GET['date'], "%Y-%m-%d")[0:3])
    except:selected_date = datetime.date.today()
    data = {}
    template='default/movies/movies-showtimes.html'
    if keyword:
        if type == 'movie':
            movie = Movies.objects.get(title = keyword)
            data['movie'] = movie
            template='default/movies/movie-showtimes-details.html'
        elif type == 'theatre':
            theatre = Theatres.objects.get(name = keyword)
            try:showtimes = ShowTime.objects.filter(movietime__theatre = theatre, date = selected_date).order_by('date')
            except:showtimes = False
            data['theater'] = theatre
            data['showtimes'] = showtimes
            template = 'default/movies/theater-details.html'
    else:
        try:
            show_times = ShowTime.objects.filter(date = selected_date).distinct('movietime')
            movie_times = MovieTime.objects.filter(id__in = [st.movietime.id for st in show_times]).distinct('movie')
            movies = Movies.objects.filter(id__in = [mt.movie.id for mt in movie_times], status = 'P').order_by('title')
        except:movies = False
        data['movies'] = movies
        
    data['view_type'] = request.GET.get('view','grid')
    data['selected_date'] = selected_date
    data['search'] = search
    data['kw'] = keyword
    if selected_date:base = selected_date
    else:base = datetime.datetime.today()
    data['dateList'] = [ base + datetime.timedelta(days=x) for x in range(0,14) ]
    return render_to_response(template,data,context_instance=RequestContext(request)) 

def movies_showtimes(request, template='default/movies/movies-showtimes.html'):
    fetched_values = ['title','slug','certification']
    sort = request.GET.get('sort','release-date')
    sorder = GET_SORT_ORDER[sort]
    q_text = ()
    q = request.GET.get('key','')
    search = request.GET.get('search',False)
    sfh = request.GET.get('sfh',False)
    
    try:selected_date = datetime.datetime(*strptime(request.GET['date'], "%Y-%m-%d")[0:3])
    except:selected_date = datetime.date.today()
    try:q_text = (Q(title__icontains=q) | Q(synopsis__icontains=q) | Q( director__icontains = q ) | Q( cast__icontains = q ))
    except:q_text = False
    try:
        show_times = ShowTime.objects.filter(date = selected_date).distinct('movietime')
        movie_times = MovieTime.objects.filter(id__in = [st.movietime.id for st in show_times]).distinct('movie')
        if q_text:movies = Movies.objects.only(*fetched_values).filter(q_text, id__in = [mt.movie.id for mt in movie_times], status = 'P').order_by(sorder)
        else:movies = Movies.objects.only(*fetched_values).filter(id__in = [mt.movie.id for mt in movie_times], status = 'P').order_by(sorder)
    except:movies = False
    
    page = int(request.GET.get('page',1))
    data = ds_pagination(movies,page,'movies',ITEMS_PER_PAGE)
    try:
        if sfh and data['count'] == 1:return HttpResponseRedirect(reverse('movies_showtim_details')+'?id='+str(data['movies'][0].id))
    except:pass 
    data['url'] = reverse('movies_movie_showtimes')
    data['sort'] = sort
    data['view_type'] = request.GET.get('view','grid')
    data['selected_date'] = selected_date
    data['today'] = datetime.date.today()
    data['search'] = search
    data['kw'] = q
    base = datetime.datetime.today()
    data['dateList'] = [ base + datetime.timedelta(days=x) for x in range(0,14) ]
    return render_to_response(template,data,context_instance=RequestContext(request)) 

def movies_showtime_details(request, template='default/movies/movie-showtimes-details.html'):
    data = {}
    try:movie = Movies.objects.prefetch_related('movie_showtimes').get(id=request.GET['id'])
    except:return HttpResponseRedirect(reverse('movies_movie_showtimes'))
    base = datetime.datetime.today()
    data['dateList'] = [ base + datetime.timedelta(days=x) for x in range(0,14) ]
    data['movie'] = movie
    return render_to_response(template,data,context_instance=RequestContext(request))

def get_showtimes_by_date(request, template='default/movies/ajax-movie-showtimes.html'):
    data={}
    send_data = {}
    try:
        try:selected_date = datetime.datetime(*strptime(request.GET['sdate'], "%Y-%m-%d")[0:3])
        except:selected_date = datetime.date.today()
        try:showtimes = ShowTime.objects.filter(movietime__movie__id = request.GET['mid'], date = selected_date).order_by('date')
        except:showtimes = False
        data['showtimes'] = showtimes
        data['selected_date'] = selected_date
        data['today'] = datetime.date.today()
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        if showtimes:send_data['show_screens'] = True
        else:send_data['show_screens'] = False
        send_data['status'] = True
    except:send_data['status'] = False    
    return HttpResponse(simplejson.dumps(send_data))
    
def theater_showtimes(request, template='default/movies/theater-showtimes.html'):
    fetched_values=['name','slug','address1','address2','pincode','phone']
    sort = request.GET.get('sort','name')
    sorder = sort
    q_text = ()
    q = request.GET.get('key','')
    search = request.GET.get('search',False)
    
    try:selected_date = datetime.datetime(*strptime(request.GET['date'], "%Y-%m-%d")[0:3])
    except:selected_date = datetime.date.today()
    try:q_text = (Q(name__icontains=q) | Q(address__address1__icontains=q))
    except:q_text = False
    
    if q:
        search = True
    try:
        show_times = ShowTime.objects.filter(date = selected_date).distinct('movietime')
        movie_times = MovieTime.objects.filter(id__in = [st.movietime.id for st in show_times]).distinct('theatre')
        if q_text:theatres = Theatres.objects.filter(q_text,id__in = [mt.theatre.id for mt in movie_times]).order_by(sorder)
        else:theatres = Theatres.objects.filter(id__in = [mt.theatre.id for mt in movie_times]).order_by(sorder)
    except:theatres = False    
    
    page = int(request.GET.get('page',1))
    data = ds_pagination(theatres,page,'theatres',ITEMS_PER_PAGE)
    data['url'] = reverse('movies_theater_showtimes')
    data['sort'] = sort
    data['view_type'] = request.GET.get('view','grid')
    data['selected_date'] = selected_date
    data['today'] = datetime.date.today()
    base = datetime.datetime.today()
    data['dateList'] = [ base + datetime.timedelta(days=x) for x in range(0,14) ]
    data['search'] = search
    data['kw'] = q
    return render_to_response(template,data,context_instance=RequestContext(request)) 

def theater_details(request, slug, template='default/movies/theater-details.html'):
    fetched_values=['name','slug','address1','address2','pincode','city','lat','lon','zoom','phone']
    data = {}
    selected_date = datetime.date.today()
    
    try:theater = Theatres.objects.get(slug=slug)
    except:return HttpResponseRedirect(reverse('movies_theater_showtimes'))
    
    try:showtimes = ShowTime.objects.filter(movietime__theatre = theater, date = selected_date).order_by('date')
    except:showtimes = False
    base = datetime.datetime.today()
    data['dateList'] = [ base + datetime.timedelta(days=x) for x in range(0,14) ]
    data['theater'] = theater
    data['showtimes'] = showtimes
    data['selected_date'] = selected_date
    data['today'] = datetime.date.today()
    return render_to_response(template,data,context_instance=RequestContext(request)) 

def theater_showtimes_by_date(request, template='default/movies/ajax-theater-showtimes.html'):
    data={}
    send_data = {}
    try:
        try:selected_date = datetime.datetime(*strptime(request.GET['sdate'], "%Y-%m-%d")[0:3])
        except:selected_date = datetime.date.today()
        try:showtimes = ShowTime.objects.filter(movietime__theatre__id = request.GET['tid'], date = selected_date).order_by('date')
        except:showtimes = False
        data['showtimes'] = showtimes
        data['selected_date'] = selected_date
        data['today'] = datetime.date.today()
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        send_data['status'] = True
    except:send_data['status'] = False    
    return HttpResponse(simplejson.dumps(send_data))

def movies_details(request, slug, template = 'default/movies/movie-details.html'):
    fetched_values=['title','slug','movie_url','movie_type','release_date','duration_hours','certification','director','cast','synopsis','ratings','writer','web']
    try:movie = Movies.objects.only(*fetched_values).prefetch_related('movie_type').get(slug = slug)
    except:return HttpResponseRedirect(reverse('movies_home_page'))
    
    if movie.release_date:
        if movie.release_date > datetime.date.today():released = False
        else:released = True
    else:released = False
    data = {'movie':movie, 'released':released}
    return render_to_response(template,data,context_instance=RequestContext(request)) 

def update_movie_view_count(request):
    try:
        movie = Movies.objects.get(id = request.GET['id'])
        movie.views = movie.views + 1
        movie.save()
        return HttpResponse('1')
    except:return HttpResponse('0')

def movie_add_to_fav(request):
    try:
        movies = Movies.objects.get(id=request.GET['id'],status='P')
        flag=add_remove_fav(movies,request.user)
        return HttpResponse(flag)
    except:return HttpResponse('0')   
