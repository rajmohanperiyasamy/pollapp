from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Count
from django.contrib import messages

from common.staff_messages import CHANNEL_MSGS
from common.utils import ds_pagination
from common.getunique import getUniqueValue
from common.static_msg import CHANNEL_MSG
from common.staff_messages import COMMON
from common.staff_utils import error_response
from common.templatetags.ds_utils import get_msg_class_name,get_status_class
from channels.form import ChannelForm, ChannelSeoForm
from channels.models import Channel, ArticleWidget, EventWidget, BusinessWidget, VideoWidget, GalleryWidget, DealWidget, AttractionWidget
from article.models import ArticleCategory
from business.models import BusinessCategory
from attraction.models import AttractionCategory
from classifieds.models import ClassifiedCategory
from deal.models import DealCategory
from events.models import EventCategory
from gallery.models import PhotoCategory
from videos.models import VideoCategory

NO_OF_ITEMS_PER_PAGE=10
MODULES = ['articles', 'business', 'events', 'photos', 'videos','deals', 'attractions']
MODULE_WIDGET = {
    'articles': ArticleWidget,
    'business': BusinessWidget,
    'events': EventWidget,
    'photos': GalleryWidget,
    'videos': VideoWidget,
    'deals' : DealWidget,
    'attractions' : AttractionWidget
}
MODULE_CAT = {
    'articles': ArticleCategory,
    'business': BusinessCategory,
    'events': EventCategory,
    'photos': PhotoCategory,
    'videos': VideoCategory,
    'deals' : DealCategory,
    'attractions' : AttractionCategory
}

@staff_member_required    
def manage_channel(request,template='channels/manage-channel.html'):
    page = int(request.GET.get('page',1))
    item_perpage=int(request.GET.get('item_perpage',NO_OF_ITEMS_PER_PAGE))
    channels = Channel.objects.all().order_by('-created_on')
    data = ds_pagination(channels,page,'channels',item_perpage)
    
    total = 0
    STATE={'P':0,'N':0,'R':0,'B':0,'S':0,'D':0}

    channel_state = channels.values('status').annotate(s_count=Count('status'))
    
    for st in channel_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    data.update({
        'total':total,
        'published':STATE['P'],
        'pending':STATE['N'],
        'rejected':STATE['R'],
        'blocked':STATE['B'],
        'scheduled':STATE['S']
    })
    
    try:
        data['msg'] = CHANNEL_MSG[request.GET['msg']]
        data['mtype'] = get_msg_class_name(request.GET['mtype'])
    except:
        pass
    return render_to_response(template, data, context_instance=RequestContext(request))


@staff_member_required
@permission_required('channel.change_channel',raise_exception=True)
def channel_add(request,id=False,template='channels/channel-update.html'):
    data = {}
    try:
        channel=Channel.objects.get(id=id)
        form=ChannelForm(instance=channel)
    except:
        channel = False
        form=ChannelForm()
    if request.method=='POST':
        if channel:
            form=ChannelForm(request.POST, instance=channel)
        else:
            form=ChannelForm(request.POST)
        if form.is_valid():
            channel_form = form.save(commit=False)
            if channel:
                channel_form.slug=getUniqueValue(Channel, slugify(channel_form.slug), instance_pk=channel.id)
            else:
                channel_form.slug=getUniqueValue(Channel, slugify(channel_form.slug))
            channel_form.seo_title = channel_form.title[:70]
            channel_form.seo_description = channel_form.description[:160]
            channel_form.modified_by = request.user
            channel_form.save()
            for module in MODULES:
                if module in request.POST:
                    try: widget = MODULE_WIDGET[module].objects.get(channel=channel)
                    except:
                        widget = MODULE_WIDGET[module](channel=channel)
                        widget.save()
                    widget.categories.clear()
                    for cat in MODULE_CAT[module].objects.filter(id__in=request.POST.getlist(module)):
                        widget.categories.add(cat)
                    widget.save()
            if channel:
                messages.success(request, str(CHANNEL_MSGS['CUS']))  
            else:
                messages.error(request, str(CHANNEL_MSGS['ERR']))
            return HttpResponseRedirect(reverse('staff_channel_manage_channel'))
        print form.errors
    
    selected_artcats = channel.get_selected_artcatids()
    selected_evecats = channel.get_selected_evecatids()
    selected_bizcats = channel.get_selected_bizcatids()
    selected_galcats = channel.get_selected_galcatids()
    selected_vidcats = channel.get_selected_vidcatids()
    selected_dealcats = channel.get_selected_dealcatids()
    selected_attractioncats = channel.get_selected_attractioncatids()
    data = {'form': form, 
            'channel': channel, 
            'l': [1,2,3],
            'cat_set': {'articles': {'all': ArticleCategory.objects.all(),
                                     'selected': selected_artcats,
                                     'count': len(selected_artcats) 
                                    },
                        'events': {'all': EventCategory.objects.all(),
                                   'selected': selected_evecats,
                                   'count': len(selected_evecats)
                                  },
                        'business': {'all': BusinessCategory.objects.all(),
                                   'selected': selected_bizcats,
                                   'count': len(selected_bizcats)
                                  },
                        'photos': {'all': PhotoCategory.objects.filter(is_editable=True),
                                   'selected': selected_galcats,
                                   'count': len(selected_galcats)
                                  },
                        'videos': {'all': VideoCategory.objects.all(),
                                   'selected': selected_vidcats,
                                   'count': len(selected_vidcats)
                                  },
                        'deals': {'all': DealCategory.objects.all(),
                                   'selected': selected_dealcats,
                                   'count': len(selected_dealcats)
                                  },
                        'attractions': {'all': AttractionCategory.objects.all(),
                                   'selected': selected_attractioncats,
                                   'count': len(selected_attractioncats)
                                  },
                       }
           }
    return render_to_response (template, data, context_instance=RequestContext(request)) 


@staff_member_required
@permission_required('channel.change_channel',raise_exception=True)
def ajax_channel_action(request,template='channels/ajax-channel-listing.html'):
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    action_objects = Channel.objects.filter(id__in=id)
    cls_count=action_objects.count()
    page = int(request.GET.get('page',1))
    item_perpage=int(request.GET.get('item_perpage',NO_OF_ITEMS_PER_PAGE))
    status=0
    
    if request.user.has_perm('channel.change_channel'):
        action_objects.update(status=action)
        status=1
        msg=str({"P": "Activated", "B": "Deactivated"}[action]+" successfully")
        mtype=get_msg_class_name('s')
    else:
        msg=str(COMMON['DENIED'])
        mtype=get_msg_class_name('w')

    channels = Channel.objects.all().order_by('-created_on')
    data = ds_pagination(channels,page,'channels',item_perpage)
    
    for channel in action_objects:
        channel.modified_by = request.user
        channel.save()
        for log in channel.audit_log.all()[:1]:
            log.action_type = action
            log.save()
            
    new_id=[]
    for cs in data['channels']:new_id.append(int(cs.id))
    for ai in id:all_ids.remove(ai)

    for ri in all_ids:
        for ni in new_id:
            if int(ni)==int(ri):
                new_id.remove(int(ri))

    data['new_id']=new_id
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagination']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    send_data['msg']=msg
    send_data['mtype']=mtype
    send_data['status']=status
    return HttpResponse(simplejson.dumps(send_data))


def ajax_channel_state(request):
    total = 0
    STATE={'P':0,'N':0,'R':0,'B':0,'S':0,'D':0}

    channel_state = Channel.objects.values('status').annotate(s_count=Count('status'))
    
    for st in channel_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    data={
        'total':total,
        'published':STATE['P'],
        'pending':STATE['N'],
        'rejected':STATE['R'],
        'blocked':STATE['B'],
        'scheduled':STATE['S']
    }
    return HttpResponse(simplejson.dumps(data))

@staff_member_required
def ajax_list_channels(request,template='channels/ajax-channel-listing.html'):
    page = int(request.GET.get('page',1))
    item_perpage=int(request.GET.get('item_perpage',NO_OF_ITEMS_PER_PAGE))
    status = request.GET.get('status','all')
    if status == "all":
        channels = Channel.objects.all().order_by('-created_on')
    else:
        channels = Channel.objects.filter(status=status).order_by('-created_on')
    data = ds_pagination(channels,page,'channels',item_perpage)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    return HttpResponse(simplejson.dumps(send_data))

@staff_member_required
@permission_required('channel.change_channel',raise_exception=True)
def change_status(request):
    obj=Channel.objects.get(id=int(request.GET['id']))
    status = request.GET['status']
    obj.status = status
    obj.modified_by = request.user
    obj.save()
    
    for log in obj.audit_log.all()[:1]:
        log.action_type = status
        log.save()
    
    html ='<span title="'+get_status_class(obj.status)+'" name="'+obj.status+'" id="id_estatus_'+str(obj.id)+'" class="inline-block status-idty icon-'+get_status_class(obj.status)+'"></span> '
    return HttpResponse(html)

def seo(request,id,template='channels/update_seo.html'):
    obj = Channel.objects.get(id = id)
    form = ChannelSeoForm(instance=obj)
    if request.POST:
        form=ChannelSeoForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':"seo updated successfully"}))
        else:
            data={'form':form,'channel':obj}
            return error_response(request,data,template,{'OOPS': 'Error in your submission!'})
    data={'form':form,'channel':obj}
    return render_to_response(template, data, context_instance=RequestContext(request))