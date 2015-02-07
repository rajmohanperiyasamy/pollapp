#Python

#Django
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.db.models import Count
from django.contrib import messages
#Library
from common.static_msg import ARTICLE_MSG
from common.admin_utils import success_response_to_save_category,response_delete_category,error_response,response_to_save_settings
from common.admin_utils import save_emailsettings, get_emailsettings
from common.templatetags.ds_utils import get_msg_class_name
from common.models import ModuleNames, ApprovalSettings

from common.forms import ApprovalSettingForm,SEOForm
from usermgmt.decorators import admin_required

from article.models import ArticleCategory,Article,ArticlePrice
from article.forms import ArticleCategoryForm,ArticleCategorySeoForm,ArticlePriceForm

"""
#####################################################################################################################
#################################   ADMIN PORTAL Articles      ######################################################
#####################################################################################################################
"""

@admin_required
def articles_settings(request, template='admin/portal/article/settings.html'):
    active=inactive=featured=0
    approval=None
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'S':0}
    category=ArticleCategory.objects.all().count()

    article_state = Article.objects.values('featured','is_active','status').annotate(s_count=Count('status'),a_count=Count('is_active'),f_count=Count('featured'))

    for st in article_state:
       STATE[st['status']]+=st['s_count']
       if st['is_active']:
            active+=st['a_count']
       else:
            inactive+=st['a_count']
       if st['featured']:
            featured+=st['f_count']

    data={
          'articles':inactive+active,
          'active':active,
          'published':STATE['P'],
          'pending':STATE['N'],
          'drafted':STATE['D'],
          'rejected':STATE['R'],
          'blocked':STATE['B'],
          'scheduled':STATE['S'],
          'featured':featured,
          'category':category,
    }
    try:
        approval = ApprovalSettings.objects.get(name='article')
        approval_form=ApprovalSettingForm(instance=approval)
    except:approval_form=ApprovalSettingForm()
    try:seo = ModuleNames.get_module_seo(name='article')
    except:seo = ModuleNames(name='article')
    if request.method=='POST':
        if approval:approval_form=ApprovalSettingForm(request.POST,instance=approval)
        else:approval_form=ApprovalSettingForm(request.POST)
        seo_form = SEOForm(request.POST)
        if approval_form.is_valid() and seo_form.is_valid():
            approvals=approval_form.save(commit=False)
            if not approval:approvals.name='article'
            approvals.modified_by=request.user
            approvals.save()

            seo.seo_title = seo_form.cleaned_data.get('meta_title')
            seo.seo_description = seo_form.cleaned_data.get('meta_description')
            seo.modified_by = request.user
            seo.save()
            save_emailsettings(request,'articles')
            extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'emailsettings':get_emailsettings('articles')}
            data.update(extra_data)
            return response_to_save_settings(request,True,data,'admin/portal/article/include_settings.html',ARTICLE_MSG)
        else:
            extra_data = {'seo':seo,'seo_form':seo_form,'approval_form':approval_form,'emailsettings':get_emailsettings('articles')}
            data.update(extra_data)
            return response_to_save_settings(request,False,data,'admin/portal/article/include_settings.html',ARTICLE_MSG)

    extra_data = {'seo':seo,'approval_form':approval_form,'emailsettings':get_emailsettings('articles')}
    data.update(extra_data)
    return render_to_response (template, data, context_instance=RequestContext(request))


################################################## CATEGORY   #########################################
@admin_required
def articles_category(request, template='admin/portal/article/category.html'):
    cat=ArticleCategory.objects.order_by('name')
    data={'categoryes':cat}
    try:data['msg']=ARTICLE_MSG[request.REQUEST['msg']]
    except:data['msg']=None
    try:data['mtype']=request.REQUEST['mtype']
    except:data['mtype']=None
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def articles_category_update(request,template='admin/portal/article/update_category.html'):
    data={}
    category=None
    try:
        category = ArticleCategory.objects.get(id = request.REQUEST['id'])
        form=ArticleCategoryForm(instance=category)
    except:form=ArticleCategoryForm()
    if request.method == "POST":
        if category:form=ArticleCategoryForm(request.POST,instance=category)
        else: form=ArticleCategoryForm(request.POST)
        if form.is_valid():
            cat_form=form.save()
            form=ArticleCategoryForm()
            data = {'form':form,'cat':category}
            append_data={'cat':cat_form,'edit_url':reverse('admin_portal_articles_category_update')}
            return success_response_to_save_category(append_data,data,template,ARTICLE_MSG)
        else:
            data = {'form':form,'cat':category}
            return error_response(data,template,ARTICLE_MSG)
    else:
        data = {'form':form,'cat':category}
        return render_to_response(template,data,context_instance=RequestContext(request))

@admin_required
def articles_category_delete(request):
    data=response_delete_category(request,ArticleCategory,ARTICLE_MSG)
    return HttpResponse(simplejson.dumps(data))

@admin_required
def articles_seo_category_update(request, template='admin/portal/article/update_category_seo.html'):
    try:
        category = ArticleCategory.objects.get(id = request.REQUEST['id'])
        form=ArticleCategorySeoForm(instance=category)
    except:return HttpResponse(ARTICLE_MSG['OOPS'])
    if request.method=='POST':
        form=ArticleCategorySeoForm(request.POST,instance=category)
        if form.is_valid():
            cat_form=form.save(commit=False)
            cat_form.slug=slugify(cat_form.slug)
            cat_form.save()
            data={'status':1,'msg':str(ARTICLE_MSG['CSUS']),'mtype':get_msg_class_name('s')}
            return HttpResponse(simplejson.dumps(data))
        else:
            data = {'form':form,'seo':category}
            return error_response(data,template,ARTICLE_MSG)
    data = {'form':form,'seo':category}
    return render_to_response (template, data, context_instance=RequestContext(request))

########################################################################## Article Price #################################################################################################

@admin_required
def articles_price(request,template='admin/portal/article/pricing.html'):

    data={}
    articleprice_obj = ArticlePrice.objects.get(id=1)
    err=False

    if request.method == "POST":
        form = ArticlePriceForm(request.POST,instance = articleprice_obj)
        if form.is_valid():
            form.save()
            messages.success(request, str(ARTICLE_MSG['APS'])) 
            return HttpResponseRedirect(reverse('admin_portal_articles_price'))
        else:
            data ['article_priceform'] = form
            data['err']=err
            return render_to_response(template,data,context_instance=RequestContext(request) )

    form = ArticlePriceForm(instance = articleprice_obj )
    data ['article_priceform'] = form
#     try:data['msg'] =ARTICLE_MSG[request.GET['msg']]
#     except:data['msg'] =False
#     try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
#     except:data['mtype']=False
    return render_to_response(template,data,context_instance=RequestContext(request) )

