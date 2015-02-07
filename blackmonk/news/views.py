import datetime,time,urllib
from datetime import timedelta

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django import forms
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.cache import cache

from news.models import News,Category
from common.models import ModuleNames
from common.utils import ds_pagination


def index(request,cat='all'):
    category = Category.objects.all()
    try:
        page = int(request.GET['page'])
    except:
        page = 1
    #News search 
    try:
        q = request.GET['q']
        news = News.objects.filter(Q(title__icontains=q)|Q(category__name__icontains=q)|Q(provider__name__icontains=q)|Q(summary__icontains=q)).order_by('-id')
        data = ds_pagination(news,page,'news',20)
        updated = updated_time(news)
        seo = ModuleNames.get_module_seo(name='news')
        data['seo'] = seo
        data['category']=category
        data['q']=q
        data['updated']=updated
        return render_to_response('default/news/home_news.html',data,context_instance=RequestContext(request))
    except:pass
    
    #News index
    if cat=='all':
        news = News.objects.all().order_by('-id')
    else:
        news = News.objects.filter(category__slug=cat).order_by('-id')
    try:
        seo = Category.objects.get(slug=cat)
    except:
        seo = ModuleNames.get_module_seo(name='news')

    updated = updated_time(news)
    data = ds_pagination(news,page,'news',20)
    data['seo'] = seo
    try: data['cat_seo'] = Category.objects.get(slug=cat)
    except: data['cat_seo'] = {"name": cat.title(), "seo_title": "News"}
    
    total = data['count']
    displayed = page * 20
    remaining = total - displayed
    data['remaining']=remaining
    data['category']=category
    data['cat']=cat
    data['updated']= updated
    return render_to_response('default/news/home_news.html',data,context_instance=RequestContext(request))

def news_detail(request,slug):
    try:news = News.objects.get(slug=slug)
    except:return HttpResponseRedirect('/news/')
    data={}
    data['news']=news
    return render_to_response('default/news/news_detail.html',data,context_instance=RequestContext(request))

def updated_time(news_obj):
    updated_time = datetime.datetime.now()
    if news_obj:
        for news in news_obj:
            updated_time = news.created_on
            pass
    else:
        news = News.objects.all().order_by('-id')
        for news in news:
            updated_time = news.created_on
            pass
    return updated_time
    
