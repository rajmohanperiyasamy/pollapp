import getsettings
import datetime

from django.db.models import Sum
from django.db.models import F

from analytics.models import AnalyticsData,PageCount,SeachKeywordCount,BrowserCount,ReferralCount,RealTimeAnalyticsData,PageVisit

def get_analytics_data():
        todays_date=datetime.date.today()
        i=1
    #for i in range(1,61):
        record_date = todays_date-datetime.timedelta(days=i)
        RealTimeAnalyticsData.objects.filter(record_date=record_date).update(status='E')
        rdata=RealTimeAnalyticsData.objects.filter(record_date=record_date)
        new_visit=0
        rdata_count=rdata.count()
        visit_duration=datetime.timedelta(hours=00, minutes=00, seconds=00)
        for rd in rdata:
            if not rd.user:new_visit+=1
            visit_duration=visit_duration+datetime.timedelta(hours=rd.total_duration.hour, minutes=rd.total_duration.minute, seconds=rd.total_duration.second)
        pageviews=rdata.aggregate(Sum('total_visits'))['total_visits__sum']
        
        visit_duration=visit_duration/rdata_count
        try:visit_duration=datetime.datetime.strptime(str(visit_duration), "%H:%M:%S.%f")
        except:visit_duration=datetime.datetime.strptime(str(visit_duration), "%H:%M:%S")
        visit_duration=datetime.timedelta(hours=visit_duration.hour,minutes=visit_duration.minute, seconds=visit_duration.second)
        
        try:analyticsdata=AnalyticsData.objects.get(data_date=record_date)
        except:analyticsdata=AnalyticsData(data_date=record_date,created_on = todays_date)
        
        analyticsdata.no_visit=rdata_count
        analyticsdata.page_view=pageviews
        analyticsdata.new_visit=new_visit
        analyticsdata.visit_duration=visit_duration
        analyticsdata.save()
        
        for pv in PageVisit.objects.filter(real_time_analytics__in=rdata):
            try:pviews=PageCount.objects.get(page=pv.page,analytics=analyticsdata)
            except:pviews=PageCount(page=pv.page,analytics=analyticsdata)
            pviews.pcount=pviews.pcount+pv.total_visits
            pviews.save()
        
        for rd in rdata:
            try:bviews=BrowserCount.objects.get(browser=rd.browser,analytics=analyticsdata)
            except:bviews=BrowserCount(browser=rd.browser,analytics=analyticsdata)
            bviews.bcount=bviews.bcount+1
            bviews.save()
            
            if rd.keyword:
                try:kviews=SeachKeywordCount.objects.get(keyword=rd.keyword,analytics=analyticsdata)
                except:kviews=SeachKeywordCount(keyword=rd.keyword,analytics=analyticsdata)
                kviews.kcount=kviews.kcount+1
                kviews.save()
            
            
            if rd.referral:
                try:rviews=ReferralCount.objects.get(referral=rd.referral,analytics=analyticsdata)
                except:rviews=ReferralCount(referral=rd.referral,analytics=analyticsdata)
                rviews.rcount=rviews.rcount+1
                rviews.save()
        
        print "Analytics Data Updated Successfully.",record_date


def expire_analytics_data():
    rdata=RealTimeAnalyticsData.objects.filter(out_time__gte=F('in_time')+datetime.timedelta(hours=02, minutes=00, seconds=00),status__in=['A','I'])
    for adata in rdata:
        adata.out_time=adata.out_time+datetime.timedelta(hours=00, minutes=10, seconds=00)
        duration=datetime.timedelta(hours=adata.total_duration.hour, minutes=adata.total_duration.minute, seconds=adata.total_duration.second)
        try:total_duration=duration+datetime.datetime.strptime(str(adata.out_time-adata.in_time), "%H:%M:%S.%f")
        except:total_duration=duration+datetime.datetime.strptime(str(adata.out_time-adata.in_time), "%H:%M:%S")
        adata.total_duration=datetime.timedelta(hours=total_duration.hour,minutes=total_duration.minute, seconds=total_duration.second)
        adata.status='E'
        adata.save()
        
    print "Analytics Idle Users Expired Successfully."


get_analytics_data()
expire_analytics_data()

