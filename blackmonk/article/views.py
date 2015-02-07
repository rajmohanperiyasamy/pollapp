from xml.dom import minidom
import os, zipfile
import random
import re
import datetime,time
from time import strptime
from datetime import timedelta
import calendar
import urllib
import math

from django.http import HttpResponse, HttpResponseRedirect  
from django.template import Context, loader  ,RequestContext
from django.shortcuts import render_to_response, get_list_or_404  
from django.db.models import Q
from django import forms  
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator
from django.utils import simplejson, timezone
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from article.models import ArticlePrice,Tag,ArticleCategory,Article
from common.getunique import getUniqueValue
from common.utils import ds_pagination,get_global_settings
from common.models import ModuleNames
from usermgmt.favoriteviews import add_remove_fav,get_fav

from django.conf import settings as my_settings

def getmonth(m,y):
    data = [0,5,6,7,8,9,10,11,12,1,2,3,4]
    current = datetime.datetime(*strptime('01/'+str(m)+'/'+str(y), "%d/%m/%Y")[0:5])
    ref = datetime.datetime(*strptime('31/04/2012', "%d/%m/%Y")[0:5])
    if ref < current:
        return 12
    else:
        return data[m]
    
NUMBER_DISPLAYED = 12
NUMBER_DISPLAYED_DASH = 12 #changed prev 10

LEADING_PAGE_RANGE_DISPLAYED = TRAILING_PAGE_RANGE_DISPLAYED =10
LEADING_PAGE_RANGE = TRAILING_PAGE_RANGE = 5
NUM_PAGES_OUTSIDE_RANGE = 2
ADJACENT_PAGES = 1


def common_list(request,category):    
    now = timezone.now()
    f_m = now.month
    f_y = now.year
    m = range((-1)*f_m,(-1)*f_m+12)
    c=0
    (dt) =[]
    try:
        for md in m:
            if md < 0:
                    md = md * (-1)
                    y,x = calendar.monthrange(f_y,md)
            else:
                    md = 12 - md
                    y,x = calendar.monthrange(f_y-1,md)
            if c==0:
                    m_first = md
                    y,xx = calendar.monthrange(f_y,md)
            date = str(xx)+'/'+str(m_first)+'/'+str(f_y)
            f_dt = datetime.datetime(*strptime(date, "%d/%m/%Y")[0:5])
            td = f_dt - timedelta(c)                                                                                                               
            c = c+x
            dt.append(td)
    except:pass
   
    (categories)=ArticleCategory.objects.all().order_by('name')
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    
    try:
        (sy)=int(request.GET['year'])
        (sm)=int(request.GET['month'])
    except:
        sm = sy = False
        
    try:
        (tagid) = int(request.GET['tagid'])
    except:
        (tagid) = False
    try:
        (module) = request.GET['module']
    except:
        (module) = False
    if category:
        article_list = Article.objects.defer('content').filter(status='P',category=category.id).select_related('category','album','created_by').order_by('-published_on').distinct()
    elif sm:
        article_list = Article.objects.defer('content').filter(status='P',published_on__year=sy,published_on__month=sm).select_related('category','album','created_by').distinct().order_by('-published_on')
    elif tagid:
        article_list = Article.objects.defer('content').filter(status='P',tags__id=tagid).select_related('category','album','created_by').order_by('-published_on').distinct()
    elif module:
        try:
            article_list = Article.objects.defer('content').filter(status ='P',module_type__name=module).select_related('category','album','created_by').order_by('-published_on').distinct()
        except:
            (module) = False 
            article_list = Article.objects.defer('content').filter(status='P').select_related('category','album','created_by').order_by('-published_on').distinct()
    else:
        article_list = Article.objects.filter(status='P').only('title','summary','slug','created_on','published_on','content','category','album','created_by').select_related('category','album','created_by').order_by('-published_on').distinct()

    data = ds_pagination(article_list,page,'articles',NUMBER_DISPLAYED)
    data['base_url'] = reverse('article_list')
    
    data['view_type'] = request.GET.get('view','grid')
    data['sitesearch'] = 'stories'
    data['module'] = module
    data['month'] = dt
    data['category'] = category
    data['categories'] = categories
    data['tagid'] = tagid
    data['sm'] = sm
    data['sy'] = sy
    data['request'] = RequestContext(request)
    return data

def list_articles(request):
    try:
        category = ArticleCategory.objects.get(id = request.GET['catid'])
    except:
        category = False
    data = common_list(request,category)
    data['seo'] = ModuleNames.get_module_seo(name='article')
    return render_to_response('default/article/displayarticles.html',data, context_instance=RequestContext(request))

def article_category_list(request,catslug):
    try:
        category = ArticleCategory.objects.get(id = request.GET['catid'])
    except:
        category = False
    try:
        if not category:
            category = ArticleCategory.objects.get(slug = catslug)
        data = common_list(request,category)
        try:
            if category:
                data['seo'] = category
            else:
                data['seo'] = ModuleNames.get_module_seo(name='article')
        except:pass
        return render_to_response('default/article/displayarticles.html',data, context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect(reverse('article_list'))

def article_details(request,slug,my=0):
    data={}
    data['sitesearch']='stories'
    try:article = Article.objects.prefetch_related('tags').select_related('category','created_by').get(slug=slug,status='P')
    except:return HttpResponseRedirect(reverse('article_list'))
   
   
    article.most_viewed = article.most_viewed + 1
    article.save(update_fields=['most_viewed'])
    try:data['rate'] = request.GET['rate']
    except:pass
    try:data['message'] = request.GET['message']
    except:pass
    try:data['disqus_sso'] = to_get_disqus_sso(request.user)
    except:pass
    data['article'] = article
    data['similar_articles'] = Article.objects.select_related('articlephotos').filter(tags__in = article.tags.all(), status='P').exclude(id=article.id).only('title','created_on','slug').distinct()[:20]
    return render_to_response('default/article/articledetail.html',data,context_instance=RequestContext(request)) 

def article_details_print_pdf(request,id,pdf=False,template='default/article/articledetail_print_pdf.html'):
    data={}
    try:data['article'] = article = Article.objects.get(id=id,status='P')
    except:return HttpResponseRedirect(reverse('article_list'))
    data['pdf']=pdf
    if pdf:
        from common.utils import  render_to_pdf
        filename=str(article.slug[:120])+'.pdf'
        return render_to_pdf(
            template,
            data,
            filename
        )
     
    else:
        return render_to_response(template,data,context_instance=RequestContext(request))

def ajax_tell_a_friend(request):
    global_settings = get_global_settings()
    scaptcha={}
    if request.method == 'POST':
        try:
            article = Article.objects.get(id=request.POST['content_id'])
            from_name = request.POST['from_name'].strip()
            to_name = request.POST['to_name'].strip()
            to_email = request.POST['to_email'].strip()
            msg = request.POST['msg']
        except:
            scaptcha['success'] = 0
            data  = simplejson.dumps(scaptcha)
            return HttpResponse(data)
       
        subject = global_settings.domain+' - '+from_name+' send you the "'+article.title+'" article details'
        tell_a_friend_data = {}
        tell_a_friend_data['from_name'] = from_name
        tell_a_friend_data['to_name'] = to_name
        tell_a_friend_data['to_email'] = to_email
        tell_a_friend_data['subject'] = subject
        tell_a_friend_data['msg'] = msg
        tell_a_friend_data['article'] = article
        email_message = render_to_string("default/article/mail_tell_a_friend.html",tell_a_friend_data,context_instance=RequestContext(request))
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,[to_email])
        email.content_subtype = "html"
        email.send()
        scaptcha['success'] = 1
        data  = simplejson.dumps(scaptcha)
        return HttpResponse(data)
    else:
        scaptcha['success'] = 0
        data  = simplejson.dumps(scaptcha)
        return HttpResponse(data)

def search_article(request):
    seo = ModuleNames.get_module_seo(name='article')
    try:
        kw = request.REQUEST['keyword'].strip()
        cat = request.REQUEST['category'].strip()
        key = {}
        key['status']='P'
        key_or = (Q(title__icontains=kw) | Q(summary__icontains=kw)| Q(content__icontains=kw))

        if cat == 'All Categories':
            article_list = Article.objects.filter(key_or,**key).order_by('-featured').distinct()
        else:
            category = ArticleCategory.objects.get(name= cat)
            article_list = Article.objects.filter(key_or,category = category,**key).order_by('-featured').distinct()
        
        data = {}
        try:page = int(request.GET['page'])
        except:page = 1
        data = ds_pagination(article_list,page,'articles',NUMBER_DISPLAYED)
        data['categories'] = ArticleCategory.objects.all()
        data['keyword'] = kw
        data['category'] = cat.replace(' ','+')
        data['search'] = True
        data['view_type'] = 'grid'
        return render_to_response('default/article/displayarticles.html',data,context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect(reverse('article_list'))
"""
def auto_suggest_address(request):
    try:data = Venue.objects.filter(venue__icontains=request.GET['term'])[:10]
    except:data = Venue.objects.all()[:10]
    main=[]
    for ve in data:
       if  ve.zip:
           values=','.join([str(ve.venue), str(ve.address1),str(ve.zip)])
       else:
            values=','.join([str(ve.venue), str(ve.address1)]) 
       b={'label':values,'id':str(ve.id),'label':values}
       main.append(b)

    return HttpResponse(simplejson.dumps(main))
"""
def auto_suggest_tag(request):
    try:
        data = Tag.objects.filter(tag__icontains=request.GET['term'])[:10]
    except:
        data = Tag.objects.all()[:10]
    response_dict = {}
    child_dict = []
    response_dict.update({'results':child_dict})
    mytags=[]
    for tag in data :
        b={'label':tag.tag,'id':tag.id,'value':tag.tag}
        mytags.append(b)
    return HttpResponse(simplejson.dumps(mytags))

@login_required
def article_add_to_fav(request):
    try:
        article = Article.objects.get(id=request.GET['id'],status='P')
        flag=add_remove_fav(article,request.user)
        return HttpResponse(flag)
    except:return HttpResponse('0')


from common.utils import get_disqus_sso

def to_get_disqus_sso(user):
    if user.is_authenticated():
        disqus_sso = get_disqus_sso(
            user.id,
            user.display_name,
            user.email, )
    else:
        disqus_sso = get_disqus_sso()
    return disqus_sso

