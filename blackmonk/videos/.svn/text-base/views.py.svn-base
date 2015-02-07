#Python Libs 

#Django Libs 
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings as my_settings

#Application Libs and Common Methods
from common.utils import ds_pagination, get_global_settings
from common.models import ModuleNames
from usermgmt.models import Favorite
from usermgmt.favoriteviews import add_remove_fav,get_fav

#Module Files(models,forms etc...)
from videos.models import VideoCategory, Videos
from videos.utils import set_video_session

ITEMS_PER_PAGE = 12

def home(request,catslug='all'):
    '''it will display all videos and videos under a particuler category'''
    try:category = VideoCategory.objects.get(slug = catslug)
    except:category = False
    page = int(request.GET.get('page',1))
    
    if not category:
        url = reverse('videos_videos_by_category')
        videos = Videos.objects.filter(status='P').select_related('category').order_by('-published_on')
        seo=ModuleNames.get_module_seo(name='videos')
    else:
        url = reverse('videos_videos_by_category',args=[catslug])
        videos = Videos.objects.filter(category = category, status='P').select_related('category').order_by('-published_on') 
        seo=category
    data = ds_pagination(videos,page,'videos',ITEMS_PER_PAGE)   
    data['url'] = url
    data['maincategory']= category
    data['seo'] = seo
    data['view_type'] = request.GET.get('view','grid')
    return render_to_response('default/videos/videos.html',data, context_instance=RequestContext(request))

def video_details(request,slug):
    '''details of particular video'''
    data={}
    try:video = Videos.objects.prefetch_related('keywords').select_related('category','created_by').get(slug=slug)
    except:return HttpResponseRedirect(reverse('videos_videos_by_category'))
    
    '''method for counting views of particular video'''
    set_video_session(request,video)
    
    data['video'] = video
    return render_to_response('default/videos/videos-details.html',data, context_instance=RequestContext(request))

def set_favourite(request):
    ''' adding a particuler video to the users favorite account '''
    try:
        video=Videos.objects.get(id=request.GET['vid'])
        url=video.get_absolute_url()
        if Favorite.create_favorite(request.user,video):
            url=url+'?&message=fav'
        else:
            url=url+'?&message=fav0'
        return HttpResponseRedirect(url)
    except:
        url=reverse('videos_videos_by_category')
        return HttpResponseRedirect(url)
    
def ajax_tell_a_friend(request):
    scaptcha={}
    global_settings = get_global_settings()
    '''user can send video info to their friends through email'''     
    if request.method == 'POST':
        video = Videos.objects.get(id=request.POST['content_id'])
        from_name = request.POST['from_name']
        to_name = request.POST['to_name']
        to_email = request.POST['to_email']
        #subject = request.POST['subject']
        msg = request.POST['msg']
        subject = global_settings.domain+' - '+from_name+' send you the "'+video.title+'" video details'
        tell_a_friend_data = {}
        tell_a_friend_data['from_name'] = from_name
        tell_a_friend_data['to_name'] = to_name
        tell_a_friend_data['to_email'] = to_email
        tell_a_friend_data['subject'] = subject
        tell_a_friend_data['msg'] = msg
        tell_a_friend_data['video'] = video
        email_message = render_to_string("default/videos/mail_tell_a_friend.html",tell_a_friend_data,context_instance=RequestContext(request))
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

def video_ajax_mostviewed(request):
    '''display most viewed videos in video detail page ajax operation '''
    data ={}
    videos=Videos.objects.filter(video_view__gte='3',status='P').order_by('-video_view')[:10]
    data={'videos':videos}
    return render_to_response('default/videos/ajax_videos_mostviewed.html',data, context_instance=RequestContext(request))

def videos_add_to_fav(request):
    try:
        videos = Videos.objects.get(id=request.GET['id'],status='P')
        flag=add_remove_fav(videos,request.user)
        return HttpResponse(flag)
    except:return HttpResponse('0')

def search_videos(request):
    categories=VideoCategory.objects.all().order_by('name')
    seo = ModuleNames.get_module_seo(name='videos')
    try:
        kw = request.GET.get('keyword').strip()
        cat = request.GET.get('category')
        key = {}
        key['status']='P'
        
        key_or = ( Q(title__icontains=kw)  | Q(description__icontains=kw) )
        data={}
        if cat == 'All Categories':
            video_list = Videos.objects.filter(key_or,**key).order_by('-featured').distinct()
        else:
            category = VideoCategory.objects.get(name = cat)
            video_list = Videos.objects.filter(key_or,category = category,**key).order_by('-featured').distinct()
        
        try:page = int(request.GET['page'])
        except:page = 1
        data = ds_pagination(video_list,page,'videos',ITEMS_PER_PAGE)
        data['keyword'] = kw
        data['category'] = cat.replace(' ','+')
        data['view_type'] = 'grid'
        data['search'] = True
        return render_to_response('default/videos/videos.html',data,context_instance=RequestContext(request))
    except:
        return HttpResponse('0')





#################REMOVE AFTER DEMO##################################
def brightcove_videos(request):
    from videos.brightcove.api import Brightcove
    data = {}
    RT="5CHbiw2SKxhU1riCQkOWhldYKubqDdxGaOs_P9Jo1M4pH-uzo0yuZw.."
    try:
        b = Brightcove(RT)
        videos = b.find_all_videos()
        data['videos'] = videos.items
    except:pass    
    data['view_type'] = request.GET.get('view','grid')
    return render_to_response('default/videos/videos-brightcove.html',data, context_instance=RequestContext(request))

def brightcove_video_details(request,bslug):
    from videos.brightcove.api import Brightcove
    data = {}
    RT="5CHbiw2SKxhU1riCQkOWhldYKubqDdxGaOs_P9Jo1M4pH-uzo0yuZw.."
    try:
        b = Brightcove(RT)
        video = b.find_video_by_id(bslug)
        data['video'] = video
    except:pass
    data['view_type'] = request.GET.get('view','grid')
    return render_to_response('default/videos/brightcove-video-details.html',data, context_instance=RequestContext(request))
