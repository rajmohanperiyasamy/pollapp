from django.http import HttpResponse, HttpResponseRedirect  
from django.template import Context, loader 
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required 
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.utils import simplejson

from common.utils import ds_pagination
from common.staff_messages import COMMENT_MSG
from common.templatetags.ds_utils import get_msg_class_name
from business.models import Business

from mptt_comments.models import MpttComment
#from community.models import Community_Comment
from mptt_comments.forms import MpttCommentForm
ITEM_PER_PAGE=10


@staff_member_required 
def comments(request,model=None,template='comments/staff/comments_listing.html'):
    key={}
    key['level__gte']=1
    if model:
        if model=='photos':mobj='photoalbum'
        elif model=='community':mobj='entry'
        else:mobj=model
        try:c_type = get_object_or_404(ContentType,model=mobj)
        except:c_type=None
        key['content_type']=c_type

    try:page=int(request.GET['page'])
    except:page=1
    comments=MpttComment.objects.prefetch_related('user').select_related('parent','parent__user','content_object').filter(**key).order_by('-submit_date')
    
    data=ds_pagination(comments,page,'comments',ITEM_PER_PAGE)
    data['m']=model
    data['count_total'] = MpttComment.objects.filter(level__gte=1).count()
    data['count_pending'] = MpttComment.objects.filter(is_public=False).count()
    data['count_published'] = MpttComment.objects.filter(is_public=True, is_removed=False, level__gte=1).count()
    data['count_blocked'] = MpttComment.objects.filter(is_removed=True).count()
    
    return render_to_response(template,data, context_instance=RequestContext(request))
 
@staff_member_required 
def ajax_comments(request,model=None):
    template='comments/staff/ajax_comment_listing.html'
    data=filter(request,model)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    else:send_data['count']=0
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    else:send_data['pagerange']='0 - 0'
    send_data['item_perpage']=data['item_perpage']
    return HttpResponse(simplejson.dumps(send_data))

@staff_member_required
def ajax_comment_action(request,model=None,template='comments/staff/ajax_delete_comment_listing.html'):
    msg=mtype=None
    send_deleted_list=[]
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    comments = MpttComment.objects.filter(id__in=id)
    action_status=0
    try:
        for i in id:send_deleted_list.append(i)
    except:pass
    if action=='DEL':
        for p in comments:
            try:
                if p.content_type.model=='business':
                    buz=Business.objects.get(id=p.object_pk)
                    c_type=ContentType.objects.get_for_model(buz)
                    if c_type.model=='business':
                        com=MpttComment.objects.filter(level__gte=1,content_type=c_type,object_pk=buz.id).exclude(rating=0)
                        com=com.exclude(id__in=id)
                        count=com.count()
                        if count:
                            total_sum=0
                            for c in com:
                                total_sum+=c.rating
                            a=round(float(total_sum/count),1)
                            avg=str(a).split('.')
                            avg[1]=int(avg[1])
                            avg[0]=int(avg[0])
                            if avg[1]==0:rating=avg[0]
                            elif avg[1]>3 and avg[1]< 8:rating=avg[0]+.5
                            else:rating=a+1
                            buz.ratings=rating
                            buz.save()
                        else:
                            buz.ratings=0
                            buz.save()
            except:pass
            
            parent = p.get_descendants(include_self=False)
            if parent:
                for child in parent:
                    try:send_deleted_list.append(child.pk)
                    except: pass
        comments.delete()
        action_status=1
        msg=str(COMMENT_MSG['CDS'])
        mtype=get_msg_class_name('s')
    elif action=='FL':
        comments.update(flag=0)
        action_status=1
        msg=str(COMMENT_MSG['CFCS'])
        mtype=get_msg_class_name('s')
    else:
        if action=='P':
            comments.update(is_public=True)
            comments.update(is_removed=False)
        elif action=='B':
            comments.update(is_removed=True)
        action_status=1
        msg=str(COMMENT_MSG['CSCS'])
        mtype=get_msg_class_name('s')
        
    data=filter(request,model)
    new_id=[]
    
    for cs in data['comments']:new_id.append(int(cs.id))
    for ai in id:all_ids.remove(ai)

    for ri in all_ids:
        for ni in new_id:
            if int(ni)==int(ri):
                new_id.remove(int(ri))
                
    data['new_id']=new_id
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagenation']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    else:send_data['count']=0
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    else:send_data['pagerange']='0 - 0'
    send_data['count_total'] = data['count_total'] 
    send_data['count_pending'] = data['count_pending']
    send_data['count_published'] = data['count_published']
    send_data['count_blocked'] = data['count_blocked']
    send_data['msg']=msg
    send_data['mtype']=mtype
    send_data['action_status']=action_status
    send_data['item_perpage']=data['item_perpage']
    send_data['send_deleted_list']=send_deleted_list
    return HttpResponse(simplejson.dumps(send_data))

def filter(request,model):
    data={}
    key={}
    key['level__gte']=1
    msg = False
    status = request.GET.get('status',None)
    flag = request.GET.get('flag',None)
    sort = request.GET.get('sort','-submit_date')
    if sort not in ['-submit_date','submit_date']:sort ='-submit_date'
    item_perpage=int(request.GET.get('item_perpage',ITEM_PER_PAGE))
    page = int(request.GET.get('page',1))  
    
    if status in ['P']:
        key['is_public']=True
        key['is_removed']=False
    elif status in ['N']:
        key['is_public']=False
        key['is_removed']=False
    elif status in ['B']:key['is_removed']=True
    
    if request.GET['flag'] == 'FL':
        key['flag__gte']=1
        flag='FL'
    else:flag=""
    
    if request.GET['sort'] in ['submit_date','-submit_date']:sort=request.GET['sort']
    else:sort='-id'
    
    if model:
        if model=='photos':mobj='photoalbum'
        elif model=='community':mobj='entry'
        else:mobj=model
        c_type = get_object_or_404(ContentType,model=mobj)
        key['content_type']=c_type
    
    comments=MpttComment.objects.prefetch_related('user').select_related('parent','parent__user','content_object').filter(**key).order_by(sort)
        
    comments=comments.distinct()
    data = ds_pagination(comments,page,'comments',item_perpage)
    data['count_total'] = MpttComment.objects.filter(level__gte=1).count()
    data['count_pending'] = MpttComment.objects.filter(is_public=False).count()
    data['count_published'] = MpttComment.objects.filter(is_public=True, is_removed=False, level__gte=1).count()
    data['count_blocked'] = MpttComment.objects.filter(is_removed=True).count()
    data['status'] = status
    data['flag'] = flag
    data['sort']= sort
    data['m']=model
    data['item_perpage']=item_perpage
    return data 

@staff_member_required
def comment_status_change(request):
    data = {'status': '1'}
    try:
        comment = MpttComment.objects.get(pk=int(request.GET['id']))
        status = request.GET['status']
        if status=='P':
            comment.is_public=True
            comment.is_removed=False
            send_data="published"
        if status=='B':
            comment.is_removed=True
            send_data="blocked"
        comment.save()
        data['html'] = '<span title="'+send_data.title()+'" name="'+status+'" id="id_estatus_'+str(comment.id)+'" class="inline-block status-idty icon-'+send_data+'"></span> '
        data['count_total'] = MpttComment.objects.filter(level__gte=1).count()
        data['count_pending'] = MpttComment.objects.filter(is_public=False).count()
        data['count_published'] = MpttComment.objects.filter(is_public=True, is_removed=False, level__gte=1).count()
        data['count_blocked'] = MpttComment.objects.filter(is_removed=True).count()
        return HttpResponse(simplejson.dumps(data))          
        #return HttpResponse(html)
    except:
        data = {'status': '0'}
        return HttpResponse(simplejson.dumps(data))
        #return HttpResponse('0')


@staff_member_required
def comments_all(request):
    comment = get_object_or_404(MpttComment, pk=comment_id)
    return render_to_response(template,data, context_instance=RequestContext(request))


@staff_member_required 
def comment_list(request,model,object_pk,template='comments/staff/comments_listing.html'):
    c_type = ContentType.objects.get(model=model)
    try:object = c_type.get_object_for_this_type(pk=object_pk)
    except:object = None
    
    key={}
    key['content_type']=c_type
    key['object_pk']=object_pk
    key['level__gte']=1
    
    try:page=int(request.GET['page'])
    except:page=1
    
    try:
        if request.GET['sort'] in ['-flag','submit_date','-submit_date']:sort=request.GET['sort']
        else:sort='-id'
    except:sort='-id'
    try:
        if request.GET['filter'] in ['published']:key['is_public']=True
        elif request.GET['filter'] in ['pending']:key['is_public']=False
        elif request.GET['filter'] in ['blocked']:key['is_removed']=True
    except:pass
    comments=MpttComment.objects.filter(**key).order_by(sort)
    count=comments.count()
    data=ds_pagination(comments,page,'comments',ITEM_PER_PAGE)
    data['object']=object
    data['count']=count
    data['model']=model
    
    data['count_total'] = MpttComment.objects.filter(level__gte=1).count()
    data['count_pending'] = MpttComment.objects.filter(is_public=False).count()
    data['count_published'] = MpttComment.objects.filter(is_public=True, is_removed=False, level__gte=1).count()
    data['count_blocked'] = MpttComment.objects.filter(is_removed=True).count()
    
    return render_to_response(template,data, context_instance=RequestContext(request))
 