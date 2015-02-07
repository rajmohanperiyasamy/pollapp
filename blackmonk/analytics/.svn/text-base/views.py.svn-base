import datetime 
import random

from django.shortcuts import HttpResponse
from django.contrib.sessions.models import Session
from django.core.cache import cache

from common.utils import get_global_settings
from analytics.models import Page,SearchKeyword,Browser,Referral,RealTimeAnalyticsData,PageVisit

BotNames=['Googlebot','Slurp','Twiceler','msnbot','KaloogaBot','YodaoBot','"Baiduspider','googlebot','Speedy Spider','DotBot']
searchkey={"google":"q","yahoo":"p","msn":"q","aol":"query","aol":"encquery","ask":"q","bing":"q"}
searchkey["netscape"]="query"
searchkey["live"]="q"
searchkey["lycos"]="query"
searchkey["altavista"]="q"
searchkey["cnn"]="query"
searchkey["looksmart"]="qt"
searchkey["about"]="terms"
searchkey["mamma"]="query"
searchkey["alltheweb"]="q"
searchkey["gigablast"]="q"
searchkey["voila"]="rdata"
searchkey["virgilio"]="qs"
searchkey["baidu"]="wd"
searchkey["alice"]="qs"
searchkey["yandex"]="text"
searchkey["najdi"]="q"
searchkey["club-internet"]="query"
searchkey["mama"]="query"
searchkey["seznam"]="q"
searchkey["search"]="q"
searchkey["wp"]="szukaj"
searchkey["onet"]="qt"
searchkey["netsprint"]="q"
searchkey["google.interia"]="q"
searchkey["szukacz"]="q"
searchkey["yam"]="k"
searchkey["pchome"]="q"
searchkey["kvasir"]="searchExpr"
searchkey["sesam"]="q"
searchkey["ozu"]="q"
searchkey["terra"]="query"
searchkey["nostrum"]="query"
searchkey["mynet"]="q"
searchkey["ekolay"]="q"
searchkey["search.ilse"]="search_for"


def get_unique_track_id():
    flag=True
    ch=('AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890')
    while flag:
        track_id=''.join(random.choice(ch) for x in range(35))
        try:RealTimeAnalyticsData.objects.get(session_id=track_id)
        except:
            falg=False
            return track_id 

def global_settings():
    if cache.get('global_settings'):
        return cache.get('global_settings')
    else:
        val=get_global_settings()
        cache.set('global_settings',val, 60*60*24)
        return val
    
def anaytics_track(request):
    try:
        user_agent=request.META.get('HTTP_USER_AGENT',None)
        if not user_agent:return HttpResponseForbidden('0')
        for botname in BotNames:
            if botname in user_agent:return HttpResponse('1')
            else:pass
    
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for: ip = x_forwarded_for.split(',')[0]
        else:ip = request.META.get('REMOTE_ADDR')
        
        is_new=request.GET.get('new',None)
        is_unload=request.GET.get('unload',None)
        referral=request.GET.get('referrer','(direct)')
        if referral=='':referral='(direct)'
        browser=request.GET.get('browser','(Unknown)')
        os_type=request.GET.get('os','(Unknown)')
        if os_type=='Mobile':browser=browser+'(Mobile)'
        track_cookie_flag=True
        
        try:session_id=request.COOKIES['bm_analytics_trackid']
        except:
            session_id=get_unique_track_id()
            track_cookie_flag=False
        
        user=request.user.is_authenticated()
        
        try:page=Page.objects.get(page__iexact=request.GET.get('page','/'))
        except:
            page=Page(page=request.GET.get('page','/'))
            page.save()

        if is_unload:
            adata=RealTimeAnalyticsData.objects.get(session_id=session_id,status__in=['A','I'],ip_address=ip)
            adata.out_time=datetime.datetime.now()
            adata.save()
            duration=visit_duration=datetime.timedelta(hours=adata.total_duration.hour, minutes=adata.total_duration.minute, seconds=adata.total_duration.second)
            try:total_duration=duration+datetime.datetime.strptime(str(adata.out_time-adata.in_time), "%H:%M:%S.%f")
            except:total_duration=duration+datetime.datetime.strptime(str(adata.out_time-adata.in_time), "%H:%M:%S")
            adata.total_duration=str(total_duration.hour)+":"+str(total_duration.minute)+":"+str(total_duration.second)
            adata.status='I'
            adata.save()
            
            pvisit=PageVisit.objects.get(real_time_analytics=adata,page=page)
            pvisit.out_time=datetime.datetime.now()
            pvisit.save() 
            duration=visit_duration=datetime.timedelta(hours=pvisit.total_duration.hour, minutes=pvisit.total_duration.minute, seconds=pvisit.total_duration.second)
            try:total_duration=duration+datetime.datetime.strptime(str(pvisit.out_time-pvisit.in_time), "%H:%M:%S.%f")
            except:total_duration=duration+datetime.datetime.strptime(str(pvisit.out_time-pvisit.in_time), "%H:%M:%S")
            pvisit.total_duration=str(total_duration.hour)+":"+str(total_duration.minute)+":"+str(total_duration.second)
            pvisit.save()   
                
            
        else:
            if not is_new:
                try:
                    adata=RealTimeAnalyticsData.objects.get(session_id=session_id,status__in=['A','I'],ip_address=ip)
                    adata.total_visits=adata.total_visits+1
                except:is_new=True
                
            if is_new:
                keyword='(Not set)'
                try:
                    if referral!='(direct)':
                        try:keyword=referral.split(searchkey[key]+'=')[1].split('&')[0]
                        except:keyword=referral.split(searchkey[key]+'=')[1]
                except:keyword='(Not provided)'
                
                try:referral=Referral.objects.get(referral__iexact=referral)
                except:
                    referral=Referral(referral=referral)
                    referral.save()
                    
                try:browser=Browser.objects.get(browser__iexact=browser)
                except:
                    browser=Browser(browser=browser)
                    browser.save()
                    
                try:keyword=SearchKeyword.objects.get(keyword__iexact=keyword)
                except:
                    keyword=SearchKeyword(keyword=keyword)
                    keyword.save()
                    
                RealTimeAnalyticsData.objects.filter(session_id=session_id).update(status='E')
                adata=RealTimeAnalyticsData(session_id=session_id,status='A',ip_address=ip)
                if user:adata.user=request.user
                adata.referral=referral
                adata.browser=browser
                adata.os_type=os_type
                adata.keyword=keyword
                adata.status='A'
                adata.total_duration='00:00:00'#datetime.timedelta(hours=00, minutes=00, seconds=01)
                
            if user and not adata.user:adata.user=request.user  
            adata.status='A'
            adata.in_time=datetime.datetime.now()
            
            adata.out_time=datetime.datetime.now()+datetime.timedelta(seconds=5)
            adata.record_date=datetime.datetime.today()
            
            adata.save()
            #adata.page.add(page)
            
            try:
                pvisit=PageVisit.objects.get(real_time_analytics=adata,page=page)
                pvisit.in_time=datetime.datetime.now()
                pvisit.total_visits=pvisit.total_visits+1
            except:
                pvisit=PageVisit(real_time_analytics=adata,page=page)
                pvisit.total_duration='00:00:00'#datetime.timedelta(hours=00, minutes=00, seconds=01)
            pvisit.save() 
        if not track_cookie_flag:
            response=HttpResponse('1')
            response.set_cookie('bm_analytics_trackid',session_id)
            return response
        return HttpResponse('1')
    except:return HttpResponse('0')
    
    
    
    
    
    



    