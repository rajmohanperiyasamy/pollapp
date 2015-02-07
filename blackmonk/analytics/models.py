from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

class AnalyticsData(models.Model):
    data_date=models.DateField()
    no_visit=models.IntegerField(default=0)
    page_view=models.IntegerField(default=0)
    new_visit=models.IntegerField(default=0)
    visit_duration=models.TimeField(null=True,blank=True)
    created_on = models.DateField(null=True,blank=True)
    
    def __unicode__(self):
        return str(self.data_date)

"""
#################################################################################################################################
"""
class Page(models.Model):
    page = models.CharField(max_length=255)
    def __unicode__(self):
        return self.page

class SearchKeyword(models.Model):
    keyword = models.CharField(max_length=150)
    def __unicode__(self):
        return self.keyword
    
class Browser(models.Model):
    browser = models.CharField(max_length=150)
    def __unicode__(self):
        return self.browser

class Referral(models.Model):
    referral = models.CharField(max_length=150)
    def __unicode__(self):
        return self.referral
"""
#################################################################################################################################
"""
class PageCount(models.Model):
    analytics=models.ForeignKey(AnalyticsData)
    page = models.ForeignKey(Page)
    pcount=models.IntegerField(default=0)
    visit_duration=models.TimeField(null=True,blank=True)
    def __unicode__(self):
        return self.page.page

class SeachKeywordCount(models.Model):
    analytics=models.ForeignKey(AnalyticsData)
    keyword = models.ForeignKey(SearchKeyword)
    kcount=models.IntegerField(default=0)
    def __unicode__(self):
        return self.keyword.keyword
    
class BrowserCount(models.Model):
    analytics=models.ForeignKey(AnalyticsData)
    browser = models.ForeignKey(Browser)
    bcount=models.IntegerField(default=0)
    def __unicode__(self):
        return self.browser.browser

class ReferralCount(models.Model):
    analytics=models.ForeignKey(AnalyticsData)
    referral = models.ForeignKey(Referral)
    rcount=models.IntegerField(default=0)
    def __unicode__(self):
        return self.referral.referral

"""
#################################################################################################################################
"""

class RealTimeAnalyticsData(models.Model):
    session_id=models.CharField(max_length=50)
    ip_address=models.CharField(max_length=20)
    os_type=models.CharField(max_length=20)
    user=models.ForeignKey(User,null=True,blank=True)
    referral = models.ForeignKey(Referral,null=True,blank=True)
    browser = models.ForeignKey(Browser)
    keyword = models.ForeignKey(SearchKeyword,null=True,blank=True)
    #page = models.ManyToManyField(Page)
    status=models.CharField(max_length=1,default='A')
    record_date= models.DateField(auto_now_add=True)
    in_time= models.DateTimeField(auto_now_add=True)
    out_time= models.DateTimeField(auto_now=True)
    total_duration= models.TimeField(null=True,blank=True)
    total_visits=models.IntegerField(default=1)
    
    def __unicode__(self):
        return self.session_id+" - "+self.status
    
class PageVisit(models.Model):
    page = models.ForeignKey(Page)
    real_time_analytics=models.ForeignKey(RealTimeAnalyticsData,related_name="analytics_pagevisits")
    in_time= models.DateTimeField(auto_now_add=True)
    out_time= models.DateTimeField(auto_now=True)
    total_duration= models.TimeField(null=True,blank=True)
    total_visits=models.IntegerField(default=1)
    
    def __unicode__(self):
        return self.page.page
