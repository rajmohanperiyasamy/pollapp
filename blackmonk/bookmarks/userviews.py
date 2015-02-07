from xml.dom import minidom
from time import strptime
import random, re, os, datetime, time, urllib, urllib2
from PIL import Image
import os
import random
import urllib
import logging
import time

from django.http import HttpResponse, HttpResponseRedirect  
from django.template import Context, loader  
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_list_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django import forms
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.utils import simplejson
from django.db.models import Count
from django.conf import settings
from django.contrib import messages

from bookmarks.models import Bookmark, BookmarkCategory
from bookmarks.forms import UserBookmarkForm, UserBookmarkSeoForm
from bs4 import BeautifulSoup

from common.getunique import getUniqueValue
from common.utils import ds_pagination, get_lat_lng, ds_cleantext
from common.forms import UploadEditorImageForm
from common.models import ApprovalSettings
from common.templatetags.ds_utils import get_msg_class_name, get_status_class
from common.user_messages import BOOKMARK_MSG
from common.staff_utils import error_response
from common import signals

NO_OF_ITEMS_PER_PAGE = 10

@login_required
def dash_board(request, template='bookmarks/user/content_manager.html'):
    categorys = BookmarkCategory.objects.all().order_by('name')   
    bookmarks = Bookmark.objects.filter(created_by=request.user).select_related('category', 'created_by').order_by('-created_on')
    bookmark_state = Bookmark.objects.values('status').filter(created_by=request.user).annotate(s_count=Count('status'))
    
    total = 0
    STATE = {'D':0, 'P':0, 'N':0, 'R':0, 'B':0}
    for st in bookmark_state:
        STATE[st['status']] += st['s_count']
        total += st['s_count']
    
    data = ds_pagination(bookmarks, '1', 'bookmarks', NO_OF_ITEMS_PER_PAGE)
    data['bookmark_list'] = bookmarks
    data['status'] = 'all'
    data['listing_type'] = 'all'
    data['created'] = 'all'
    data['sort'] = '-created_on'
    try:data['msg'] = BOOKMARK_MSG[request.GET['msg']]
    except:data['msg'] = None
    try:data['mtype'] = get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] = None
    data['category'] = categorys
    data['total'] = total
    data['published'] = STATE['P']
    data['drafted'] = STATE['D']
    data['pending'] = STATE['N']
    data['rejected'] = STATE['R']
    data['blocked'] = STATE['B']
    data['search'] = False
    
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def ajax_dash_board(request, template='bookmarks/user/ajax_object_listing.html'):
    data = filter_bookmark(request)
    send_data = {}
    send_data['html'] = render_to_string(template, data, context_instance=RequestContext(request))
    if data['search']:send_data['search'] = True
    if data['has_next']:send_data['next'] = True
    if data['has_previous']:send_data['previous'] = True
    if data['count']:send_data['count'] = data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange'] = str(data['from_range']) + ' - ' + str(data['to_range'])
    return HttpResponse(simplejson.dumps(send_data))

@login_required
def ajax_bookmark_action(request, template='bookmarks/user/ajax_object_listing.html'):
    try:id = request.GET['ids'].split(',')
    except:id = request.GET['ids']
    action = request.GET['action']
    action_bookmark = Bookmark.objects.filter(id__in=id)
    cls_count = action_bookmark.count()
     
    if action == 'DEL':
        for atr_del in action_bookmark:
            signals.create_notification.send(sender=None,user=request.user, obj=atr_del, not_type='deleted from',obj_title=atr_del.title)
        action_bookmark.delete()
        msg = str(BOOKMARK_MSG['SBD'])
        mtype = get_msg_class_name('s')
    else:pass
 
    data = filter_bookmark(request)
 
    send_data = {}
    send_data['html'] = render_to_string(template, data, context_instance=RequestContext(request))
    send_data['pagination'] = render_to_string('common/pagination_ajax_delete.html', data, context_instance=RequestContext(request))
    if data['search']:send_data['search'] = True
    if data['has_next']:send_data['next'] = True
    if data['has_previous']:send_data['previous'] = True
    if data['count']:send_data['count'] = data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange'] = str(data['from_range']) + ' - ' + str(data['to_range'])
    send_data['total'] = Bookmark.objects.filter(created_by=request.user).count()
    send_data['msg'] = msg
    send_data['mtype'] = mtype     
    return HttpResponse(simplejson.dumps(send_data))

def filter_bookmark(request):
    data = key = {}
    q = ()
    status = request.GET.get('status', 'all')
    listing_type = request.GET.get('listing', 'all')
    sort = request.GET.get('sort', '-created_on')
    action = request.GET.get('action', False)
    ids = request.GET.get('ids', False)
    search = request.GET.get('search', False)
    item_perpage = int(request.GET.get('item_perpage', NO_OF_ITEMS_PER_PAGE))
    page = int(request.GET.get('page', 1))  
    
    if status != 'all' and status != '':
        key['status'] = status
   
    key['created_by'] = request.user
    
    if search:
        search_type = request.GET.get('type', None)
        search_keyword = request.GET.get('kwd', "").strip()
        search_category = request.GET.get('cat', None)
        
        if search_category:
            categorys = BookmarkCategory.objects.get(id=search_category)
            key['category'] = categorys
        if search_type:
            if search_type == 'title':key['title__icontains'] = search_keyword
            elif search_type == 'desc':key['summary__icontains'] = search_keyword
            else:key['created_by__display_name__icontains'] = search_keyword
        
        if search_keyword:
            q = (Q(title__icontains=search_keyword) | Q(category__name__icontains=search_keyword) | Q(summary__icontains=search_keyword) | Q(created_by__display_name__icontains=search_keyword))
            bookmarks = Bookmark.objects.filter(q, **key).select_related('category', 'created_by').order_by(sort)
        else:
            bookmarks = Bookmark.objects.filter(**key).select_related('category', 'created_by').order_by(sort)
    else:
        bookmarks = Bookmark.objects.filter(**key).select_related('category', 'created_by').order_by(sort)
    
    data = ds_pagination(bookmarks, page, 'bookmark_list', item_perpage)
    data['status'] = status
    if search:
        data['search_keyword'] = request.GET.get('kwd',"").strip()
    data['listing_type'] = listing_type
    data['sort'] = sort
    data['search'] = search
    data['item_perpage'] = item_perpage
    return data 


@login_required
def ajax_bookmark_state(request):
    total = 0
    STATE = {'D':0, 'P':0, 'N':0, 'R':0, 'B':0}
 
    bookmark_state = Bookmark.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))
    for st in bookmark_state:
       STATE[st['status']] += st['s_count']
       total += st['s_count']
    data = {
          'total'       :total,
          'published'   :STATE['P'],
          'pending'     :STATE['N'],
          'drafted'     :STATE['D'],
          'rejected'    :STATE['R'],
          'blocked'     :STATE['B']
    }
#     return HttpResponse(simplejson.dumps(data))

#def get_img_url(site,url):
    #if "http://" in url:    return url
    #elif "https://" in url: return url
    #else:
        #try:    s_url = 'http://'+(site.split('http://')[1]).split('/')[0]
        #except: s_url = 'https://'+(site.split('https://')[1]).split('/')[0]        
        #return '%s/%s'%(s_url,url)

def get_img_url(site,url):    
    prefixes = [ "http://", "https://" ]
    if True in [ prefix in url for prefix in prefixes ]: return url
    else: return '%s/%s'%([ prefix+(site.split(prefix)[1]).split('/')[0] for prefix in prefixes if prefix in site ][0], url ) 


@login_required
def bookmark_preview(request, template='bookmarks/user/preview.html'):
    data = {}
    bookmark = Bookmark.objects.get(id=int(request.GET['id']))
    data['bookmark'] = bookmark
    return render_to_response(template, data, context_instance=RequestContext(request))

def filter_number(val):
    data = ''
    for x in val:
        try:
            if int(x) >= 0 and int(x) <= 9:
                data = data + x
        except:pass
    return data

def bookmark_fetch_images(request):
    try:
        source_url = request.POST['source_url']
        source_url = source_url.replace(' ', '+')
        if source_url[-1]=='/':
           source_url = source_url[:-1]
        try:
            Bookmark.objects.get(source_url=source_url,created_by=request.user)
            data= { 'err_msg' : "Bookmark already exist for this URL, Try again with different URL" }
            return render_to_response('bookmarks/user/ajax_fetch_images.html', data,context_instance=RequestContext(request))
        except:
            pass
        source_html = urllib2.urlopen(source_url)
        soup = BeautifulSoup(source_html)
        b_title = b_seo_description = ""
        for title in soup.title:
            b_title = title.string[:200]
            b_seo_description = title
        for meta in soup.find_all('meta'):
            try:
                if 'title' in meta.get('property',''):
                    b_title = meta['content'][:200]
            except: b_title = b_title
            try:
                if meta['name'] == 'description':
                    b_seo_description = meta['content'][:350]
            except: b_seo_description = b_seo_description
        img_urls = []
        img_urls_rem = []
        try:
            for img in soup.find_all("img"):
                Image_url = get_img_url(source_url, img['src'])
                if (True in [img_ext in Image_url for img_ext in ['.jpg', '.jpeg', '.png']]) and ('captcha' not in Image_url):
                    img_urls.append(Image_url)
            for img in soup.find_all(lambda tag: tag.name == "img" and tag.has_key("width") and int(filter_number(tag["width"])) < 80):
                img_urls_rem.append(get_img_url(source_url, img['src']))
        except:pass
        data = {}
        title = b_title = ds_cleantext(b_title)
        summary = b_seo_description[:200]
        data['slug'] = slugify(b_title)
        
        data['img_url_list'] = list(set(img_urls) - set(img_urls_rem))
        form = UserBookmarkForm()
        data['source_url'] = source_url
        data['seo_title'] = title
        data['seo_description'] = b_seo_description
         
        
        form.fields['title'].initial = title
        form.fields['summary'].initial = summary
        data['form'] = form
        
        return render_to_response('bookmarks/user/bookmark_form_details.html', data,context_instance=RequestContext(request))
    except urllib2.HTTPError, e:
        data= { 'reason': e.reason, 'err_msg' : "cannot fetch the requested URL. Try again with different URL" }
        return render_to_response('bookmarks/user/bookmark_form_details.html', data,context_instance=RequestContext(request))

@login_required
def add_bookmark(request, template='bookmarks/user/bookmark_form.html'):
    data = {}
    if request.method == "POST":
        form = UserBookmarkForm(request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.created_by = request.user
            bookmark.modified_by = request.user
            #try:    slug = request.POST['slug'].strip()
            #except: slug = bookmark.title
            #bookmark.slug = getUniqueValue(Bookmark, slugify(slug), instance_pk=bookmark.id)
            bookmark.slug = getUniqueValue(Bookmark, slugify(bookmark.title), instance_pk=bookmark.id) 
            # ~ ~ ~
            try:
                bookmark.image_url = request.POST['image_url']
            except:
                bookmark.image_url = None
            bookmark.source_url = request.POST['source_url'].replace(' ', '+')
            bookmark.seo_title = request.POST['seo_title']
            bookmark.seo_description = request.POST['seo_description']
            bookmark.summary = request.POST['summary']
            approval_settings = ApprovalSettings.objects.get(name='bookmark')
            if approval_settings.free:
                bookmark.status = 'P'
            else:
                bookmark.status = 'N'
            bookmark.save()
            messages.success(request, str(BOOKMARK_MSG['BAS']))
            signals.create_notification.send(sender=None,user=request.user, obj=bookmark, not_type='added in',obj_title=bookmark.title)
            signals.create_staffmail.send(sender=None,object=bookmark,module='bookmarks',action='A',user=request.user)
        return  HttpResponseRedirect('/user/bookmarks/')
    else:
        return render_to_response(template, data, context_instance=RequestContext(request))
      

def bookmark_edit_fetch_images(request):
    import sys
    try:
        source_url = Bookmark.objects.get(id=request.POST['id']).source_url
        present_imageurl = Bookmark.objects.get(id=request.POST['id']).image_url
        source_html = urllib2.urlopen(source_url)
        soup = BeautifulSoup(source_html)
        img_urls = []
        img_urls_rem = []
        try:
            for img in soup.find_all("img"):
                Image_url = get_img_url(source_url,img['src'])
                if (True in [img_ext in Image_url for img_ext in ['.jpg','.jpeg','.png']]) and ('captcha' not in Image_url):
                    img_urls.append(Image_url)
            for img in soup.find_all(lambda tag: tag.name=="img" and tag.has_key("width") and int(filter_number(tag["width"])) < 80):
                img_urls_rem.append(get_img_url(source_url,img['src']))
        except:
            pass
        data = {}
        data['img_url_list'] = list(set(img_urls) - set(img_urls_rem))
         
        return render_to_response('bookmarks/user/ajax_edit_fetch_images.html', data)
    except:
        pass

@login_required
def edit_bookmark(request, id, template='bookmarks/user/bookmark_form.html'):
    data = {}
    bookmark = Bookmark.objects.get(id=id)
    if request.method == "POST":
        bookmark.title = request.POST['title']
        bookmark.slug = getUniqueValue(Bookmark, slugify(bookmark.title), instance_pk=bookmark.id)
        bookmark.category = BookmarkCategory.objects.get(id=request.POST['category'])
        try:    bookmark.image_url = request.POST['image_url']
        except: bookmark.image_url = None
        
        approval_settings = ApprovalSettings.objects.get(name='bookmark')
        if approval_settings.free_update:
            bookmark.status = 'P'
        else:
            bookmark.status = 'N'
        bookmark.save()
        messages.success(request, str(BOOKMARK_MSG['BUS']))
        signals.create_notification.send(sender=None,user=request.user, obj=bookmark, not_type='updated in',obj_title=bookmark.title)
        signals.create_staffmail.send(sender=None,object=bookmark,module='bookmarks',action='U',user=request.user)
        return  HttpResponseRedirect('/user/bookmarks/')
    else:
        data['bookmark'] = bookmark
        data['form'] = UserBookmarkForm(instance=bookmark)
        data['category_list'] = BookmarkCategory.objects.all()
        try:
            source_url = bookmark.source_url
            #present_imageurl = bookmark.image_url
            source_html = urllib2.urlopen(source_url)
            soup = BeautifulSoup(source_html)
            img_urls = []
            img_urls_rem = []
            try:
                for img in soup.find_all("img"):
                    Image_url = get_img_url(source_url,img['src'])
                    if (True in [img_ext in Image_url for img_ext in ['.jpg','.jpeg','.png']]) and ('captcha' not in Image_url):
                        img_urls.append(Image_url)
                for img in soup.find_all(lambda tag: tag.name=="img" and tag.has_key("width") and int(filter_number(tag["width"])) < 80):
                    img_urls_rem.append(get_img_url(source_url,img['src']))
            except:
                pass
            data['img_url_list'] = list(set(img_urls) - set(img_urls_rem))
        except:
            pass
        return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def seo(request, id, template='usercp_seo_form.html'):
    bookmark = Bookmark.objects.get(id=id)
    form = UserBookmarkSeoForm(instance=bookmark)
    if request.POST:
        form = UserBookmarkSeoForm(request.POST, instance=bookmark)
        if form.is_valid():
            #seo = form.save(commit=False)
            #seo.slug = slugify(seo.slug)
            #seo.save()
            form.save()
            return HttpResponse(simplejson.dumps({'status':1, 'mtype':get_msg_class_name('s'), 'msg':str(BOOKMARK_MSG['BSUS'])}))
        else:
            data = {'form':form, 'bookmark':bookmark}
            return error_response(request, data, template, BOOKMARK_MSG)
    data = {'form':form, 'bookmark':bookmark}
    return render_to_response(template, data, context_instance=RequestContext(request))

@login_required
def change_status(request):
    try:
        bookmark = Bookmark.objects.get(id=int(request.GET['id']))
        status = request.GET['status']
        bookmark.status = status
        bookmark.save()
        html = '<span title="' + get_status_class(bookmark.status) + '" name="' + bookmark.status + '" id="id_estatus_' + str(bookmark.id) + '" class="inline-block status-idty icon-' + get_status_class(bookmark.status) + '"></span> '          
        return HttpResponse(html)
    except:return HttpResponse('0')



