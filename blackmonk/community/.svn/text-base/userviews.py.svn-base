from django.http import HttpResponse, HttpResponseRedirect  
from django.shortcuts import render_to_response
from django.template import Context,RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.utils.html import strip_tags
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db.models import Count
from django.contrib import messages

from common.templatetags.ds_utils import get_msg_class_name
from common.staff_messages import ADVICE_MSG,COMMON
from common.getunique import getUniqueValue
from common.utils import ds_pagination
from common.fileupload import upload_photos,delete_photos
from common.models import ApprovalSettings
from common import signals

from community.models import Topic,Entry

NO_OF_ITEMS_PER_PAGE=10


@login_required
def manage_advice(request,template='advice/user/content_manager.html'):
    advice = Entry.objects.filter(created_by=request.user).select_related('topic','created_by').order_by('-created_on')
    advice_state = Entry.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))
    
    page = int(request.GET.get('page',1))
    total = 0
    STATE={'P':0,'B':0,'N':0}
    for st in advice_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    
    data = ds_pagination(advice,page,'advice',NO_OF_ITEMS_PER_PAGE)
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    
    data['categories'] = Topic.objects.all().order_by('name')
    data['total'] =total
    data['published'] =STATE['P']
    data['blocked'] =STATE['B']
    data['search'] =False
    data['pending'] =STATE['N']
    return render_to_response(template,data, context_instance=RequestContext(request))

@login_required
def ajax_advice_state(request,template='advice/user/ajax_sidebar.html'):
    status = request.GET.get('status','all')
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
   
    if status == 'all':
        advice_state = Entry.objects.values('status').annotate(s_count=Count('status'))
    else:
        advice_state = Entry.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))

    for st in advice_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
        
    data={
          'total':total,
          'published':STATE['P'],
          'blocked':STATE['B'],
          'pending':STATE['N']
    }
    return HttpResponse(simplejson.dumps(data))


@login_required
def ajax_list_advice(request,template='advice/user/ajax_object_listing.html'):
    data=filter(request)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    else:send_data['count']=0
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    else:send_data['pagerange']='0 - 0'
    send_data['item_perpage']=data['item_perpage']
    return HttpResponse(simplejson.dumps(send_data))


@login_required
def ajax_advice_action(request,template='advice/user/ajax_object_listing.html'):
    msg=mtype=None
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    action=request.GET['action']
    advice = Entry.objects.filter(id__in=id,created_by=request.user)
    status=0
    if action=='DEL':
        for adv in advice:
            signals.celery_delete_index.send(sender=None,object=adv)
            signals.create_notification.send(sender=None,user=request.user, obj=adv, not_type='deleted from',obj_title=adv.question)
            if adv.entry_type == 'Q':
                msg=str(ADVICE_MSG['QDS'])
            elif adv.entry_type == 'P':
                msg=str(ADVICE_MSG['PDS'])
            else:
                msg=str(ADVICE_MSG['ADS'])
        advice.delete()
        status=1
        #msg=str(ADVICE_MSG['ADS'])
        mtype=get_msg_class_name('s')
    else:pass

    data=filter(request)
                
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagenation']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    else:send_data['count']=0
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    else:send_data['pagerange']=0-0
    send_data['total'] = Entry.objects.filter(created_by=request.user).count()
    send_data['msg']=msg
    send_data['mtype']=mtype
    send_data['status']=status
    send_data['item_perpage']=data['item_perpage']
    return HttpResponse(simplejson.dumps(send_data))

   
def filter(request):
    data=key={}
    args = q=()
    msg = False
    status = request.GET.get('status','all')
    listing_type = request.GET.get('listing','all')
    created = request.GET.get('created','all')
    sort = request.GET.get('sort','-created_on')
    
    action = request.GET.get('action',False)
    ids = request.GET.get('ids',False)
   
    search = request.GET.get('search',False)
    item_perpage=int(request.GET.get('item_perpage',NO_OF_ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))  
    entry_type = request.GET.get('entry_type')
    
    key['created_by']=request.user
    if entry_type:
        key['entry_type'] = entry_type
    if status!='all' and status!='':key['status'] = status
    if listing_type!='all':key['is_featured'] = listing_type
    if created!='all':
        if created =='CSM':key['created_by'] = request.user
        else:args = (Q(created_by = request.user))
    
    if search:
        search_type = request.GET.get('type',None)
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
        
        if search_category:
            categorys = Topic.objects.get(id=search_category)
            key['category'] = categorys
        
        if search_type:
            if search_type=='title':key['title__icontains'] = search_keyword
            elif search_type=='content':key['content__icontains'] = search_keyword
            else:key['created_by__profile__display_name__icontains'] = search_keyword
        if search_keyword:
            q =(Q(title__icontains=search_keyword)|Q(topic__name__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            if len(args) == 0 :advice = Entry.objects.filter(q,**key).select_related('topic','created_by').order_by(sort)
            else:advice = Entry.objects.filter(q,**key).select_related('topic','created_by').order_by(sort)
        else:
            if len(args) == 0 :advice = Entry.objects.filter(**key).select_related('topic','created_by').order_by(sort)
            else:advice = Entry.objects.filter(**key).select_related('topic','created_by').order_by(sort)
    else:
        if len(args) == 0 :
            advice = Entry.objects.filter(**key).select_related('topic','created_by').order_by(sort)
        else:
            advice = Entry.objects.filter(**key).select_related('topic','created_by').order_by(sort)
    data = ds_pagination(advice,page,'advice',item_perpage)
    if entry_type:
        data["entry_type"] = entry_type
    data['status'] = status
    if search:
        data['search_keyword'] = request.GET.get('kwd',"").strip()
    data['listing_type'] = listing_type
    data['created'] = created
    data['total'] = Entry.objects.filter(created_by=request.user).count()
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    return data 

"""
####################################################################################################################
#################################################     ADD    #######################################################
####################################################################################################################
"""

# @login_required
# def add_advice(request):
#     data={}
#     try:
#         adv=Entry.objects.get(id=request.REQUEST['id'],status__in="['N','D']")
#         form=AdviceForm(instance=adv)
#     except:
#         form=AdviceForm()
#         adv=False
#     if request.POST:
#         if adv:form=AdviceForm(request.POST,instance=adv)
#         else:form=AdviceForm(request.POST)
#         if form.is_valid():
#             advice=form.save(commit=False)
#             advice.slug=getUniqueValue(Entry,slugify(advice.question))
#             advice.created_by =  advice.modified_by = request.user
#             approval_settings=ApprovalSettings.objects.get(name='advice')
#             if not approval_settings.free:advice.status = 'P'
#             else:advice.status = 'N'
#             advice.save()
#             try:tags=request.POST['tags'].split(',')
#             except:tags=request.POST['tags']
#             add_tags(advice,tags)
#             if not adv:
#                 signals.create_staffmail.send(sender=None,object=advice,module='advice',action='A',user=request.user)
#                 signals.create_notification.send(sender=None,user=request.user, obj=advice, not_type='added in',obj_title=advice.question)
#             signals.celery_update_index.send(sender=None,object=advice)
#             if 'id' in request.REQUEST:
#                 messages.success(request, str(ADVICE_MSG['AUS']))
#             else:
#                 messages.success(request, str(ADVICE_MSG['AAS']))
#             return HttpResponseRedirect(reverse('user_manage_advice'))
#     try:
#         if request.GET['qus']:form.fields['question'].initial=request.GET['qus']
#     except:pass
#     data['form']=form
#     data['adv']=adv
#     return render_to_response('advice/user/add_advice.html',data,context_instance=RequestContext(request))  


@login_required
def preview_advice(request,id):
    data={}
    data['advice']=advice= Entry.objects.get(id=id,created_by=request.user)
    return render_to_response('advice/user/preview.html',data,context_instance=RequestContext(request))  

def add_tags(advice,taglist):
    advice.tags.clear()
    for tag in taglist:
        try:objtag = Tag.objects.get(tag__iexact = tag)
        except:
            objtag = Tag(tag=tag)
            objtag.save()
        advice.tags.add(objtag)
    advice.save()

def auto_suggest_tag(request):
    try:data = Tag.objects.filter(tags__icontains=request.GET['term'])[:10]
    except:data = Tag.objects.all()[:10]
    main=[]
    for ve in data:
       b={'label':ve.tag,'id':str(ve.id),'label':ve.tag}
       main.append(b)
    return HttpResponse(simplejson.dumps(main))

