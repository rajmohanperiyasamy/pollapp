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
from common.static_msg import BUSINESS_MSG
from common.admin_utils import success_response_to_save_parent_category,response_delete_attribute_bus
from common.admin_utils import error_response,response_to_save_settings,response_to_save_attribute
from common.admin_utils import response_delete_paymentoption,response_to_save_paymentoption,response_delete_category
from common.admin_utils import save_emailsettings,get_emailsettings
from common.templatetags.ds_utils import get_msg_class_name
from common.models import ModuleNames,ApprovalSettings
from common.getunique import getUniqueValue
from common.forms import ApprovalSettingForm,SEOForm
from usermgmt.decorators import admin_required

from business.models import BusinessCategory,Attributes,AttributeGroup,BusinessPrice,AttributeValues,Business,PaymentOptions,BusinessClaimSettings
from business.forms import AttributesForm,AttributeKeyForm,CategoryForm,SEOCategoryForm,BusinessPriceForm,PaymentOptionsForm,BusinessClaimSettingsForm

"""
#####################################################################################################################
#################################   ADMIN PORTAL BUSINESS    ########################################################
#####################################################################################################################
"""

@admin_required
def business_setting(request, template='admin/portal/business/settings.html'):
    approval=social=claim=None
    active=inactive=parent_cat=sub_cat=0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    LIST={'F':0,'S':0,'B':0}
    
    payment_level = BusinessPrice.objects.filter(level_visibility=True)
    business_attribute=AttributeGroup.objects.all().count()
    business_attribute_key=Attributes.objects.all().count()
    business_category = BusinessCategory.objects.all()
    business_state = Business.objects.values('featured_sponsored','is_active','status').annotate(s_count=Count('status'),a_count=Count('is_active'),f_count=Count('featured_sponsored'))
    
    for st in business_state:
        STATE[st['status']]+=st['s_count']
        try:LIST[st['featured_sponsored']]+=st['f_count']
        except:pass
        if st['is_active']:
            active+=st['a_count']
        else:
            inactive+=st['a_count']
    
    for ct in business_category:
        if ct.parent_cat==None:
            parent_cat+=1
        else:
            sub_cat+=1
            
    data={
          'count_business':active+inactive,
          'active_business':active,
          'inactive_business':inactive,
          
          'published_business':STATE['P'],
          'pending_business':STATE['N'],
          'drafted_business':STATE['D'],
          'rejected_business':STATE['R'],
          'blocked_business':STATE['B'],
          
          'featured_business':LIST['F'],
          'sponsored_business':LIST['S'],
          'basic_business':LIST['B'],
          
          'business_category':sub_cat+parent_cat,
          'sub_category':sub_cat,
          'parent_category':parent_cat,
          
          'payment_level':payment_level,
          'business_attribute':business_attribute,
          'business_attribute_key':business_attribute_key
    }
    try:
        approval = ApprovalSettings.objects.get(name='business')
        approval_form=ApprovalSettingForm(instance=approval)
    except:approval_form=ApprovalSettingForm()
    try:
        claim = BusinessClaimSettings.objects.all()[:1][0]
        claim_form=BusinessClaimSettingsForm(instance=claim)
    except:claim_form=BusinessClaimSettingsForm()
    try:seo = ModuleNames.get_module_seo(name='business')
    except:seo = ModuleNames(name='business')
    if request.method=='POST':
        ############################################
        if approval:approval_form=ApprovalSettingForm(request.POST,instance=approval)
        else:approval_form=ApprovalSettingForm(request.POST)
        ############################################
        if claim:claim_form=BusinessClaimSettingsForm(request.POST,instance=claim)
        else:claim_form=BusinessClaimSettingsForm(request.POST)
        seo_form = SEOForm(request.POST)
        ############################################
        if approval_form.is_valid() and claim_form.is_valid()  and seo_form.is_valid():
            claim_form.save()
            approvals=approval_form.save(commit=False)
            if not approval:approvals.name='business'
            approvals.modified_by=request.user
            approvals.save()
            
            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            ############################################
            save_emailsettings(request,'business')
            ############################################
            data['emailsettings']=get_emailsettings('business')
            extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'claim_form':claim_form,'claim':claim,'business':True}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/portal/business/include_settings.html',BUSINESS_MSG)
        else:
            extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'claim_form':claim_form,'claim':claim,'business':True}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/portal/business/include_settings.html',BUSINESS_MSG)
    extra_data = {'seo':seo,'approval_form':approval_form,'claim_form':claim_form,'claim':claim,'business':True,'emailsettings':get_emailsettings('business')}
    data.update(extra_data)
    return render_to_response (template, data, context_instance=RequestContext(request))
################################################## CATEGORY #########################################

@admin_required
def business_category(request, template='admin/portal/business/category.html'):
    business=BusinessCategory.objects.filter(parent_cat=None).order_by('name')
    data={'parentcategoryes':business}
    data['pcatcount']=business.count()
    try:data['msg']=BUSINESS_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def business_category_update(request,template='admin/portal/business/update_category.html'):
    data={}
    data['pcatcount']=BusinessCategory.objects.filter(parent_cat=None).count()
    category=None
    try:
        category = BusinessCategory.objects.get(id = request.REQUEST['id'])
        form = CategoryForm(instance=category,id=category.id)
    except:
        form = CategoryForm()
    if request.method=='POST':
        if category:
            form = CategoryForm(request.POST,instance=category)
        else:
            form = CategoryForm(request.POST)
        if form.is_valid():
            cat_form=form.save(commit=False)
            if category:
                cat_form.slug = getUniqueValue(BusinessCategory,slugify(cat_form.slug),instance_pk=cat_form.id)
            else:
                cat_form.slug = getUniqueValue(BusinessCategory,slugify(cat_form.slug))
            cat_form.save()
            form=CategoryForm()
            data['form']=form
            data['cat']=category
            append_data={'cat':cat_form,'edit_url':reverse('admin_portal_business_category_update'),'business':True}
            return success_response_to_save_parent_category(append_data,data,template,BUSINESS_MSG,cat_form.parent_cat)
        else:
            data['form']=form
            data['cat']=category
            return error_response(data,template,BUSINESS_MSG)
    data['form']=form
    data['cat']=category
    return render_to_response(template,data,context_instance=RequestContext(request))

@admin_required
def business_category_delete(request):
    data=response_delete_category(request,BusinessCategory,BUSINESS_MSG)
    uncategorised_biz = Business.objects.filter(categories=None)
    if uncategorised_biz.exists():
        uc_parent = BusinessCategory.objects.get_or_create(
            name='Uncategorized',
            slug='uncategorized_parent',
            parent_cat=None
        )[0]
        default_cat = BusinessCategory.objects.get_or_create(
            name='Uncategorized',
            slug='uncategorized_sub',
            parent_cat=uc_parent
        )[0]
        for biz in uncategorised_biz:
            biz.categories.add(default_cat)
    return HttpResponse(simplejson.dumps(data))

@admin_required
def business_seo_category_update(request, template='admin/portal/business/update_category_seo.html'):
    try:seo = BusinessCategory.objects.get(id=int(request.REQUEST['id']))
    except:return HttpResponse(BUSINESS_MSG['CNF'])
    form=SEOCategoryForm(instance=seo)
    if request.method=='POST':
        form=SEOCategoryForm(request.POST,instance=seo)
        if form.is_valid():
            seo=form.save(commit=False)
            seo.slug = getUniqueValue(BusinessCategory,slugify(seo.slug),instance_pk=seo.id)
            seo.save()
            data={'status':1,'msg':str(BUSINESS_MSG['CSUS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(data))
        else:
            data={'seo':seo,'form':form}
            return error_response(data,template,BUSINESS_MSG)
    data = {'form':form,'seo':seo}
    return render_to_response (template, data, context_instance=RequestContext(request))

"""
######################################################################################################################
###########################################      ATTRIBUTES      #####################################################
######################################################################################################################
"""

@admin_required
def business_attribute_group(request):
    allatt = AttributeGroup.objects.all().order_by('order_by','name')
    data = {'attributeall':allatt}
    try:data['msg']=BUSINESS_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response('admin/portal/business/attribute_group.html', data, context_instance=RequestContext(request))


@admin_required
def business_attribute_group_update(request,template='admin/portal/business/update_attribute_group.html'):
    attribute=None
    try:
        attribute = AttributeGroup.objects.get(id=request.REQUEST['id'])
        form= AttributesForm(instance=attribute)
    except:form= AttributesForm()
    if request.method=='POST':
        if attribute:form= AttributesForm(request.POST,instance=attribute)
        else:form= AttributesForm(request.POST)
        if form.is_valid():
            att = form.save()
            form= AttributesForm()
            data={'attribute':attribute,'form':form}
            append_data={'cat':att,'edit_url':reverse('admin_portal_business_attribute_group_update')}
            return response_to_save_attribute(request,append_data,data,template,BUSINESS_MSG,True,True)
        else:
            data={'attribute':attribute,'form':form}
            return error_response(data,template,BUSINESS_MSG)
    data={'attribute':attribute,'form':form}
    return render_to_response(template, data, context_instance=RequestContext(request))
    
@admin_required
def business_attribute_group_delete(request):
    data=response_delete_attribute_bus(request,AttributeGroup,BUSINESS_MSG,True)
    return HttpResponse(simplejson.dumps(data))
    
"""
######################################################################################################################
##########################################       ATTRIBUTES      #####################################################
######################################################################################################################
"""

@admin_required
def business_attributes(request):
    data={}
    try:data['msg']=BUSINESS_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    data['parentcategoryes']=BusinessCategory.objects.filter(parent_cat=None).order_by('name')
    return render_to_response('admin/portal/business/attribute.html', data, context_instance=RequestContext(request))

@admin_required
def business_attributes_load(request):
    try:
        id=int(request.POST['id'])
        allatt = AttributeGroup.objects.all().order_by('order_by','name')
        try:attrbutes=Attributes.objects.filter(category__id=id).order_by('attribute_group','type')
        except:attrbutes=None
        try:
            cat=BusinessCategory.objects.get(id=id)
            if cat.parent_cat:parentattrbutes=Attributes.objects.filter(category__id=cat.parent_cat.id).order_by('attribute_group','type')
            else:parentattrbutes=None 
        except:parentattrbutes=None 
        data = {'attributeall':allatt,'cid':id,'attrbutes':attrbutes,'parentattrbutes':parentattrbutes}
        return render_to_response('admin/portal/business/include_attribute.html', data, context_instance=RequestContext(request))
    except:
        return HttpResponse(str(BUSINESS_MSG['OOPS']))
        
@admin_required
def business_attributes_update(request,template='admin/portal/business/update_attribute.html'):
    attributes=None
    attributegroup = AttributeGroup.objects.get(id=request.REQUEST['gid'])
    category=BusinessCategory.objects.get(id=request.REQUEST['cid'])
    try:
        attributes = Attributes.objects.get(id=request.REQUEST['id'])
        form= AttributeKeyForm(instance=attributes)
    except:form= AttributeKeyForm()
    if request.method=='POST':
        if attributes:form= AttributeKeyForm(request.POST,instance=attributes)
        else:form= AttributeKeyForm(request.POST)
        if form.is_valid():
            att = form.save(commit=False)
            att.category=category
            att.attribute_group=attributegroup
            att.staff_created = True
            att.save()
            if att.type!='C':
                if attributes:
                     if request.POST['av_id']:
                        try:av_ids = request.POST['av_id'].split(',')
                        except:av_ids = request.POST['av_id']
                        for av_id in av_ids:
                            av = AttributeValues.objects.get(id=av_id)
                            name = request.POST['default_values_%d'%(av.id)].strip()
                            is_staff = request.POST['isstaff_%d'%(av.id)]
                            if name:
                                av.name = name
                                if is_staff == '0':av.staff_created = False
                                else:av.staff_created = True
                                av.save()
                            else:av.delete()
                            
                if request.POST['default_values']:
                    try:dvalues = request.POST['default_values'].split(',')
                    except:dvalues = request.POST['default_values']
                    for dv in dvalues:
                        dv = dv.strip()
                        if dv != '':
                            try:av = AttributeValues.objects.get(attribute_key=att,name=dv)
                            except:
                                av = AttributeValues(attribute_key=att)
                                av.staff_created = True
                                av.name = dv
                                av.save() 
            else:
                av=AttributeValues.objects.filter(attribute_key=att)
                av.delete()
                
            form=AttributeKeyForm()
            data={'attributegroup': attributegroup,'attributes':attributes,'form':form,'category':category}
            append_data={'cat':att,'edit_url':reverse('admin_portal_business_attributes_update'),'attributegroup': attributegroup,'attributes':attributes,'category':category}
            return response_to_save_attribute(request,append_data,data,template,BUSINESS_MSG,False)
        else:
            data={'attributegroup': attributegroup,'attributes':attributes,'form':form,'category':category}
            return error_response(data,template,BUSINESS_MSG)
    data={'attributegroup': attributegroup,'attributes':attributes,'form':form,'category':category}
    return render_to_response(template, data, context_instance=RequestContext(request))

@admin_required
def business_attributes_delete(request):
    data=response_delete_attribute_bus(request,Attributes,BUSINESS_MSG,False)
    return HttpResponse(simplejson.dumps(data))

@admin_required
def ajax_business_attribute_values_delete(request):
    try:
        av = AttributeValues.objects.get(id=request.GET['av_id'])
        av.delete()
        return HttpResponse('1')
    except: return HttpResponse('0')


"""
######################################################################################################################
###########################################    PaymentOptions    #####################################################
######################################################################################################################
"""

@admin_required
def business_paymentoptions(request):
    paymentoptions = PaymentOptions.objects.all().order_by('name')
    data = {'paymentoptions':paymentoptions}
    try:data['msg']=BUSINESS_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response('admin/portal/business/paymentoptions.html', data, context_instance=RequestContext(request))


@admin_required
def business_paymentoptions_update(request,template='admin/portal/business/update_paymentoption.html'):
    paymentoption=None
    try:
        paymentoption = PaymentOptions.objects.get(id=request.REQUEST['id'])
        form= PaymentOptionsForm(instance=paymentoption)
    except:form= PaymentOptionsForm()
    if request.method=='POST':
        if paymentoption:form= PaymentOptionsForm(request.POST,instance=paymentoption)
        else:form= PaymentOptionsForm(request.POST)
        if form.is_valid():
            att = form.save()
            form= PaymentOptionsForm()
            data={'attribute':paymentoption,'form':form}
            append_data={'cat':att,'edit_url':reverse('admin_portal_business_paymentoptions_update')}
            return response_to_save_paymentoption(request,append_data,data,template,BUSINESS_MSG)
        else:
            data={'attribute':paymentoption,'form':form}
            return error_response(data,template,BUSINESS_MSG)
    data={'attribute':paymentoption,'form':form}
    return render_to_response(template, data, context_instance=RequestContext(request))

        
@admin_required
def business_paymentoptions_delete(request):
    data=response_delete_paymentoption(request,PaymentOptions,BUSINESS_MSG)
    return HttpResponse(simplejson.dumps(data))

"""
#####################################################################################################################
################################## BUSINESS PRICING #################################################################
#####################################################################################################################
"""   
    
@admin_required
def business_price(request,template='admin/portal/business/pricing.html'):
    data={}
    try:message = Messages[request.GET['msg']]
    except:message = False
    BusinessPriceFormsets=modelformset_factory(BusinessPrice,extra=3,form=BusinessPriceForm,max_num=3)    
    if request.method == 'POST':
        data['business_price_forms']=business_price_forms=BusinessPriceFormsets(request.POST)
        if business_price_forms.is_valid():
            business_price_forms.save()
            messages.success(request, str(BUSINESS_MSG['PUS'])) 
            return HttpResponseRedirect(reverse('admin_portal_business_price'))
        else:data['business_price_forms'] = business_price_forms
    else: data['business_price_forms']=BusinessPriceFormsets()
    try:data['msg'] =BUSINESS_MSG[request.GET['msg']]
    except:data['msg'] =False
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype']=False
    return render_to_response(template, data, context_instance=RequestContext(request))   


@admin_required
def business_sponsored_price(request):
    error=[]
    try:
        categories = BusinessCategory.objects.all()
        for cat in categories:
            price_month = float(request.POST['monthly_price_%d'%(cat.id)])
            price_year = float(request.POST['yearly_price_%d'%(cat.id)])
            if float(price_month) > 0.0:cat.price_month = price_month
            else:
                error.append('Please enter price greater than zero(0) for'+cat.name)
            if float(price_year) > 0.0:cat.price_year = price_year
            else:
                error.append('Please enter price greater than zero(0) for'+cat.name)
            cat.save()
        if len(error)>0:
            data={'msg':str(BUSINESS_MSG['CATP']),'mtype':get_msg_class_name('e')}
            return HttpResponse(simplejson.dumps(data))
        data={'msg':str(BUSINESS_MSG['CPUS']),'mtype':get_msg_class_name('s')}
        return HttpResponse(simplejson.dumps(data))
    except:
        data={'msg':str(BUSINESS_MSG['OOPS']),'mtype':get_msg_class_name('e')}
        return HttpResponse(simplejson.dumps(data))

