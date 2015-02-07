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
#Library
from common.static_msg import BOOKMARK_MSG
from common.admin_utils import success_response_to_save_category,response_delete_category,error_response,response_to_save_settings
from common.admin_utils import save_emailsettings,get_emailsettings
from common.templatetags.ds_utils import get_msg_class_name
from common.models import ModuleNames,ApprovalSettings
from common.getunique import getUniqueValue
from common.forms import ApprovalSettingForm,SEOForm
from usermgmt.decorators import admin_required

from bookmarks.models import BookmarkCategory,Bookmark
from bookmarks.forms import BookmarkCategoryForm,BookmarkCategorySeoForm

"""
#####################################################################################################################
#################################   ADMIN PORTAL Bookmarks      ######################################################
#####################################################################################################################
"""
@admin_required
def bookmarks(request, template='admin/portal/bookmarks/home.html'):
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    
    category        = BookmarkCategory.objects.all().count()
    bookmark_state  = Bookmark.objects.values('status').annotate(s_count=Count('status'))
    
    for st in bookmark_state:
       STATE[st['status']]+=st['s_count']
   
    data={
          'bookmarks':0,
          'published':STATE['P'],
          'pending':STATE['N'],
          'drafted':STATE['D'],
          'rejected':STATE['R'],
          'blocked':STATE['B'],
          'category':category
    }
    return render_to_response (template, data, context_instance=RequestContext(request))

################################################## CATEGORY   #########################################

@admin_required
def bookmarks_category(request, template='admin/portal/bookmarks/category.html'):
    cat = BookmarkCategory.objects.all().order_by('name')
    data={'category_list':cat}
    try:data['msg']=BOOKMARK_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def bookmarks_category_update(request,template='admin/portal/bookmarks/update_category.html'):
    data={}
    category=None
    try:
        category = BookmarkCategory.objects.get(id = request.REQUEST['id'])
        form=BookmarkCategoryForm(instance=category)
    except:
        form=BookmarkCategoryForm()
    if request.method == "POST":
        if category:form=BookmarkCategoryForm(request.POST,instance=category)
        else: form=BookmarkCategoryForm(request.POST)
        if form.is_valid():
            cat_form=form.save()
            form=BookmarkCategoryForm()
            data = {'form':form,'cat':category}
            append_data={'cat':cat_form,'edit_url':reverse('admin_portal_bookmarks_category_update')}
            return success_response_to_save_category(append_data,data,template,BOOKMARK_MSG)
        else:
            data = {'form':form,'cat':category}
            return error_response(data,template,BOOKMARK_MSG)
    else: 
        data = {'form':form,'cat':category}
        return render_to_response(template,data,context_instance=RequestContext(request))

@admin_required
def bookmarks_category_delete(request):
    data=response_delete_category(request,BookmarkCategory,BOOKMARK_MSG)
    return HttpResponse(simplejson.dumps(data))

################################################## Approval  #########################################
@admin_required
def bookmarks_settings(request, template='admin/portal/bookmarks/settings.html'):
    approval=None
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0}
    
    category        = BookmarkCategory.objects.all().count()
    bookmark_state  = Bookmark.objects.values('status').annotate(s_count=Count('status'))
    
    for st in bookmark_state:
       STATE[st['status']]+=st['s_count']
   
    data={
          'bookmarks':0,
          'published':STATE['P'],
          'pending':STATE['N'],
          'drafted':STATE['D'],
          'rejected':STATE['R'],
          'blocked':STATE['B'],
          'category':category
    }
    try:
        approval = ApprovalSettings.objects.get(name='bookmark')
        approval_form=ApprovalSettingForm(instance=approval)
    except:approval_form=ApprovalSettingForm()
    try:seo = ModuleNames.get_module_seo(name='bookmark')
    except:seo = ModuleNames(name='bookmark')
    if request.method=='POST':
        if approval:approval_form=ApprovalSettingForm(request.POST,instance=approval)
        else:approval_form=ApprovalSettingForm(request.POST)
        seo_form = SEOForm(request.POST)
        if approval_form.is_valid()  and seo_form.is_valid():
            approvals=approval_form.save(commit=False)
            if not approval:approvals.name='bookmark'
            approvals.modified_by=request.user
            approvals.save()
            
            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            save_emailsettings(request,'bookmarks')
            extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'emailsettings':get_emailsettings('bookmarks')}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/portal/bookmarks/include_settings.html',BOOKMARK_MSG)
        else:
            extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'emailsettings':get_emailsettings('bookmarks')}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/portal/bookmarks/include_settings.html',BOOKMARK_MSG)
    extra_data = {'seo':seo,'approval_form':approval_form,'emailsettings':get_emailsettings('bookmarks')}
    data.update(extra_data)
    return render_to_response (template, data, context_instance=RequestContext(request))

"""
####################################################################################################
###################################### Calssifieds SEO #############################################
####################################################################################################
"""
@admin_required
def bookmarks_seo(request, template='admin/portal/bookmarks/seo.html'):
    classifieds=BookmarkCategory.objects.order_by('name')
    data={'category':classifieds}
    try:data['msg']=BOOKMARK_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def bookmarks_seo_update(request, template='admin/portal/bookmarks/update_seo.html'):
    try:seo = ModuleNames.get_module_seo(name='bookmark')
    except:seo=None
    form=None
    if request.method=='POST':
        form = SEOForm(request.POST)
        try:seo = ModuleNames.get_module_seo(name='bookmark')
        except:seo = ModuleNames(name='bookmark')
        if form.is_valid():
            title = form.cleaned_data.get('meta_title')
            description = form.cleaned_data.get('meta_description')
            keyword = form.cleaned_data.get('meta_keywords')
            seo.seo_title = title
            seo.seo_description = description
            seo.modified_by = request.user
            seo.save()
            data={'status':1,'msg':str(BOOKMARK_MSG['HSUS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(data))
        else:
            data={'seo':seo,'form':form}
            return error_response(data,template,BOOKMARK_MSG)
    data={'seo':seo,'form':form}
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def bookmarks_seo_category_update(request, template='admin/portal/bookmarks/update_category_seo.html'):
    try:
        category = BookmarkCategory.objects.get(id = request.REQUEST['id'])
        form=BookmarkCategorySeoForm(instance=category)
    except:return HttpResponse(BOOKMARK_MSG['OOPS'])
    if request.method=='POST':
        form=BookmarkCategorySeoForm(request.POST,instance=category)
        if form.is_valid():
            cat_form=form.save(commit=False)
            cat_form.slug=slugify(cat_form.slug)
            cat_form.save()
            data={'status':1,'msg':str(BOOKMARK_MSG['CSUS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(data))
        else:
            data = {'form':form,'seo':category}
            return error_response(data,template,BOOKMARK_MSG)
    data = {'form':form,'seo':category}
    return render_to_response (template, data, context_instance=RequestContext(request))

