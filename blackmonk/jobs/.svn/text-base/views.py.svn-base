import random
from PIL import Image
import os
import stat

from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Q
from django.utils.translation import ugettext as _


from common.utils import ds_pagination
from jobs.models import JobCategory,JobTitle,JobCompany,JobDetail,JobSettings
from common.models import ModuleNames



ITEM_PER_PAGE = 10

def get_ttl_ids(objects):
    dict = []
    for object in objects:
        dict.append(object.title.id)
    return list(set(dict))

def get_cmp_ids(objects):
    dict = []
    for object in objects:
        dict.append(object.company.id)
    return list(set(dict))


def category_list(request):
    category1 = JobCategory.objects.all().order_by('name')[:9]
    category2 = JobCategory.objects.all().order_by('name')[9:18]
    category3 = JobCategory.objects.all().order_by('name')[18:27]
    seo = ModuleNames.get_module_seo(name='jobs')
    jobs=JobSettings.objects.only('post_buttonurl').all()[:1][0]
    if jobs.post_buttonurl:post_button = jobs.post_buttonurl
    else:post_button = False
    data = {'category1':category1,'category2':category2,'category3':category3,'seo':seo,'post_button':post_button}
    return render_to_response('default/jobs/category-index.html',locals(),context_instance=RequestContext(request))

def job_list(request):
    seo = ModuleNames.get_module_seo(name='jobs')
    try:order = request.GET['order']
    except:order= '-active_on'
    jobs = JobDetail.objects.filter(is_active=True).order_by(order)
    ttl_ids = get_ttl_ids(jobs)
    cmp_ids = get_cmp_ids(jobs)
    titles = JobTitle.objects.filter(id__in=ttl_ids).exclude(title='').order_by('-count')[:10]
    companys = JobCompany.objects.filter(id__in=cmp_ids).exclude(company='').order_by('-count')[:10]
    
    try:page = int(request.GET['page'])
    except:page = 1
    
    data = ds_pagination(jobs,page,'jobs',ITEM_PER_PAGE)
    data['order']=order
    data['titles']=titles
    data['seo']=seo
    data['companys']=companys
    data['url'] = '/jobs/joblist/?order=%s'%(order)
    jobs=JobSettings.objects.only('post_buttonurl').all()[:1][0]
    if jobs.post_buttonurl:data['post_button'] = jobs.post_buttonurl
    else:data['post_button'] = False
    return render_to_response('default/jobs/job-list.html',data,context_instance=RequestContext(request))

def attribute_search(request,slug=False):
    seo = ModuleNames.get_module_seo(name='jobs')
    bc=False
    urlappend=''
    jobs = []
    att_type = 'Attribute'
    try:order = request.GET['order']
    except:order= '-active_on'
    message = False
    try:
        if slug=='src':
            bc=request.GET['src']
            jobs=JobDetail.objects.filter(is_active=True,source=bc).order_by(order)
            att_type = "source"
            urlappend = '?src=%s&order=%s'%(bc,order)
        if slug=='cmp':
            bc=request.GET['cmp']
            jobs=JobDetail.objects.filter(is_active=True,company__id=bc).order_by(order)
            att_type = "company"
            urlappend = '?cmp=%s&order=%s'%(bc,order)
        if slug=='ttl':
            bc=request.GET['ttl']
            jobs=JobDetail.objects.filter(is_active=True,title__id=bc).order_by(order)
            att_type = "title"
            urlappend = '?ttl=%s&order=%s'%(bc,order)
        if not slug:
            category=JobCategory.objects.get(slug=slug)
            jobs=JobDetail.objects.filter(is_active=True,category=category).order_by(order)
            att_type = "category"
            seo = category
            bc = category.name
            urlappend = '?order=%s'%(order)
    except:return HttpResponseRedirect('/jobs/joblist/')
    
    try:page = int(request.GET['page'])
    except:page = 1
    
    '''if jobs: 
        message= _('Out of %(jobcount)s job(s) found in the selected %(category)s') % {'jobcount': jobs.count(), 'category':category}
    else:
        message = _("Sorry! There are no Jobs in the selected %(category)s.") %{'category':att_type}'''
    
    ttl_ids = get_ttl_ids(jobs)
    cmp_ids = get_cmp_ids(jobs)
    titles = JobTitle.objects.filter(id__in=ttl_ids).exclude(title='').order_by('-count')[:10]
    companys = JobCompany.objects.filter(id__in=cmp_ids).exclude(company='').order_by('-count')[:10]
    
    data = ds_pagination(jobs,page,'jobs',ITEM_PER_PAGE)
    data['url'] = '/jobs/attsearch/%s/%s'%(slug,urlappend)
    data['bc']=bc
    data['seo']=seo 
    data['jsearch']=True
    data['att_type']=att_type
    data['titles']=titles
    data['companys']=companys
    data['message']=message
    jobs=JobSettings.objects.only('post_buttonurl').all()[:1][0]
    if jobs.post_buttonurl:data['post_button'] = jobs.post_buttonurl
    else:data['post_button'] = False
    return render_to_response('default/jobs/job-list.html',data,context_instance=RequestContext(request))     

def search_job(request):
    seo = ModuleNames.get_module_seo(name='jobs')
    try:order = request.GET['order']
    except:order= '-active_on'
    try:
        skw = request.GET['skw'].strip()
        lkw = request.GET['lkw'].strip()
    except:skw=lkw=''
   
    key = {}
    key['is_active']=True
    if lkw!='':key['location__icontains']=lkw
    
    key_or = (Q(title__title__icontains=skw) | Q(category__name__icontains=skw) | Q(source__icontains=skw) | Q(company__company__icontains=skw))
    jobs = JobDetail.objects.filter(key_or,**key).order_by(order).distinct()
    
    if jobs.count()==0:
        if skw:message = _("Sorry! '%s' did not return any results. Try another keyword."%(skw))
        elif lkw:message = _("Sorry! '%s' did not return any results. Try another Location."%(lkw))
    else:
        message = _(" %(jobcount)s Jobs found for keyword '%(keyword)s'.") %{'jobcount':jobs.count(),'keyword':skw}
        
    ttl_ids = get_ttl_ids(jobs)
    cmp_ids = get_cmp_ids(jobs)
    titles = JobTitle.objects.filter(id__in=ttl_ids).exclude(title='').order_by('-count')[:10]
    companys = JobCompany.objects.filter(id__in=cmp_ids).exclude(company='').order_by('-count')[:10]
    
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    data = ds_pagination(jobs,page,'jobs',ITEM_PER_PAGE)
    data['skw']=skw
    data['lkw']=lkw
    data['seo']=seo
    data['order']=order
    data['message']=message
    data['titles']=titles
    data['companys']=companys
    data['jsearch']=True
    data['url'] = '/jobs/search/?order=%s&skw=%s&lkw=%s'%(order,skw,lkw)
    jobs=JobSettings.objects.only('post_buttonurl').all()[:1][0]
    if jobs.post_buttonurl:data['post_button'] = jobs.post_buttonurl
    else:data['post_button'] = False
    return render_to_response('default/jobs/job-list.html',data,context_instance=RequestContext(request))

