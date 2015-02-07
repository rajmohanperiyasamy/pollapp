from xml.dom import minidom
import os, zipfile
import random
import re
import datetime,time
from time import strptime
from datetime import timedelta
import calendar
import urllib

from django.http import HttpResponse, HttpResponseRedirect  
from django.template import Context, loader  ,RequestContext
from django.shortcuts import render_to_response, get_list_or_404  
from django.db.models import Q
from django import forms  
from django.template.defaultfilters import slugify
from django.core.paginator import Paginator
from django.utils import simplejson
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from bookmarks.models import BookmarkCategory,Bookmark
from common.getunique import getUniqueValue
from common.utils import ds_pagination,get_global_settings
from common.models import ModuleNames

from django.conf import settings as my_settings

def getmonth(m,y):
    data = [0,5,6,7,8,9,10,11,12,1,2,3,4]
    current = datetime.datetime(*strptime('01/'+str(m)+'/'+str(y), "%d/%m/%Y")[0:5])
    ref = datetime.datetime(*strptime('31/04/2012', "%d/%m/%Y")[0:5])
    if ref < current:
        return 12
    else:
        return data[m]
    
NUMBER_DISPLAYED = 8
NUMBER_DISPLAYED_DASH = 12 #changed prev 10

LEADING_PAGE_RANGE_DISPLAYED = TRAILING_PAGE_RANGE_DISPLAYED =10
LEADING_PAGE_RANGE = TRAILING_PAGE_RANGE = 5
NUM_PAGES_OUTSIDE_RANGE = 2
ADJACENT_PAGES = 1


def common_list(request,category):    
    now = datetime.datetime.now()
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
   
    (categories)=BookmarkCategory.objects.all().order_by('name')
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
        bookmark_list = Bookmark.objects.filter(status='P',category=category.id).distinct().order_by('-created_on')
    elif sm:
        bookmark_list = Bookmark.objects.filter(status='P',published_on__year=sy,published_on__month=sm).distinct().order_by('-created_on')
    elif tagid:
        bookmark_list = Bookmark.objects.filter(status='P',tags__id=tagid).distinct().order_by('-created_on')
    elif module:
        try:
            bookmark_list = Bookmark.objects.filter(status ='P',module_type__name=module).distinct().order_by('-created_on')
        except:
            (module) = False 
            bookmark_list = Bookmark.objects.filter(status='P').distinct().order_by('-created_on')
    else:
        bookmark_list = Bookmark.objects.filter(status='P').distinct().order_by('-created_on')

    data = ds_pagination(bookmark_list,page,'bookmarks',NUMBER_DISPLAYED)
    data['base_url'] = reverse('bookmark_list')
    
    
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


def list_bookmarks(request):
    try:
        category = BookmarkCategory.objects.get(id = request.GET['catid'])
    except:
        category = False
    data = common_list(request,category)
    data['seo'] = ModuleNames.get_module_seo(name='bookmark')
    return render_to_response('default/bookmarks/displaybookmarks.html',data, context_instance=RequestContext(request))

def bookmark_category_list(request,catslug):
    try:
        category = BookmarkCategory.objects.get(id = request.GET['catid'])
    except:
        category = False
    try:
        if not category:
            category = BookmarkCategory.objects.get(slug = catslug)
        data = common_list(request,category)
        try:
            if category:
                data['seo'] = category
            else:
                data['seo'] = ModuleNames.get_module_seo(name='bookmark')
        except:pass
        return render_to_response('default/bookmarks/displaybookmarks.html',data, context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect(reverse('bookmark_list'))

def bookmark_details(request,slug,my=0):
    data={}
    data['sitesearch']='stories'
    try:
        bookmark = Bookmark.objects.get(slug=slug,status='P')
    except:
        return HttpResponseRedirect(reverse('bookmark_list'))
   
    data['category']=BookmarkCategory.objects.all().order_by('name')
   
    try:
        if request.session['bookmarkview%s'%(bookmark.id)] != bookmark.id:
            request.session['bookmarkview%s'%(bookmark.id)] = bookmark.id
            bookmark.most_viewed = bookmark.most_viewed + 1
            bookmark.save()
    except:
        try:
            request.session['bookmarkview%s'%(bookmark.id)] = bookmark.id 
            bookmark.most_viewed = bookmark.most_viewed + 1
            bookmark.save()
        except:pass
    try:
        data['rate'] = request.GET['rate']
    except:pass
    try:
        data['message'] = request.GET['message']
    except:pass
    data['bookmark'] = bookmark
    data['related_bookmark'] = Bookmark.objects.filter(Q(category=bookmark.category) | Q(title__icontains=bookmark.title) | Q(summary__icontains=bookmark.title),status='P')[:8]
    #popular_bookmark = Bookmark.objects.filter(is_active=True,status='P').order_by('-most_viewed')[:8]
    data['justin_bookmark'] = Bookmark.objects.filter(status='P').order_by('-id')[:8]
    return render_to_response('default/bookmarks/bookmarkdetail.html',data,context_instance=RequestContext(request))


def ajax_tell_a_friend(request):
    global_settings = get_global_settings()
    scaptcha={}
    if request.method == 'POST':
        try:
            bookmark = Bookmark.objects.get(id=request.POST['content_id'])
            from_name = request.POST['from_name'].strip()
            to_name = request.POST['to_name'].strip()
            to_email = request.POST['to_email'].strip()
            msg = request.POST['msg']
        except:
            scaptcha['success'] = 0
            data  = simplejson.dumps(scaptcha)
            return HttpResponse(data)
       
        subject = global_settings.domain+' - '+from_name+' send you the "'+bookmark.title+'" bookmark details'
        tell_a_friend_data = {}
        tell_a_friend_data['from_name'] = from_name
        tell_a_friend_data['to_name'] = to_name
        tell_a_friend_data['to_email'] = to_email
        tell_a_friend_data['subject'] = subject
        tell_a_friend_data['msg'] = msg
        tell_a_friend_data['bookmark'] = bookmark
        email_message = render_to_string("default/bookmarks/mail_tell_a_friend.html",tell_a_friend_data,context_instance=RequestContext(request))
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,[to_email])
        email.content_subtype = "html"
        email.send()
        scaptcha['success'] = 1
        data  = simplejson.dumps(scaptcha)
        return HttpResponse(data)
        
    else:
        data = {}
        data['bookmark'] = Bookmark.objects.get(id=request.GET['b_id'])
        return render_to_response('default/bookmarks/tell_friend_form.html',data,context_instance=RequestContext(request))
        #scaptcha['success'] = 0
        #data  = simplejson.dumps(scaptcha)
        #return HttpResponse(data)
        
def search_bookmark(request):
    seo = ModuleNames.get_module_seo(name='gallery')
    try:
        kw = request.REQUEST['keyword'].strip()
        cat = request.REQUEST['category'].strip()
        key = {}
        key['status']='P'
        try:
            key['category']=BookmarkCategory.objects.get(slug = cat)
        except:pass
        key_add = False
        key_or = ( Q(title__icontains=kw)  | Q(summary__icontains=kw) )
        if key_add:
            bookmark_list = Bookmark.objects.filter(key_or,key_add,**key).order_by('-created_on').distinct()
        else:
            bookmark_list = Bookmark.objects.filter(key_or,**key).order_by('-created_on').distinct()
        data={}
        try:page = int(request.GET['page'])
        except:page = 1
        data = ds_pagination(bookmark_list,page,'bookmarks',NUMBER_DISPLAYED)
        data['s_key'] = kw
        data['s_cat'] = cat
        return render_to_response('default/bookmarks/bookmark_search_listing.html',data,context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect(reverse('bookmark_list'))
        #print "err"
        #import sys
        #print sys.exc_info()
        #return HttpResponseRedirect(reverse('bookmark_list'))
