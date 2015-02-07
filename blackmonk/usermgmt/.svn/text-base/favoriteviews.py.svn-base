from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson

from common.utils import  ds_pagination
from usermgmt.models import Favorite
from article.models import Article
from business.models import Business
from events.models import Event
from videos.models import Videos
from gallery.models import PhotoAlbum
from movies.models import Movies
from attraction.models import Attraction
from classifieds.models import Classifieds

ITEM_PER_PAGE=8

@login_required
def favorites_home(request,template='account/favorite/favorite-home.html'):
    try:page=int(request.GET['page'])
    except:page=1
    view='event'
    allobjects=Favorite.objects.filter(user=request.user)
    object=allobjects.values_list('object_id', flat=True).filter(content_type__model=view)
    objects=Event.objects.filter(id__in=object).order_by('-id')
    
    data = ds_pagination(objects,page,'events',ITEM_PER_PAGE)
    data['view']=view
    data['module_template']='account/favorite/'+view+'.html'
    #data['event_count']=objects.count()
    #data['articles_count']=Article.objects.filter(id__in=allobjects.values_list('object_id', flat=True).filter(content_type__model='article'),status='P').count()
    #data['business_count']=Business.objects.filter(id__in=allobjects.values_list('object_id', flat=True).filter(content_type__model='business'),status='P').count()
    #data['videos_count']=Videos.objects.filter(id__in=allobjects.values_list('object_id', flat=True).filter(content_type__model='videos'),status='P').count()
    return render_to_response(template,data,context_instance=RequestContext(request))
    
@login_required
def ajax_myfav_list(request,view):
    try:page=int(request.GET['page'])
    except:page=1
    if view!='article' and view!='photoalbum' and view!='videos' and view!='movies' and view!='attraction' and view!='event'  and view!='classifieds' and view!='business':
        view='event'
    object=Favorite.objects.values_list('object_id', flat=True).filter(content_type__model=view,user=request.user)
    if view=='article':
        objects=Article.objects.select_related('articlephotos').filter(id__in=object,status='P').order_by('-id')
    elif view=='event':
        objects=Event.objects.filter(id__in=object).order_by('-id')
    elif view=='photoalbum':
        objects=PhotoAlbum.objects.filter(id__in=object).order_by('-id')
    elif view=='videos':
        objects=Videos.objects.filter(id__in=object).order_by('-id')
    elif view=='movies':
        objects=Movies.objects.filter(id__in=object).order_by('-id')
    elif view=='attraction':
        objects=Attraction.objects.filter(id__in=object).order_by('-id')  
    elif view=='classifieds':
        objects=Classifieds.objects.filter(id__in=object).order_by('-id')                                 
    elif view=='business':
        objects=Business.objects.filter(id__in=object).order_by('-id')
    
    else:objects=[]
    
    if view=='article':lview='articles'
    elif view=='event':lview='events'
    elif view=='photoalbum':lview='gallery'
    elif view=='videos':lview='videos'
    elif view=='movies':lview='movies'
    elif view=='attraction':lview='attractions'
    elif view=='classifieds':lview='classifieds'
    elif view=='business':lview='businesslist'
    else:lview=view
    data = ds_pagination(objects,page,lview,ITEM_PER_PAGE)
    return render_to_response('account/favorite/'+view+'.html',data,context_instance=RequestContext(request))

@login_required
def ajax_myfav_delete(request):
    try:
        fav=Favorite.objects.filter(content_type__model=request.GET['module'],user=request.user,object_id=request.GET['id'])
        fav.delete()
        allobjects=Favorite.objects.filter(user=request.user)
        data={'status':1}
        #data['article_count']=Article.objects.filter(id__in=allobjects.values_list('object_id', flat=True).filter(content_type__model='article'),status='P').count()
        #data['forum_count']=Forum.objects.filter(id__in=allobjects.values_list('object_id', flat=True).filter(content_type__model='forum')).count()
        #data['business_count']=Business.objects.filter(id__in=allobjects.values_list('object_id', flat=True).filter(content_type__model='business'),status='P').count()
        #data['videos_count']=Videos.objects.filter(id__in=allobjects.values_list('object_id', flat=True).filter(content_type__model='videos'),status='P').count()
        return HttpResponse(simplejson.dumps(data))
    except:
        return HttpResponse(simplejson.dumps({'status':0}))
    

def add_remove_fav(obj,user):
    try:
        try:
            model = ContentType.objects.get_for_model(obj)
            fav=Favorite.objects.get(content_type__pk=model.id,object_id=obj.id)
            return 2
        except:
           fav=Favorite(content_object=obj,user=user)
           fav.save()
           return 1
    except:return 0
    
def get_fav(obj,user):
    try:
        model = ContentType.objects.get_for_model(obj)
        fav=Favorite.objects.get(content_type__pk=model.id,object_id=obj.id)
        return fav.id
    except:return False    
    
