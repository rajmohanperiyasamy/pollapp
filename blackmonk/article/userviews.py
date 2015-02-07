from bs4 import BeautifulSoup
import datetime
from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Count, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_list_or_404
from django.template import Context, loader, RequestContext
from django.template.defaultfilters import slugify
from django.template.loader import render_to_string
from django.utils import simplejson, timezone
from django.views.decorators.csrf import csrf_exempt
import logging
import os
from random import sample
import random
import re
from time import strptime
import time
import urllib
import urllib2
from xml.dom import minidom

from PIL import Image
from article.forms import ArticleUserForm, UserArticleSeoForm
from article.models import Article, ArticleCategory, Tag, ArticlePrice
from common import signals
from common.fileupload import upload_photos, delete_photos, get_default_images, \
    upload_photos_forgallery, delete_photos
from common.forms import UploadEditorImageForm
from common.getunique import getUniqueValue
from common.mail_utils import mail_publish_article
from common.models import ApprovalSettings, PaymentConfigure
from common.staff_utils import error_response
from common.templatetags.ds_utils import get_msg_class_name, get_status_class
from common.user_messages import ARTICLE_MSG
from common.utils import ds_pagination, get_lat_lng
from common.utilviews import crop_and_save_coverphoto
from gallery.models import PhotoAlbum, PhotoCategory, Photos
from payments.models import PaymentOrder
from payments.utils import get_invoice_num


article_album_cat = PhotoCategory.objects.get_or_create(name="Articles", slug='articles', is_editable=False)[0]
rand = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
NO_OF_ITEMS_PER_PAGE=10
status_dict = {
    'Rejected': 'R',
    'Draft': 'D',
    'Published': 'P',
    'Expired': 'E',
    'Pending': 'N',
    'Blocked': 'B',
    'Scheduled': 'S',
}
@login_required
def dash_board(request,template='article/user/content_manager.html'):
    show = request.GET.get('show', None)
    if show is None:
        articles = Article.objects.defer('content','summary').filter(created_by=request.user).select_related('category','created_by').order_by('-created_on')
    else:
        articles = Article.objects.defer('content','summary').filter(status=status_dict[show], created_by=request.user).select_related('category','created_by').order_by('-created_on')
    article_state = articles.values('status').annotate(s_count=Count('status'))
    
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'S':0}
    for st in article_state:
        STATE[st['status']]+=st['s_count']
        total+=st['s_count']
    
    data = ds_pagination(articles,'1','articles',NO_OF_ITEMS_PER_PAGE)
    data['status']='all'
    data['listing_type']='all'
    data['created']='all'
    data['sort']='-created_on'
    try:data['msg'] =ARTICLE_MSG[request.GET['msg']]
    except:data['msg'] =None
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    data['total'] =total
    data['published'] =STATE['P']
    data['drafted'] =STATE['D']
    data['pending'] =STATE['N']
    data['rejected'] =STATE['R']
    data['blocked'] =STATE['B']
    data['scheduled'] =STATE['S']
    data['search'] =False
    if show is not None:
        data['show'] = status_dict[show]
    return render_to_response(template,data, context_instance=RequestContext(request))

@login_required
def ajax_dash_board(request,template='article/user/ajax_object_listing.html'):
    data=filter_article(request)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    return HttpResponse(simplejson.dumps(send_data))

@login_required
def ajax_article_action(request,template='article/user/ajax_object_listing.html'):
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    action=request.GET['action']
    action_article = Article.objects.filter(id__in=id)
    cls_count=action_article.count()
    
    if action=='DEL':
        for atr_del in action_article:
            signals.create_notification.send(sender=None,user=request.user, obj=atr_del, not_type='deleted from',obj_title=atr_del.title)
            signals.celery_delete_index.send(sender=None,object=atr_del)
            try:atr_del.album.delete()
            except:pass
        action_article.delete()
        msg=str(ARTICLE_MSG['SAD'])
        mtype=get_msg_class_name('s')
    else:pass

    data=filter_article(request)
    
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagination']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['total']:send_data['total']=data['total']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    send_data['msg']=msg
    send_data['mtype']=mtype     
    return HttpResponse(simplejson.dumps(send_data))

def filter_article(request):
    data=key={}
    q=()
    status = request.GET.get('status','all')
    listing_type = request.GET.get('listing','all')
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
   
    key['created_by'] = request.user
    
    if search:
        search_type = request.GET.get('type',None)
        search_keyword = request.GET.get('kwd',"").strip()
        search_category = request.GET.get('cat',None)
        
        if search_category:
            categorys = ArticleCategory.objects.get(id=search_category)
            key['category'] = categorys
        if search_type:
            if search_type=='title':key['title__icontains'] = search_keyword
            elif search_type=='desc':key['summary__icontains'] = search_keyword
            else:key['created_by__display_name__icontains'] = search_keyword
        
        if search_keyword:
            q =(Q(title__icontains=search_keyword)|Q(category__name__icontains=search_keyword)|Q(summary__icontains=search_keyword)|Q(created_by__display_name__icontains=search_keyword))
            articles = Article.objects.defer('content').filter(q,**key).select_related('category','created_by').order_by(sort)
        else:
            articles = Article.objects.defer('content').filter(**key).select_related('category','created_by').order_by(sort)
    else:
        articles = Article.objects.defer('content').filter(**key).select_related('category','created_by').order_by(sort)
    
    data = ds_pagination(articles,page,'articles',item_perpage)
    if search:
        data['search_keyword'] = request.GET.get('kwd',"").strip()
    data['status'] = status
    data['listing_type'] = listing_type
    data['sort']= sort
    data['total'] = Article.objects.filter(created_by=request.user).count()
    data['search']= search
    data['item_perpage']=item_perpage
    return data 


@login_required
def ajax_article_state(request):
    total = 0
    STATE={'D':0,'P':0,'N':0,'R':0,'B':0,'S':0}

    article_state = Article.objects.filter(created_by=request.user).values('status').annotate(s_count=Count('status'))
    for st in article_state:
       STATE[st['status']]+=st['s_count']
       total+=st['s_count']
    data={
          'total':total,
          'published':STATE['P'],
          'pending':STATE['N'],
          'drafted':STATE['D'],
          'rejected':STATE['R'],
          'blocked':STATE['B'],
          'scheduled':STATE['S'],
    }
    return HttpResponse(simplejson.dumps(data))

@login_required
def article_type(request,template='article/user/article_type.html'):
    data = {}
    data['pricing']=ArticlePrice.objects.filter()[:1][0]
    data['payment_settings']=PaymentConfigure.get_payment_settings()
    if request.POST:
        type = request.POST['article_type']
        payment_mode=request.POST.get('payment_mode','offline')
        return HttpResponseRedirect(reverse('article_add_article')+'?a_tpe='+type+'&payment_mode='+payment_mode)
    return render_to_response(template,data, context_instance=RequestContext(request))  

@login_required
def add_article(request,template='article/user/article_form.html'):
    data = {}
    try:
        article = Article.objects.get(id=request.REQUEST['aid'])
        data['article'] = article
        data['article_type'] = article_type = article.article_type
        if request.method =='POST': 
            form = ArticleUserForm(request.POST,instance=article)
            data['slug'] = request.POST['slug'].strip()
            data['article_tags'] = request.POST['tags'].split(',')
        else: 
            form = ArticleUserForm(instance=article)
            data['slug'] = article.slug
            data['article_tags'] = article.tags.all()
    except:
        article = False
        if request.POST: form = ArticleUserForm(request.POST)
        else: form = ArticleUserForm()
        data['article_type'] = article_type = request.REQUEST.get('a_tpe', 'FR')
        data['payment_mode'] = request.REQUEST.get('payment_mode','offline')
    if request.method =='POST':
        data['new_pic'] = request.POST.getlist('new_pic')
        if form.is_valid():
            pricing = ArticlePrice.objects.filter()[:1][0]
            appreoval_settings = ApprovalSettings.objects.get(name='article')
            savearticleform = form.save(commit=False)
            
            slug = request.POST['slug'].strip()
            slug = savearticleform.title
            if article:
                savearticleform.slug = getUniqueValue(Article,slugify(slug),instance_pk=savearticleform.id)
            else:
                savearticleform.slug = getUniqueValue(Article,slugify(slug))
            
            savearticleform.is_active = True
            savearticleform.created_by = savearticleform.modified_by = request.user
            savearticleform.article_type = article_type
            savearticleform.seo_title = savearticleform.title[:70]
            savearticleform.seo_description = savearticleform.summary[:160]
            if not article:
                savearticleform.status = 'N'
                savearticleform.payment_mode=request.REQUEST.get('payment_mode','False')
            
            photo_ids = request.POST.getlist('photo_id', [])
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
            if not article or article.status=='D': 
                submit_type = request.POST.get('save_button')
                if submit_type == 'draft':
                    savearticleform.status = 'D'
                else:
                    if savearticleform.status == 'D' and savearticleform.article_type != 'FR':
                            savearticleform.status = 'D'
                    else:
                        if appreoval_settings.free:
                            savearticleform.status = 'P'
                            if not savearticleform.published_on:
                                savearticleform.published_on = timezone.now()
                        else:
                            savearticleform.status = 'N'
            else:
                if appreoval_settings.free_update and article.status=='P':
                    savearticleform.status='P'
                    savearticleform.published_on = timezone.now()
                else:savearticleform.status='N'

            savearticleform.save()
            if savearticleform.status == 'P':
                try:mail_publish_article(savearticleform)
                except:pass

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
            savearticleform.save()
            if "cover_id" in request.POST:
                crop_and_save_coverphoto(request, cobj=savearticleform)
            paid = False
            if article_type=='FR' and pricing.ownstory_is_paid:paid=True
            elif article_type=='PR' and pricing.pressrelease_is_paid:paid=True
            elif article_type=='A' and pricing.advertorial_is_paid:paid=True
            elif article_type=='RR' and pricing.requestreview_is_paid:paid=True
            if article and article.status!='D':
                if savearticleform.status=='P':
                    if paid:
                        if appreoval_settings.paid_update:
                            savearticleform.status='P'
                            try:mail_publish_article(savearticleform)
                            except:pass
                        else:savearticleform.status='N'
                    else:
                        if appreoval_settings.free_update:
                            savearticleform.status='P'
                            try:mail_publish_article(savearticleform)
                            except:pass
                        else:savearticleform.status='N'
                    signals.create_staffmail.send(sender=None,object=savearticleform,module='articles',action='U',user=request.user)
                savearticleform.save()
                for log in savearticleform.audit_log.all()[:2]:
                    if log.action_type == 'U':
                        log.delete()
                signals.celery_update_index.send(sender=None,object=savearticleform)
                signals.create_notification.send(sender=None,user=request.user, obj=savearticleform, not_type='updated in',obj_title=savearticleform.title)
                messages.success(request, str(ARTICLE_MSG['YUS']))
                return HttpResponseRedirect(reverse('article_dash_board'))
            else:
                if submit_type == 'draft':
                    for log in savearticleform.audit_log.all():
                        if log.action_type == 'U':
                            log.delete()
                    messages.success(request, str(ARTICLE_MSG['YAS']))
                    return HttpResponseRedirect(reverse('article_dash_board'))
                else:
                    if paid:
                        payment_settings=PaymentConfigure.get_payment_settings()
                        if article:
                            payment_mode=article.payment_mode
                        else:
                            payment_mode=request.POST.get('payment_mode','offline')
                        if payment_settings.online_payment and payment_mode=='online':
                            return HttpResponseRedirect(reverse('article_payments_confirm',args=[savearticleform.id]))
                        else:
                            savearticleform.article_type=article_type
                            savearticleform.status = 'D'
                            savearticleform.is_paid=False
                            savearticleform.save()
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
                                save_to_paymentorder(request,savearticleform,article_type,sp_cost)
                            signals.create_notification.send(sender=None,user=request.user, obj=savearticleform, not_type='submitted in',obj_title=savearticleform.title)
                            signals.celery_update_index.send(sender=None,object=savearticleform)
                            signals.create_staffmail.send(sender=None,object=savearticleform,module='articles',action='A',user=request.user)    
                            #messages.success(request, str(ARTICLE_MSG['YAS']))
                            #return HttpResponseRedirect(reverse('article_dash_board'))
                            return HttpResponseRedirect(reverse('article_payments_offline_confirm',args=[savearticleform.id]))
                    else:
                        signals.celery_update_index.send(sender=None,object=savearticleform)
                        signals.create_notification.send(sender=None,user=request.user, obj=savearticleform, not_type='submitted in',obj_title=savearticleform.title)
                        signals.create_staffmail.send(sender=None,object=savearticleform,module='articles',action='A',user=request.user) 
                        messages.success(request, str(ARTICLE_MSG['YAS']))
                        return HttpResponseRedirect(reverse('article_dash_board'))
    data['form'] = form
    data['payment_settings'] = PaymentConfigure.get_payment_settings()
    return render_to_response(template,data, context_instance=RequestContext(request)) 
    
@csrf_exempt
@login_required
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
    photos.caption = caption
    photos.created_by = request.user
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


@login_required
def ajax_get_default_photos(request):  
    id=request.GET['ids']
    return get_default_images(request,id,ArticlePhotos)

@login_required
def seo(request,id,template='usercp_seo_form.html'):
    article = Article.objects.defer('content','summary').get(id = id)
    form=UserArticleSeoForm(instance=article)
    if request.POST:
        form=UserArticleSeoForm(request.POST,instance=article)
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({'status':1,'mtype':get_msg_class_name('s'),'msg':str(ARTICLE_MSG['ASUS'])}))
        else:
            data={'form':form,'article':article}
            return error_response(request,data,template,ARTICLE_MSG)
    data={'form':form,'article':article}
    return render_to_response(template,data, context_instance=RequestContext(request))

@login_required    
def save_to_paymentorder(request,object,type,price):
    po=PaymentOrder(content_object = object)
    po.invoice_no = get_invoice_num()
    po.payment_mode = 'Offline'
    po.status = 'Pending'
    po.amount = price
    po.user = request.user
    po.listing_type = type
    po.object_name=object.get_payment_title()
    po.save()
    return True

@login_required
def article_user_preview(request,id,template='article/user/preview.html'):
    data = {}
    try:article=Article.objects.get(id=id,created_by = request.user)
    except:pass
    data['article'] = article
    return render_to_response(template,data, context_instance=RequestContext(request))    


