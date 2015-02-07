from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db.models import Count
from django.utils.translation import ugettext as _

from common.templatetags.ds_utils import get_msg_class_name
from common.staff_messages import SWEEPSTAKES_MSG,COMMON
from common.getunique import getUniqueValue
from common.utils import ds_pagination
from common.staff_utils import error_response
from common.fileupload import upload_logo,delete_photos_fake
from common.models import AvailableApps
 
from sweepstakes.models import Sweepstakes,SweepstakesOffers,SweepstakesImages,SweepstakesPoints
from sweepstakes.forms import SweepstakesForm,SweepstakesSeoForm,SweepstakesOffersFrom
from sweepstakes.utils import get_unique,get_contest_end_date,LABLE_DIST,EXTRA_LABLE_DIST

NO_OF_ITEMS_PER_PAGE=10

@staff_member_required
def manage_sweepstakes(request,template='sweepstakes/staff/home.html'):
    sweepstakes = Sweepstakes.objects.all().select_related('created_by').order_by('-created_on')
    sweepstakes_state = Sweepstakes.objects.values('status').annotate(s_count=Count('status'))
    
    page = int(request.GET.get('page',1))
    total = 0
    STATE={'E':0,'P':0,'N':0,'B':0}
    
    for st in sweepstakes_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    
    data = ds_pagination(sweepstakes,page,'sweepstakes',NO_OF_ITEMS_PER_PAGE)
    data['status']='all'
    data['created']='all'
    data['sort']='-created_on'
    try:data['msg'] =SWEEPSTAKES_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    data['total'] =total
    data['published'] =STATE['P']
    data['blocked'] =STATE['B']
    data['expired']=STATE['E']
    data['pending']=STATE['N']
    data['search'] =False
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
def ajax_sweepstakes_state(request,template='sweepstakes/staff/ajax_sidebar.html'):
    status = request.GET.get('status','all')
    total = 0
    STATE={'E':0,'P':0,'N':0,'B':0}
    if status == 'all':sweepstakes_state = Sweepstakes.objects.values('status').annotate(s_count=Count('status'))
    else:sweepstakes_state = Sweepstakes.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))
    for st in sweepstakes_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    data={'total':total,'published':STATE['P'],'blocked':STATE['B'],'expired':STATE['E'],'pending':STATE['N']}
    return HttpResponse(simplejson.dumps(data))

@staff_member_required
def ajax_list_sweepstakes(request,template='sweepstakes/staff/ajax_listing.html'):
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

@staff_member_required
def ajax_sweepstakes_action(request,template='sweepstakes/staff/ajax_delete_listing.html'):
    msg=mtype=None
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    sweepstakes = Sweepstakes.objects.filter(id__in=id)
    status=0
    if action=='DEL':
        if request.user.has_perm('sweepstakes.delete_sweepstakes'):
            sweepstakes.delete()
            status=1
            msg=str(SWEEPSTAKES_MSG['SDS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    else:
        if request.user.has_perm('sweepstakes.publish_sweepstakes'):
            sweepstakes.update(status=action)
            status=1
            msg=str(SWEEPSTAKES_MSG['SSCS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    data=filter(request)
    new_id=[]
    
    for cs in data['sweepstakes']:new_id.append(int(cs.id))
    for ai in id:all_ids.remove(ai)

    for ri in all_ids:
        for ni in new_id:
            if int(ni)==int(ri):
                new_id.remove(int(ri))
                
    data['new_id']=new_id
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
        else:args = (~Q(created_by = request.user))
    
    if search:
        search_keyword = request.GET.get('kwd',"").strip()
        
        if search_keyword:
            q =(Q(title__icontains=search_keyword)|Q(contest_id__icontains=search_keyword)|Q(sweepstakes_id__icontains=search_keyword))
            if len(args) == 0 :sweepstakes = Sweepstakes.objects.filter(~Q(status='D'),q,**key).select_related('created_by').order_by(sort)
            else:sweepstakes = Sweepstakes.objects.filter(~Q(status='D'),q,**key).select_related('created_by').exclude(created_by = request.user).order_by(sort)
        else:
            if len(args) == 0 :sweepstakes = Sweepstakes.objects.filter(~Q(status='D'),**key).select_related('created_by').order_by(sort)
            else:sweepstakes = Sweepstakes.objects.filter(~Q(status='D'),**key).select_related('created_by').exclude(created_by = request.user).order_by(sort)
    else:
        if len(args) == 0 :sweepstakes = Sweepstakes.objects.filter(~Q(status='D'),**key).select_related('created_by').order_by(sort)
        else:sweepstakes = Sweepstakes.objects.filter(~Q(status='D'),args,**key).select_related('created_by').order_by(sort)
    
    data = ds_pagination(sweepstakes,page,'sweepstakes',item_perpage)
    data['status'] = status
    data['created'] = created
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    return data 

@staff_member_required
def change_status_sweepstakes(request):
    try:
        sweepstakes=Sweepstakes.objects.get(id=int(request.GET['id']))
        status = request.GET['status']
        sweepstakes.status = status
        sweepstakes.save()
        html ='<span title="'+sweepstakes.get_status().title()+'" name="'+sweepstakes.status+'" id="id_estatus_'+str(sweepstakes.id)+'" class="inline-block status-idty icon-'+sweepstakes.get_status()+'"></span> '          
        return HttpResponse(html)
    except:return HttpResponse('0')

"""
####################################################################################################################
#################################################     ADD    #######################################################
####################################################################################################################
"""

@staff_member_required
def add_sweepstakes(request):
    data={}
    availableapps=AvailableApps.objects.filter(contest='A',status='A').order_by('slug')
    form=SweepstakesForm()
    if request.POST:
        form=SweepstakesForm(request.POST)
        if form.is_valid():
            app_list=request.POST.getlist('available_apps',None)
            sweepstakes=form.save(commit=False)
            if sweepstakes.slug:sweepstakes.slug=getUniqueValue(Sweepstakes,slugify(sweepstakes.slug))
            else:sweepstakes.slug=getUniqueValue(Sweepstakes,slugify(sweepstakes.title))
            sweepstakes.created_by =  sweepstakes.modified_by = request.user
            sweepstakes.status='P'
            sweepstakes.contest_id=get_unique('CI')
            sweepstakes.sweepstakes_id=get_unique('SI')
            sweepstakes.created_by=sweepstakes.modified_by=request.user
            
            if sweepstakes.duration=='W':sweepstakes.select_winners_on=request.POST['duration_week']
            elif sweepstakes.duration=='M':sweepstakes.select_winners_on=request.POST['duration_month']
            if sweepstakes.duration=='N':sweepstakes.current_end_date=sweepstakes.end_date
            else:sweepstakes.current_end_date=get_contest_end_date(request,sweepstakes)
            
            if 'reg_point' in app_list:sweepstakes.reg_point=request.POST.get("reg_point",0)
            else:sweepstakes.reg_point=0
            if 'fb_point' in app_list:sweepstakes.fb_point=request.POST.get("fb_point",0)
            else:sweepstakes.fb_point=0
            if 'friend_point' in app_list:sweepstakes.friend_point=request.POST.get("friend_point",0)
            else:sweepstakes.friend_point=0
            if 'comments' in app_list:sweepstakes.comments=request.POST.get("comments",0)
            else:sweepstakes.comments=0
            
            sweepstakes.save()
            
            for app in availableapps:
                s_points=SweepstakesPoints(app=app,sweepstake=sweepstakes)
                if app.slug in app_list:s_points.app_point=request.POST.get(app.slug,0)
                else:s_points.app_point=0
                s_points.save()
                if app.slug in EXTRA_LABLE_DIST.keys():
                    if app.slug=='advice':
                        if app.slug in app_list:sweepstakes.advice_e=request.POST.get(str(app.slug)+"_e",0)
                        else:sweepstakes.advice_e=0
                    elif app.slug=='discussions':
                        if app.slug in app_list:sweepstakes.discussions_e=request.POST.get(str(app.slug)+"_e",0)
                        else:sweepstakes.discussions_e=0
            sweepstakes.save()
            
            return HttpResponseRedirect(reverse('staff_manage_sweepstakes')+'?msg=SAS&mtype=s')
    data['form']=form
    data['daterange']=[x for x in range(1,32)]
    
    available_apps=[]
    for app in availableapps:
        available_apps.append({'id':app.slug,'slug':app.slug,'name':app.name,'label':LABLE_DIST[app.slug]})
        if app.slug in EXTRA_LABLE_DIST.keys():
            available_apps.append({'id':str(app.slug)+"_e",'slug':app.slug,'name':app.name,'label':EXTRA_LABLE_DIST[app.slug]})
    available_apps.append({'id':"comments",'slug':'comments','name':"Comments",'label':"Post an Comment/Review"})
    available_apps.append({'id':"reg_point",'slug':'reg_point','name':"Registering",'label':"Registering for Contest"})
    available_apps.append({'id':"fb_point",'slug':'fb_point','name':"Facebook Share",'label':"Sharing in Facebook"})
    available_apps.append({'id':"friend_point",'slug':'friend_point','name':"Invite Friends",'label':"Inviting Friends for Contest"})
    data['available_apps']=available_apps
    return render_to_response('sweepstakes/staff/add_sweepstakes.html',data,context_instance=RequestContext(request))  

@staff_member_required
#@permission_required('sweepstakes.change_sweepstakes',raise_exception=True)
def edit_sweepstakes(request,id):
    sweepstake=get_object_or_404(Sweepstakes,id=id)
    availableapps=AvailableApps.objects.filter(contest='A',status='A').order_by('slug')
    data={}
    form=SweepstakesForm(instance=sweepstake)
    if request.POST:
        app_list=request.POST.getlist('available_apps',None)
        form=SweepstakesForm(request.POST,instance=sweepstake)
        if form.is_valid():
            sweepstakes=form.save(commit=False)
            if sweepstakes.slug:sweepstakes.slug=getUniqueValue(Sweepstakes,slugify(sweepstakes.slug),instance_pk=sweepstakes.id)
            else:sweepstakes.slug=getUniqueValue(Sweepstakes,slugify(sweepstakes.title))
            sweepstakes.created_by =  sweepstakes.modified_by = request.user
            sweepstakes.modified_by=request.user

            if sweepstakes.duration=='W':sweepstakes.select_winners_on=request.POST['duration_week']
            elif sweepstakes.duration=='M':sweepstakes.select_winners_on=request.POST['duration_month']
            if sweepstakes.duration=='N':sweepstakes.current_end_date=sweepstakes.end_date
            else:sweepstakes.current_end_date=get_contest_end_date(request,sweepstakes)
           
            if 'reg_point' in app_list:sweepstakes.reg_point=request.POST.get("reg_point",0)
            else:sweepstakes.reg_point=0
            if 'fb_point' in app_list:sweepstakes.fb_point=request.POST.get("fb_point",0)
            else:sweepstakes.fb_point=0
            if 'friend_point' in app_list:sweepstakes.friend_point=request.POST.get("friend_point",0)
            else:sweepstakes.friend_point=0
            if 'comments' in app_list:sweepstakes.comments=request.POST.get("comments",0)
            else:sweepstakes.comments=0
            
            sweepstakes.save()
            
            for app in availableapps:
                s_points=SweepstakesPoints.objects.get(app=app,sweepstake=sweepstakes)
                if app.slug in app_list:s_points.app_point=request.POST.get(app.slug,0)
                else:s_points.app_point=0
                s_points.save()
                if app.slug in EXTRA_LABLE_DIST.keys():
                    if app.slug=='advice':
                        if app.slug in app_list:sweepstakes.advice_e=request.POST.get(str(app.slug)+"_e",0)
                        else:sweepstakes.advice_e=0
                    elif app.slug=='discussions':
                        if app.slug in app_list:sweepstakes.discussions_e=request.POST.get(str(app.slug)+"_e",0)
                        else:sweepstakes.discussions_e=0
            sweepstakes.save()
            return HttpResponseRedirect(reverse('staff_manage_sweepstakes')+'?msg=SAS&mtype=s')
    data['form']=form
    data['daterange']=[x for x in range(1,32)]
    data['sweepstake']=sweepstake
    try:data['cselect_winners_on']=int(sweepstake.select_winners_on)
    except:pass
    availableapps=AvailableApps.objects.filter(contest='A',status='A').order_by('slug')
    availableapps_points=SweepstakesPoints.objects.select_related('app','sweepstake').filter(sweepstake=sweepstake)
    available_apps=[]
    for app in availableapps_points:
        available_apps.append({'id':app.app.slug,'slug':app.app.slug,'name':app.app.name,'label':LABLE_DIST[app.app.slug],'flag':app.app_point})
        if app.app.slug in EXTRA_LABLE_DIST.keys():
            if app.app.slug=='advice':available_apps.append({'id':str(app.app.slug)+"_e",'slug':app.app.slug,'name':app.app.name,'label':EXTRA_LABLE_DIST[app.app.slug],'flag':sweepstake.advice_e})
            elif app.app.slug=='discussions':available_apps.append({'id':str(app.app.slug)+"_e",'slug':app.app.slug,'name':app.app.name,'label':EXTRA_LABLE_DIST[app.app.slug],'flag':sweepstake.discussions_e})
    available_apps.append({'id':"comments",'slug':'comments','name':"Comments",'label':"Post an Comment/Review",'flag':sweepstake.comments})
    available_apps.append({'id':"reg_point",'slug':'reg_point','name':"Registering",'label':"Registering for Contest",'flag':sweepstake.reg_point})
    available_apps.append({'id':"fb_point",'slug':'fb_point','name':"Facebook Share",'label':"Sharing in Facebook",'flag':sweepstake.fb_point})
    available_apps.append({'id':"friend_point",'slug':'friend_point','name':"Invite Friends",'label':"Inviting Friends for Contest",'flag':sweepstake.friend_point})
    
    data['available_apps']=available_apps
    return render_to_response('sweepstakes/staff/update_sweepstakes.html',data,context_instance=RequestContext(request))  

@staff_member_required
def preview_sweepstakes(request,id):
    data={}
    data['sweepstakes']=sweepstakes= Sweepstakes.objects.get(id=id)
    data['offers']=SweepstakesOffers.objects.filter(sweepstakes=sweepstakes)
    
    available_apps=[]
    availableapps=AvailableApps.objects.filter(contest='A',status='A').order_by('slug')
    
    availableapps_points=SweepstakesPoints.objects.filter(sweepstake=sweepstakes)
    
    for app in availableapps_points:
        available_apps.append({'name':app.app.name,'label':LABLE_DIST[app.app.slug],'point':app.app_point})
        if app.app.slug in EXTRA_LABLE_DIST.keys():
            if app.app.slug=='advice':available_apps.append({'name':app.app.name,'label':EXTRA_LABLE_DIST[app.app.slug],'point':sweepstakes.advice_e})
            elif app.app.slug=='discussions':available_apps.append({'name':app.app.name,'label':EXTRA_LABLE_DIST[app.app.slug],'point':sweepstakes.discussions_e})
            
    available_apps.append({'name':"Comments",'label':"Post an Comment/Review",'point':sweepstakes.comments})
    available_apps.append({'name':"Registering",'label':"Registering for Contest",'point':sweepstakes.reg_point})
    available_apps.append({'name':"Facebook Share",'label':"Sharing in Facebook",'point':sweepstakes.fb_point})
    available_apps.append({'name':"Invite Friends",'label':"Inviting Friends for Contest",'point':sweepstakes.friend_point})
    data['available_apps']=available_apps
    
    return render_to_response('sweepstakes/staff/preview.html',data,context_instance=RequestContext(request))  

@staff_member_required
def seo_sweepstakes(request,id,template='sweepstakes/staff/update_seo.html'):
    sweepstakes = Sweepstakes.objects.get(id = id)
    form=SweepstakesSeoForm(instance=sweepstakes)
    if request.POST:
        form=SweepstakesSeoForm(request.POST,instance=sweepstakes)
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(SWEEPSTAKES_MSG['SSUS'])}))
        else:
            data={'form':form,'sweepstakes':sweepstakes}
            return error_response(request,data,template,SWEEPSTAKES_MSG)
    data={'form':form,'sweepstakes':sweepstakes}
    return render_to_response(template,data, context_instance=RequestContext(request))

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################

@staff_member_required
def sweepstakes_update_offer(request,bid,id=None):
    if not request.user.has_perm('sweepstakes.add_sweepstakes') and not request.user.has_perm('sweepstakes.change_sweepstakes'):
        raise PermissionDenied
    data={}
    data['sweepstakes']=sweepstakes= Sweepstakes.objects.get(id=bid)
    if id:
        data['offer']=offer=SweepstakesOffers.objects.get(id=id)
        form=SweepstakesOffersFrom(instance=offer)
    else:form=SweepstakesOffersFrom()
    if request.method=='POST':
        if id:form=SweepstakesOffersFrom(request.POST,instance=offer)
        else:form=SweepstakesOffersFrom(request.POST)
        if form.is_valid():
            offer=form.save(commit=False)
            offer.sweepstakes=sweepstakes
            offer.description=offer.description[:1000]
            try:offer.image=SweepstakesImages.objects.get(id=int(request.POST['image_id']))
            except:pass
            offer.save()
            return HttpResponse(simplejson.dumps({'status':1,'id':offer.id,'msg':str(SWEEPSTAKES_MSG['SOUS']),'mtype':get_msg_class_name('s')}))
        else:
            data['form']=form
            html=render_to_string('sweepstakes/staff/update_offer.html',data,context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'status':0,'html':html,'msg':str(SWEEPSTAKES_MSG['OOPS']),'mtype':get_msg_class_name('e')}))
    data['form']=form
    return render_to_response('sweepstakes/staff/update_offer.html',data,context_instance=RequestContext(request))

@staff_member_required
def sweepstakes_delete_offer(request):
    try:
        if request.user.has_perm('sweepstakes.add_sweepstakes') and request.user.has_perm('sweepstakes.change_sweepstakes'):
            offer=SweepstakesOffers.objects.get(id=int(request.POST['id']))
            offer.delete()
            return HttpResponse(simplejson.dumps({'status':1,'msg':str(SWEEPSTAKES_MSG['SODS']),'mtype':get_msg_class_name('s')}))
        else:
            return HttpResponse(simplejson.dumps({'status':0,'msg':str(SWEEPSTAKES_MSG['OOPS']),'mtype':get_msg_class_name('e')}))
    except:
        return HttpResponse(simplejson.dumps({'status':0,'msg':str(SWEEPSTAKES_MSG['OOPS']),'mtype':get_msg_class_name('e')}))

@staff_member_required
def sweepstakes_offer_load_html(request):
    try:
        if request.user.has_perm('sweepstakes.add_sweepstakes') and request.user.has_perm('sweepstakes.change_sweepstakes'):
            offer=SweepstakesOffers.objects.get(id=int(request.POST['id']))
            sweepstakes= Sweepstakes.objects.get(id=offer.sweepstakes.id)
            data={'offer':offer,'sweepstakes':sweepstakes}
            html=render_to_string('sweepstakes/staff/load_offer.html',data,context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'html':html,'status':1}))
        else:return HttpResponse(simplejson.dumps({'status':0}))
    except:return HttpResponse(simplejson.dumps({'status':0}))

#############################################################################################################################
#############################################################################################################################
#############################################################################################################################
    
@staff_member_required
def ajax_upload_photos(request):  
    try:sweepstakes = Sweepstakes.objects.get(id=request.GET['id'])
    except:sweepstakes=False
    return upload_logo(request,SweepstakesImages,sweepstakes,True)

@staff_member_required
def ajax_upload_photos_offer(request):  
    try:sweepstakes = SweepstakesOffers.objects.get(id=request.GET['id'])
    except:sweepstakes=False
    return upload_logo(request,SweepstakesImages,sweepstakes,True)

@staff_member_required
def ajax_delete_photos(request,pk):
    return delete_photos_fake(request)  
