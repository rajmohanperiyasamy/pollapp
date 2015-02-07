import getsettings

import httplib2
import datetime
from decimal import *
from operator import itemgetter
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

from django.core.cache import cache

from common.models import AvailableApps,CommonConfigure,AnalyticsSettings
from analytics.models import AnalyticsData,Page,SearchKeyword,Browser,Referral,PageCount,SeachKeywordCount,BrowserCount,ReferralCount

def get_analytics_profiles_id():
    if cache.get('GOOGLE_ANALYTICS_PROFILE'):
        return cache.get('GOOGLE_ANALYTICS_PROFILE')
    else:
        val=get_analytics_profiles()
        cache.set('GOOGLE_ANALYTICS_PROFILE',val, 60*60*24*30)
        return val
    
def get_analytics_profiles():
    first_Webproperty_Id=CommonConfigure.objects.all()[0].google_analytics_script
    service = initialize_service()
    accounts = service.management().accounts().list().execute()
    if accounts.get('items'):
        for firstAccountId in accounts.get('items'):
            firstAccountId=firstAccountId.get('id')
            webproperties = service.management().webproperties().list(accountId=firstAccountId).execute()
            if webproperties.get('items'):
              profiles = service.management().profiles().list( accountId=firstAccountId,webPropertyId=first_Webproperty_Id).execute()
              for profile in profiles.get('items', []):
                  web_id=profile.get('webPropertyId')
                  profile_id=profile.get('id')
                  return profile_id


def initialize_service():
    ats=AnalyticsSettings.objects.all()[0]
    f = file(ats.key_file.path, 'rb')
    key = f.read()
    f.close()
    credentials = SignedJwtAssertionCredentials(
        ats.email,
        key,
        scope='https://www.googleapis.com/auth/analytics.readonly',
        access_type='online',
    )
    http = httplib2.Http()
    http = credentials.authorize(http)
    return build('analytics', 'v3', http=http)




def pagePaths(start_date,end_date):
    a=[]
    b=[]
    listing=[]
    metrics = 'ga:pageviews'
    dimensions = 'ga:pagePath'
    range=500000
    service = initialize_service()
    start_date = str(start_date)
    end_date = str(end_date)
    v = end_date.split(" ")
    w = start_date.split(" ")
    start_date =w[0]
    end_date =v[0]
    dataset = service.data().ga().get(ids='ga:' + get_analytics_profiles_id(),start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions,sort='-ga:pageviews' ).execute()
    data_list = dataset['rows'] 
    for row in data_list:
            count = 1
            for vals in row:
                if count == 1:
                    a.append(str(vals))
                else:
                    b.append(int(vals))
                count+=1
    Pages=dict(zip(a,b))
    Pages_path=[]
    Pages_path=sorted(Pages.items(), key=itemgetter(1),reverse=True)
    disabled_apps=AvailableApps.get_inactive_app_slug()
    for app in disabled_apps:
        for tup in Pages_path:
            if tup[0].split('/')[1] == app:Pages_path.remove(tup) 
    Pages_path=Pages_path[0:20]
    a=a[0:20]
    total_views=0
    for m in b:
        total_views=total_views+m
    percentage=[]
    n=0
    for m in b:
        n=float(n)
        n = float(m) / float(total_views)
        n=n*100
        n="%.2f" % n
        percentage.append(n)
    percentage_list = dict(zip(a,percentage)) 
    percentage_list=sorted(percentage_list.items(), key=itemgetter(1),reverse=True)
    return  Pages_path,percentage_list

def browser_views(start_date,end_date):
    a=[]
    b=[]
    start_date=start_date
    end_date=end_date
    pageViews=0
    metrics = 'ga:visits'
    dimensions = 'ga:browser'
    start_date = str(start_date)
    end_date = str(end_date)
    v = end_date.split(" ")
    w = start_date.split(" ")
    start_date =w[0]
    end_date =v[0]
    service = initialize_service()
    dataset = service.data().ga().get(ids='ga:' + get_analytics_profiles_id(),start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions , sort='-ga:visits' ).execute()
    data_list = dataset['rows'] 
    for row in data_list:
            count = 1
            for vals in row:
                if count == 1:
                    a.append(str(vals))
                else:
                    b.append(int(vals))
                count+=1
    browser= dict(zip(a,b))
    for k in browser.values():
        pageViews=k+pageViews 
    browsers_pageviews=[]
    browsers_pageviews=browser.values()
    browsers=sorted(browser.items(), key=itemgetter(1),reverse=True)
    browsers=browsers[0:20]
    a=a[0:20]
    total_views=0
    for m in b:
        total_views=total_views+m
    percentage=[]
    n=0
    for m in b:
        n=float(n)
        n = float(m) / float(total_views)
        n=n*100
        n="%.2f" % n
        percentage.append(n)
    percentage_list = dict(zip(b,percentage)) 
    percentage_list=sorted(percentage_list.items(), key=itemgetter(1),reverse=True)
    return pageViews,browsers,percentage_list

def Source(start_date,end_date):
    a=[]
    b=[]
    metrics = 'ga:visits'
    dimensions = 'ga:source'
    start_date = str(start_date)
    end_date = str(end_date)
    v = end_date.split(" ")
    w = start_date.split(" ")
    start_date =w[0]
    end_date =v[0]
    service = initialize_service()
    dataset = service.data().ga().get(ids='ga:' + get_analytics_profiles_id(),start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions , sort='-ga:visits').execute()
    data_list = dataset['rows'] 
    for row in data_list:
            count = 1
            for vals in row:
                if count == 1:
                    a.append(str(vals))
                else:
                    b.append(int(vals))
                count+=1
    Sources=dict(zip(a,b))
    Referrals=sorted(Sources.items(), key=itemgetter(1),reverse=True)
    Referral=Referrals[0:20]
    a=a[0:20]
    total_visits=0
    for m in b:
        total_visits=total_visits+m
    percentage=[]
    n=0
    for m in b:
        n=float(n)
        n = float(m) / float(total_visits)
        n=n*100
        n="%.2f" % n
        percentage.append(n)
    percentage_list = dict(zip(a,percentage)) 
    percentage_list=sorted(percentage_list.items(), key=itemgetter(1),reverse=True)
    return  Referral,percentage_list



def keywords(start_date,end_date):
    a=[]
    b=[]
    count = 0
    keyview=[]
    all=[]
    metrics = 'ga:pageviews'
    dimensions = 'ga:keyword'
    start_date = str(start_date)
    end_date = str(end_date)
    v = end_date.split(" ")
    w = start_date.split(" ")
    start_date =w[0]
    end_date =v[0]
    service = initialize_service()
    dataset = service.data().ga().get(ids='ga:' + get_analytics_profiles_id(),start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions , sort='-ga:pageviews').execute()
    data_list = dataset['rows'] 
    for row in data_list:
            count = 1
            for vals in row:
                if count == 1:
                    a.append(str(vals))
                else:
                    b.append(int(vals))
                count+=1 
    keywords=dict(zip(a,b))
    top_keywords=sorted(keywords.items(), key=itemgetter(1),reverse=True)
    Searchkeywords=top_keywords[0:20]
    a=a[0:20]
    total_visits=0
    for m in b:
        total_visits=total_visits+m
    percentage=[]
    n=0
    for m in b:
        n=float(n)
        n = float(m) / float(total_visits)
        n=n*100
        n="%.2f" % n
        percentage.append(n)
    percentage_list = dict(zip(a,percentage)) 
    percentage_list=sorted(percentage_list.items(), key=itemgetter(1),reverse=True)
    return  Searchkeywords,percentage_list


def Avg_time(start_date,end_date):
    a=0.0
    b=0
    c=0
    count = 0
    metrics = 'ga:timeOnSite'
    metrics2 = 'ga:visits'
    dimensions = 'ga:browser'
    start_date = str(start_date)
    end_date = str(end_date)
    service = initialize_service()
    dataset = service.data().ga().get(ids='ga:' + get_analytics_profiles_id(),start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions ).execute()
    data_list = dataset['rows']
    
    dataset2 = service.data().ga().get(ids='ga:' + get_analytics_profiles_id(),start_date=start_date,end_date=end_date, metrics = metrics2 ,dimensions = dimensions ).execute()
    data_list2 = dataset2['rows'] 
    
    for row in data_list:
            count = 1
            for vals in row:
                if count == 2:
                    a = a + float(vals)
                count+=1
    for row in data_list2:
            count = 1
            for vals in row:
                if count == 2:
                    b = b + int(vals)
                count+=1
                
    d=0
    try:
        d = a/b
        w = d/60
        a = datetime.timedelta(minutes = w)
        datetime.timedelta(0, c)
    except:pass
    return  a

def visitor_type(start_date,end_date):
    a=[]
    b=[]
    visitors={}
    metrics = 'ga:visits'
    dimensions = 'ga:visitorType'
    start_date = str(start_date)
    end_date = str(end_date)
    service = initialize_service()
    v = end_date.split(" ")
    w = start_date.split(" ")
    start_date =w[0]
    end_date =v[0]
    dataset = service.data().ga().get(ids='ga:' + get_analytics_profiles_id(),start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions ).execute()
    data_list = dataset['rows'] 
    for row in data_list:
            count = 1
            for vals in row:
                if count == 1:
                    a.append(str(vals))
                else:
                    b.append(int(vals))
                count+=1
    visitors= dict(zip(a,b)) 
    total_visitors=0
    for k,v in visitors.items():
        total_visitors=total_visitors+v
    new_visitor=visitors['New Visitor']  
    return_data1= new_visitor
    return_data2= total_visitors
    return return_data1,return_data2

def page_views(start_date,end_date):
    a=[]
    b=[]
    pageViews=0
    metrics = 'ga:pageviews'
    dimensions = 'ga:browser'
    start_date = str(start_date)
    end_date = str(end_date)
    v = end_date.split(" ")
    w = start_date.split(" ")
    start_date =w[0]
    end_date =v[0]
    service = initialize_service()
    dataset = service.data().ga().get(ids='ga:' + get_analytics_profiles_id(),start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions ).execute()
    data_list = dataset['rows'] 
    for row in data_list:
            count = 1
            for vals in row:
                if count == 1:
                    a.append(str(vals))
                else:
                    b.append(int(vals))
                count+=1
    browser= dict(zip(a,b))
    for k in browser.values():
        pageViews=k+pageViews 
    browsers_pageviews=[]
    browsers_pageviews=browser.values()
    browsers=sorted(browser.items(), key=itemgetter(1),reverse=True)
    browsers=browsers[0:20]
    return_data={}
    return_data=pageViews
    return return_data

def country_views(start_date,end_date):
    metrics = 'ga:visitors'
    dimensions = 'ga:country'
    start_date = str(start_date)
    end_date = str(end_date)
    service = initialize_service()
    dataset = service.data().ga().get(ids='ga:' + get_analytics_profiles_id(),start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions ).execute()
    country=[]
    for co in dataset['rows']:country.append({co[0]:co[1]})
    return country


def get_google_analytics_data():
    todays_date=datetime.date.today()
        #i=1
    for i in range(1,61):
        end_date = todays_date-datetime.timedelta(days=i)
        start_date = todays_date-datetime.timedelta(days=i)
        ret=visitor_type(start_date,end_date)
        new_visitor=ret[0]
        visits=ret[1]
        
        #country=country_views(start_date,end_date)
        pageviews=page_views(start_date,end_date)
        average_time_perpage=Avg_time(start_date,end_date)
        pages= pagePaths(start_date,end_date)
        Pages_path = pages[0]
        browse=browser_views(start_date,end_date)
        browsers = browse[1]
        refer = Source(start_date,end_date)
        Referrals = refer[0]
        keyword = keywords(start_date,end_date)
        Searchkeywords = keyword[0]
        
        try:analyticsdata=AnalyticsData.objects.get(data_date=start_date)
        except:analyticsdata=AnalyticsData(data_date=start_date,created_on = todays_date)
        analyticsdata.no_visit=visits
        analyticsdata.page_view=pageviews
        analyticsdata.new_visit=new_visitor
        analyticsdata.visit_duration=average_time_perpage
        analyticsdata.save()
    
        for pages in Pages_path:
            try:page=Page.objects.get(page__iexact=pages[0][:255])
            except:
                page=Page(page=pages[0][:255])
                page.save()
            try:pviews=PageCount.objects.get(page=page,analytics=analyticsdata)
            except:pviews=PageCount(page=page,analytics=analyticsdata)
            pviews.pcount=pages[1]
            pviews.save()
        
        for kwd in Searchkeywords:
            try:keyword=SearchKeyword.objects.get(keyword__iexact=kwd[0][:150])
            except:
                keyword=SearchKeyword(keyword=kwd[0][:150])
                keyword.save()
            try:kviews=SeachKeywordCount.objects.get(keyword=keyword,analytics=analyticsdata)
            except:kviews=SeachKeywordCount(keyword=keyword,analytics=analyticsdata)
            kviews.kcount=kwd[1]
            kviews.save()
            
        for bows in browsers:
            try:bow=Browser.objects.get(browser__iexact=bows[0][:150])
            except:
                bow=Browser(browser=bows[0][:150])
                bow.save()
            try:bviews=BrowserCount.objects.get(browser=bow,analytics=analyticsdata)
            except:bviews=BrowserCount(browser=bow,analytics=analyticsdata)
            bviews.bcount=bows[1]
            bviews.save()
        
        for refs in Referrals:
            try:ref=Referral.objects.get(referrals__iexact=refs[0][:150])
            except:
                ref=Referral(referral=refs[0][:150])
                ref.save()
            try:rviews=ReferralCount.objects.get(referral=ref,analytics=analyticsdata)
            except:rviews=ReferralCount(referral=ref,analytics=analyticsdata)
            rviews.rcount=refs[1]
            rviews.save()
        
        print "Google Analytics Data Updated Successfully.",end_date

get_google_analytics_data()




