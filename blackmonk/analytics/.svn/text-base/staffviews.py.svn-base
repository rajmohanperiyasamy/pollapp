#from __future__ import division
import datetime
import time
import calendar
from operator import itemgetter

from django.contrib.admin.views.decorators import staff_member_required
from django.template import Context
from django.template.loader import render_to_string
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Count,Sum
from django.shortcuts import HttpResponse
from django.utils import simplejson
from django.template.loader import render_to_string
#from django.contrib.gis.geoip import GeoIP

from analytics.models import AnalyticsData,PageCount,SeachKeywordCount,BrowserCount,ReferralCount
from analytics.models import Page,SearchKeyword,Browser,Referral,RealTimeAnalyticsData,PageVisit

#geoip_obj = GeoIP()

@staff_member_required    
def analytic(request):
    try:
        dates=request.GET['date'].split(" - ")
        filter_dates=[]
        for dates_t in dates:
            filter_dates.append(datetime.datetime.strptime(dates_t,'%d %b, %Y'))
        alalytics_data=AnalyticsData.objects.filter(data_date__range=filter_dates).order_by('data_date')
        s_sdate,s_edate=filter_dates
    except:
        today=datetime.datetime.today()
        onemonthbefore=today-datetime.timedelta(days=30)
        alalytics_data=AnalyticsData.objects.filter(data_date__range=[onemonthbefore,today]).order_by('data_date')
        s_sdate,s_edate=onemonthbefore,today
    if alalytics_data:
        o_start_date=start_date = alalytics_data[0].data_date
        o_end_date=end_date = alalytics_data.reverse()[0].data_date
        
        date_list=[]
        day_data=[]
        pageviews=visits=new_visit=count=0
        #visit_duration=datetime.datetime.strptime("00:00:00", "%H:%M:%S")
        visit_duration=datetime.timedelta(hours=00, minutes=00, seconds=00)
         ############################### 
        for i,ad in enumerate(alalytics_data):
            
            day_data.append({'date':str(ad.data_date.strftime("%b %d, %Y")),'visit':ad.no_visit,'page':ad.page_view})
            pageviews=pageviews+ad.page_view
            visits=visits+ad.no_visit
            new_visit=new_visit+ad.new_visit
            visit_duration=visit_duration+datetime.timedelta(hours=ad.visit_duration.hour, minutes=ad.visit_duration.minute, seconds=ad.visit_duration.second)
       
        
        if alalytics_data.count()>0:
            visit_duration=visit_duration/alalytics_data.count()
            try:visit_duration=datetime.datetime.strptime(str(visit_duration), "%H:%M:%S.%f")
            except:visit_duration=datetime.datetime.strptime(str(visit_duration), "%H:%M:%S")
            visit_duration=datetime.timedelta(hours=visit_duration.hour,minutes=visit_duration.minute, seconds=visit_duration.second)
        
        ############################### 
        for m in alalytics_data:
            new_date=0
            new_date = o_start_date+datetime.timedelta(days=7)
            o_start_date=new_date
            if new_date >= o_end_date: break
            else:date_list.append(new_date)
            count+=1
        week_lists=date_list
        
        
        if count<=1:
            date_list=[]
            o_start_date=start_date
            date_list.append(o_start_date)
            for m in alalytics_data:
                new_day=0
                new_day=o_start_date+datetime.timedelta(days=1)
                o_start_date=new_day
                if new_day > o_end_date:break
                else:date_list.append(new_day)
        if count>10:
            date_list=[]
            o_start_date=start_date
            date_list.append(o_start_date)
            for m in alalytics_data:
                new_day=0
                new_day=o_start_date+datetime.timedelta(days=31)
                o_start_date=new_day
                if new_day > o_end_date:break
                else:date_list.append(new_day)
    
        temp_start_date=start_date
        week_data=[]
        wi=0
        for i,d in enumerate(week_lists):
            wk_data=AnalyticsData.objects.filter(data_date__range=[temp_start_date,d]).aggregate(Sum('page_view'),Sum('no_visit'))
            week_data.append({'date':str(temp_start_date.strftime("%b %d, %Y"))+" - "+str(d.strftime("%b %d, %Y")),'visit':wk_data['no_visit__sum'],'page':wk_data['page_view__sum']})
            temp_start_date=d+datetime.timedelta(days=1)
            wi=i+1
        if temp_start_date < end_date:
            wk_data=AnalyticsData.objects.filter(data_date__range=[temp_start_date,end_date]).aggregate(Sum('page_view'),Sum('no_visit'))
            week_data.append({'date':str(temp_start_date.strftime("%b %d, %Y"))+" - "+str(end_date.strftime("%b %d, %Y")),'visit':wk_data['no_visit__sum'],'page':wk_data['page_view__sum']})
        ###############################
        temp_month_lists=[]
        month_data=[]
        for m in alalytics_data:
            mdate=m.data_date.strftime("%m %Y")
            if mdate not in temp_month_lists:
                
                temp_month_lists.append(mdate)
                year=int(m.data_date.strftime("%Y"))
                month=int(m.data_date.strftime("%m"))
                day=calendar.monthrange(year,month)[1]
                
                ldate=datetime.datetime.strptime('%d-%d-%d'%(year,month,day),'%Y-%m-%d')
                t_endate=datetime.datetime.strptime('%d-%d-%d'%(end_date.year,end_date.month,end_date.day),'%Y-%m-%d')
                if ldate > t_endate:ldate=t_endate
                mn_data=AnalyticsData.objects.filter(data_date__range=[m.data_date,ldate]).aggregate(Sum('page_view'),Sum('no_visit'))
                month_data.append({'date':str(m.data_date.strftime("%b %d, %Y"))+" - "+str(ldate.strftime("%b %d, %Y")),'visit':mn_data['no_visit__sum'],'page':mn_data['page_view__sum']})
            
        ##############################
        if len(date_list)==0:length=732
        else:length=float(732)/float(len(date_list))
        return_data={
                     'day_data':day_data,
                     'week_data':week_data,
                     'month_data':month_data,
    
                     'start_date': start_date, 
                     'end_date': end_date, 
                     'date_list': date_list,
                     
                     'pageviews': pageviews,
                     'new_visitor': new_visit, 
                     'visits': visits, 
                     'length': length, 
                     'average_time_perpage': visit_duration,
                     }
    else:return_data={'nodata':True,'start_date':s_sdate,'end_date':s_edate}
    return render_to_response('analytics/analytics.html',return_data, context_instance=RequestContext(request))  
   
def analytic_extra(request):
    data={}
    try:
        sdate=datetime.datetime.strptime('%d-%d-%d'%(request.GET['sdate']),'%Y-%m-%d')
        edate=datetime.datetime.strptime('%d-%d-%d'%(request.GET['edate']),'%Y-%m-%d')
    except:
        edate=datetime.datetime.today()
        sdate=edate-datetime.timedelta(days=30)

    sdate=datetime.datetime.strptime(request.GET['sdate'],'%Y-%m-%d')
    edate=datetime.datetime.strptime(request.GET['edate'],'%Y-%m-%d')
    """##################################################################"""
    """##################################################################"""
    pages={}
    pageviews = PageCount.objects.values('page__page').filter(analytics__data_date__range=[sdate,edate]).annotate(c_pages=Sum('pcount')).order_by('-c_pages')
    pagetotal=0
    for p in pageviews:
        pages[p['page__page']]=p['c_pages']
        pagetotal=pagetotal+p['c_pages']
    p_data=sorted(pages.items(), key=itemgetter(1),reverse=True)
    pages_data=[]
    i=1
    for p,v in p_data:
        avg=round(float(v)/float(pagetotal),3)*100
        pages_data.append({'sno':i,'obj':p,'visit':v,'avg':avg})
        i+=1
    pdata={'objects':pages_data,'title':'Pages','objects_count':i}
    data['pages']=render_to_string('analytics/extra.html',pdata, context_instance=RequestContext(request))
    """##################################################################"""
    """##################################################################"""
    keyword={}
    keywordviews = SeachKeywordCount.objects.values('keyword__keyword').filter(analytics__data_date__range=[sdate,edate]).annotate(c_keyword=Sum('kcount')).order_by('-c_keyword')
    keywordtotal=0
    for k in keywordviews:
        keyword[k['keyword__keyword']]=k['c_keyword']
        keywordtotal=keywordtotal+k['c_keyword']
    k_data=sorted(keyword.items(), key=itemgetter(1),reverse=True)
    keyword_data=[]
    i=1
    for k,v in k_data:
        avg=round(float(v)/float(keywordtotal),3)*100
        keyword_data.append({'sno':i,'obj':k,'visit':v,'avg':avg})
        i+=1
    kdata={'objects':keyword_data,'title':'Keywords','objects_count':i}
    data['keyword']=render_to_string('analytics/extra.html',kdata, context_instance=RequestContext(request))
    """##################################################################"""
    """##################################################################"""
    referral={}
    referralviews = ReferralCount.objects.values('referral__referral').filter(analytics__data_date__range=[sdate,edate]).annotate(c_referral=Sum('rcount')).order_by('-c_referral')
    referraltotal=0
    for k in referralviews:
        referral[k['referral__referral']]=k['c_referral']
        referraltotal=referraltotal+k['c_referral']
    k_data=sorted(referral.items(), key=itemgetter(1),reverse=True)
    referral_data=[]
    i=1
    for k,v in k_data:
        avg=round(float(v)/float(referraltotal),3)*100
        referral_data.append({'sno':i,'obj':k,'visit':v,'avg':avg})
        i+=1
    rdata={'objects':referral_data,'title':'Referrals','objects_count':i}
    data['referral']=render_to_string('analytics/extra.html',rdata, context_instance=RequestContext(request))
    """##################################################################"""
    """##################################################################"""
    browser={}
    browserviews = BrowserCount.objects.values('browser__browser').filter(analytics__data_date__range=[sdate,edate]).annotate(c_browser=Sum('bcount')).order_by('-c_browser')
    browsertotal=0
    for k in browserviews:
        browser[k['browser__browser']]=k['c_browser']
        browsertotal=browsertotal+k['c_browser']
    k_data=sorted(browser.items(), key=itemgetter(1),reverse=True)
    browser_data=[]
    i=1
    for k,v in k_data:
        if int(v) > 0:
            avg=round(float(v)/float(browsertotal),3)*100
            browser_data.append({'sno':i,'obj':k,'visit':v,'avg':avg})
            i+=1
    bdata={'objects':browser_data,'title':'Browsers','objects_count':i}
    data['browser']=render_to_string('analytics/extra.html',bdata, context_instance=RequestContext(request))
    """##################################################################"""
    
    return HttpResponse(simplejson.dumps(data))

def get_disc_top(d,total):
    dict=sorted(d.items(), key=itemgetter(1),reverse=True)
    temp_list=[]
    i=1
    for k,v in dict:
        temp_list.append({'sno':i,'obj':k,'visit':v,'avg':round((v/float(total))*100,2)})
        i+=1
    return temp_list


@staff_member_required
def analytic_live(request):
    data={}
    active_pages={}
    top_referrals={}
    top_search_keywords={}
    top_browser={}
    top_countrys={}
    total_visits=unique_visits=loggedin_user=returning_users=0
    active_pages_total=top_referrals_total=top_search_keywords_total=top_browser_total=top_countrys=0
    apages=[]
    treferrals=[]
    tbrowsers=[]
    tkeywods=[]
    
    
    active_users=RealTimeAnalyticsData.objects.prefetch_related('analytics_pagevisits','analytics_pagevisits__page').select_related('referral','keyword','browser').filter(status='A')
    ctime=datetime.datetime.now() - datetime.timedelta(hours=1)
    idle_users=RealTimeAnalyticsData.objects.filter(status='I',out_time__gte=ctime).count()
    for au in active_users:
        total_visits=total_visits+au.total_visits
        unique_visits=unique_visits+1
        if au.user:loggedin_user+=1
        if au.total_visits>1:returning_users+=1
    
        try:
            for pv in au.analytics_pagevisits.all():
                page=pv.page.page
                if page not in active_pages.keys():active_pages[page]=pv.total_visits
                else:active_pages[page]=active_pages[page]+pv.total_visits
                active_pages_total+=pv.total_visits
        except:pass
        
        
        try:
            referral=au.referral.referral
            if referral not in top_referrals.keys():top_referrals[referral]=1
            else:top_referrals[referral]=top_referrals[referral]+1
            top_referrals_total+=1
        except:pass
        
        try:
            keywords=au.keyword.keyword
            if keywords not in top_search_keywords.keys():top_search_keywords[keywords]=1
            else:top_search_keywords[keywords]=top_search_keywords[keywords]+1
            top_search_keywords_total+=1
        except:pass
        
        try:
            browser=au.browser.browser
            if browser not in top_browser.keys():top_browser[browser]=1
            else:top_browser[browser]=top_browser[browser]+1
            top_browser_total+=1
        except:pass
    
    data['total_visits']=total_visits
    data['unique_visits']=unique_visits
    data['loggedin_user']=loggedin_user
    data['returning_users']=returning_users
    data['idle_users']=idle_users
    
    data['active_pages']=get_disc_top(active_pages,active_pages_total)
    data['top_referrals']=get_disc_top(top_referrals,top_referrals_total)
    data['top_search_keywords']=get_disc_top(top_search_keywords,top_search_keywords_total)
    data['top_browser']=get_disc_top(top_browser,top_browser_total)
    #data['top_countrys']=top_countrys
    
    return render_to_response('analytics/analytics_live.html',data, context_instance=RequestContext(request))  


