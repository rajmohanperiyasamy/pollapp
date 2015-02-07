import datetime
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView
from operator import itemgetter
import operator

from article.models import Article
from attraction.models import Attraction
from banners.models import BannerAdvertisements
from bookmarks.models import Bookmark
from business.models import Business
from classifieds.models import Classifieds
from common.models import AvailableApps, Notification, CSVfile
from deal.models import Deal
from events.models import Event
from gallery.models import PhotoAlbum
from movies.models import Movies
from videos.models import Videos

from common.utils import ds_pagination
from common.models import ContactEmails
from common.templatetags.ds_utils import get_msg_class_name
from common.staff_messages import ENQUIRY_MSG

User = get_user_model()


@staff_member_required    
def analytic(request):
        return HttpResponse("Got error while fetching data from google analytics,Please try after sometime.")
        


@staff_member_required 
def modules_data(request):
    date_range=False
    try:
        dates=request.GET['date'].split(" - ")
        filter_dates=[]
        for dates_t in dates:
            filter_dates.append(datetime.datetime.strptime(dates_t,'%d %b, %Y'))
        date_range=True
            
    except:
        filter_dates=[]
        date_range=False
        pass
    table=get_apps_table()
    modules=get_apps_dict()
    modules_staff_day=get_apps_dict()
    modules_staff_2day=get_apps_dict()
    modules_staff_week=get_apps_dict()
    modules_staff_month=get_apps_dict()
    modules_staff_year=get_apps_dict()
    modules_staff_date_range=get_apps_dict()
    
    modules_user_day=get_apps_dict()
    modules_user_2day=get_apps_dict()
    modules_user_week=get_apps_dict()
    modules_user_month=get_apps_dict()
    modules_user_year=get_apps_dict()
    modules_user_date_range=get_apps_dict()
    
    if date_range:
        get_custom_date_range_data(modules_user_date_range,modules_staff_date_range,table,filter_dates)
    get_custom_daya_data(modules_user_day,modules_staff_day,table,1)
    get_custom_daya_data(modules_user_2day,modules_staff_2day,table,2)
    get_custom_daya_data(modules_user_week,modules_staff_week,table,7)
    get_custom_daya_data(modules_user_month,modules_staff_month,table,31)
    get_custom_daya_data(modules_user_year,modules_staff_year,table,365)
    return_data={}
    total_modules_datas=total_modules_data()
    return_data['modules_staff_day'] = modules_staff_day
    return_data['modules_staff_2day'] = modules_staff_2day
    return_data['modules_staff_week'] = modules_staff_week
    return_data['modules_staff_month'] = modules_staff_month
    return_data['modules_staff_year'] = modules_staff_year
    return_data['modules_user_day'] = modules_user_day
    return_data['modules_user_2day'] = modules_user_2day
    return_data['modules_user_week'] = modules_user_week
    return_data['modules_user_month'] = modules_user_month
    return_data['modules_user_year'] = modules_user_year
    return_data['total_modules'] = total_modules_datas[0]
    return_data['modules_sequence'] = total_modules_datas[1]
    return_data['percentage_modules'] = total_modules_datas[2]
    return_data['users_module'] = total_modules_datas[7]
    return_data['staff_module'] = total_modules_datas[8]
    return_data['percentage_users'] = total_modules_datas[9]
    return_data['percentage_staff'] = total_modules_datas[10]
    return_data['modules_staff_date_range'] = modules_staff_date_range
    return_data['modules_user_date_range'] = modules_user_date_range
    return_data['filter_dates']=filter_dates
    try:
        return_data['start_date']=filter_dates[0]
        return_data['end_date']=filter_dates[1]
    except:
        return_data['start_date']=False
        return_data['end_date']=False
    return  render_to_response('analytics/dashboard_content.html',return_data, context_instance=RequestContext(request))  
     
def get_apps_table(apps=False):
    if not apps:apps=get_available_apps_list()
    data={}
    if 'events' in apps:
        data['Event']=Event
    if 'article' in apps:
        data['Article']=Article
    if 'gallery' in apps:
        data['Photos']=PhotoAlbum
    if 'videos' in apps:
        data['Videos']=Videos
    if 'movies' in apps:
        data['Movies']=Movies
    if 'classifieds' in apps:
        data['Classifieds']=Classifieds
    if 'deal' in apps:
        data['Deal']=Deal
    if 'business' in apps:
        data['Business']=Business
    if 'attraction' in apps:
        data['Attraction']=Attraction
    return data

def get_available_apps_list():
    return [app.module_name for app in AvailableApps.get_active_apps_module_name()] 

def get_apps_dict(apps=False):
    if not apps:apps=get_available_apps_list()
    data={}
    if 'events' in apps:
        data['Event']=0
    if 'article' in apps:
        data['Article']=0
    if 'gallery' in apps:
        data['Photos']=0
    if 'videos' in apps:
        data['Videos']=0
    if 'movies' in apps:
        data['Movies']=0
    if 'classifieds' in apps:
        data['Classifieds']=0
    if 'deal' in apps:
        data['Deal']=0
    if 'business' in apps:
        data['Business']=0
    if 'attraction' in apps:
        data['Attraction']=0
    return data

def get_custom_daya_data(mod_user,mod_staff,table,list_days):
    todays_date=datetime.datetime.today()
    day= todays_date-datetime.timedelta(days=list_days)
    count=0
    for n,m in table.items():
        value=m.objects.filter(created_on__gt=day,created_on__lt=todays_date,created_by__is_staff=False)
        value=value.count()
        mod_user[n]=value
    count=0
    for n,m in table.items():
        value=m.objects.filter(created_on__gt=day,created_on__lt=todays_date,created_by__is_staff=True)
        value=value.count()
        mod_staff[n]=value

def get_custom_date_range_data(mod_user,mod_staff,table,dates):
    start_date=dates[0]
    end_day= dates[1]
    count=0
    for n,m in table.items():
        value=m.objects.filter(created_on__gt=start_date,created_on__lt=end_day,created_by__is_staff=False)
        value=value.count()
        mod_user[n]=value
    count=0
    for n,m in table.items():
        value=m.objects.filter(created_on__gt=start_date,created_on__lt=end_day,created_by__is_staff=True)
        value=value.count()
        mod_staff[n]=value



def total_modules_data():
    return_data={}
    published,new,blocked,draft,modules,staff_modules,users_modules=get_custom_analtics_data()
    percentage_modules=percentage(modules)
    percentage_users=percentage(users_modules)
    percentage_staff=percentage(staff_modules)
    modules_sequence=['Event','Article','Photos','Videos','Movies','Classifieds','Deal','Business','Attraction']
    modules=sorted(modules.items(), key=itemgetter(1),reverse=True)
    users_modules=sorted(users_modules.items(), key=itemgetter(1),reverse=True)
    staff_modules=sorted(staff_modules.items(), key=itemgetter(1),reverse=True)
    percentage_modules=sorted(percentage_modules.items(), key=itemgetter(1),reverse=True)
    percentage_users=sorted(percentage_users.items(), key=itemgetter(1),reverse=True)
    percentage_staff=sorted(percentage_staff.items(), key=itemgetter(1),reverse=True)
    return modules,modules_sequence,percentage_modules,published,new,blocked,draft,users_modules,staff_modules,percentage_users,percentage_staff

def get_custom_analtics_data():
    apps=get_available_apps_list()
    
    published=get_apps_dict(apps)
    new=get_apps_dict(apps)
    blocked=get_apps_dict(apps)
    draft=get_apps_dict(apps)
    modules=get_apps_dict(apps)
    staff_modules=get_apps_dict(apps)
    users_modules=get_apps_dict(apps)
    
    data=get_apps_table(apps)
    for key in data.keys():
        value=data[key]
        data_a= total_posts_by_staff_and_users(value)
        users= data_a[0]
        staff=data_a[1]
        
        M_user=value.objects.all()
        M_users=M_user.count()
        module= element_status(M_user)
        
        published[key]=module[1]
        new[key]=module[0]
        blocked[key]=module[3]
        draft[key]=module[2]
        modules[key]=M_users
        users_modules[key]=users
        staff_modules[key]=staff
    return published,new,blocked,draft,modules,staff_modules,users_modules

def total_posts_by_staff_and_users(tb_name):
    staff=tb_name.objects.filter(created_by__is_staff=True)
    staff=staff.count()
    users=tb_name.objects.filter(created_by__is_staff=False)
    users=users.count()
    if not staff:
        staff=0
    if not users:
        users=0
    return users,staff

def element_status(modules_data):
    count_p=0
    count_n=0
    count_b=0
    count_d=0
    for m in modules_data:
        if m.status=='P':
            count_p+=1
        if m.status=='B':
            count_b+=1
        if m.status=='N':
            count_n+=1
        if m.status=='D':
            count_d+=1
    return count_n,count_p,count_d,count_b

def percentage(diction):
    count =0
    for m,n in diction.items():
        count=count +n
    a=[]
    b=[]
    for m,n in diction.items():
        z=n*100
        try:
            z=float(z)/float(count)
            z="%.1f" % z
        except:
            z='0.00'
        a.append(m)
        b.append(z)
    percentage_modules=dict(zip(a,b))
    return percentage_modules

def users_info(request):
    todays_date=datetime.datetime.today()
    week_end_date = todays_date-datetime.timedelta(days=7)
    two_week_end_date = todays_date-datetime.timedelta(days=14)
    month_end_date = todays_date-datetime.timedelta(days=31)
    user = User.objects.all()
    week_users=User.objects.filter(date_joined__gt=week_end_date,date_joined__lt=todays_date)
    week_two_users=User.objects.filter(date_joined__gt=two_week_end_date,date_joined__lt=todays_date)
    month_users=User.objects.filter(date_joined__gt=month_end_date,date_joined__lt=todays_date)
    
    popular_modules=get_custom_popular_module()
    
    total=0
    for m in popular_modules.values():
        total=m+total
    percentage_modules=percentage(popular_modules)
    popular_modules=sorted(popular_modules.items(), key=itemgetter(1),reverse=True)
    
    one_month=get_users(month_users,31)
    two_week=get_users(week_two_users,14)
    one_week=get_users(week_users,7)
    dd = DateDict(one_month)
    de=dict(dd)
    week_users=week_users.count()
    week_two_users=week_two_users.count()
    month_users=month_users.count()
    count_a=0
    count=0
    count_b=0
    for m in user:
        if m.is_active==True:
            count_a+=1
        else:
            count_b+=1
    us=user.count()
    return_data={}
    date_list=[]
    today=todays_date-datetime.timedelta(days=1)
    for m in range(10):
        if today>=month_end_date:
            date_list.append(today)
            today=today-datetime.timedelta(days=7)
            count+=1
        else:
            break
    dates_list=[]
    for i in reversed(date_list):
        dates_list.append(i)
    length=733/count
    maxValue_month = max(one_month.iteritems(), key=operator.itemgetter(1))[0]
    maxValue_2week = max(two_week.iteritems(), key=operator.itemgetter(1))[0]
    maxValue_1week = max(one_week.iteritems(), key=operator.itemgetter(1))[0]
    grid_value = one_month[maxValue_month]
    no = grid_value/10
    if no<1:
        grid_numbers = 3
    elif no>6:
        grid_numbers = 6
    else:
        "%.0f" % no
        grid_numbers=no
    one_month_key=sorted(one_month.keys())
    two_week_key=sorted(two_week.keys())
    one_week_key=sorted(one_week.keys())
    return_data['one_month']=one_month
    return_data['two_week']=two_week
    return_data['one_week']=one_week
    return_data['one_month_key']=one_month_key
    return_data['two_week_key']=two_week_key
    return_data['one_week_key']=one_week_key
    return_data['totalusers']=us
    return_data['date_list']=dates_list
    return_data['length']=length
    return_data['blocked_users']=count_b
    return_data['popular_modules']=popular_modules
    return_data['percentage_modules']=percentage_modules
    return_data['grid_numbers']=grid_numbers


    return render_to_response('analytics/dashboard_users_stats.html',return_data, context_instance=RequestContext(request))

def get_custom_popular_module():
    apps=get_available_apps_list()
    data=get_apps_table(apps)
    popular_modules=get_apps_dict(apps)
    for key in data.keys():
        value=data[key]
        module=modules_user(value)
        popular_modules[key]=module
    return popular_modules

def modules_user(table):
    mod=table.objects.order_by('created_by').distinct('created_by')
    mod=mod.count()
    return mod

def get_users(list,rang):
    todays_date=datetime.datetime.today()
    date_dic={}
    for m in range(rang):
        todays_date=todays_date-datetime.timedelta(days=1)
        todays_te=todays_date.date()
        date_dic[todays_te]=0
    for m in list:
        v=m.date_joined
        dates=v.date()
        try:date_dic[dates]+=1
        except:pass
    return date_dic

class DateDict(dict):
    def __init__(self, dd):
        self.sorted_keys = dd.keys()[:]
        self.sorted_keys.sort()
        dict.__init__(self, dd)
    def __iter__(self):
        for key in self.sorted_keys:
            yield key
#render_to_response('analytics/bar.html',{'modules': modules, 'name': "vikrant singh"})


###### Home Page Feature

def feature_test(request,template='general/add-home-feature.html'):
    data = {}
    try:module = request.GET['find']
    except:module = False
    data['module'] = module
    return render_to_response(template,data, context_instance=RequestContext(request))   

def auto_sgt_moduls(request,template='general/ajax-add-feature.html'):
    try:mod = request.GET['md']
    except:mod = False
    main=[]
    return HttpResponse(simplejson.dumps(main))

def dsply_sgstd_module(request,template='general/ajax-add-feature.html'):
    send_data = {'status':0}
    return HttpResponse(simplejson.dumps(send_data))
    
def save_featured_content(request,template='general/manage-home-featured.html'):
    data = {}
    return render_to_response(template,data, context_instance=RequestContext(request))  
        
def ajax_todo_lists(request,template='general/ajax-todo-list.html'):
    data = {}
    total_cnt=0
    apps=get_available_apps_list()
    if 'events' in apps:
        data['event_count'] = Event.objects.filter(status='N').count()
        total_cnt=total_cnt+data['event_count']
    if 'article' in apps:
        data['articles_count'] = articles_count=Article.objects.filter(status='N').count()
        total_cnt=total_cnt+data['articles_count']
    if 'gallery' in apps:
        data['photo_count'] = photos_count = PhotoAlbum.objects.filter(status='N',category__is_editable=True).count()
        total_cnt=total_cnt+data['photo_count']
    if 'videos' in apps:
        data['videos_count'] = videos_count=Videos.objects.filter(status='N').count()
        total_cnt=total_cnt+data['videos_count']
    if 'classifieds' in apps:
        data['classifieds_count'] = classifieds_count=Classifieds.objects.filter(status='N').count()
        total_cnt=total_cnt+data['classifieds_count']
    if 'business' in apps:
        data['business_count'] = business_count=Business.objects.filter(status='N').count()
        total_cnt=total_cnt+data['business_count']
    if 'bookmarks' in apps:
        data['bookmark_count'] =bookmark_count=Bookmark.objects.filter(status='N').count()
        total_cnt=total_cnt+data['bookmark_count']
    if 'banners' in apps:
        data['banner_count'] =banner_count=BannerAdvertisements.objects.filter(status='N').count()
        total_cnt=total_cnt+data['banner_count']
        
    data['cnt'] = total_cnt
    html = render_to_string(template ,data,context_instance=RequestContext(request))      
    send_data = {'status':1,'temp':html,'total_cnt':total_cnt}    
    return HttpResponse(simplejson.dumps(send_data))
    
def ajax_staff_notification(request,template='general/ajax-notification.html'):
    data = {}
    apps=get_available_apps_list()
    notifications = Notification.objects.filter(content_type__app_label__in=apps).order_by('-id')[:20]
    data['nots'] = notifications
    not_count = Notification.objects.filter(is_read = False).count()
    temp = render_to_string(template ,data,context_instance=RequestContext(request))  
    send_data = {'status':1,'temp':temp,'not_cnt':not_count}   
    return HttpResponse(simplejson.dumps(send_data)) 
      
def reset_notification(request):
    try:
        Notification.objects.filter(is_read = False).update(is_read = True)
        return HttpResponse('1')
    except:return HttpResponse('0')


class DeleteCSVfile(DeleteView):
    model = CSVfile
    success_url = "/staff/"
    
    def post(self, *args, **kwargs):
        module = self.get_object().module
        try: self.success_url = reverse('staff_%s_import_csv' % (module))
        except: pass 
        return self.delete(*args, **kwargs)

class PreviewCSVfileLog(DetailView):
    model = CSVfile
    template_name = "common/csvfile_log.html"
    
"""
######################## Enquiry Views ##############################################
"""   
NO_OF_ITEMS_PER_PAGE = 10
@staff_member_required
def ajax_list_enquiry(request,template='common/ajax_enquiry_listing.html'):
    data=filter_enquiry(request)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    else:send_data['count']=0
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    else:send_data['pagerange']='0 - 0'
    send_data['item_perpage']=data['item_perpage']
    return HttpResponse(simplejson.dumps(send_data))

@staff_member_required
def filter_enquiry(request):
    key={}
    args = q=()
    action = request.GET.get('action',False)
    sort = request.GET.get('sort','-created_on')
    ids = request.GET.get('ids',False)
    item_perpage=int(request.GET.get('item_perpage',NO_OF_ITEMS_PER_PAGE))
    page = int(request.GET.get('page',1))  
    contacts_list = ContactEmails.objects.all().order_by(sort)
    
    data = ds_pagination(contacts_list,page,'contacts_list',item_perpage)
    data['item_perpage']=item_perpage
    data['sort']= sort
    return data 

@staff_member_required
def enquiry_action(request,template='common/ajax_enquiry_delete.html'):
    msg=mtype=None
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    contact_objs = ContactEmails.objects.filter(id__in=id)
    status=0
    
    if action=='DEL':
        if request.user.has_perm('contactemails.delete_contactemails'):
            contact_objs.delete()
            status=1
            msg=str(CLASSIFIED_MSG['CDS'])
            mtype=get_msg_class_name('s')
        else:
            msg=str(COMMON['DENIED'])
            mtype=get_msg_class_name('w')
    else:
        contact_objs.update(status=action)
        status=1
        if action == "R":
            msg=str(ENQUIRY_MSG['EMR'])
        else:
            msg=str(ENQUIRY_MSG['EMUR'])
        mtype=get_msg_class_name('s')
    
    data=filter_enquiry(request)
    new_id=[]
    
    for cs in data['contacts_list']:new_id.append(int(cs.id))
    for ai in id:all_ids.remove(ai)

    for ri in all_ids:
        for ni in new_id:
            if int(ni)==int(ri):
                new_id.remove(int(ri))
                
    data['new_id']=new_id
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagenation']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    else:send_data['count']=0
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    else:send_data['pagerange']='0 - 0'
    send_data['msg']=msg
    send_data['mtype']=mtype
    send_data['status']=status
    send_data['item_perpage']=data['item_perpage']   
    return HttpResponse(simplejson.dumps(send_data))
    
@staff_member_required
def enquiry_detail(request,id,template='common/enquiry_detail.html'):
    data={}
    try:
        contact_detail = ContactEmails.objects.get(id=id)
        contact_detail.status = 'R'
        contact_detail.save()
        data['contact_detail'] = contact_detail
    except:pass
    return render_to_response(template,data, context_instance=RequestContext(request))
    
    