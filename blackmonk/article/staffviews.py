from bs4 import BeautifulSoup
import csv
import datetime
from django.conf import settings as my_settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils import simplejson, timezone
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext as _
from django.views.decorators.csrf import csrf_exempt

from article.forms import ArticleStaffForm, ArticleSeoForm
from article.models import Article, ArticleCategory, Tag, ArticlePrice
from article.tasks import process_articles_csv_upload
from common import signals
from common.fileupload import get_default_images, upload_photos_forgallery, \
    delete_photos
from common.forms import UploadEditorImageForm
from common.getunique import getUniqueValue
from common.mail_utils import mail_publish_article
from common.models import CSVfile
from common.staff_messages import ARTICLE_MSG, COMMON
from common.staff_utils import error_response
from common.templatetags.ds_utils import get_msg_class_name, get_status_class
from common.utils import ds_pagination
from common.utilviews import crop_and_save_coverphoto
from gallery.models import PhotoAlbum, PhotoCategory, Photos
from payments.models import PaymentOrder
from payments.utils import get_invoice_num


#from photo_library  import signals
article_album_cat = PhotoCategory.objects.get_or_create(name="Articles", slug='articles', is_editable=False)[0]
rand = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
NO_OF_ITEMS_PER_PAGE=10
FEATURE_LIMIT=8

########################### MANAGE ARTICLE ############################
@staff_member_required
def list_articles(request,template='article/staff/home.html'):
    categorys = ArticleCategory.objects.all().order_by('name')
    articles = Article.objects.all().order_by('-created_on')
    article_state = articles.values('status').annotate(s_count=Count('status'))

    total = 0
    STATE={'P':0,'N':0,'R':0,'B':0,'S':0, 'D':0}
    for st in article_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']

    data = ds_pagination(articles,'1','articles',NO_OF_ITEMS_PER_PAGE)
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'

    data['category'] = categorys
    data['total'] =total
    data['published'] =STATE['P']
    data['pending'] =STATE['N']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['scheduled'] =STATE['S']
    data['drafted'] =STATE['D']
    data['search'] =False
    try:data['recent'] = request.GET['pending_articles']
    except:data['recent'] = False
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
def ajax_list_articles(request,template='article/staff/ajax-article-listing.html'):
    data=filter_article(request)
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
def ajax_article_action(request,template='article/staff/ajax_delete_listing.html'):
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    article_list = Article.objects.filter(id__in=id)
    cls_count=article_list.count()
    status=0

    if action=='DEL':
        if request.user.has_perm('article.delete_article'):
            signals.celery_delete_indexs.send(sender=None,objects=article_list)
            for article in article_list:
                try:
                    article.album.delete()
                except:
                    pass
            article_list.delete()
            status=1
            msg=str(ARTICLE_MSG['SAD'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    else:
        if request.user.has_perm('article.publish_article'):
            article_list.update(status=action)
            signals.celery_update_indexs.send(sender=None,objects=article_list)
            status=1
            msg=str(ARTICLE_MSG[action])
            mtype=get_msg_class_name('s')
            if action=='P':
                try:
                    for article in article_list:mail_publish_article(article)
                except:pass
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')

    for article in article_list:
        article.save()
        for log in article.audit_log.all()[:1]:
            log.action_type = action
            log.save()
    data=filter_article(request)

    new_id=[]
    for cs in data['articles']:new_id.append(int(cs.id))
    for ai in id:all_ids.remove(ai)

    for ri in all_ids:
        for ni in new_id:
            if int(ni)==int(ri):
                new_id.remove(int(ri))

    data['new_id']=new_id
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagination']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
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

def filter_article(request):
    data=key={}
    q=()
    created_user = False
    status = request.GET.get('status','all')
    listing_type = request.GET.get('listing','all')
    created = request.GET.get('created','all')
    sort = request.GET.get('sort','-created_on')
    action = request.GET.get('action',False)
    ids = request.GET.get('ids',False)
    search = request.GET.get('search',False)
    item_perpage=int(request.GET.get('item_perpage',NO_OF_ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))

    if status!='all' and status!='':key['status'] = status
    if listing_type!='all':
        if listing_type =='F':key['featured'] = True
        else:key['featured'] = False

    if created!='all':
        if created =='CSM':key['created_by'] = request.user
        else:created_user = True
    if search:
        search_type = request.GET.get('type',None)
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
        
        if search_category:
            categorys = ArticleCategory.objects.get(id=search_category)
            key['category'] = categorys
        if search_type:
            if search_type=='title':key['title__icontains'] = search_keyword
            elif search_type=='desc':key['content__icontains'] = search_keyword
            else:key['created_by__display_name__icontains'] = search_keyword
        else:
            q =(Q(title__icontains=search_keyword)|Q(category__name__icontains=search_keyword)|Q(summary__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))    
        if search_keyword or search_type:
            if not created_user:
                articles = Article.objects.filter(**key).select_related('category','created_by').order_by(sort)
            else:
                articles = Article.objects.filter(**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
            if q:
                articles = articles.filter(q)     
        else:
            if not created_user:
                articles = Article.objects.filter(**key).select_related('category','created_by').order_by(sort)
            else:
                articles = Article.objects.filter(**key).select_related('category','created_by').exclude(created_by = request.user).order_by(sort)
    else:
        if not created_user:
            articles = Article.objects.filter(**key).select_related('category','created_by').order_by(sort)
        else:
            articles = Article.objects.select_related('category','created_by').exclude(created_by = request.user).order_by(sort)


    data = ds_pagination(articles,page,'articles',item_perpage)
    data['status'] = status
    data['listing_type'] = listing_type
    data['created'] = created
    data['sort']= sort
    data['search']= search
    data['item_perpage']=item_perpage
    return data


@staff_member_required
def ajax_article_state(request):
    status = request.GET.get('status','all')
    total = 0
    STATE={'P':0,'N':0,'R':0,'B':0,'S':0,'D':0}

    if status == 'all':
        article_state = Article.objects.values('status').annotate(s_count=Count('status'))
    else:
        article_state = Article.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))

    for st in article_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    data={
        'total':total,
        'published':STATE['P'],
        'pending':STATE['N'],
        'rejected':STATE['R'],
        'blocked':STATE['B'],
        'scheduled':STATE['S']
    }
    return HttpResponse(simplejson.dumps(data))

@staff_member_required
@permission_required('article.add_article',raise_exception=True)
def article_type(request,template='article/staff/article_type.html'):
    data = {}
    data['pricing']=ArticlePrice.objects.filter()[:1][0]
    if request.method=='POST':
        try:
            type = request.POST['article_type']
            try:
                price=request.POST['price_'+type]
                url=reverse('staff_article_add_article')+'?a_tpe='+type+'&price='+str(price)
            except:url=reverse('staff_article_add_article')+'?a_tpe='+type
            return HttpResponseRedirect(url)
        except:
            messages.error(request, str(ARTICLE_MSG['err']))
            return HttpResponseRedirect(reverse('staff_article_home'))
    return render_to_response(template,data, context_instance=RequestContext(request))


@staff_member_required
def add_article(request,template='article/staff/addArticle.html'):
    data = {}
    data['published_on'] = timezone.now()
    try:
        article = Article.objects.get(id=request.REQUEST['aid'])
        form = ArticleStaffForm(instance=article)
        if not request.user.has_perm('article.change_article'):raise PermissionDenied
    except:
        article = False
        form = ArticleStaffForm()
        if not request.user.has_perm('article.add_article'):raise PermissionDenied
        pricing=ArticlePrice.objects.filter()[:1][0]
        data['article_tpe'] = article_type = request.REQUEST.get('a_tpe',
             request.POST.get('article_type', 'FR')
        )
        try:data['price']=price=request.REQUEST['price']
        except:pass
        if article_type=='FR' or article_type=='RR' or article_type=='A' or article_type=='PR':data['article_type']=article_type
        else:
            messages.error(request, str(ARTICLE_MSG['err']))
            return HttpResponseRedirect(reverse('staff_article_home'))

    data['article']=article
    if article:
            data['article_tags']=article.tags.all()
            data['slug'] = article.slug

    if request.POST:
        if article:form = ArticleStaffForm(request.POST,instance=article)
        else:form = ArticleStaffForm(request.POST)
        try:data['slug'] = request.POST['slug'].strip()
        except:pass
        data['new_pic']=request.POST.getlist('new_pic')
        try:data['article_tags'] = request.POST['tags'].split(',')
        except:data['article_tags'] = request.POST['tags']
        data['article_tpe'] = request.POST['article_type']
        publish_on = datetime.datetime.strptime(request.POST['published_on'], '%m/%d/%Y').date()
        data['published_on'] = timezone.now().replace(year=publish_on.year, month=publish_on.month, day=publish_on.day)
        now = timezone.now()
        if form.is_valid():
            savearticleform = form.save(commit=False)
            try:slug = request.POST['slug'].strip()
            except:slug = savearticleform.title
            savearticleform.slug = getUniqueValue(Article,slugify(slug),instance_pk=savearticleform.id)
            savearticleform.is_active = True
            try:
                if not savearticleform.created_by:savearticleform.created_by = request.user
            except:savearticleform.created_by = request.user
            savearticleform.modified_by = request.user

            photo_ids = request.POST.getlist('photo_id',[])
            soup = BeautifulSoup(savearticleform.content)
            for img in soup.findAll("img"):
                try:
                    eimg = Photos.objects.get(photo=img.attrs['src'].split('/site_media/')[-1])
                    photo_ids.append(eimg.id)
                except:pass
            if photo_ids:
                if article and article.album:
                    album = article.album
                else:
                    album = PhotoAlbum()
                    album.created_by = request.user
                    album.category = article_album_cat
                    album.is_editable = False
                    album.status = 'N'
                album.title = savearticleform.title
                album.slug = getUniqueValue(PhotoAlbum, slugify(slug))
                album.seo_title = savearticleform.title[:70],
                album.seo_description = album.summary = savearticleform.summary[:160]
                album.save()

                savearticleform.album = album
                Photos.objects.filter(id__in=photo_ids).update(album=album)


            savearticleform.article_type = request.POST['article_type']
            submit_type = request.POST.get('save_button', 'publish')
            savearticleform.published_on = data['published_on']

            if submit_type == 'publish':
                if now.date() < data['published_on'].date():
                    savearticleform.status = 'S'
                else:
                    savearticleform.status = 'P'
            elif submit_type == 'save':
                if article:
                    if savearticleform.status != 'D':
                        if now.date() < data['published_on'].date():
                            savearticleform.status = 'S'
                        else:
                            if savearticleform.status != 'B':
                                savearticleform.status = 'P'
                else:
                    savearticleform.status = 'D'
                    savearticleform.published_on = None

            savearticleform.seo_title = savearticleform.title
            savearticleform.seo_description = savearticleform.summary

            savearticleform.save()
            if "cover_id" in request.POST:
                crop_and_save_coverphoto(request, cobj=savearticleform)

            savearticleform.tags.clear()
            tags = request.POST['tags'].split(',')
            for tag in tags:
                tag = tag.strip()[:50]
                if tag != '':
                    try:objtag = Tag.objects.get(tag = tag)
                    except:
                        objtag = Tag(tag = tag)
                        objtag.save()
                    savearticleform.tags.add(objtag)

            if not article:
                if article_type=='FR':
                    article_type='Article Own Story'
                    price_flag=pricing.ownstory_is_paid
                    sp_cost=pricing.ownstory_price
                elif article_type=='PR':
                    article_type='Article Pressrelease'
                    price_flag=pricing.pressrelease_is_paid
                    sp_cost=pricing.pressrelease_price
                elif article_type=='A':
                    article_type='Article Advertorial'
                    price_flag=pricing.advertorial_is_paid
                    sp_cost=pricing.advertorial_price
                elif article_type=='RR':
                    article_type='Article Review Request'
                    price_flag=pricing.requestreview_is_paid
                    sp_cost=pricing.requestreview_price
                if price_flag:
                    try:sp_cost=float(request.POST['price'])
                    except:pass
                    save_to_paymentorder(request,savearticleform,article_type,sp_cost)
            signals.celery_update_index.send(sender=None,object=savearticleform)
            if 'aid' in request.REQUEST:
                messages.success(request, str(ARTICLE_MSG['YUS']))
            else:
                messages.success(request, str(ARTICLE_MSG['YAS']))
            return HttpResponseRedirect(reverse('staff_article_home'))
        else:
            data['form'] = form
    else:
        data['form'] = form

    return render_to_response(template,data, context_instance=RequestContext(request))

@csrf_exempt
@staff_member_required
def upload_image_from_editor(request):
    form = UploadEditorImageForm(request.POST, request.FILES)
    try:
        caption = request.POST['caption'] + str(timezone.now())
    except:
        caption = str(timezone.now())
    if form.is_valid():
        photo = form.cleaned_data.get('upload')
    else:
        result = [{'error': form.non_field_errors()}]
        return HttpResponse(simplejson.dumps(result), mimetype='application/javascript')

    photos = Photos()
    photos.photo = photo
    photos.caption=caption
    photos.created_by=request.user
    photos.save()
    return HttpResponse("""
    <script type='text/javascript'>
        window.parent.CKEDITOR.tools.callFunction(%s, '%s');
    </script>""" % (request.GET['CKEditorFuncNum'], photos.photo.url))
    #return HttpResponse(result)
    '''
    result = "{"
    result = result +"status: 'UPLOADED',"
    result = result +"image_url: '"+art_photo+"'"
    result = result +"}"
    return HttpResponse(simplejson.dumps(result), mimetype='application/javascript')
    '''


@login_required
def ajax_upload_photos(request):
    if request.method == "POST":
        gal_id = request.POST.get('gal_id')
        aid = request.GET.get('id')
        if gal_id and gal_id.isdigit():
            album = PhotoAlbum.objects.get(id=gal_id)
        elif aid and aid.isdigit():
            article = Article.objects.get(id=aid)
            album = article.album
        else:
            album = None
        response = upload_photos_forgallery(request,Photos,album,'album')
        return response
    else:
        try:
            article = Article.objects.get(id=request.GET['id'])
            album = article.album
            return upload_photos_forgallery(request,Photos,album,'album')
        except:
            return HttpResponse('No Object')

@staff_member_required
def ajax_get_default_photos(request):
    id=request.GET['ids']
    return get_default_images(request,id,ArticlePhotos)

@login_required
def ajax_delete_photos(request,pk):
    return delete_photos(request,ArticlePhotos,pk)


@staff_member_required
@permission_required('article.change_article',raise_exception=True)
def seo(request,id,template='article/staff/update_seo.html'):
    article = Article.objects.defer('content','summary').get(id = id)
    form=ArticleSeoForm(instance=article)
    if request.POST:
        form=ArticleSeoForm(request.POST,instance=article)
        if form.is_valid():
            #seo=form.save(commit=False)
            #seo.slug=slugify(seo.slug)
            #seo.save()
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(ARTICLE_MSG['ASUS'])}))
        else:
            data={'form':form,'article':article}
            return error_response(request,data,template,ARTICLE_MSG)
    data={'form':form,'article':article}
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
@permission_required('article.publish_article',raise_exception=True)
def change_status(request):
    try:
        article=Article.objects.get(id=int(request.GET['id']))
        status = request.GET['status']
        article.status = status
        if status=='P':
            article.published_on = timezone.now()
        article.save()
        if status=='P':
            try:mail_publish_article(article)
            except:pass

        for log in article.audit_log.all()[:1]:
            log.action_type = status
            log.save()
        '''
        if status == 'P':
            publish_business_mail(business)
        if status == 'R':
            reject_business_mail(business)
        '''
        signals.celery_update_index.send(sender=None,object=article)
        html ='<span title="'+get_status_class(article.status)+'" name="'+article.status+'" id="id_estatus_'+str(article.id)+'" class="inline-block status-idty icon-'+get_status_class(article.status)+'"></span> '
        return HttpResponse(html)
    except:return HttpResponse('0')


@staff_member_required
@permission_required('article.promote_articles',raise_exception=True)
def feature_article_lightbox(request,template='article/staff/feature-article.html'):
    data = {}
    try:
        article=Article.objects.defer('content','summary').get(id=int(request.GET['aid']))
        data['article'] = article
    except:return HttpResponseRedirect(reverse('staff_article_home'))
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
@permission_required('article.promote_articles',raise_exception=True)
def feature_article_image(request):
    try:
        article=Article.objects.defer('content','summary').get(id = int(request.GET['aid']))
        article.featured = True
        article.save()
        ph = Photos.objects.filter(id__in = article.get_photos())
        for photo in ph:
            photo.featured = False
            photo.save()
        featured_obj = Photos.objects.get(id = int(request.GET['pid']))
        featured_obj.featured = True
        featured_obj.save()
        return HttpResponse('1')
    except:return HttpResponse('0')

@staff_member_required
@permission_required('article.promote_articles',raise_exception=True)
def feature_article(request):
    try:
        #article=Article.objects.defer('content','summary').get(id=int(request.GET['id']))
        article=Article.objects.get(id=int(request.GET['id']))
        featured = request.GET['status']
        if featured == 'F':
            article.featured = True
        else:
            article.featured = False
        article.save()
        for log in article.audit_log.all()[:1]:
            log.action_type = featured
            log.save()
        return HttpResponse('1')
    except:return HttpResponse('0')

@staff_member_required
def feature_count(request):
    """
    article_count=Article.objects.filter(featured=True).count()
    f article_count < FEATURE_LIMIT:
        return HttpResponse(1)
    """
    return HttpResponse(1)

@staff_member_required
def article_preview(request,id,template='article/staff/preview.html'):
    data = {}
    try:article=Article.objects.get(id=id)
    except:article = False
    data['article'] = article
    return render_to_response(template,data, context_instance=RequestContext(request))

@staff_member_required
def save_to_paymentorder(request,object,type,price):
    po=PaymentOrder(content_object = object)
    po.invoice_no = get_invoice_num()
    po.payment_mode = 'Offline'
    po.status = 'Success'
    po.amount = price
    po.user = request.user
    po.listing_type = type
    po.object_name=object.get_payment_title()
    po.save()
    return True

# Variables used for CSV
ARTICLE_TYPE_DIST={'FR':'OWNSTORY','PR':'PRESSRELEASE','A':'ADVERTORIAL','RR':'REVIEWREQUEST'}
STATUS_DIST={'P':'PUBLISHED','N':'PENDING','R':'REJECTED','B':'BLOCKED','D':'DRAFTED','S':'SCHEDULED'}
MAX_UPLOAD_FILESIZE = 2097152


@staff_member_required
@permission_required('article.add_article',raise_exception=True)
def articles_import_csv(request):
    if request.method=='POST':
        inputfile = request.FILES['articlescsv']
        if inputfile.size > MAX_UPLOAD_FILESIZE:
            messages.error(request, "The file is too big, please make sure the size of your file is less than or equals 2Mb!")
            return HttpResponseRedirect(reverse('staff_articles_import_csv'))
        else:
            csvfile = CSVfile(
                file=inputfile,
                module='articles',
                status='N',
                uploaded_by=request.user
            )
            csvfile.save()
            process_articles_csv_upload.delay(csvfile)
            older_files = CSVfile.objects.filter(module='articles').order_by('-uploaded_on').values_list('id', flat=True)[5:]
            CSVfile.objects.filter(id__in=older_files).delete()
            messages.success(request, "Your article listings are being added,\nyou will receive notification through email once completed!")
            return HttpResponseRedirect(reverse('staff_article_home'))
    else:
        data = {
            'filehistory': CSVfile.objects.filter(module='articles').order_by('-uploaded_on'),
        }
        return render_to_response('article/staff/import_csv.html', data, context_instance=RequestContext(request))


@staff_member_required
def articles_export_csv(request,template='article/staff/export_csv.html'):
    data = {}
    ''' export users records into csv format '''
    if request.method == "POST":

        try:data['start_date'] = start_date = datetime.datetime.strptime(request.POST['start_date'], "%d/%m/%Y")
        except:data['start_date'] = start_date = False
        try:data['end_date'] = end_date = datetime.datetime.strptime(request.POST['end_date'], "%d/%m/%Y")
        except:data['end_date'] = end_date = False
        data['order'] = order= request.POST.get('order','-id')
        data['ltype'] = ltype=request.POST.getlist('ltype',None)
        data['status'] = status=request.POST.getlist('status',None)
        data['category']=category=request.POST.getlist('category',None)
        key={}
        if start_date and end_date:key['created_on__range']=[start_date,end_date]
        if ltype:key['article_type__in'] = ltype
        if status:key['status__in'] = status
        if category:key['category__id__in'] = category
        if key:articles = Article.objects.filter(**key).order_by(order)
        else:articles = Article.objects.all().order_by(order)
        if articles.count()==0:
            data['categorys'] = ArticleCategory.objects.all().order_by('name')
            data['error_msg'] = _('No records were found for your search. Please try again!')
            return render_to_response (template, data, context_instance=RequestContext(request))
        response = HttpResponse(mimetype='text/csv')
        if start_date and end_date:
            sdate=request.POST['start_date'].replace('/','-')
            edate=request.POST['end_date'].replace('/','-')
            file_name='articles_'+sdate+'_to_'+edate
        else:file_name='articles'
        response['Content-Disposition'] = 'attachment;filename="%s.csv"'%(file_name)
        headers = [
                   'TITLE','CATEGORY','ARTICLE_TYPE','STATUS','SUMMARY','DESCRIPTION','SEO_TITLE','SEO_DESCRIPTION','FEATURED','TAGS',
                   'PUBLISHED_ON'
                   ]
        writer = csv.writer(response)
        writer.writerow(headers)
        for article in articles:
            tags=','.join([tag.tag for tag in article.tags.all() if tag.tag])
            try:article_type=ARTICLE_TYPE_DIST[article.article_type]
            except:article_type=ARTICLE_TYPE_DIST['FR']
            status=STATUS_DIST[article.status]
            seo_title = article.seo_title.encode('utf-8').strip() if article.seo_title else ""
            seo_description = article.seo_description.encode('utf-8').strip() if article.seo_description else ""
            try:
                ART_CATNAME = article.category.name
            except:
                ART_CATNAME = "Uncategorized"
            article_list=[
                article.title.encode('utf-8').strip(),
                ART_CATNAME,
                article_type,
                status,
                article.summary.encode('utf-8').strip(),
                article.content.encode('utf-8').strip(),
                seo_title,
                seo_description,
                article.featured,
                tags,
                article.published_on.strftime('%m/%d/%y') if article.published_on else ""
            ]
            article_list = [smart_unicode(text).encode('utf-8', 'ignore') for text in article_list]
            writer.writerow(article_list)
        return response

    else:
        data['categorys'] = ArticleCategory.objects.all().order_by('name')
        return render_to_response (template, data, context_instance=RequestContext(request))