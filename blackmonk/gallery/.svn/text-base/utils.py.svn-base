from gallery.models import *
from article.models import Article
from events.models import Event
import datetime
from time import strptime
from django.conf import settings as my_settings

from django.core.mail import EmailMessage
from common.utils import get_global_settings
from django.template import  Template,Context
#from usermgmt.adminviews import  *
from gallery.models import Tag as GalleryTag

def save_gallery_tags(gallery,tags):
    try:tags=tags.split(',')
    except:tags=tags
    gallery.tags.clear()
    for tag in tags:
        tag = tag.strip()[:150]
        try:t = GalleryTag.objects.get(tag__iexact=tag)
        except:
            t = GalleryTag(tag=tag)
            t.save()
        gallery.tags.add(t)
        

def publish_gallery_mail(gallery):
    try:
        global_settings=get_global_settings()
        to_emailids = [gallery.created_by.email]
        email_temp = EmailTemplates.objects.get(code='gpg')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": gallery.created_by.display_name,"GALLERY_NAME": gallery.title,"GALLERY_URL": gallery.get_album_url(),
                    "WEBSITE": global_settings.domain,"ADD_GALLERY_URL":global_settings.website_url+'/gallery/a/addgallery/'})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass  
def reject_gallery_mail(gallery):
    try:
        global_settings=get_global_settings()
        to_emailids = [gallery.created_by.email]
        email_temp = EmailTemplates.objects.get(code='grg')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": gallery.created_by.display_name,"GALLERY_NAME": gallery.title,"GALLERY_URL": gallery.get_album_url(),
                    "WEBSITE": global_settings.domain,"ADD_GALLERY_URL":global_settings.website_url+'/gallery/a/addgallery/'})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass          


def get_albumid_and_imageid(url):
    try:
        url_l = url.split('/')
        allk=url_l[len(url_l)-1]
    except:
        return False
    try:
        allk_l = allk.split('#')
        akey = allk_l[0].split('_')
        pkey = allk_l[1].split('_')
        return akey + pkey
    except:
        allk_l = allk.split('-')
        pkey = allk_l[0].split('_')
        akey = [False,False]
        return akey + pkey

def get_imageid(url):
    try:
        url_l = url.split('/')
        allk=url_l[len(url_l)-1]
        allk_l = allk.split('-')
        id_key = allk_l[0].split('_')
        return id_key 
    except:
        return False



def add_photo_to_movie(photo_id,photo_key,movieObject,request):
    import datetime
    from common.getunique import getUniqueValue
    from django.template.defaultfilters import slugify
    catid = 6
    try:
        category = PhotoCategory.objects.get(id=catid)
    except:
        category = PhotoCategory.objects.get(name='Movies')
    try:
        album = PhotoAlbum.objects.get(id=aid)
    except:
        title = movieObject.title
        album = PhotoAlbum(category=category,title=title,caption=title,is_active=False,created_by=request.user,modified_by=request.user)
        album.seo_title = title
        album.seo_description = movieObject.synopsis[:350]
        album.slug = getUniqueValue(PhotoAlbum,slugify(title))
        album.save()
    photo = Photos(created_by=request.user,modified_by=request.user)
    photo.is_active=True
    photo.title=album.title
    photo.photo_id = photo_id
    photo.published_on = datetime.datetime.now()
    photo.album=album
    photo.photo_key = photo_key
    photo.save()
    return album.id

def save_tags_article_event(gallery, tags, related_article, related_event):
    #from article.utils import from_articleurl_to_object
    from events.utils import from_eventurl_to_object
    gallery.tags.clear()
    for tag in tags:
        try:
            t = Tag.objects.get(tag=tag)
        except:
            t = Tag(tag=tag)
            t.save()
        gallery.tags.add(t)
    gallery.related_articles.clear()
    for article in related_article:
        article = from_articleurl_to_object(article)
        if article:
            gallery.related_articles.add(article)
    gallery.related_events.clear()
    for event in related_event:
        event = from_eventurl_to_object(event)
        if event:
            gallery.related_events.add(event)
    return True

def from_galleryurl_to_object(galleryurl):
    try:
        slug = galleryurl.split('/gallery/photos/')[1].split('.html')[0]
        return PhotoAlbum.objects.get(slug=slug)
    except:
        return False



def set_album_session(request,album,v):
    if v == 'album':
        flag = 'galbumview'
        try:
            if request.session['%s%s'%(flag,album.id)] != album.id:
                request.session['%s%s'%(flag,album.id)] = album.id
                album.most_viewed = album.most_viewed + 1
                album.save()
                return True
            else:
                return False
        except:
            request.session['%s%s'%(flag,album.id)] = album.id 
            album.most_viewed = album.most_viewed + 1
            album.save()
            return True
    elif v == 'like':
        flag = 'galbumlike'
        try:
            if request.session['%s%s'%(flag,album.id)] != album.id:
                request.session['%s%s'%(flag,album.id)] = album.id
                album.like_count = album.like_count + 1
                album.save()
                return True
            else:
                return False
        except:
            request.session['%s%s'%(flag,album.id)] = album.id 
            album.like_count = album.like_count + 1
            album.save()
            return True
    
def set_comment_session(request,comment,v):        
    if v == 'comment':
        flag = 'galbumcommentlike'
        try:
            if request.session['%s%s'%(flag,comment.id)] != comment.id:
                request.session['%s%s'%(flag,comment.id)] = comment.id
                comment.like_count = comment.like_count + 1
                comment.save()
                return True
            else:
                return False
        except:
            request.session['%s%s'%(flag,comment.id)] = comment.id 
            comment.like_count = comment.like_count + 1
            comment.save()
            return True
    elif v == 'abuse':
        flag = 'galbumcommentabuse'
        try:
            if request.session['%s%s'%(flag,comment.id)] != comment.id:
                request.session['%s%s'%(flag,comment.id)] = comment.id
                comment.abuse_count = comment.abuse_count + 1
                comment.save()
                return True
            else:
                return False
        except:
            request.session['%s%s'%(flag,comment.id)] = comment.id 
            comment.abuse_count = comment.abuse_count + 1
            comment.save()
            return True

def process_cloud_tag(instance):
    ''' distribution algo n tags to b bucket, where b represents
    font size. '''
    entry = instance
    # be sure you save twice the same entry, otherwise it wont update the new tags.
    entry_tag_list = entry.tags.all()

    for tag in entry_tag_list:
        tag.total_ref = tag.get_album_count();
        tag.save()

    