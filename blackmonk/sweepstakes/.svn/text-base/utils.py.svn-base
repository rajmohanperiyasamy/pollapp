import random
import calendar
import datetime
from dateutil.relativedelta import relativedelta,SU,MO,TU,WE,TH,FR,SA

from sweepstakes.models import Sweepstakes

DATE_DIST={'SU':SU(+1),'MO':MO(+1),'TU':TU(+1),'WE':WE(+1),'TH':TH(+1),'FR':FR(+1),'SA':SA(+1)}

LABLE_DIST={
            "advice":"Ask a Question",
            "articles":"Add an Article",
            "bookmarks":"Add a Bookmark",
            "business":"Add a Listing",
            "classifieds":"Post a Classifed Ad ",
            "deals":"Buy a Deal",
            "discussions":"Add a Topic",
            "events":"Add an Event",
            "photos":"Add a Photo/Gallery",
            "videos":"Add a Video"
            }
EXTRA_LABLE_DIST={
            'advice':'Answer a Question',
            "discussions":"Reply to Topic"
            }

LABLE_DIST_P={
            "advice":"Asking a Question in Advice",
            "articles":"Adding an Article",
            "bookmarks":"Adding a Bookmark",
            "business":"Adding a Listing/Business",
            "classifieds":"Posting a Classifed Ad ",
            "deals":"Buying a Deal",
            "discussions":"Adding a Topic in Discussion",
            "events":"Adding an Event",
            "photos":"Adding a Photo/Gallery",
            "videos":"Adding a Video"
            }
EXTRA_LABLE_DIST_P={
            'advice':'Answering a Question in Advice',
            "discussions":"Replying to Topic in Discussion"
            }

def get_unique(val):
    ch=("1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    flag=True
    while flag:
        uvalue=''.join(random.choice(ch) for x in range(15))
        uvalue=val+uvalue
        if val=="CI":
            try:Sweepstakes.objects.filter(contest_id=uvalue)[0]
            except:
                flag=False
                return uvalue
        else:
            try:Sweepstakes.objects.filter(sweepstakes_id=uvalue)[0]
            except:
                flag=False
                return uvalue

def get_contest_end_date(request,obj):
    if obj.duration=='W':
        date=datetime.datetime.strptime('%d-%d-%d'%(obj.start_date.year,obj.start_date.month,obj.start_date.day+1),'%Y-%m-%d') 
        c_end_date = date+ relativedelta(weekday=DATE_DIST[request.POST['duration_week']])
    elif obj.duration=='M':
        date=obj.start_date
        end_date=int(request.POST['duration_month'])
        
        if end_date <= date.day:month=date.month+1
        else:month=date.month
        ldate=calendar.monthrange(date.year,month)[1]
        if end_date > ldate:
            c_end_date=datetime.datetime.strptime('%d-%d-%d'%(date.year,month,ldate),'%Y-%m-%d')
        else:
            c_end_date=datetime.datetime.strptime('%d-%d-%d'%(date.year,month,end_date),'%Y-%m-%d')
    if obj.duration=='W' or obj.duration=='M':
        if c_end_date > obj.end_date:return obj.end_date
        else:return c_end_date
    else:return obj.end_date 
    
def get_contest_next_end_date(obj):
    if obj.duration=='W':
        date=datetime.datetime.strptime('%d-%d-%d'%(obj.start_date.year,obj.start_date.month,obj.start_date.day+1),'%Y-%m-%d') 
        c_end_date = date+ relativedelta(weekday=DATE_DIST[obj.select_winners_on])
    elif obj.duration=='M':
        date=obj.start_date
        end_date=int(obj.select_winners_on)
        
        if end_date <= date.day:month=date.month+1
        else:month=date.month
        ldate=calendar.monthrange(date.year,month)[1]
        if end_date > ldate:
            c_end_date=datetime.datetime.strptime('%d-%d-%d'%(date.year,month,ldate),'%Y-%m-%d')
        else:
            c_end_date=datetime.datetime.strptime('%d-%d-%d'%(date.year,month,end_date),'%Y-%m-%d')
    if obj.duration=='W' or obj.duration=='M':
        if c_end_date > obj.end_date:return obj.end_date
        else:return c_end_date
    else:return obj.end_date  
             