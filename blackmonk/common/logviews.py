from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import Template ,Context
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.template import RequestContext
from common.utils import ds_pagination
from common.templatetags.ds_utils import get_msg_class_name
from django.utils import simplejson
from events.models import Event
from article.models import Article
from movies.models import Movies
from news.models import News
from videos.models import Videos
from business.models import Business
from gallery.models import PhotoAlbum
from movies.models import Movies
from classifieds.models import Classifieds
from attraction.models import Attraction
from channels.models import Channel
from community.models import Entry
NO_OF_ITEMS_PER_PAGE=5
FEATURE_LIMIT=8

MODULES = {
    "events": Event,
    "article": Article,
    "videos": Videos,
    "business":Business,
    "photos":PhotoAlbum,
    "movies":Movies,
    "classifieds":Classifieds,
    "attraction":Attraction,
    "channel": Channel,
    "community":Entry,
}
def log(request):
    type = request.GET['type']
    id = request.GET['obj_id']
    obj = MODULES[type].objects.get(id=id)
    object_log = obj.audit_log.all()
    data = {}
    if "sort" in request.GET:
        object_log = object_log.order_by(request.GET['sort'])
    #data = ds_pagination(object_log,int(request.GET.get('page',1)),'object_log',NO_OF_ITEMS_PER_PAGE)
    data['object_log'] = object_log
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    data['obj'] = obj
    data['type'] = type
    send_data={}
    send_data['html']=render_to_string("logs/staff/ajax-list-log.html", data,context_instance=RequestContext(request))
    if "ajax" in request.GET:
        data['sort'] = request.GET['sort']
        return render_to_response("logs/staff/ajax-list-log.html", data, context_instance=RequestContext(request))
    if request.GET.get('action')=='ajax':
        return HttpResponse(simplejson.dumps(send_data))
    return render_to_response("logs/staff/logs.html", data, context_instance=RequestContext(request))


def log_delete(request):
    id = request.GET['obj_id']
    type = request.GET['type']
    obj = MODULES[type].objects.get(id=id)
    
    if "ids" in request.GET:
        object_log = obj.audit_log.filter(pk__in=request.GET['ids'].split(","))
        object_log.delete()
    else: 
        pk = request.GET['log_id']
        object_log = obj.audit_log.get(pk=pk)
        object_log.delete()
    msg="The log has been deleted"
    mtype=get_msg_class_name('s')
    send_data={}
    send_data['msg']=msg
    send_data['mtype']=mtype
    return HttpResponse(simplejson.dumps(send_data))
