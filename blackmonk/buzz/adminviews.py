import datetime,time

from django.http import HttpResponse, HttpResponseRedirect  
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import permission_required,user_passes_test
from usermgmt.decorators import admin_required
from django.db.models import Q
from django.template import RequestContext
from django.utils import simplejson
from django.core.paginator import Paginator
from django.utils.translation import ugettext as _


from common.utils import *
from buzz.forms import BuzzCategoryForm,TwitterlistsForm,TwitterSettingsForm
from buzz.models import Category,BuzzTwitterLists,TwitterAPISettings
from twitter_login.models import TwitterUser
from django.template.defaultfilters import slugify
from common.getunique import getUniqueValue
from common.admin_utils import success_response_to_save_category,error_response,response_delete_category
from common.static_msg import BUZZ_MSG
from common.templatetags.ds_utils import get_msg_class_name
from common.forms import SEOForm 
from common.models import ModuleNames 

@admin_required  
def buzz_settings(request,template='admin/portal/buzz/twitter-config.html'):
    try:api_settings = TwitterAPISettings.objects.all()[:1][0]
    except:api_settings=False
    if api_settings:form=TwitterSettingsForm(instance=api_settings)
    else:form=TwitterSettingsForm()
    
    try:seo = ModuleNames.get_module_seo(name='buzz')
    except:seo=None
    
    data={'api_settings':api_settings,'form':form,'seo':seo,
          'buzz_cat':Category.objects.count(),
          'twitter_list':BuzzTwitterLists.objects.count()
          }  
    return render_to_response (template, data, context_instance=RequestContext(request))     

@admin_required    
def update_api_settings(request,template='admin/portal/buzz/include-twitter-config.html'): 
    try:api_settings = TwitterAPISettings.objects.all()[:1][0]
    except:api_settings=False
    if request.method=='POST':
        if api_settings:form = TwitterSettingsForm(request.POST,instance=api_settings)
        else:form = TwitterSettingsForm(request.POST)
        
        if form.is_valid():
           form.save()
        else:form = form
        seoform = SEOForm(request.POST)
        try:seo = ModuleNames.get_module_seo(name='buzz')
        except:seo = ModuleNames(name='buzz')
        if seoform.is_valid():
            seo.seo_title = seoform.cleaned_data.get('meta_title')
            seo.seo_description = seoform.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save() 

    data={'api_settings':api_settings,'form':form,'seo':seo,'seoform':seoform,
          'buzz_cat':Category.objects.count(),'twitter_list':BuzzTwitterLists.objects.count()}  
    html=render_to_string(template,data,context_instance=RequestContext(request))
    return_data = {'html':html,'msg':str(BUZZ_MSG['TASS']),'mtype':get_msg_class_name('s')}
    return HttpResponse(simplejson.dumps(return_data))   

@admin_required
def buzz_categories(request,template='admin/portal/buzz/category.html'):
    data={}
    buzz_cats=Category.objects.all().order_by('name')
    data={'buzz_cats':buzz_cats}
    try:data['msg']=BUZZ_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response(template,data, context_instance=RequestContext(request))

@admin_required
def buzz_category_update(request,template='admin/portal/buzz/update_category.html'):
    data={}
    cat=None
    try:cat = Category.objects.get(id=request.REQUEST['id'])
    except:form = BuzzCategoryForm()
    form = BuzzCategoryForm(instance=cat)
    if request.method=='POST':
        if cat:form = BuzzCategoryForm(request.POST,instance=cat)
        else:form = BuzzCategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            if not cat:category.created_by=category.modified_by=request.user
            else:category.modified_by=request.user
            if cat:getUniqueValue(Category,slugify(category.slug),instance_pk=category.id)
            else:getUniqueValue(Category,slugify(category.slug))
            category.save()   
            form=BuzzCategoryForm()
            data = {'form':form,'cat':cat}
            append_data={'cat':category,'edit_url':reverse('adminportal_buzz_category_update')}
            return success_response_to_save_category(append_data,data,template,BUZZ_MSG)
        else:
            data = {'form':form,'cat':cat}
            return error_response(data,template,BUZZ_MSG)
    data = {'form':form,'cat':cat}
    return render_to_response(template,data,context_instance=RequestContext(request))

@admin_required
def buzz_category_delete(request):
    data=response_delete_category(request,Category,BUZZ_MSG)
    return HttpResponse(simplejson.dumps(data))


@admin_required
def buzz_twitter_lists(request,template='admin/portal/buzz/twitter_list.html'):
    data={}
    lists_obj = BuzzTwitterLists.objects.filter().exclude(lists_name__iexact = 'dummy')
    data={'lists_obj':lists_obj}
    try:data['msg']=BUZZ_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response(template,data, context_instance=RequestContext(request))

@admin_required
def buzz_lists_update(request,template='admin/portal/buzz/update-list.html'):
    data={}
    lists_obj=None
    try:
        lists_obj = BuzzTwitterLists.objects.get(id=int(request.REQUEST['id']))
        sel_cat_obj = Category.objects.get(id=lists_obj.category.id)
        data['sel_cat_id'] = sel_cat_obj.id
        form = TwitterlistsForm(instance=lists_obj)
    except:
        form = TwitterlistsForm()
        sel_cat_obj = None
    cat_objs = []
    cat_obs = Category.objects.filter(occupied=False).order_by('-name');
    for cat_ob in cat_obs:
        cat_objs.append(cat_ob)
    if sel_cat_obj:cat_objs.append(sel_cat_obj)
    data['cat_objs'] = cat_objs
    if request.method=='POST':
        if lists_obj:form = TwitterlistsForm(request.POST,instance=lists_obj)
        else:form = TwitterlistsForm(request.POST)
        if form.is_valid():
            list = form.save(commit=False)
            if not lists_obj:list.created_by=list.modified_by=request.user
            else:list.modified_by=request.user
            try:
                ct_obj= Category.objects.get(pk=request.POST['pre_cat_id'])
                ct_obj.occupied = False
                ct_obj.save()
            except:pass       
            cat= Category.objects.get(id=request.POST['category'])
            list.category = cat
            cat.occupied = True
            cat.save()   
            list.save()
            form=TwitterlistsForm()
            data['form'] = form
            data['cat'] = lists_obj
            append_data={'cat':list,'edit_url':reverse('adminportal_buzz_twitter_update')}
            
            lightbox_html=render_to_string(template,data)
            append_html=render_to_string('admin/portal/common/append_category_list.html',append_data)
            send_data={'append_html':append_html, 'lightbox_html':lightbox_html,'status':True,'msg':str(BUZZ_MSG['TWLS']),'mtype':get_msg_class_name('s'),'id':append_data['cat'].id}
            return HttpResponse(simplejson.dumps(send_data))
            
        else:
            data['form'] = form
            data['cat'] = lists_obj
            return error_response(data,template,BUZZ_MSG)
    data['form'] = form
    data['cat'] = lists_obj
    return render_to_response(template,data,context_instance=RequestContext(request))

@admin_required
def buzz_lists_delete(request):
    try:
        try:id=request.GET['id'].split(',')
        except:id=request.GET['id']
        lists = BuzzTwitterLists.objects.filter(id__in=id)
        for list in lists:
            cat= Category.objects.get(id=list.category.id)
            cat.occupied = False
            cat.save()   
        lists.delete()
        status=1
        msg=BUZZ_MSG['TDLS']
        mtype='s'
    except:
        status=0
        msg=BUZZ_MSG['OOPS']
        mtype='e'
    data={'status':status,'msg':str(msg),'mtype':get_msg_class_name(mtype)}
    return HttpResponse(simplejson.dumps(data))

       
