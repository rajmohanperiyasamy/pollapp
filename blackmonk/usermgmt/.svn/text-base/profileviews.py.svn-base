from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse ,Http404
from django.shortcuts import render_to_response
from django.contrib.auth import get_user_model
from django.template import RequestContext
from django.utils import simplejson

from common.utils import  ds_pagination
from usermgmt.forms import *
from usermgmt.models import  *
from locality.models import  Locality
from article.models import Article
from events.models import Event
#from forum.models import Post,Topic
from classifieds.models import Classifieds
from gallery.models import Photos,PhotoAlbum
from videos.models import Videos
from community.models import Entry
from business.models import Business
from banners.models import BannerAdvertisements
from bookmarks.models import Bookmark
User = get_user_model()


def user_profile(request,username,template="account/profile/public_profile.html"):
    data = {}
    try:
        userid=User.objects.get(profile_slug=username)
        privacy, created = ProfilePrivacy.objects.get_or_create(profile_id=userid.id)
    except User.DoesNotExist:raise Http404
    if not privacy.is_public and not request.user.id is userid.id:
        template = "account/profile/private.html"
    data['profile']=userid
    data['privacy']=privacy
    return render_to_response(template,data, context_instance=RequestContext(request))

   
def user_public_profile(request):
     try:
        id=request.GET['id']
        userid=User.objects.get(pk=id)
        url='/profile/'+userid.profile_slug
        return HttpResponseRedirect(url)
     except:
        return HttpResponseRedirect('/')

def ajax_contribution(request,username):
    data = {
        'article': Article.objects.filter(created_by__profile_slug=username,status='P').count(),
        'events': Event.objects.filter(created_by__profile_slug=username,status='P').count(),
        'photos': PhotoAlbum.objects.filter(created_by__profile_slug=username,status='P').count(),
        'videos': Videos.objects.filter(created_by__profile_slug=username,status='P').count(),
#         'discussion': Post.objects.filter(user__profile_slug=username).count(),
        'classifieds': Classifieds.objects.filter(created_by__profile_slug=username,status='P').count(),
        }
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')

def ajax_profile_module_deatils(request,username):
    view = request.GET['module']
    ITEM_PER_PAGE=8
    try:
        userid=User.objects.get(profile_slug=username)
        privacy, created = ProfilePrivacy.objects.get_or_create(profile_id=userid.id)
    except User.DoesNotExist:raise Http404
    data = {}
    
    try:page=int(request.GET['page'])
    except:page=1
    if view not in ('articles', 'events', 'photos', 'videos', 'business', 'community', 'classifieds','bookmarks'):
        view='articles'
    
    if view=='articles':
        object=Article.objects.select_related('album').filter(created_by__profile_slug=username,status='P').order_by('-id')
    elif view=='events':
        object=Event.objects.select_related('album').filter(created_by__profile_slug=username,status='P').order_by('-id')
    elif view=='photos':
        object=PhotoAlbum.objects.prefetch_related('album_photos').filter(created_by__profile_slug=username,status='P').order_by('-id')
    elif view=='videos':
        object=Videos.objects.select_related('keywords').filter(created_by__profile_slug=username,status='P').order_by('-id')
        ITEM_PER_PAGE=6
    elif view=='business':
        object=Business.objects.filter(created_by__profile_slug=username,status='P').select_related('album').order_by('-id')
        ITEM_PER_PAGE=6
    elif view=='classifieds':
        object=Classifieds.objects.filter(created_by__profile_slug=username,status='P').select_related('album').order_by('-id')
        ITEM_PER_PAGE=12
    elif view=='community':
        object=Entry.objects.filter(created_by__profile_slug=username,status='P').order_by('-id')
        ITEM_PER_PAGE=4
    elif view=='bookmarks':
        object=Bookmark.objects.filter(created_by__profile_slug=username,status='P').order_by('-id')
        ITEM_PER_PAGE=8
        
    data = ds_pagination(object,page,view,ITEM_PER_PAGE)
    data['view']=view
    data['object_count']=object.count()
    data['profile']=userid
    data['view_type'] = request.GET.get('view_type','grid')
    return render_to_response('account/profile/'+view+'.html',data,context_instance=RequestContext(request))
