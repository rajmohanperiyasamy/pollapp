from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from common.getunique import getUniqueValue
from django.db.models import Count
from common.staff_messages import BOOKMARK_MSG, COMMON
from common.utils import ds_pagination, get_global_settings, get_lat_lng, ds_cleantext
from django.utils import simplejson
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from bs4 import BeautifulSoup
from django.template.defaultfilters import slugify
from common.templatetags.ds_utils import get_msg_class_name, get_status_class
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.contrib import messages

import random, re, os, datetime, time, urllib, urllib2
from common.staff_utils import error_response
from bookmarks.models import Bookmark, BookmarkCategory
from bookmarks.forms import BookmarkForm, BookmarkSeoForm

NO_OF_ITEMS_PER_PAGE = 10
NO_OF_ITEMS_FEATURED = 8

@staff_member_required
def bookmarks_home(request, template='bookmarks/staff/bookmarks_home.html'):
    categorys = BookmarkCategory.objects.all().order_by('name')
    bookmarks = Bookmark.objects.select_related('category', 'created_by').exclude(status='D').order_by('-created_on')
    total = 0
    STATE = {'P':0, 'N':0, 'R':0, 'B':0}
    for bookmark in bookmarks:
        STATE[bookmark.status] += 1
        total += 1

    data = ds_pagination(bookmarks, '1', 'bookmarks', NO_OF_ITEMS_PER_PAGE)
    try:
        bookmark = Bookmark.objects.filter(status='P', featured=True)
        sum = bookmark.count()
        if sum >= NO_OF_ITEMS_FEATURED:
            data['feature_limit'] = True
    except:data['feature_limit'] = False
    data['bookmark_list'] = Bookmark.objects.all().exclude(status='D').order_by('-created_on')
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
    data['pending'] = STATE['N']
    data['rejected'] = STATE['R']
    data['blocked'] = STATE['B']
    data['search'] = False
    try:data['recent'] = request.GET['pending_bookmark']
    except:data['recent'] = False
    return render_to_response(template, data, context_instance=RequestContext(request))

#def get_img_url(site,url):
#    if "http://" in url:    return url
#    elif "https://" in url: return url
#    else:
#        try:    s_url = 'http://'+(site.split('http://')[1]).split('/')[0]
#        except: s_url = 'https://'+(site.split('https://')[1]).split('/')[0]
#        return '%s/%s'%(s_url,url)

def get_img_url(site, url):
    prefixes = [ "http://", "https://" ]
    if True in [ prefix in url for prefix in prefixes ]: return url
    else: return '%s/%s' % ([ prefix + (site.split(prefix)[1]).split('/')[0] for prefix in prefixes if prefix in site ][0], url)


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
        if source_url[-1] == '/':
           source_url = source_url[:-1]
        try:
            Bookmark.objects.get(source_url=source_url, created_by=request.user)
            data = { 'err_msg' : "Bookmark already exist for this URL, Try again with different URL" }
            return render_to_response('bookmarks/staff/ajax_fetch_images.html', data, context_instance=RequestContext(request))
        except:
            pass
        source_url = source_url.replace(' ', '+')
        source_html = urllib2.urlopen(source_url)
        soup = BeautifulSoup(source_html)
        for title in soup.title:
            b_title = title.string[:200]
            b_seo_description = title
        for meta in soup.find_all('meta'):
            try:
                if 'title' in meta.get('property', ''):
                    b_title = meta['content'][:200]
            except:b_title = b_title
            try:
                if meta.get('name', '') == 'description' or 'description' in meta.get('property', ''):
                    b_seo_description = (meta['content'].strip())[:350]
            except:b_seo_description = b_seo_description
        img_urls = []
        img_urls_rem = []
        try:
            for img in soup.find_all("img"):
                Image_url = get_img_url(source_url, img['src'])
                if (True in [img_ext in Image_url for img_ext in ['.jpg', '.jpeg', '.png']]) and ('captcha' not in Image_url):
                    img_urls.append(Image_url)
            for img in soup.find_all(lambda tag: tag.name == "img" and tag.has_key("width") and int(filter_number(tag["width"])) < 80):
                img_urls_rem.append(get_img_url(source_url, img['src']))
        except:
            pass
        data = {}

        title = b_title = ds_cleantext(b_title)
        summary = b_seo_description[:200]
        data['slug'] = slugify(b_title)
        data['img_url_list'] = list(set(img_urls) - set(img_urls_rem))
        form = BookmarkForm()
        data['source_url'] = source_url
        data['seo_title'] = title
        data['seo_description'] = b_seo_description


        form.fields['summary'].initial = summary
        form.fields['title'].initial = title
        data['form'] = form

        return render_to_response('bookmarks/staff/ajax_fetch_images.html', data, context_instance=RequestContext(request))
    except:
        data = { 'err_msg' : "Sorry cannot fetch the requested URL. Try again with different URL" }
        return render_to_response('bookmarks/staff/ajax_fetch_images.html', data, context_instance=RequestContext(request))

@staff_member_required
def bookmarks_add(request):
    data = {}
    if request.method == "POST":
        form = BookmarkForm(request.POST)
        if form.is_valid():
            bookmark = form.save(commit=False)
            bookmark.created_by = request.user
            bookmark.modified_by = request.user
            try:    slug = request.POST['slug'].strip()
            except: slug = bookmark.title
            bookmark.slug = getUniqueValue(Bookmark, slugify(slug), instance_pk=bookmark.id)
            # ~ ~ ~
            try:
                bookmark.image_url = request.POST['image_url']
            except:
                bookmark.image_url = None
            bookmark.source_url = request.POST['source_url'].strip().replace(' ', '+')
            bookmark.seo_title = request.POST['seo_title'].strip()
            bookmark.seo_description = request.POST['seo_description'].strip()
            bookmark.summary = request.POST['summary'].strip()
            bookmark.status = 'P'
            bookmark.published_on = datetime.datetime.now()
            bookmark.save()
            messages.success(request, str(BOOKMARK_MSG['YBS']))
        return  HttpResponseRedirect('/staff/bookmarks/')
    else:
        if not request.user.has_perm('bookmarks.add_bookmark'):raise PermissionDenied
        return render_to_response('bookmarks/staff/bookmarks_add.html', context_instance=RequestContext(request))

@staff_member_required
def bookmark_preview(request, template='bookmarks/staff/preview.html'):
    data = {}
    bookmark = Bookmark.objects.get(id=int(request.GET['id']))
    data['bookmark'] = bookmark
    return render_to_response(template, data, context_instance=RequestContext(request))


def bookmark_edit_fetch_images(request):
    try:
        source_url = Bookmark.objects.get(id=request.POST['id']).source_url
        present_imageurl = Bookmark.objects.get(id=request.POST['id']).image_url
        source_html = urllib2.urlopen(source_url)
        soup = BeautifulSoup(source_html)
        img_urls = []
        img_urls_rem = []
        try:
            for img in soup.find_all("img"):
                Image_url = get_img_url(source_url, img['src'])
                if (True in [img_ext in Image_url for img_ext in ['.jpg', '.jpeg', '.png']]) and ('captcha' not in Image_url):
                    img_urls.append(Image_url)
            for img in soup.find_all(lambda tag: tag.name == "img" and tag.has_key("width") and int(filter_number(tag["width"])) < 80):
                img_urls_rem.append(get_img_url(source_url, img['src']))
        except:
            pass
        data = {}
        data['img_url_list'] = list(set(img_urls) - set(img_urls_rem))
        return render_to_response('bookmarks/staff/ajax_edit_fetch_images.html', data)
    except:
        pass

@staff_member_required
def bookmark_edit(request, id, template='bookmarks/staff/bookmarks_edit.html'):
    data = {}
    bookmark = Bookmark.objects.get(id=id)
    if request.method == "POST":
        bookmark.title = request.POST['title']
        bookmark.slug = request.POST['slug']
        bookmark.summary = request.POST['summary']
        bookmark.category = BookmarkCategory.objects.get(id=request.POST['category'])
        try:    bookmark.image_url = request.POST['image_url']
        except: bookmark.image_url = None
        bookmark.save()
        messages.success(request, str(BOOKMARK_MSG['YBUS']))
        return  HttpResponseRedirect('/staff/bookmarks/')
    else:
        data['bookmark'] = bookmark
        data['category_list'] = BookmarkCategory.objects.all()
        try:
            source_url = bookmark.source_url
            present_imageurl = bookmark.image_url
            source_html = urllib2.urlopen(source_url)
            soup = BeautifulSoup(source_html)
            img_urls = []
            img_urls_rem = []
            try:
                for img in soup.find_all("img"):
                    Image_url = get_img_url(source_url, img['src'])
                    if (True in [img_ext in Image_url for img_ext in ['.jpg', '.jpeg', '.png']]) and ('captcha' not in Image_url):
                        img_urls.append(Image_url)
                for img in soup.find_all(lambda tag: tag.name == "img" and tag.has_key("width") and int(filter_number(tag["width"])) < 80):
                    img_urls_rem.append(get_img_url(source_url, img['src']))
            except:
                pass
            data['img_url_list'] = list(set(img_urls) - set(img_urls_rem))
            data["present_imageurl"] = present_imageurl
        except:
            pass
        return render_to_response(template, data, context_instance=RequestContext(request))


@staff_member_required
def ajax_list_bookmark(request, template='bookmarks/staff/ajax_bookmark_list.html'):
    data = filter_bookmark(request)
    send_data = {}
    send_data['html'] = render_to_string(template, data, context_instance=RequestContext(request))
    if data['search']:          send_data['search'] = True
    if data['has_next']:        send_data['next'] = True
    if data['has_previous']:    send_data['previous'] = True
    if data['count']:           send_data['count'] = data['count']
    else:send_data['count']=0
    if data['from_range'] and data['to_range']:
        send_data['pagerange'] = str(data['from_range']) + ' - ' + str(data['to_range'])
    else:send_data['pagerange']='0 - 0'
    return HttpResponse(simplejson.dumps(send_data))

@staff_member_required
def ajax_bookmark_action(request, template='bookmarks/staff/ajax_delete_listing.html'):
    try:    id = request.GET['ids'].split(',')
    except: id = request.GET['ids']
    try:    all_ids = request.GET['all_ids'].split(',')
    except: all_ids = request.GET['all_ids']
    action = request.GET['action']
    action_bookmark = Bookmark.objects.filter(id__in=id)
    cls_count = action_bookmark.count()
    status = 0

    if action == 'DEL':
        if request.user.has_perm('bookmark.delete_bookmark'):
            action_bookmark.delete()
            status = 1
            msg = str(BOOKMARK_MSG['BDS'])
            mtype = get_msg_class_name('s')
        else:
            msg = str(COMMON['DENIED'])
            mtype = get_msg_class_name('w')
    else:
        if request.user.has_perm('bookmark.publish_bookmark'):
            action_bookmark.update(status=action)
            if action == 'P':
                for bookmark in action_bookmark:
                    bookmark.published_on = datetime.datetime.now()
                    bookmark.save()
            status = 1
            msg = str(BOOKMARK_MSG[action])
            mtype = get_msg_class_name('s')
        else:
            msg = str(COMMON['DENIED'])
            mtype = get_msg_class_name('w')

    data = filter_bookmark(request)

    new_id = []
    for cs in data['bookmark_list']:new_id.append(int(cs.id))
    for ai in id:all_ids.remove(ai)

    for ri in all_ids:
        for ni in new_id:
            if int(ni) == int(ri):
                new_id.remove(int(ri))

    data['new_id'] = new_id
    send_data = {}
    send_data['html'] = render_to_string(template, data, context_instance=RequestContext(request))
    send_data['pagination'] = render_to_string('common/pagination_ajax_delete.html', data, context_instance=RequestContext(request))
    if data['search']:send_data['search'] = True
    if data['has_next']:send_data['next'] = True
    if data['has_previous']:send_data['previous'] = True
    if data['count']:send_data['count'] = data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange'] = str(data['from_range']) + ' - ' + str(data['to_range'])
    send_data['msg'] = msg
    send_data['mtype'] = mtype
    send_data['status'] = status
    return HttpResponse(simplejson.dumps(send_data))

@staff_member_required
def ajax_bookmark_state(request):
    status = request.GET.get('status', 'all')
    total = 0
    STATE = {'P':0, 'N':0, 'R':0, 'B':0}

    if status == 'all':
        bookmark_state = Bookmark.objects.values('status').exclude(status='D').annotate(s_count=Count('status'))
    else:
        bookmark_state = Bookmark.objects.filter(created_by=request.user).values('status').exclude(status='D').annotate(s_count=Count('status'))

    for st in bookmark_state:
       STATE[st['status']] += st['s_count']
       total += st['s_count']
    data = {
          'total':total,
          'published':STATE['P'],
          'pending':STATE['N'],
          'rejected':STATE['R'],
          'blocked':STATE['B']
    }
    return HttpResponse(simplejson.dumps(data))

@staff_member_required
@permission_required('bookmark.change_bookmark', raise_exception=True)
def seo(request, id, template='bookmarks/staff/update_seo.html'):
    ins = Bookmark.objects.get(id=id)
    form = BookmarkSeoForm(instance=ins)
    if request.POST:
        form = BookmarkSeoForm(request.POST, instance=ins)
        if form.is_valid():
            #seo=form.save(commit=False)
            #seo.slug=slugify(seo.slug)
            #seo.save()
            form.save()
            return HttpResponse(simplejson.dumps({'status':1, 'mtype':get_msg_class_name('s'), 'msg':str(BOOKMARK_MSG['BSUS'])}))
        else:
            data = {'form':form, 'bookmark':ins}
            return error_response(request, data, template, BOOKMARK_MSG)
    data = {'form':form, 'bookmark':ins}
    return render_to_response(template, data, context_instance=RequestContext(request))


@staff_member_required
@permission_required('bookmark.publish_bookmark', raise_exception=True)
def bookmark_change_status(request):
    try:
        bookmark = Bookmark.objects.get(id=request.GET['id'])
        status = request.GET['status']
        bookmark.status = status
        if status == 'P': bookmark.published_on = datetime.datetime.now()
        bookmark.save()
        html = '<span title="' + get_status_class(bookmark.status) + '" name="' + bookmark.status + '" id="id_estatus_' + str(bookmark.id) + '" class="inline-block status-idty icon-' + get_status_class(bookmark.status) + '"></span> '
        return HttpResponse(html)
    except:return HttpResponse('0')

def filter_bookmark(request):
    data = key = {}
    q = ()
    args=()
    status = request.GET.get('status', 'all')
    listing_type = request.GET.get('listing', 'all')
    sort = request.GET.get('sort', '-created_on')
    action = request.GET.get('action', False)
    ids = request.GET.get('ids', False)
    search = request.GET.get('search', False)
    item_perpage = int(request.GET.get('item_perpage', NO_OF_ITEMS_PER_PAGE))
    page = int(request.GET.get('page', 1))
    created = request.GET.get('created','all')
    
    if status != 'all' and status != '':
        key['status'] = status
    
    if created!='all':
        if created =='CSM':key['created_by'] = request.user
        elif created =='CSO':args = (~Q(created_by = request.user))

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
            if args:bookmarks = Bookmark.objects.filter(q,args,**key).select_related('category', 'created_by').order_by(sort)
            else:bookmarks = Bookmark.objects.filter(q, **key).select_related('category', 'created_by').order_by(sort)
        else:
            if args:bookmarks = Bookmark.objects.filter(args,**key).select_related('category', 'created_by').order_by(sort)
            else:bookmarks = Bookmark.objects.filter(**key).select_related('category', 'created_by').order_by(sort)
    else:
        if args:bookmarks = Bookmark.objects.filter(args,**key).select_related('category', 'created_by').order_by(sort)
        else:bookmarks = Bookmark.objects.filter(**key).select_related('category', 'created_by').order_by(sort)

    data = ds_pagination(bookmarks, page, 'bookmark_list', item_perpage)
    data['status'] = status
    data['listing_type'] = listing_type
    data['sort'] = sort
    data['search'] = search
    data['item_perpage'] = item_perpage
    return data


