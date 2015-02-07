from blackmonk.movies.models import *

from django.http import HttpResponse,HttpRequest,HttpResponseRedirect
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.template import Context, loader
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required,user_passes_test
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
User = get_user_model()
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.db.models import Count

from common.utils import *
from movies.models import *
from movies.forms import AddMovieForm 
from django.conf  import settings
from common.models import ModuleNames


ITEMS_PER_PAGE = 5


def user_home_listing(request):
    ''' Movie Home User  ( listing ) '''
    data = {}
    item_perpage = int(request.GET.get('item_perpage',ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))
    
    moviedisplay = Movies.objects.filter(created_by=request.user).select_related('category','created_by').order_by('-id')
    categories = MovieType.objects.order_by('name')
    movie_state = Movies.objects.values('status').filter(created_by=request.user).annotate(s_count=Count('status'))
    
    msg = request.GET.get('msg',"")
    
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0,'K':0}
    for st in movie_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    data = ds_pagination(moviedisplay,page,'moviedisplay',item_perpage)
    try:data['msg'] =MOVIE_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    data['categories'] = categories
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    data['data_type'] = True
    data['published'] =STATE['P']
    data['drafted'] =STATE['D']
    data['pending'] =STATE['N']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['total'] =total

    return render_to_response('movies/user/user-home.html',data,context_instance=RequestContext(request)) 

