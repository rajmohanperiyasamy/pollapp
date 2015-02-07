
#Django
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.forms.models import modelformset_factory
from django.utils import simplejson
from django.contrib import messages
from django.db.models import Count

#Library
from usermgmt.decorators import admin_required
from common.static_msg import BANNER_MSG
#from common.admin_utils import success_response_to_save_category,error_response,response_delete_category
#from common.admin_utils import response_to_save_settings,save_emailsettings,get_emailsettings
from common.admin_utils import save_emailsettings, get_emailsettings
from common.templatetags.ds_utils import get_msg_class_name
from common.getunique import getUniqueValue
from common.admin_utils import success_response_to_save_category,response_to_save_settings
from common.models import ModuleNames, ApprovalSettings
from common.forms import ApprovalSettingForm,SEOForm
from banners.models import BannerZones, BannerPayment , BannerZones, BannerAdvertisements
from banners.adminforms import AddBannerZoneForm, BannerPaymentForm



@admin_required
def mange_banner_zones(request, template='admin/banners/manage-zones.html'):
    data = {}
    data['banner_zones'] = BannerZones.objects.all().order_by('-id')
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def add_banner_zone(request, template = 'admin/banners/add-zones.html'):
    data={}
    try:
        zone_obj = BannerZones.objects.get(id=request.REQUEST['bzid'])
        message = 'BZUS' 
    except:
        zone_obj = None
        message = 'BZAS' 
    if request.POST:
        form = AddBannerZoneForm(request.POST,instance=zone_obj)
        if form.is_valid():
            add_banner_zone = form.save(commit=False)
            add_banner_zone.save()
            form.save_m2m()
            banner_zones = BannerZones.objects.all().order_by('-id')
            html = 'admin/banners/include-banner-zones.html'
            status = True
        else:
            banner_zones = None
            html = template
            form = form
            status = False
        html=render_to_string(html,{'zone_obj':zone_obj,'form':form,'banner_zones':banner_zones})
        data['html'] = html
        data['status'] = status
        data['msg'] = str(BANNER_MSG[message])
        data['mtype'] = get_msg_class_name('s')
        return HttpResponse(simplejson.dumps(data))
    else:
        data['form'] = AddBannerZoneForm(instance=zone_obj)
        data['zone_obj'] = zone_obj
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def delete_banner_zone(request):
    data = {}
    try:
        try:ids = request.GET['id'].split(',')
        except:ids = request.GET['id']
        BannerZones.objects.filter(id__in = ids).delete()
        message = 'BZDS'
        msg_class = 's'
        status = True
    except:
        status = False
        message = 'OOPS'
        msg_class = 'e'    
    data['msg'] = str(BANNER_MSG[message])
    data['mtype'] = get_msg_class_name(msg_class)
    data['status'] = status
    return HttpResponse(simplejson.dumps(data))    
    
@admin_required
def banner_payment_settings(request,template='admin/banners/banner-payments.html'):
    data={}
    BannerPaymentFormSets = modelformset_factory(BannerPayment,extra=3,form=BannerPaymentForm,max_num=3)
    """
    try:payment_obj = BannerPayment.objects.all()[:1][0]
    except:payment_obj = None
    """
    if request.method == 'POST':
        data['banner_payment_forms'] = banner_payment_forms = BannerPaymentFormSets(request.POST)
        if banner_payment_forms.is_valid():
            banner_payment_forms.save()
            messages.success(request, str(BANNER_MSG['BAPUS']))
            return HttpResponseRedirect(reverse('admin_configuration_banners_banner_payment_settings'))
        else:data['banner_payment_forms'] = banner_payment_forms
    else:data['banner_payment_forms']= banner_payment_forms = BannerPaymentFormSets() 
    return render_to_response (template, data, context_instance=RequestContext(request))    

@admin_required
def banner_settings(request, template='admin/banners/settings.html'):
    active=inactive=featured=0
    approval=None
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    zones=BannerZones.objects.all().count()
    banners = BannerAdvertisements.objects.values('is_active','status').annotate(b_active=Count('is_active'),b_status=Count('status'))
    for ban in banners:
        STATE[ban['status']]+=ban['b_status']
        if ban['is_active']==True:
            active+=ban['b_active']
        else:
            inactive+=ban['b_active']
    data={
          'banners':inactive+active,
          'active':active,
          'published':STATE['P'],
          'pending':STATE['N'],
          'drafted':STATE['D'],
          'rejected':STATE['R'],
          'blocked':STATE['B'],
          'zone':zones,
    }
    try:
        approval = ApprovalSettings.objects.get(name='banners')
        approval_form=ApprovalSettingForm(instance=approval)
    except:approval_form=ApprovalSettingForm()
    if request.method=='POST':
        if approval:approval_form=ApprovalSettingForm(request.POST,instance=approval)
        else:approval_form=ApprovalSettingForm(request.POST)
        if approval_form.is_valid():
            approvals=approval_form.save(commit=False)
            if not approval:approvals.name='banners'
            approvals.modified_by=request.user
            approvals.save()
            
            save_emailsettings(request,'banners')
            extra_data = {'approval_form':approval_form,'emailsettings':get_emailsettings('banners')}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/banners/include_settings.html',BANNER_MSG)
        else:
            extra_data = {'approval_form':approval_form,'emailsettings':get_emailsettings('banners')}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/banners/include_settings.html',BANNER_MSG)

    extra_data = {'approval_form':approval_form,'emailsettings':get_emailsettings('banners')}
    data.update(extra_data)
    return render_to_response (template, data, context_instance=RequestContext(request))
    