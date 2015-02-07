#Python Libs
import time,datetime
from time import strptime
#Django Libs and Methods
from django.http import HttpResponse, HttpResponseRedirect  
from django.template import Context, loader  
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_list_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django import forms
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.db.models.query import prefetch_related_objects

from django.contrib import messages
from common.staff_messages import POLLS_MSG
from common.utils import ds_pagination,get_global_settings,get_lat_lng
from common.staff_messages import POLLS_MSG,COMMON
from common.templatetags.ds_utils import get_msg_class_name,get_status_class
from polls.models import Poll, Choices
from polls.forms import PollsForm 
from django.core.cache import cache

NO_OF_ITEMS_PER_PAGE=10
NO_OF_ITEMS_FEATURED=8

def ajax_polls_action(request,template='polls/staff/ajax_delete_listing.html'):
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    action_polls = Poll.objects.filter(id__in=id)
    cls_count=action_polls.count()
    status=0
    
    if action=='DEL':
#        if request.user.has_perm('polls.delete_polls'):
        action_polls.delete()
        status=1
        msg=str(POLLS_MSG['PDS'])
        mtype=get_msg_class_name('s')
    else:
        action_polls.update(status=action)
        status=1
        msg=str(POLLS_MSG[action])
        mtype=get_msg_class_name('s')

        
    data=filter_poll(request)
    
    new_id=[]
    for cs in data['polls']:new_id.append(int(cs.id))
    for ai in id:all_ids.remove(ai)

    for ri in all_ids:
        for ni in new_id:
            if int(ni)==int(ri):
                new_id.remove(int(ri))
    
    data['new_id']=new_id
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagination']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
    
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    send_data['msg']=msg
    send_data['mtype']=mtype   
    send_data['status']=status  
    return HttpResponse(simplejson.dumps(send_data))

def filter_poll(request):
    data=key={}
    q=()
    created_user = False
    status = request.GET.get('status','all')
    listing_type = request.GET.get('listing','all')
    created = request.GET.get('created','all')
    sort = request.GET.get('sort','-created_on')
    action = request.GET.get('action',False)
    ids = request.GET.get('ids',False)
    search = request.GET.get('search',False)
    item_perpage=int(request.GET.get('item_perpage',NO_OF_ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))  
    
    if status!='all' and status!='':key['status'] = status
    if created!='all':
        if created =='CSM':key['created_by'] = request.user
        else:created_user = True
    if search:
        search_type = request.GET.get('type',None)
        search_keyword = request.GET.get('kwd',"").strip()
        search_status = request.GET.get('srch_status',None)
    
        if search_status:
            key['status'] = search_status
        
        if search_type:
            if search_type=='title':key['title__icontains'] = search_keyword
            elif search_type=='postedby':key['created_by__display_name__icontains'] = search_keyword
        
        if search_keyword:
            q =(Q(title__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            if not created_user:polls = Poll.objects.filter(~Q(status='D'),q,**key).select_related('created_by').order_by(sort)
            else:polls = Poll.objects.filter(~Q(status='D'),q,**key).select_related('created_by').exclude(created_by = request.user).order_by(sort)
        else:
            if not created_user:
                polls = Poll.objects.filter(~Q(status='D'),**key).select_related('created_by').order_by(sort) 
            else:
                polls = Poll.objects.filter(~Q(status='D'),**key).select_related('created_by').exclude(created_by = request.user).order_by(sort)
                
    else:
        if not created_user:
            polls = Poll.objects.filter(~Q(status='D'),**key).select_related('created_by').order_by(sort)
        else:
            try:polls = Poll.objects.filter(~Q(status='D'),**key).select_related('created_by').exclude(created_by = request.user).order_by(sort)
            except:
                pass
    
    data = ds_pagination(polls,page,'polls',item_perpage)
    data['status'] = status
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    return data     

@staff_member_required
def add_poll(request,template = 'polls/staff/add_poll.html'):
    data = {}
    try:poll_flag = Poll.objects.prefetch_related('choices').get(id=request.REQUEST['pid'])
    except:
        poll_flag = False
    if not request.POST:
        if poll_flag:form =  PollsForm(instance=poll_flag)
        else:form = PollsForm()
    else:
        if poll_flag:form =  PollsForm(request.POST,instance=poll_flag)
        else:form = PollsForm(request.POST)
        if form.is_valid():
            poll=form.save(commit=False)
            poll.created_by = poll.modified_on = request.user
            poll.slug=''
            if not poll_flag:poll.status = 'N'
            if poll_flag and poll_flag.status=='B':poll.status = 'N'
            poll.save()
            if 'pid' in request.REQUEST:
                messages.success(request, str(POLLS_MSG['PUS']))
            else:
                messages.success(request, str(POLLS_MSG['PAS']))        
        
        try:
            
            choices = request.POST.getlist('choices')
            choiceids = request.POST.getlist('choiceids')
            i = 0
            for ch in choices:
                if ch.strip()!='':
                    try:choice_obj = Choices.objects.get(poll=poll,id=choiceids[i])
                    except:choice_obj = Choices(poll=poll)
                    choice_obj.choice = ch
                    choice_obj.save()
                    i = i+1
            
            return HttpResponseRedirect('/staff/polls/')
        except:
            pass
            staff_member_required
 
        else:
            data['form']=form
    data['form'] = form
    data ['poll'] = poll_flag       
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
def home(request , template = 'polls/staff/home.html'):
    polls = Poll.objects.select_related('choices','created_by').order_by('-created_on')
    poll_state = Poll.objects.values('status').exclude(status='D').annotate(s_count=Count('status'))
    total = 0
    STATE={'P':0,'N':0,'B':0,'E':0}
    for st in poll_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    
    data = ds_pagination(polls,'1','polls',NO_OF_ITEMS_PER_PAGE)
    try:
        art = Poll.objects.filter(status = 'P',featured = True)
        sum = art.count()
        if sum >= NO_OF_ITEMS_FEATURED:
            data['feature_limit'] = True
    except:data['feature_limit'] = False  
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    try:data['msg'] = POLLS_MSG[request.GET['msg']]
    except:data['msg'] = None
    try:data['mtype'] = get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    data['total'] =total
    data['published'] =STATE['P']
    data['pending'] =STATE['N']
    data['blocked'] =STATE['B']
    data['expired'] =STATE['E']
    data['search'] =False
    return render_to_response(template, data, context_instance=RequestContext(request))

@staff_member_required
def ajax_list_polls(request,template='polls/staff/ajax-poll-listing.html'):
    data=filter_poll(request)
    send_data={}    
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    return HttpResponse(simplejson.dumps(send_data))

@staff_member_required
@permission_required('polls.publish_polls',raise_exception=True)
def change_status(request):
    try:
        status=request.GET['status']
        polls=Poll.objects.get(id=int(request.GET['id']))
        status = status
        polls.status = status
        polls.save()
        try:cache.clear()
        except:pass
        if status=='P':Poll.objects.filter(status = 'P').exclude(id = polls.id).update(status = 'B')
        html ='<span title="'+get_status_class(polls.status)+'" name="'+polls.status+'" id="id_estatus_'+str(polls.id)+'" class="inline-block status-idty icon-'+get_status_class(polls.status)+'"></span> '          
        return HttpResponse(html)
    except:return HttpResponse('0')

@staff_member_required
def ajax_polls_state(request):
    status = request.GET.get('status','all')
    total = 0
    STATE={'P':0,'N':0,'B':0,'E':0}
   
    if status == 'all':
        polls_state = Poll.objects.values('status').annotate(s_count=Count('status'))
    else:
        polls_state = Poll.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))

    for st in polls_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    data={
          'total':total,
          'published':STATE['P'],
          'pending':STATE['N'],
          'blocked':STATE['B'],
          'expired':STATE['E']
          
    }
    return HttpResponse(simplejson.dumps(data))

@staff_member_required
def polls_preview(request,template='polls/staff/preview.html'):
    data = {}
    try:poll=Poll.objects.prefetch_related('choices').get(id=int(request.GET['pid']))
    except:pass
    data['poll'] = poll
    return render_to_response(template,data, context_instance=RequestContext(request)) 
   
@staff_member_required
def ajax_delete_choice(request):
    data={}
    try:
        choice=Choices.objects.get(poll__id=request.GET['pid'],id=request.GET['cid'])
        choice.delete()
        data['status'] = True
    except:
        data['status'] = False
    return HttpResponse(simplejson.dumps(data))    
        
    
    
    
