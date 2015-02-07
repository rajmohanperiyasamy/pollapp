from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Q
from django.utils import simplejson

from common.models import ModuleNames
from common.utils import ds_pagination
from django.conf import settings as my_settings

from gallery.models import PhotoCategory,PhotoAlbum,Photos,Tag as GalleryTag
from gallery.utils import set_album_session
from usermgmt.favoriteviews import add_remove_fav,get_fav

NUMBER_DISPLAYED = 12

def gallery_home(request,catslug='all',template='default/gallery/home.html'):
    ''' gallery home page'''
    try:category = PhotoCategory.objects.get(slug = catslug)
    except:category = False
    page = int(request.GET.get('page',1))
    if category:
        photoalbums = PhotoAlbum.objects.filter(status='P',category = category).prefetch_related('album_photos').select_related('category').order_by('-published_on')
        seo = category
        url = reverse('gallery_listing',args=[category.slug])
    else:
        photoalbums = PhotoAlbum.objects.filter(status='P').prefetch_related('album_photos').select_related('category','created_by').order_by('-published_on')
        seo = ModuleNames.get_module_seo(name='gallery')
        url = reverse('gallery_home')
    photoalbums = photoalbums.only('title','slug','most_viewed','published_on','category','created_by')    
    data = ds_pagination(photoalbums,page,'photoalbums',NUMBER_DISPLAYED)    
    data['seo'] = seo
    data['url'] = url
    data['photocategories'] = PhotoCategory.objects.only('name','slug').order_by('name')
    data['view_type'] = request.GET.get('view','grid')
    data["selected_category"]=category
    return render_to_response(template,data,context_instance=RequestContext(request))  

def ajax_gallery_lsiting(request,template='default/gallery/ajax_home_photos.html'):
    data={}
    page = 1
    try: cat=PhotoCategory.objects.get(id=request.GET['cid'])
    except:cat='all'
    if cat!='all':allphotos= PhotoAlbum.objects.filter(status='P',category=cat).prefetch_related('album_photos').select_related('category').order_by('-published_on')
    else:allphotos= PhotoAlbum.objects.filter(status='P').prefetch_related('album_photos').select_related('category').order_by('-published_on')
    
    data = ds_pagination(allphotos,page,'allphotos',NUMBER_DISPLAYED)
    
    if cat!='all':data['url'] = reverse('gallery_listing',args=[cat.slug])
    else:data['url'] = reverse('gallery_listing',args=['all'])
    return render_to_response(template,data,context_instance=RequestContext(request))  

def gallery_detail(request,slug,template='default/gallery/gallerydetails.html'):
    album = None
    try: album = PhotoAlbum.objects.prefetch_related('album_photos').select_related('category').get(status='P', slug=slug)
    except: pass
    try: album = PhotoAlbum.objects.prefetch_related('album_photos').select_related('category').get(category__is_editable=False, slug=slug)
    except: pass
    
    if album:
        data = {'album': album}
        return render_to_response(template, data, context_instance=RequestContext(request))

    return HttpResponseRedirect(reverse('gallery_home'))

def like_gallery(request):
    album = PhotoAlbum.objects.get(id=request.REQUEST['gid'])
    if set_album_session(request,album,'like'):
        return HttpResponse('You liked this')
    else:
        return HttpResponse('You already liked this album')

def ajax_related_album(request):
    try:
        cid=request.GET['catid']
        aid=request.GET['aid']
        #relatedalbum = PhotoAlbum.objects.filter(category__id=cid).exclude(id=aid).order_by('?')[:5]
        relatedalbum_photos= Photos.objects.filter(album__status='P',album__category__id=cid).select_related('album').exclude(album__id=aid).order_by('album__id').distinct('album__id')
        data = {'relatedalbum_photos': relatedalbum_photos,}
    except:data={}
    return render_to_response('default/gallery/ajax_relatedalbum.html',data, context_instance=RequestContext(request))


def ajax_tell_a_friend(request):
    scaptcha = {}
    from common.utils import get_global_settings
    global_settings = get_global_settings()
    if request.method == 'POST':
        album = PhotoAlbum.objects.get(id=request.POST['content_id'])
        from_name = request.POST['from_name']
        to_name = request.POST['to_name']
        to_email = request.POST['to_email']
        msg = request.POST['msg']
        subject = global_settings.domain+' - '+from_name+' send you the "'+album.title+'" Photo gallery details'
        
        tell_a_friend_data = {}
        tell_a_friend_data['from_name'] = from_name
        tell_a_friend_data['to_name'] = to_name
        tell_a_friend_data['to_email'] = to_email
        tell_a_friend_data['subject'] = subject
        tell_a_friend_data['msg'] = msg
        tell_a_friend_data['album'] = album
        email_message = render_to_string("default/gallery/mail_tell_a_friend.html",tell_a_friend_data,context_instance=RequestContext(request))
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


def gallery_count(request,id):
    try:
        album = PhotoAlbum.objects.get(id=id)
        album.most_viewed = album.most_viewed + 1
        album.save()
        return HttpResponse('1')
    except:return HttpResponse('0')

def gallery_add_to_fav(request):
    try:
        gal = PhotoAlbum.objects.get(id=request.GET['id'],status='P')
        flag=add_remove_fav(gal,request.user)
        return HttpResponse(flag)
    except:return HttpResponse('0')

def search_gallery(request):
    categories=PhotoCategory.objects.all().order_by('name')
    seo = ModuleNames.get_module_seo(name='gallery')
    try:
        kw = request.GET.get('keyword').strip()
        cat = str(request.GET.get('category'))
        catid = 'all'
        key = {}
        key['status']='P'
        if kw:keyword = kw
        else:keyword = ' '
            
        key_or = (Q(title__icontains=kw)|Q(summary__icontains=kw))
        
        if cat == 'All Categories':
            gallery_list = PhotoAlbum.objects.filter(key_or,**key).order_by('-is_featured').distinct()
        else:
            category = PhotoCategory.objects.get(name = cat)
            gallery_list = PhotoAlbum.objects.filter(key_or,category=category,**key).order_by('-is_featured').distinct()
        
        data={}
        try:page = int(request.GET['page'])
        except:page = 1
        data = ds_pagination(gallery_list,page,'photoalbums',NUMBER_DISPLAYED)
        data['keyword'] = keyword
        data['category'] = cat.replace(' ', '+')
        data['search'] = True
        data['view_type'] = 'grid'
        data['photocategories'] = PhotoCategory.objects.all()
        return render_to_response('default/gallery/home.html',data,context_instance=RequestContext(request))
    except:
        return HttpResponseRedirect(reverse('gallery_home'))
