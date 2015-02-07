import datetime
import urllib
import oauth2 as oauth
from time import strptime

from django.core.mail import EmailMessage
from django.template import  Template,Context

from common.utils import get_global_settings
from usermgmt.adminviews import  *
from videos.models import *
from common.models import GallerySettings

def vimeo(query,per_page,relevant,page):
    data=[]
    try:
        API_REST_URL = 'http://vimeo.com/api/rest/v2?format=json&method=vimeo.videos.search&per_page='+str(per_page)+'&query='+str(query)+'&sort='+str(relevant)+"&full_response=1&page="+page;
        
        settings=GallerySettings.get_obj()
        key=settings.vimeo_api_key
        secret=settings.vimeo_api_secret
        consumer = oauth.Consumer(key=key,secret=secret)
        client = oauth.Client(consumer)
        resp, content = client.request(API_REST_URL, "GET")
        content=eval(content)
        for v in content['videos']['video']:
            try:
                image_url=v['thumbnails']['thumbnail'][0]['_content'].replace("\\","")#description duration
                data.append({'owner':v['owner'], 'title':v['title'],'upload_date':v['upload_date'],'id':v['id'],'username':v['owner']['display_name'],'image_url':image_url,'no_plays':v['number_of_plays'],'description':v['description'],'duration':v['duration']})
            except: pass
        return data
    except:
        return data

def validate_vimeo(key,secret):
    try:
        print key,secret
        API_REST_URL = 'http://vimeo.com/api/rest/v2?format=json&method=vimeo.videos.search&per_page=1&query=vimeo&sort=relevant';
        consumer = oauth.Consumer(key=key,secret=secret)
        client = oauth.Client(consumer)
        resp, content = client.request(API_REST_URL, "GET")
        content=eval(content)
        try:
            content['err']
            return False
        except:return True
    except:return False

def video_action(selected,ids):
  
        ids=ids.split(',')
        videos = Videos.objects.filter(id__in=ids)
        if selected=='delete':
            videos.delete()
            msg = 'Video(s) Delected Successfully'
        elif selected =='activate':
            videos.update(is_active = True)
            videos.update(status = 'P')
            msg = 'Selected Videos Published '
        elif selected =='deactivate':
            videos.update(is_active = False) 
            videos.update(status = 'N')
            msg = 'Selected videos be in pending '
        elif selected == 'blocked':
            videos.update(status = 'B') #  B indicates that the particular video is blocked    
            msg = 'Selected video(s) are now blocked '
         
        elif selected == 'featured':
            videos.update(featured = True)
            msg = 'Selected Video(s) are now featured '
        return msg        



def publish_Videos_mail(videos):
    global_settings=get_global_settings()
    try:
        to_emailids = [videos.created_by.email]
        email_temp = EmailTemplates.objects.get(code='vpv')
        s = Template(email_temp.subject)
        t= Template(email_temp.template)
        c= Context({ "USERNAME": videos.created_by.display_name,"WEBSITE": global_settings.domain,
                    "ADD_VIDEO_URL":global_settings.website_url+'/videos/addvideo/'})
        email_message=t.render(c)
        subject = s.render(c)
        email= EmailMessage(subject,email_message, my_settings.DEFAULT_FROM_EMAIL,to_emailids)
        email.content_subtype = "html"
        email.send()
    except:
        pass

def set_comment_session(request,comment,v):        
    if v == 'comment':
        flag = 'videocommentlike'
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
        flag = 'videocommentabuse'
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
        
def set_video_session(request,video):
    flag = 'videoview'
    try:
        if request.session['%s%s'%(flag,video.id)] != video.id:
            request.session['%s%s'%(flag,video.id)] = video.id
            video.video_view = video.video_view + 1
            video.save()
            return True
        else:
            return False
    except:
        request.session['%s%s'%(flag,video.id)] = video.id 
        video.video_view = video.video_view + 1
        video.save()
        return True        

def process_cloud_tag(instance):
    ''' distribution algo n tags to b bucket, where b represents
    font size. '''
    entry = instance
    # be sure you save twice the same entry, otherwise it wont update the new tags.
    entry_tag_list = entry.keywords.all()

    for tag in entry_tag_list:
        tag.total_ref = tag.get_videos_count();
        tag.save()
        
        
 