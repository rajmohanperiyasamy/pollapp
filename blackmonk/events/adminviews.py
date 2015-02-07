#Python

#Django
from django.http import HttpResponseRedirect, HttpResponse ,Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.forms.models import modelformset_factory
from django.utils import simplejson
from django.db.models import Count
from django.contrib import messages
#Library
from common.static_msg import EVENTS_MSG
from common.admin_utils import success_response_to_save_category,error_response,response_delete_category,response_to_save_settings
from common.admin_utils import save_emailsettings,get_emailsettings
from common.templatetags.ds_utils import get_msg_class_name
from common.models import ModuleNames,ApprovalSettings
from common.getunique import getUniqueValue
from common.forms import ApprovalSettingForm,SEOForm
from usermgmt.decorators import admin_required

from events.models import Event,EventCategory,EventPrice
from events.forms import EventCategoryForm,CategorySEOForm,EventPriceForm

"""
#####################################################################################################################
#################################   ADMIN PORTAL EVENTS   ###########################################################
#####################################################################################################################
"""
@admin_required
def event_settings(request, template='admin/portal/events/settings.html'):
    approval=None
    active=inactive=0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0}
    LIST={'F':0,'S':0,'B':0}
    
    payment_level = EventPrice.objects.filter(level_visibility=True)
    
    events_category = EventCategory.objects.all().count()
    events_state = Event.objects.values('listing_type','is_active','status').annotate(s_count=Count('status'),a_count=Count('is_active'),f_count=Count('listing_type'))
    
    for st in events_state:
        STATE[st['status']]+=st['s_count']
        try:LIST[st['listing_type']]+=st['f_count']
        except:pass
        if st['is_active']:
            active+=st['a_count']
        else:
            inactive+=st['a_count']
    
    data={
          'no_events':active+inactive,
          'no_active_events':active,
          'no_inactive_events':inactive,
          
          'no_published_events':STATE['P'],
          'no_pending_events':STATE['N'],
          'no_drafted_events':STATE['D'],
          'no_rejected_events':STATE['R'],
          'no_blocked_events':STATE['B'],
          'no_expired_events':STATE['E'],
          
          'no_featured_events':LIST['F'],
          'no_sponsored_events':LIST['S'],
          'no_basic_events':LIST['B'],
          
          'event_category':events_category,
          
          'payment_level':payment_level
          
    }
    try:
        approval = ApprovalSettings.objects.get(name='events')
        approval_form=ApprovalSettingForm(instance=approval)
    except:approval_form=ApprovalSettingForm()
    try:seo = ModuleNames.get_module_seo(name='events')
    except:seo = ModuleNames(name='events')
    if request.method=='POST':
        ############################################
        if approval:approval_form=ApprovalSettingForm(request.POST,instance=approval)
        else:approval_form=ApprovalSettingForm(request.POST)
        seo_form = SEOForm(request.POST)
        ############################################
        if approval_form.is_valid() and seo_form.is_valid():
           approvals=approval_form.save(commit=False)
           if not approval:approvals.name='events'
           approvals.modified_by=request.user
           approvals.save()
           ############################################
           save_emailsettings(request,'events')
           seo.seo_title = seo_form.cleaned_data.get('meta_title')
           seo.seo_description = seo_form.cleaned_data.get('meta_description')
           seo.modified_by = request.user
           seo.save()
           extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'emailsettings':get_emailsettings('events')}
           data.update(extra_data)
           return response_to_save_settings(request,True,data,'admin/portal/events/include_settings.html',EVENTS_MSG)
        else:
            extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'emailsettings':get_emailsettings('events')}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/portal/events/include_settings.html',EVENTS_MSG)
    extra_data = {'seo':seo,'approval_form':approval_form,'emailsettings':get_emailsettings('events')}
    data.update(extra_data)
    return render_to_response (template, data, context_instance=RequestContext(request))

################################################## CATEGORY #########################################
@admin_required
def event_category(request, template='admin/portal/events/category.html'):
    category=EventCategory.objects.order_by('name')
    data={'category':category}
    try:data['msg']=EVENTS_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def event_category_update(request,template='admin/portal/events/update_category.html'):
    cat=None
    try:cat = EventCategory.objects.get(id=request.REQUEST['id'])
    except:form = EventCategoryForm()
    form = EventCategoryForm(instance=cat)
    if request.method=='POST':
        if cat:form = EventCategoryForm(request.POST,instance=cat)
        else:form = EventCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            if cat:category.slug=getUniqueValue(EventCategory,slugify(category.slug),instance_pk=category.id)
            else:category.slug=getUniqueValue(EventCategory,slugify(category.slug))
            category.save()    
            form=EventCategoryForm()
            data = {'form':form,'cat':cat}
            append_data={'cat':category,'edit_url':reverse('admin_portal_event_category_update')}
            return success_response_to_save_category(append_data,data,template,EVENTS_MSG)
        else:
            data = {'form':form,'cat':cat}
            return error_response(data,template,EVENTS_MSG)
    else:
        data = {'form':form,'cat':cat}
        return render_to_response(template,data,context_instance=RequestContext(request))

@admin_required
def event_category_delete(request):
    data=response_delete_category(request,EventCategory,EVENTS_MSG)
    return HttpResponse(simplejson.dumps(data))

@admin_required
def event_seo_category_update(request, template='admin/portal/events/update_category_seo.html'):
    try:seo = EventCategory.objects.get(id=int(request.REQUEST['id']))
    except:return HttpResponse("?msg=Oops!!! Event not found")
    form=CategorySEOForm(instance=seo)
    if request.method=='POST':
        form = CategorySEOForm(request.POST,instance=seo)
        if form.is_valid():
            seo=form.save(commit=False)
            if seo.slug:seo.slug = getUniqueValue(EventCategory,slugify(seo.slug),instance_pk=seo.id)
            else:seo.slug = getUniqueValue(EventCategory,slugify(seo.name),instance_pk=seo.id)
            seo.save()
            data={'status':1,'msg':str(EVENTS_MSG['CSUS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(data))
        else:
            data={'seo':seo,'form':form}
            return error_response(data,template,EVENTS_MSG)
    data={'seo':seo,'form':form}
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def event_price(request,template='admin/portal/events/pricing.html'):
    ''' method for updating event price information '''
    data={}
    EventPriceFormsets=modelformset_factory(EventPrice,extra=3,form=EventPriceForm,max_num=3)
    if request.method == 'POST':
        data['event_price_forms']=event_price_forms=EventPriceFormsets(request.POST)
        if event_price_forms.is_valid():
            event_price_forms.save()
            messages.success(request, str(EVENTS_MSG['PUS']))
            return HttpResponseRedirect(reverse('admin_portal_event_price')+'?msg=PUS&mtype=s')
        else:data['event_price_forms'] = event_price_forms
    else:data['event_price_forms']=event_price_forms=EventPriceFormsets() 
    try:data['msg'] =EVENTS_MSG[request.GET['msg']]
    except:data['msg'] =False
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype']=False
    print data['msg']
    print data['mtype']
    return render_to_response(template, data, context_instance=RequestContext(request))


    