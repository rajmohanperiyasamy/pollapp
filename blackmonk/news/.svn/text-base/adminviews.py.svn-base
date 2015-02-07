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
from common.static_msg import NEWS_MSG
from common.admin_utils import success_response_to_save_category,error_response,response_delete_category,success_response_to_save_provider,response_delete_provider,response_to_save_settings
from common.templatetags.ds_utils import get_msg_class_name
from common.getunique import getUniqueValue
from common.forms import SEOForm
from common.models import ModuleNames
from usermgmt.decorators import admin_required
from news.models import News,Category,Provider
from news.forms import CategoryForm,ProviderForm,SEOCategoryForm

"""
#####################################################################################################################
#################################   ADMIN PORTAL NEWS        ########################################################
#####################################################################################################################
"""

@admin_required
def news_settings(request, template='admin/portal/news/settings.html'):
    active=inactive=0
    
    news=News.objects.all().count()
    news_category = Category.objects.all().count()
    news_provider = Provider.objects.values('is_active').annotate(a_count=Count('is_active'))
    
    for st in news_provider:
        if st['is_active']:
            active+=st['a_count']
        else:
            inactive+=st['a_count']
    
    data={
          'provider':active+inactive,
          'active_provider':active,
          'inactive_provider':inactive,
          'category':news_category,
          'news':news
    }
    try:seo = ModuleNames.get_module_seo(name='news')
    except:seo = ModuleNames(name='news')        
    if request.method=='POST':
        seo_form = SEOForm(request.POST)
        if seo_form.is_valid(): 
            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            extra_data = {'seo':seo,'seo_form':seo_form}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/portal/news/include_settings.html',NEWS_MSG)
        else:
            extra_data = {'seo':seo,'seo_form':seo_form}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/portal/news/include_settings.html',NEWS_MSG)

    data['seo'] = seo
    return render_to_response (template, data, context_instance=RequestContext(request))


################################################## CATEGORY #########################################

@admin_required
def news_category(request, template='admin/portal/news/category.html'):
    category=Category.objects.all().order_by('name')
    data={'category':category}
    try:data['msg']=NEWS_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def news_category_update(request,template='admin/portal/news/update_category.html'):
    data={}
    category=None
    try:
        category= Category.objects.get(id = request.REQUEST['id'])
        form=CategoryForm(instance=category)
    except:
        form=CategoryForm()
    if request.method=='POST':
        if category:form=CategoryForm(request.POST,instance=category)
        else: form=CategoryForm(request.POST)
        if form.is_valid():
            cat_form=form.save(commit=False)
            if category:cat_form.slug = getUniqueValue(Category,slugify(cat_form.slug),instance_pk=cat_form.id)
            else:cat_form.slug = getUniqueValue(Category,slugify(cat_form.slug))
            cat_form.save()
            form=CategoryForm()
            data = {'form':form,'cat':category}
            append_data={'cat':cat_form,'edit_url':reverse('admin_portal_news_category_update')}
            return success_response_to_save_category(append_data,data,template,NEWS_MSG)
        else:
            data = {'form':form,'cat':category}
            return error_response(data,template,NEWS_MSG)
    data = {'form':form,'cat':category}
    return render_to_response(template,data,context_instance=RequestContext(request))


@admin_required
def news_category_delete(request):
    data=response_delete_category(request,Category,NEWS_MSG)
    return HttpResponse(simplejson.dumps(data))

@admin_required
def news_seo_category_update(request, template='admin/portal/news/update_category_seo.html'):
    try:seo = Category.objects.get(id=int(request.REQUEST['id']))
    except:return HttpResponse(NEWS_MSG['CNF'])
    form=SEOCategoryForm(instance=seo)
    if request.method=='POST':
        form=SEOCategoryForm(request.POST,instance=seo)
        if form.is_valid():
            seo=form.save(commit=False)
            seo.slug = getUniqueValue(Category,slugify(seo.slug),instance_pk=seo.id)
            seo.save()
            data={'status':1,'msg':str(NEWS_MSG['CSUS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(data))
        else:
            data={'seo':seo,'form':form}
            return error_response(data,template,NEWS_MSG)
    data = {'form':form,'seo':seo}
    return render_to_response (template, data, context_instance=RequestContext(request))

################################################## CATEGORY #########################################
@admin_required
def news_provider(request, template='admin/portal/news/provider.html'):
    providers=Provider.objects.all().order_by('name')
    data={'providers':providers}
    try:data['msg']=NEWS_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def news_provider_update(request,template='admin/portal/news/update_provider.html'):
    try:
        data={}
        provider=None
        try:
            provider= Provider.objects.get(id = request.REQUEST['id'])
            form=ProviderForm(instance=provider)
        except:form=ProviderForm()
        if request.method=='POST':
            if provider:form=ProviderForm(request.POST,instance=provider)
            else: form=ProviderForm(request.POST)
            if form.is_valid():
                cat_form=form.save()
                form=ProviderForm()
                data = {'form':form,'cat':provider}
                append_data={'cat':cat_form,'edit_url':reverse('admin_portal_news_provider_update')}
                return success_response_to_save_provider(append_data,data,template,NEWS_MSG)
            else:
                data = {'form':form,'cat':provider}
                return error_response(data,template,NEWS_MSG)
        data = {'form':form,'cat':provider}
        return render_to_response(template,data,context_instance=RequestContext(request))
    except:return HttpResponse(str(NEWS_MSG['OOPS']))
    

@admin_required
def news_provider_delete(request):
    data=response_delete_provider(request,Provider,NEWS_MSG)
    return HttpResponse(simplejson.dumps(data))

@admin_required
def news_provider_change_status(request):
    data={}
    try:
        app = Provider.objects.get(id=request.GET['id'])
        if app.is_active:
            app.is_active=False
            status='1'
        else:
            app.is_active=True
            status='2'  
        app.save()
        return HttpResponse(status)     
    except:
        return HttpResponse('0') 
    
@admin_required
def update_news(request):
    from news.tasks import news_feed
    try:
        result=news_feed.delay()
        msg_cls = 's'
        msg = 'FNS'
    except:
        msg_cls = 'e'
        msg = 'OOPS'
    return HttpResponse(simplejson.dumps({'mtype':get_msg_class_name(msg_cls), 'msg':str(NEWS_MSG[msg])}))  
    
