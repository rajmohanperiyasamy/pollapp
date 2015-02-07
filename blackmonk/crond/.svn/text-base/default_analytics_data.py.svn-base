import getsettings
from django.template.loader import get_template 
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.template import Template ,Context
from decimal import *
import datetime
from operator import itemgetter
import time
import httplib2
from domains import *

from common.models import AnalyticDefaultData
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run
from os import listdir
from operator import itemgetter

CLIENT_SECRETS = '../common/client_secrets.json'
MISSING_CLIENT_SECRETS_MESSAGE = '%s is missing' % CLIENT_SECRETS

FLOW = flow_from_clientsecrets(CLIENT_SECRETS,
    scope='https://www.googleapis.com/auth/analytics.readonly',
    message=MISSING_CLIENT_SECRETS_MESSAGE)

# A file to store the access token
TOKEN_FILE_NAME = 'analytics.dat'

def prepare_credentials():
  storage = Storage(TOKEN_FILE_NAME)
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run(FLOW, storage) #run Auth Flow and store credentials

  return credentials

def initialize_service():
  http = httplib2.Http()

  credentials = prepare_credentials()
  http = credentials.authorize(http)  # authorize the http object

  return build('analytics', 'v3', http=http)



def get_first_profile_id(service):
  # Get a list of all Google Analytics accounts for this user
  accounts = service.management().accounts().list().execute()


  if accounts.get('items'):
    # Get the first Google Analytics account
    all = accounts.get('items')
    for al in all:
        a = al.get('id')
        webproperties = service.management().webproperties().list(accountId=a).execute()

        for acc in webproperties.get('items'):
            for k in acc:
                if str(k) == "websiteUrl":
                    if "http://www.onlinecalgary.com" in acc[k]:
                        break
                    break
                break
            break
        firstAccountId = a
        
    # Get a list of all the Web Properties for the first account
    webproperties = service.management().webproperties().list(accountId=firstAccountId).execute()


    if webproperties.get('items'):
      # Get the first Web Property ID
      firstWebpropertyId = webproperties.get('items')[0].get('id')

      # Get a list of all Profiles for the first Web Property of the first Account
      profiles = service.management().profiles().list(
          accountId=firstAccountId,
          webPropertyId=firstWebpropertyId).execute()

      if profiles.get('items'):
        # return the first Profile ID
        return profiles.get('items')[0].get('id')

  return None

GOOGLE_ANALYTICS_PROFILE = get_first_profile_id(initialize_service())


def analytic_default():
        delete_old_data()
        todays_date=datetime.date.today()
        end_date = todays_date-datetime.timedelta(days=1)
        start_date = end_date-datetime.timedelta(days=30)
        ret=visitor_type(start_date,end_date)
        new_visitor=ret[0]
        visits=ret[1]
        pageviews=page_views(start_date,end_date)
        average_time_perpage=Avg_time(start_date,end_date)
        dday_views=Day_data(start_date,end_date)
        daily=dday_views[0]
        day_visits=dday_views[1]
        week_views=week_data(start_date,end_date)
        weekly = week_views[0]
        week_visits=week_views[1]
        month_views=month_data(start_date,end_date)
        monthly=month_views[0]
        month_visits=month_views[1]
        data_analytic=AnalyticDefaultData(total_visits=visits,unique_visits=new_visitor,pageviews=pageviews,avg_visit_time=average_time_perpage,daily_page_views=daily,daily_visits=day_visits,weekly_page_views=weekly,weekly_visits=week_visits,monthly_page_views=monthly,monthly_visits=month_visits)
        data_analytic.save()
        datas = AnalyticDefaultData.objects.all()
        if datas:
            print "successfully saved the data"
        else:
            print "no data"   

def delete_old_data():
    AnalyticDefaultData.objects.all().delete()
    


def Day_data(start_date,end_date):
    days={}
    visits={}
    metrics = 'ga:pageviews'
    metrics_visit='ga:visits'
    dimensions = 'ga:nthDay'
    start_date = str(start_date)
    end_date = str(end_date)
    v = end_date.split(" ")
    w = start_date.split(" ")
    start_date =w[0]
    end_date =v[0]
    a=[]
    b=[]
    w=[]
    x=[]
    u=[]
    v=[]
    #sort=['visits']
    service = initialize_service()
    dataset = service.data().ga().get(ids='ga:' + GOOGLE_ANALYTICS_PROFILE,start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions ).execute()
    dataset2 = service.data().ga().get(ids='ga:' + GOOGLE_ANALYTICS_PROFILE,start_date=start_date,end_date=end_date, metrics = metrics_visit ,dimensions = dimensions ).execute()
    data_list = dataset['rows'] 
    data_list2 = dataset2['rows'] 
    for row in data_list:
            count = 1
            for vals in row:
                if count == 1:
                    a.append(int(vals))
                else:
                    b.append(int(vals))
                count+=1
            
    for row in data_list2:
            count = 1
            for vals in row:
                if count == 1:
                    w.append(int(vals))
                else:
                    x.append(int(vals))
                count+=1
    day_visits=dict(zip(w,x))
    daily= dict(zip(a,b))
    return_data={}       
    return_data1 = daily
    return_data2 = day_visits
    return return_data1,return_data2


def week_data(start_date,end_date):
    weeks={}
    visits={}
    metrics = 'ga:pageviews'
    metrics_visit='ga:visits'
    dimensions = 'ga:nthWeek'
    start_date = str(start_date)
    end_date = str(end_date)
    v = end_date.split(" ")
    w = start_date.split(" ")
    start_date =w[0]
    end_date =v[0]
    a=[]
    b=[]
    w=[]
    x=[]
    service = initialize_service()
    dataset = service.data().ga().get(ids='ga:' + GOOGLE_ANALYTICS_PROFILE,start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions ).execute()
    dataset2 = service.data().ga().get(ids='ga:' + GOOGLE_ANALYTICS_PROFILE,start_date=start_date,end_date=end_date, metrics = metrics_visit ,dimensions = dimensions ).execute()
    data_list = dataset['rows'] 
    data_list2 = dataset2['rows'] 
    for row in data_list:
            count = 1
            for vals in row:
                if count == 1:
                    a.append(int(vals))
                else:
                    b.append(int(vals))
                count+=1
            
    for row in data_list2:
            count = 1
            for vals in row:
                if count == 1:
                    w.append(int(vals))
                else:
                    x.append(int(vals))
                count+=1
    week_visits=dict(zip(w,x))
    weekly= dict(zip(a,b)) 
    return_data={}       
    return_data1= weekly
    return_data2 = week_visits
    return return_data1,return_data2


def month_data(start_date,end_date):
    month={}
    visits={}
    metrics = 'ga:pageviews'
    metrics_visit='ga:visits'
    dimensions = 'ga:nthMonth'
    start_date = str(start_date)
    end_date = str(end_date)
    v = end_date.split(" ")
    w = start_date.split(" ")
    start_date =w[0]
    end_date =v[0]
    a=[]
    b=[]
    w=[]
    x=[]
    service = initialize_service()
    dataset = service.data().ga().get(ids='ga:' + GOOGLE_ANALYTICS_PROFILE,start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions ).execute()
    dataset2 = service.data().ga().get(ids='ga:' + GOOGLE_ANALYTICS_PROFILE,start_date=start_date,end_date=end_date, metrics = metrics_visit ,dimensions = dimensions ).execute()
    data_list = dataset['rows'] 
    data_list2 = dataset2['rows'] 
    for row in data_list:
            count = 1
            for vals in row:
                if count == 1:
                    a.append(int(vals))
                else:
                    b.append(int(vals))
                count+=1
            
    for row in data_list2:
            count = 1
            for vals in row:
                if count == 1:
                    w.append(int(vals))
                else:
                    x.append(int(vals))
                count+=1
    month_visits=dict(zip(w,x))
    monthly= dict(zip(a,b)) 
    return_data={}       
    return_data1 = monthly
    return_data2 = month_visits
    return return_data1,return_data2


def visitor_type(start_date,end_date):
    a=[]
    b=[]
    visitors={}
    metrics = 'ga:visits'
    dimensions = 'ga:visitorType'
    start_date = str(start_date)
    end_date = str(end_date)
    service = initialize_service()
    dataset = service.data().ga().get(ids='ga:' + GOOGLE_ANALYTICS_PROFILE,start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions ).execute()
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
    service = initialize_service()
    dataset = service.data().ga().get(ids='ga:' + GOOGLE_ANALYTICS_PROFILE,start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions ).execute()
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
    dataset = service.data().ga().get(ids='ga:' + GOOGLE_ANALYTICS_PROFILE,start_date=start_date,end_date=end_date, metrics = metrics ,dimensions = dimensions ).execute()
    data_list = dataset['rows']
    
    dataset2 = service.data().ga().get(ids='ga:' + GOOGLE_ANALYTICS_PROFILE,start_date=start_date,end_date=end_date, metrics = metrics2 ,dimensions = dimensions ).execute()
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
    

analytic_default()
