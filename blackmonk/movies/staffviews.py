import datetime
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils import simplejson
from django.utils.html import strip_tags

from common import signals
from common.fileupload import upload_photos, upload_photos_forgallery, \
    delete_photos
from common.getunique import getUniqueValue
from common.models import Address
from common.staff_messages import MOVIE_MSG, COMMON
from common.staff_utils import error_response
from common.templatetags.ds_utils import get_msg_class_name
from common.utils import ds_pagination, get_lat_lng, get_global_settings
from gallery.models import PhotoAlbum, PhotoCategory, Photos
from movies.forms import AddMovieForm, MovieTypeSEOForm, AddTheatreForm, \
    TheatresSEOFORM, AddMovieCriticsReviewForm, AddressForm
from movies.models import Movies, Theatres, MovieType, CriticReview, MovieTime, \
    ShowTime, CriticSource
from mptt_comments.models import MpttComment


User = get_user_model()
#from gallery.utils import *

movie_content_type = ContentType.objects.get(model='movies')

movie_album_cat = PhotoCategory.objects.get_or_create(name="Movies", slug='movies', is_editable=False)[0]

rand = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'

ITEMS_PER_PAGE = 10

@staff_member_required  
def movie_listing(request):
    ''' Movie Home ( listing ) '''
    item_perpage = int(request.GET.get('item_perpage',ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))
    
    moviedisplay = Movies.objects.all().select_related('category','created_by').order_by('-id')
    categories = MovieType.objects.order_by('name')
    movie_state = Movies.objects.values('status').annotate(s_count=Count('status'))
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0,'K':0}
    for st in movie_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    data = ds_pagination(moviedisplay,page,'moviedisplay',item_perpage)
    
    data['categories'] = categories
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    data['data_type'] = True
    data['published'] =STATE['P']
    data['pending'] =STATE['N']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['total'] =total

    return render_to_response('movies/staff/movie-home-listing.html',data,context_instance=RequestContext(request)) 


@staff_member_required
def ajax_display_movie(request,template='movies/staff/ajax-movie-listing.html'):
    ''' Movies listing method(ajax) for displaying videos based on the parameters passed by user''' 
    
    data=filter_movies(request)

    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    else:send_data['count']=0
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    else:send_data['pagerange']='0 - 0'
    return HttpResponse(simplejson.dumps(send_data))

@staff_member_required
def filter_movies(request):
    ''' videos filtering functions based on status,created by,search'''
    today=datetime.datetime.now()
    today_date=today.date()
    
    key={}
    q=()
    created_user = False
    status = request.GET.get('status','all')
    listing_type = request.GET.get('listing','all')
    created = request.GET.get('created','all')
    sort = request.GET.get('sort','-created_on')
    action = request.GET.get('action',False)
    ids = request.GET.get('ids',False)
    search = request.GET.get('search',False)
    item_perpage=int(request.GET.get('item_perpage',ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))
    if page < 1:
        page = 1
    if status!='all' and status!='':
        key['status'] = status
    
    sort_val = sort
    if sort == 'upcoming':
        key['release_date__gt']=today_date 
        sort =  '-created_on' 
    if sort == 'nowplaying':
        key['release_date__lte']=today_date
        key['status'] = 'P' 
        sort =  '-created_on'
               
    if created!='all':
        if created =='CSM':key['created_by'] = request.user
        else:created_user = True
    ########
    if search:
        search_type = request.GET.get('type','-created_on')
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
        if search_type == 'upcoming':
            key['release_date__gt'] =today_date
            
        if search_type == 'nowplaying':
            key['status'] = 'P'
            key['release_date__lte'] = today_date
        if search_category:
            key['movie_type__id'] = search_category
        if search_keyword:
            
            q =(Q(title__icontains=search_keyword)|Q(synopsis__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            if not created_user:moviedisplay = Movies.objects.filter(q,**key).select_related('created_on').order_by(sort)
            else:moviedisplay = Movies.objects.filter(q,**key).select_related('created_on').exclude(created_by = request.user).order_by(sort)
        else:
            if not created_user:moviedisplay = Movies.objects.filter(~Q(status='D'),**key).select_related('created_on').order_by(sort)
            else:moviedisplay = Movies.objects.filter(**key).select_related('created_on').exclude(created_by = request.user).order_by(sort)
    #################################
    else:
        if not created_user:moviedisplay = Movies.objects.filter(**key).select_related('created_on').order_by(sort)
        else:moviedisplay = Movies.objects.filter(**key).select_related('created_on').exclude(created_by = request.user).order_by(sort)   
    
    data = ds_pagination(moviedisplay,page,'moviedisplay',item_perpage)
    data['status'] = status
    data['listing_type'] = listing_type
    data['created'] = created
    if sort:
        data['sort']= sort_val
    data['search']= search
    data['item_perpage']=item_perpage
    return data


@staff_member_required
def ajax_movie_action(request,template='movies/staff/movie-ajax-delete-listing.html'):  #
    ''' ajax method for performing actions(update status,delete) ''' 
    key={}
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    movies = Movies.objects.filter(id__in=id)
    movie_count=movies.count()
    status=0
    msg=mtype=''
    
    if action=='DEL':
        if request.user.has_perm('movies.delete_movies'):
            signals.celery_delete_indexs.send(sender=None,objects=movies)
            for movie in movies: 
                try:movie.album.delete()
                except:pass
                try:MpttComment.objects.filter(content_type=movie_content_type, object_pk=movie.id).delete()
                except:pass
            movies.delete()
            status=1
            msg=str(MOVIE_MSG['MDS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    else:
        if request.user.has_perm('movies.publish_movies'):
            movies.update(status=action)
            signals.celery_update_indexs.send(sender=None,objects=movies)
            status=1
            msg=str(MOVIE_MSG['MSCS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    for movie in movies:
        movie.save()
        for log in movie.audit_log.all()[:1]:
            log.action_type = action
            log.save()
    data=filter_movies(request)
    
    new_id=[]
    for vid in data['moviedisplay']:new_id.append(int(vid.id))
    for ai in id:all_ids.remove(ai)

    for ri in all_ids:
        for ni in new_id:
            if int(ni)==int(ri):
                new_id.remove(int(ri))
                
    data['new_id']=new_id
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagenation']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    send_data['msg']=msg
    send_data['mtype']=mtype    
    send_data['status']=status  
    return HttpResponse(simplejson.dumps(send_data)) 

@staff_member_required
def ajax_movie_state(request):
    estatus = request.GET.get('status','all')
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'E':0,'K':0}
    if estatus == 'all':
        movie_state = Movies.objects.values('status').annotate(s_count=Count('status'))
    else:
        movie_state = Movies.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))

    for st in movie_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    data={
          'total':total,
          'published':STATE['P'],
          'pending':STATE['N'],
          'rejected':STATE['R'],
          'blocked':STATE['B'],
          'status':estatus,
    }
    return HttpResponse(simplejson.dumps(data))

@staff_member_required
@permission_required('movies.publish_movies',raise_exception=True)
def ajax_change_status(request):
    get_movie = Movies.objects.get(id=int(request.GET['id']))
    get_action = request.GET['status']
    if get_movie:
        get_movie.status = get_action
        if get_action == 'P':
            get_movie.is_active=True
        else:
            get_movie.is_active=False
    get_movie.save()
    for log in get_movie.audit_log.all()[:1]:
        log.action_type = get_action
        log.save()
        
    signals.celery_update_index.send(sender=None,object=get_movie)
    html ='<span title="'+get_movie.get_movie_status().title()+'" name="'+get_movie.status+'" id="id_icon_published'+str(get_movie.id)+'" class="inline-block status-idty icon-'+get_movie.get_movie_status()+'"></span> '     
    return HttpResponse(html)
    #return HttpResponse(simplejson.dumps(data))     


@staff_member_required
@permission_required('movies.add_movies',raise_exception=True)
def add_movie_details(request):
    data = {}
    if request.POST:
        data['new_pic']=request.POST.getlist('new_pic')
        try:data['movie_tags'] = request.POST['tags'].split(',')
        except:data['movie_tags'] = request.POST['tags']
        form = AddMovieForm(request.POST,request.FILES)
        if form.is_valid():
            add_movie_form=form.save(commit=False)
            add_movie_form.created_by = add_movie_form.modified_by = request.user
            add_movie_form.slug=getUniqueValue(Movies,slugify(add_movie_form.title))
            try: yt_url = add_movie_form.movie_url  
            except:yt_url = False
            if yt_url:
                try:
                    add_movie_form.movie_url=yt_url.split('v=')[1].split('&')[0]
                    add_movie_form.is_vimeo=False
                except:
                    try:
                        add_movie_form.movie_url=yt_url.split('.com/')[1].split('/')[0]
                        add_movie_form.is_vimeo=True
                    except:pass
            add_movie_form.status = 'P'
            tags = request.POST['tags'].split(',')
            twitter_hash = ''
            for tag in tags:
                tag = tag.strip()[:50]
                if tag != '': 
                    if len(tags) == 1:
                        twitter_hash = twitter_hash +tag
                    else:
                        twitter_hash = twitter_hash + tag + ','    
            add_movie_form.twitter_hash  = twitter_hash
           
            add_movie_form.seo_title=add_movie_form.title[:200]
            add_movie_form.seo_description=strip_tags(add_movie_form.synopsis[:350])
           
            photo_ids = request.POST.getlist('photo_id',None)
            if photo_ids:
                album = PhotoAlbum()
                album.created_by = request.user
                album.category = movie_album_cat
                album.title = add_movie_form.title
                album.is_editable = False
                album.seo_title = add_movie_form.title[:70]
                album.slug = getUniqueValue(PhotoAlbum, slugify(add_movie_form.slug))
                album.seo_description = album.summary = add_movie_form.synopsis[:160]
                album.status = 'N'
                album.save()
                add_movie_form.album = album
                Photos.objects.filter(id__in=photo_ids).update(album=album)
           
            add_movie_form.save()
            form.save_m2m()
            add_movie_form.save()
            signals.celery_update_index.send(sender=None,object=add_movie_form)
            for log in add_movie_form.audit_log.all():
                if log.action_type=="U":
                    log.delete()
           
            messages.success(request, str(MOVIE_MSG['YES']))
            return HttpResponseRedirect(reverse('staff_movie_listing'))
        else:
            data['form']= form
            return render_to_response('movies/staff/add-movie-details.html',data,context_instance=RequestContext(request))
    else:
        data['form']=AddMovieForm()
    return render_to_response('movies/staff/add-movie-details.html',data, context_instance=RequestContext(request))

@staff_member_required
def ajax_upload_photos(request):
    if request.method == "POST":
        gal_id = request.POST.get('gal_id')
        mid = request.GET.get('id')
        if gal_id and gal_id.isdigit():
            album = PhotoAlbum.objects.get(id=gal_id)
        elif mid:
            movie = Movies.objects.get(id=mid)
            album = movie.album
        else: 
            album = None
        response = upload_photos_forgallery(request,Photos,album,'album')
        return response
    else:
        movie = Movies.objects.get(id=request.GET['id'])
        album = movie.album
        return upload_photos_forgallery(request,Photos,album,'album')


@staff_member_required
def ajax_delete_photos(request,pk):
    return delete_photos(request,MoviesPhoto,pk)

#################  Ajax Image Uploading End #################


#############################
@staff_member_required
@permission_required('movies.change_movies',raise_exception=True)
def edit_movie_detail(request):
    data = {}
    try:edit_movie = Movies.objects.get(id=request.REQUEST['id'])
    except:HttpResponseRedirect(reverse('staff_display_movie'))
    form=AddMovieForm(instance=edit_movie)
    if request.POST:
        try:data['movie_tags'] = request.POST['tags'].split(',')
        except:data['movie_tags'] = request.POST['tags']
        form = AddMovieForm(request.POST,request.FILES,instance=edit_movie)
        if form.is_valid():
            edit_movie_form=form.save(commit=False)
            edit_movie_form.slug=getUniqueValue(Movies,slugify(edit_movie_form.title),instance_pk=edit_movie_form.id)
            edit_movie_form.modified_by = request.user
            tags = request.POST['tags'].split(',')
            try:yt_url = request.POST['movie_url'] 
            except:yt_url = False
           
            if yt_url:
                try:
                    edit_movie_form.movie_url=yt_url.split('v=')[1].split('&')[0]
                    edit_movie_form.is_vimeo=False
                except:
                    try:
                        edit_movie_form.movie_url=yt_url.split('.com/')[1].split('/')[0]
                        edit_movie_form.is_vimeo=True
                    except:pass
            try:
                add_movie_form.image = request.POST['image']
            except:
                pass
            twitter_hash = ''
            for tag in tags:
                tag = tag.strip()
                if tag != '': 
                    if len(tags) == 1:
                        twitter_hash = twitter_hash +tag
                    else:
                        twitter_hash = twitter_hash + tag + ','    

            edit_movie_form.twitter_hash  = twitter_hash
           
            photo_ids = request.POST.getlist('photo_id',None)
            if photo_ids:
                if edit_movie.album:
                    album = edit_movie.album
                else:
                    album = PhotoAlbum()
                    album.created_by = request.user
                    album.category = movie_album_cat
                    album.is_editable = False
                    album.status = 'N'
                album.title = edit_movie_form.title
                album.slug = getUniqueValue(PhotoAlbum, slugify(edit_movie_form.title))
                album.seo_title = edit_movie_form.title[:70]
                album.seo_description = album.summary = edit_movie_form.synopsis[:160]
                album.save()
                edit_movie_form.album = album
                Photos.objects.filter(id__in=photo_ids).update(album=album)
           
            edit_movie_form.save()
            form.save_m2m() 
            messages.success(request, str(MOVIE_MSG['MES']))
            signals.celery_update_index.send(sender=None,object=edit_movie_form)
            return HttpResponseRedirect(reverse('staff_movie_listing'))
    else:   
        data['form'] = form
        data['movie'] = edit_movie  
        try:
            data['hash_tags'] = edit_movie.twitter_hash.split(',')
        except:data['hash_tags']=False
    return render_to_response('movies/staff/edit-movie.html',data,context_instance=RequestContext(request))

@staff_member_required
@permission_required('movies.change_movies',raise_exception=True)
def ajax_movie_seo(request,template='movies/staff/add-movie-seo.html'):
    ''' ajax method for editing/updating SEO of movie ''' 
    movie = Movies.objects.get(id=request.REQUEST['movie_id'])
    form=MovieTypeSEOForm(instance=movie) 
    if request.POST:
        form=MovieTypeSEOForm(request.POST,instance=movie) 
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(MOVIE_MSG['MSUS'])}))
        else:
            data={'form':form,'movie':movie}
            return error_response(request,data,template,MOVIE_MSG)
    data={'form':form,'movie':movie}
    return render_to_response(template,data, context_instance=RequestContext(request))   



@staff_member_required
def upload_pic(request):
    data={}
    try:
        movie = Movies.objects.get(id=request.GET['movie_id'])
        data['movie']=movie
    except:
        return HttpResponseRedirect('/staff/movies/addmoviestep1/')
    
    return render_to_response('movies/staff/upload-picture.html',data, context_instance=RequestContext(request))

@staff_member_required
def add_showtimes(request):
    data = {}
    theatres = Theatres.objects.order_by('name')
    try :
        movie = Movies.objects.get(id=request.REQUEST['movie_id'])
    except:
        return HttpResponseRedirect('/staff/movies/?message=Movie Not Found')
    i = range(0,7)
    today = datetime.datetime.now()
    dates = []
    for val in i:
        dates.append(today + datetime.timedelta(val))
    try:
        added = MovieTime.objects.filter(movie=movie)
    except:added=False
    
    data['movie'] = movie
    data['theatres']=theatres
    data['added'] = added
    data['dates'] = dates
    return render_to_response('movies/staff/movieshowtime-add.html',data,context_instance=RequestContext(request))   
 
@staff_member_required
def add_movie_show_details(request):
    try:
        theatre = Theatres.objects.get(id=request.GET['theatre'])
        movie = Movies.objects.get(id=request.GET['id'])
        try:
            save_show = MovieTime.objects.get(theatre=theatre,movie=movie)
            ShowTime.objects.filter(movietime=save_show).delete()
        except:
            save_show = MovieTime(theatre=theatre,movie=movie)
        added = MovieTime.objects.filter(movie=movie)
        save_show.save()
        ran = range(1,8)
        show_time = request.GET['show_time'].strip().split(',,')
        for (i,sh) in zip(ran,show_time):
            if sh==':':
                continue;
            else:
                st = ShowTime(movietime=save_show)
                st.date=datetime.datetime.now()+datetime.timedelta(i-1)
                
                st.show_times = sh
                if st.show_times ==':,':
                    pass
                else:
                    status = '1'
                    st.save() 
        msg = MOVIE_MSG['MSAS']
        mtype=get_msg_class_name('s')
        html=render_to_string('movies/staff/load_latest_showtime.html',{'movie_preview':movie,'added':added},context_instance=RequestContext(request))
    except:
        movie = Movies.objects.get(id=request.GET['id'])
        added = MovieTime.objects.filter(movie=movie)
        status = '0'
        msg =MOVIE_MSG['OOPS']
        mtype=get_msg_class_name('e')
        html=render_to_string('movies/staff/load_latest_showtime.html',{'movie_preview':movie,'added':added},context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps({'status':status,'mtype':mtype,'html':html,'msg':str(msg)}))    

@staff_member_required
def edit_showtime_movie(request):
    data = {}
    id = request.REQUEST['id']
    movietime = MovieTime.objects.get(id=id)
    theatres = Theatres.objects.order_by('name')
    i = range(0,7)
    today = datetime.datetime.now()
    dates = []
    for val in i:
        dates.append(today+datetime.timedelta(val))
    return render_to_response('movies/staff/movieshowtime-edit.html',locals(),context_instance=RequestContext(request))
  
@staff_member_required
def update_movie_ajax_showtime(request):
    try:
        ids  = request.POST['edit_movietime']
        movietime = MovieTime.objects.get(id=ids)
        movie = movietime.movie.id
        ShowTime.objects.filter(movietime = movietime).delete()
        ran = range(1,8)
        show_time = request.POST['show_time'].strip().split(',,')
        
        for (i,sh) in zip(ran,show_time):
            if sh==':':
                continue;
            else: 
                st = ShowTime(movietime=movietime)
                st.date=datetime.datetime.now()+datetime.timedelta(i-1)
                
                st.show_times = sh
                if st.show_times ==':,':
                    pass
                else:
                    st.save()
        status = '1'
        msg = MOVIE_MSG['MSTUS']
        movie_preview = Movies.objects.get(id=movie)
        added = MovieTime.objects.filter(movie=movie_preview)
        html=render_to_string('movies/staff/load_latest_showtime.html',{'movie_preview':movie_preview,'added':added},context_instance=RequestContext(request))          
        mtype =get_msg_class_name('s')
        return HttpResponse(simplejson.dumps({'status':1,'mtype':mtype,'html':html,'msg':str(msg)}))  # movie showtime updated successfully            
    except:
        msg = MOVIE_MSG['OOPS']
        movie_preview = Movies.objects.get(id=movie)
        added = MovieTime.objects.filter(movie=movie_preview)
        html=render_to_string('movies/staff/load_latest_showtime.html',{'movie_preview':movie_preview,'added':added},context_instance=RequestContext(request))          
        mtype =get_msg_class_name('e')
        return HttpResponse(simplejson.dumps({'status':1,'mtype':mtype,'html':html,'msg':str(msg)}))  # movie showtime updated successfully
    
@staff_member_required
def delete_movie_showtime(request):
    get_show = MovieTime.objects.get(id=request.GET['id'])
    movie = Movies.objects.get(id=get_show.movie.id)
    get_show.delete()
    try:
        added = MovieTime.objects.filter(movie=get_show.movie)
    except:
        pass
    mtype =get_msg_class_name('s')
    html=render_to_string('movies/staff/load_latest_showtime.html',{'movie_preview':movie,'added':added},context_instance=RequestContext(request))          
    return HttpResponse(simplejson.dumps({'status':1,'html':html,'mtype':mtype,'msg':str(MOVIE_MSG['MSDS'])}))


@staff_member_required
def movie_preview(request):
    data = {}
    try :
        showtimes = request.REQUEST['view'] 
    except:
        showtimes = False   
    movie_preview = Movies.objects.get(id=int(request.REQUEST['id']))
    try:
        added = MovieTime.objects.filter(movie=movie_preview)
    except:added=False
    
    msg = request.GET.get('msg',"")
    try:data['msg'] =MOVIE_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    if showtimes=='st':
        data['showtimes'] = showtimes 
    if showtimes=='cr':
        data['review'] = showtimes
    data['added'] = added
    data['movie_preview'] = movie_preview
    return render_to_response('movies/staff/movie-preview.html',data,context_instance=RequestContext(request))


@staff_member_required
def add_movie_critic_review(request):
    data = {}
    try:movie_preview = Movies.objects.get(id=request.REQUEST['movie_id'])
    except:return HttpResponseRedirect('/staff/movies/?message=Sorry some problem in adding critic review')
    if request.method=='POST':
        form = AddMovieCriticsReviewForm(request.POST)
        if form.is_valid():
            add_cr_obj = form.save(commit=False)
            add_cr_obj.rating=int(request.POST['rating'])
            add_cr_obj.movie = movie_preview
            add_cr_obj.save()
            return HttpResponseRedirect('/staff/movies/moviepreview/?id='+str(movie_preview.id)+'&msg=MCRAS&mtype=s&view=cr')
        else:
            form=AddMovieCriticsReviewForm()
            data['form']=form
            data['movie_preview']=movie_preview
            return render_to_response('movies/staff/add-critics-review.html',data, context_instance=RequestContext(request))
    else:
        cr_reviews=CriticReview.objects.values_list('source__id', flat=True).filter(movie__id=movie_preview.id)
        form=AddMovieCriticsReviewForm(cr_reviews=cr_reviews)
        source = CriticSource.objects.exclude(id__in=cr_reviews).order_by('source_title')
    if not source:
        return HttpResponse('<div class="group no-data" style="padding:50px;"><p>Oops !!! Review has been added for all the source !!!</p></div>')
    data['form']=form
    data['movie_preview']=movie_preview
    return render_to_response('movies/staff/add-critics-review.html',data, context_instance=RequestContext(request))

@staff_member_required
def save_critic_review(request):
    try:movie_preview = Movies.objects.get(id=request.REQUEST['movie_id'])
    except:return HttpResponseRedirect('/staff/movies/?message=Sorry some problem in adding critic review')
    if request.method=='POST':               
        form = AddMovieCriticsReviewForm(request.POST)
        if form.is_valid():
            add_cr_obj = form.save(commit=False)
            add_cr_obj.rating=int(request.POST['rating'])
            add_cr_obj.movie = movie_preview
            add_cr_obj.save()
            status = '1'
            mtype =get_msg_class_name('s')
            html=render_to_string('movies/staff/load_latest_review.html',{'movie_preview':movie,'added':added},context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'status':status,'mtype':mtype,'html':html,'msg':'Critic review saved successfully'}))    
        else:
            status = '0'
            msg = MOVIE_MSG['OOPS']
            mtype =get_msg_class_name('e')
    return HttpResponse(simplejson.dumps({'status':1,'mtype':mtype,'msg':str(msg)})) 

@staff_member_required
def edit_critics_reviews_ajax(request):
    data = {}
    movie_preview = Movies.objects.get(id=request.REQUEST['mid'])
    critics=CriticReview.objects.get(id=request.REQUEST['id'])
    cr_reviews=CriticReview.objects.values_list('source__id', flat=True).filter(movie__id=movie_preview.id).exclude(id=critics.id)
    form=AddMovieCriticsReviewForm(instance=critics,cr_reviews=cr_reviews)
    if request.method == 'POST':
        form=AddMovieCriticsReviewForm(request.POST,instance=critics)
        if form.is_valid():
            edit_critics = form.save(commit=False)
            edit_critics.save()
            data['msg'] =msg=  'Critic Review Updated '
            html=render_to_string('movies/staff/load_latest_review.html',{'movie_preview':movie_preview},context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'html':html,'msg':msg}))
        else:
            data['form'] = form
            data['critics'] = critics 
            data['movie_preview'] = movie_preview  
            html=render_to_string('movies/staff/edit-critic-review.html',data, context_instance=RequestContext(request))
            return HttpResponse(simplejson.dumps({'status':0,'html':html}))
    data['form'] = form
    data['critics'] = critics 
    data['movie_preview'] = movie_preview  
    return render_to_response('movies/staff/edit-critic-review.html',data, context_instance=RequestContext(request))

@staff_member_required
def delete_movie_review(request):
    get_show = CriticReview.objects.get(id=request.GET['id'])
    movie = Movies.objects.get(id=get_show.movie.id)
    get_show.delete()
 ######################## Recheck it Nit Required 
    try:
        added = MovieTime.objects.filter(movie=movie_preview)
    except:added=False
############################################  
    mtype =get_msg_class_name('s')  
    html=render_to_string('movies/staff/load_latest_review.html',{'movie_preview':movie,'added':added},context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps({'status':1,'mtype':mtype,'html':html,'msg':str(MOVIE_MSG['MCRDS'])}))



#######################################  Theatre Seaction ######################################
@staff_member_required
def image_upload(request):
    return 1













@staff_member_required 
def theatre_listing(request):
    ''' Theatre Home ( listing ) '''
    data = {}
    item_perpage = int(request.GET.get('item_perpage',ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))
    
    theatredisplay = Theatres.objects.all().select_related('category','added_by').order_by('-id')
    # categories = MovieType.objects.order_by('name')
    total = 0
    msg = request.GET.get('msg',"")
    
    data = ds_pagination(theatredisplay,page,'theatredisplay',item_perpage)
    try:data['msg'] =MOVIE_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    #data['sort']='-added_on'
    
    return render_to_response('movies/staff/theatre-home-listing.html',data,context_instance=RequestContext(request))
  
global_settings = get_global_settings()

@staff_member_required
@permission_required('movies.add_movies',raise_exception=True)
def add_theatre_ajax(request,template='movies/staff/add-theatre.html'):
    data = {}
    from common.utils import get_global_settings
    global_settings = get_global_settings()
    if request.POST:
        data['new_pic']=request.POST.getlist('new_pic')
    
        form = AddTheatreForm(request.POST,request.FILES)
        add_form = AddressForm(request.POST)
        if form.is_valid() and add_form.is_valid():
            add_theatre = form.save(commit=False) 
            address = add_form.save(commit=False) 
            add_theatre.slug =slug= slugify(add_theatre.name)
            address.status='P'
            
            address.created_by = request.user
            address.modified_by = request.user
            address.seo_title = None
            address.venue = add_theatre.name[:100]
            address.address_type = 'theatres'
            address.slug=getUniqueValue(Address,slugify(add_theatre.name),instance_pk=address.id)
            try:
                address.lat, address.lon, address.zoom = get_lat_lng(request.POST['lat_lng'])
                try:address.zoom = int(request.POST['zoom'])
                except:pass
            except:
                address.lat, address.lon, address.zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
            add_theatre.address=address
            address.save()

            add_theatre.theatreseo_title=add_theatre.name[:200]
            add_theatre.theatreseo_description=add_theatre.name
            try:
                add_theatre.is_multiplex= request.POST['multiplex']
            except:
                add_theatre.is_multiplex = False
            add_theatre.address=address
            add_theatre.save()
            messages.success(request, str(MOVIE_MSG['MTAS']))
            #msg=str(MOVIE_MSG['MTAS'])
            signals.celery_update_index.send(sender=None,object=add_theatre)
            return HttpResponseRedirect(reverse('staff_theatre_listing'))  
            #send_data={'status':True,'msg':msg,'mtype':get_msg_class_name('s'),'id':add_theatre.id}
            #theatredisplay = Theatres.objects.all().order_by('-id')   
            #send_data['lightbox_html']=render_to_string("movies/staff/theatre-ajax-listing.html",{'theatredisplay':theatredisplay},context_instance=RequestContext(request))
            #return HttpResponse(simplejson.dumps(send_data))
        else:
            data = {'form':form,'add_form':add_form}
            msg = MOVIE_MSG
            return error_response(request,data,template,MOVIE_MSG)
   
    data['form'] = AddTheatreForm()
    data['add_form'] = AddressForm()
    return render_to_response(template,data,context_instance=RequestContext(request))



@staff_member_required
def theatre_action(request,template='movies/staff/theatre-ajax-delete-listing.html'):  #
    ''' ajax method for performing actions(update status,delete) ''' 
    
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    theatres = Theatres.objects.filter(id__in=id)
    theatre_count=theatres.count()
    status=0
    
    if action=='DEL':
        if request.user.has_perm('movies.delete_movies'):
            signals.celery_delete_indexs.send(sender=None,objects=theatres)
            theatres.delete()
            msg=str(MOVIE_MSG['TDS'])
            mtype=get_msg_class_name('s')
            status=1
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    else:
        if request.user.has_perm('movies.publish_movies'):
            theatres.update(status=action)
            signals.celery_update_indexs.send(sender=None,objects=theatres)
            msg=str(MOVIE_MSG['TSCS'])
            mtype=get_msg_class_name('s')
            status=1
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    
    data=filter_theatre(request)
    
    new_id=[]
    for vid in data['theatredisplay']:new_id.append(int(vid.id))
    for ai in id:all_ids.remove(ai)

    for ri in all_ids:
        for ni in new_id:
            if int(ni)==int(ri):
                new_id.remove(int(ri))
                
    data['new_id']=new_id
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagenation']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    send_data['msg']=msg
    send_data['mtype']=mtype    
    send_data['status']=status  
    return HttpResponse(simplejson.dumps(send_data)) 

@staff_member_required
def filter_theatre(request):
    ''' videos filtering functions based on status,created by,search'''
    key = {}
    q=()
    search = request.GET.get('search',False)
    item_perpage=int(request.GET.get('item_perpage',ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))  
    if search:
        search_keyword = request.GET.get('kwd',"").strip()
        if search_keyword:
            q =(Q(name__icontains=search_keyword)|Q(address__address1__icontains=search_keyword)|Q(address__address2__icontains=search_keyword)|Q(address__created_by__display_name__icontains=search_keyword))
            theatredisplay = Theatres.objects.filter(q,**key).order_by("-id")
        else:
            theatredisplay = Theatres.objects.filter(**key).order_by("-id")
    else:
        theatredisplay = Theatres.objects.filter(**key).order_by("-id")
    
    data = ds_pagination(theatredisplay,page,'theatredisplay',item_perpage)
    data['search']= search
    data['item_perpage']=item_perpage
    return data

@staff_member_required
def ajax_display_theatre(request,template='movies/staff/theatre-ajax-listing.html'):
    ''' Theatre listing method(ajax) for displaying videos based on the parameters passed by user''' 
    
    
    data=filter_theatre(request)

    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
        
    return HttpResponse(simplejson.dumps(send_data))

###################################Edit Theatre In color box#########################
@staff_member_required
@permission_required('movies.change_movies',raise_exception=True)
def edit_theatre(request,template = 'movies/staff/edit-theatre.html'):
    data = {}
    msg = ''
    theatre=Theatres.objects.get(id=int(request.REQUEST['id']))
    addr = Address.objects.get(id = theatre.address_id)
    if not request.POST:
        form = AddTheatreForm(instance=theatre) 
        data['form'] = form
        add_form = AddressForm(instance=addr)
        data['add_form']=add_form
    else:
        form = AddTheatreForm(request.POST,request.FILES,instance=theatre)
        add_form = AddressForm(request.POST,instance=addr)

        if form.is_valid() and add_form.is_valid():
            edit_theatre = form.save(commit=False)
            edit_theatre.theatre = theatre
            edit_theatre.slug =slug= slugify(edit_theatre.name)
            address = add_form.save(commit=False) 
            address.status='P'
        
            address.created_by = request.user
            address.modified_by = request.user
            address.seo_title = None
            address.venue = edit_theatre.name
            address.address_type = 'theatres'
            address.slug=getUniqueValue(Address,slugify(edit_theatre.name),instance_pk=address.id)
            try:
                address.lat, address.lon, address.zoom = get_lat_lng(request.POST['lat_lng'])
                try:address.zoom = int(request.POST['zoom'])
                except:pass
            except:
                address.lat, address.lon, address.zoom = [global_settings.google_map_lat, global_settings.google_map_lon, global_settings.google_map_zoom]
            edit_theatre.address=address
            address.save()
            try:
                add_movie_form.image = request.POST['image']
            except:
                pass
            try:
                edit_theatre.is_multiplex= request.POST['multiplex']
            except:
                edit_theatre.is_multiplex = False
            edit_theatre.save()
            msg = str(MOVIE_MSG['TU'])
            messages.success(request, str(MOVIE_MSG['MTUS']))
            return HttpResponseRedirect(reverse('staff_theatre_listing'))     
        else:
            data = {'form':form,'add_form':add_form}
            msg = MOVIE_MSG
            return error_response(request,data,template,MOVIE_MSG)
    data['theatre']=theatre 
    return render_to_response(template,data,context_instance=RequestContext(request))


########################################Not Using Right Now Ask to the bosses
@staff_member_required
def add_theatre_pic(request):  
    try:theatre = Theatres.objects.get(id=request.GET['id'])
    except: theatre = None
    return upload_photos(request,Theatres,theatre,'theatre')
################################End##########################################




@staff_member_required
@permission_required('movies.change_movies',raise_exception=True)
def ajax_theatre_seo(request,template='movies/staff/add-theatre-seo.html'):
    ''' ajax method for editing/updating SEO of Theatre ''' 
    
    theatre = Theatres.objects.get(id=request.REQUEST['theatre_id'])
    form=TheatresSEOFORM(instance=theatre) 
    if request.POST:
        form=TheatresSEOFORM(request.POST,instance=theatre)
        if form.is_valid():
            form.save()
            mtype =get_msg_class_name('s')
            return HttpResponse(simplejson.dumps({'status':1,'mtype':mtype,'msg':str(MOVIE_MSG['TSU'])}))
        else:
            data={'form':form,'theatre':theatre}
            return error_response(request,data,template,MOVIE_MSG)
    data={'form':form,'theatre':theatre}
    return render_to_response(template,data, context_instance=RequestContext(request))   

@staff_member_required
def theatre_preview(request):
    data = {}
    try :
        showtimes = request.REQUEST['view'] 
    except:
        showtimes = False  
    
    try:
        theatre_preview = Theatres.objects.get(id=int(request.REQUEST['id']))
        movies = Movies.objects.order_by('title')
    except:
        pass
    i = range(0,7)
    today = datetime.datetime.now()
    dates = []
    for val in i:
        dates.append(today+datetime.timedelta(val))
    try:
        added = MovieTime.objects.filter(theatre=theatre_preview)
    except:pass
    if showtimes =='st':
        data['showtimes'] = showtimes
    return render_to_response('movies/staff/theatre-details.html',locals(),context_instance=RequestContext(request))

@staff_member_required
def add_theatre_showtime(request):
    data = {}
    movie = Movies.objects.order_by('title')
    try :
        theatres = Theatres.objects.get(id=request.REQUEST['theatre_id'])
    except:
        return HttpResponseRedirect('/staff/movies/?message=Theatre Not Found')
    i = range(0,7)
    today = datetime.datetime.now()
    dates = []
    for val in i:
        dates.append(today+datetime.timedelta(val))
    try:
        added = MovieTime.objects.filter(theatre=theatres.id)
    except:added=False
    
    data['movie'] = movie
    data['theatres']=theatres
    data['added'] = added
    data['dates'] = dates
    return render_to_response('movies/staff/theatreshowtimeadd.html',data,context_instance=RequestContext(request))

@staff_member_required
def save_theatre_showtime(request):
    try:
        theatre = Theatres.objects.get(id=request.GET['id'])
        movie = Movies.objects.get(id=request.GET['movie'])
        
        try:
            save_show = MovieTime.objects.get(theatre=theatre,movie=movie)
            ShowTime.objects.filter(movietime=save_show).delete()
        except:
            save_show = MovieTime(theatre=theatre,movie=movie)
        
        added = MovieTime.objects.filter(theatre=theatre.id)
        save_show.save()
        ran = range(1,8)
        show_time = request.GET['show_time'].strip().split(',,')
        for (i,sh) in zip(ran,show_time):
            if sh==':':
                continue;
            else:
                st = ShowTime(movietime=save_show)
                st.date=datetime.datetime.now()+datetime.timedelta(i-1)
                
                st.show_times = sh
                if st.show_times ==':,':
                    pass
                else:
                    status = '1'
                    st.save() 
        msg = MOVIE_MSG['MSAS']
        mtype =get_msg_class_name('s')
        html=render_to_string('movies/staff/load_latest_showtime_theatre.html',{'theatre_preview':theatre,'added':added},context_instance=RequestContext(request))
    except:
        movie = Movies.objects.get(id=request.GET['id'])
        added = MovieTime.objects.filter(movie=movie)
        status = '0'
        msg =MOVIE_MSG['OOPS']
        mtype =get_msg_class_name('e')
        html=render_to_string('movies/staff/load_latest_showtime.html',{'movie_preview':movie,'added':added},context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps({'status':status,'mtype':mtype,'html':html,'msg':str(msg)}))    



@staff_member_required
def edit_theatre_showtime(request):
    #theatre = Theatres.objects.get(id=request.GET['id'])
    movies = Movies.objects.order_by('title')
    i = range(0,7)
    today = datetime.datetime.now()
    dates = []
    for val in i:
        dates.append(today+datetime.timedelta(val))
    id = request.REQUEST['id']
    movietime = MovieTime.objects.get(id=id)
        #added = MovieTime.objects.filter(theatre=theatre)
#     try:""
#     except:pass
    return render_to_response('movies/staff/edit-theatre-show.html',locals(), context_instance=RequestContext(request))

@staff_member_required 
def save_edit_theatre_show(request):  
    try: 
        ids  = request.POST['edit_movietime']
        movietime = MovieTime.objects.get(id=ids)
        movie = movietime.movie.id
        ShowTime.objects.filter(movietime = movietime).delete()
        theatre = Theatres.objects.get(id=request.POST['theatreid'])
      
        added = MovieTime.objects.filter(theatre=theatre.id)
        ran = range(1,8)
        show_time = request.POST['show_time'].strip().split(',,')
        for (i,sh) in zip(ran,show_time):
            if sh==':':
                continue;
            else:
                st = ShowTime(movietime=movietime)
                st.date=datetime.datetime.now()+datetime.timedelta(i-1)
                
                st.show_times = sh
                if st.show_times ==':,':
                    pass
                else:
                    status = '1'
                    st.save() 
        msg = MOVIE_MSG['TSUS']
        mtype =get_msg_class_name('s')
        html=render_to_string('movies/staff/load_latest_showtime_theatre.html',{'theatre_preview':theatre,'added':added},context_instance=RequestContext(request))
    except:
        added = MovieTime.objects.filter(movie=movie)
        theatre = Theatres.objects.get(id=request.POST['theatreid'])
        status = '0'
        msg =MOVIE_MSG['OOPS']
        mtype =get_msg_class_name('e')
        html=render_to_string('movies/staff/load_latest_showtime_theatre.html',{'theatre_preview':theatre,'added':added},context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps({'status':status,'mtype':mtype,'html':html,'msg':str(msg)}))    

@staff_member_required
def delete_theatres_showtime(request):
    get_show = MovieTime.objects.get(id=request.GET['id'])
    movie = Movies.objects.get(id=get_show.movie.id)
    get_show.delete()
    try:
        added = MovieTime.objects.filter(theatre=get_show.theatre)
    except:
        pass
    html=render_to_string('movies/staff/load_latest_showtime_theatre.html',{'theatre_preview':get_show.theatre,'added':added},context_instance=RequestContext(request))
    return HttpResponse(simplejson.dumps({'status':1,'html':html,'mtype':'s','msg':str(MOVIE_MSG['MSDS'])}))

