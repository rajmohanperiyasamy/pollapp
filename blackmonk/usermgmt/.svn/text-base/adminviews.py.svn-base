#Python Libs
import datetime,time
from time import strptime
import random
import string
from common.getunique import getUniqueValue
from django.template.defaultfilters import slugify
from random import random,choice
try:
    from hashlib import sha1
except ImportError:
    import sha
import csv
from PIL import Image

#Django Libs and Methods
from django.http import HttpResponseRedirect, HttpResponse ,Http404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import Group,Permission
from django.contrib.auth import get_user_model
User = get_user_model()
from django.db.models import Q
from django.http import HttpResponse
from common.getunique import getUniqueValue
from django.template.defaultfilters import slugify
from django.core.cache import cache
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
from django.conf import settings 
from django.utils import simplejson
from django.utils.translation import ugettext as _
from django.contrib import messages

#Application Libs and Common Methods
from common.templatetags.ds_utils import get_msg_class_name,get_status_class
from common.admin_utils import success_response_create_user,error_response_create_user, get_unique_username
from common.static_msg import ADMIN_MSG
from common.utils import  *

#Module Files(models,forms etc...)
from usermgmt.models import EmailTemplates,Favorite,ProfilePrivacy
from article.models import Article
from events.models import Event
from bookmarks.models import Bookmark
from gallery.models import PhotoAlbum
from videos.models import Videos
from classifieds.models import Classifieds
from community.models import Entry
from business.models import Business
from banners.models import BannerReports, BannerAdvertisements
from usermgmt.decorators import admin_required
from usermgmt.adminforms import CreateUserForm,EditUserForm,CreateStaffForm,UpdateStaffForm,AddRoleForm,PromoteUserForm
from django.contrib.auth import get_user_model
User = get_user_model()

ITEM_PER_PAGE = 12

########################################################################## User Management ################################################################################################

@admin_required
def admin_overviews(request):
    ''' admin overview '''
    return HttpResponseRedirect(reverse('admin_portal'))

@admin_required
def display_users(request , template='admin/usermgmt/display_users.html'):
    ''' display all registered users'''
    profiles = User.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')
    page = int(request.GET.get('page',1)) 
    data=ds_pagination(profiles,page,'profiles',ITEM_PER_PAGE)
    data['sort'] = '-date_joined'
    data['view_by']='all'
    data['search'] = False
    data['count'] = len(profiles) 
    
    try:data['msg'] =ADMIN_MSG[request.GET['msg']]
    except:data['msg'] = False
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype'] =None
    
    try:
        message=request.GET['message']
        data['msg'] = message
    except:pass
    
    return render_to_response (template, data, context_instance=RequestContext(request))

def filter_users(request):
    ''' method for managing users (sort,filter,search etc..) '''
    data=key={}
    q=()
    key['is_staff'] = False
    key['is_superuser'] = False 
    sort = request.GET.get('sort','-date_joined')
    view_by = request.GET.get('view_by','all')
    search = request.GET.get('search',False)
    page = int(request.GET.get('page',1))  
    
    if search:
        search_keyword = request.GET.get('kwd',"").strip()
        if search_keyword:
            q =(Q(profile_slug__icontains=search_keyword)|Q(useremail__icontains=search_keyword)|Q(display_name__icontains=search_keyword)|Q(about__icontains=search_keyword)|Q(city__icontains=search_keyword))
            profiles=User.objects.filter(q,**key).order_by(sort)
        else:
            profiles=User.objects.filter(**key).order_by(sort)
    else:
        profiles=User.objects.filter(**key).order_by(sort)
    
    def filter_by_isactive(profiles, is_active):
        return [u for u in profiles if u.is_active==is_active]
    if view_by !='all':
        profiles = filter_by_isactive(profiles, view_by=='actv')
    data = ds_pagination(profiles,page,'profiles',ITEM_PER_PAGE)
    data['sort'] = sort
    data['search'] = search
    data['view_by'] = view_by
    return data 

@admin_required
def ajax_display_users(request , template='admin/usermgmt/ajax-display-users.html'):
    ''' ajax method for managing users '''
    data=filter_users(request) 
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    '''if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])'''
    return HttpResponse(simplejson.dumps(send_data))

@admin_required
def ajax_change_user_status(request):
    ''' ajax method for changing users status '''
    send_data={}
    try:
        user=User.objects.get(id=int(request.GET['id']))
        if user.is_active:
            user.status = 'B'
            send_data['status_class']='icon-inactive-user' 
            send_data['status_text']='Active'
        else:
            user.status = 'A'  
            send_data['status_class']='icon-active-user'
            send_data['status_text']='Inactive'  
        user.save()
        send_data['success']=True
    except:send_data['success']=False
    return HttpResponse(simplejson.dumps(send_data))

@admin_required
def ajax_deactivate_user_status(request):
    send_data={}
    try:
        user=User.objects.get(id=int(request.GET['id']))
        user.status = 'B'
        send_data['status_class']='icon-inactive-user' 
        send_data['status_text']='Active'
        user.save()
        send_data['success']=True
    except:send_data['success']=False
    return HttpResponse(simplejson.dumps(send_data))
    
@admin_required
def ajax_create_user(request,template='admin/usermgmt/ajax-create-users.html'): 
    ''' ajax method for creating user account ''' 
    try:user = User.objects.get(id=request.REQUEST['uid']) 
    except:user=False
    if not request.POST:
        if user:form = CreateUserForm(instance=user)
        else:form = CreateUserForm()
    else:
        if user:form = CreateUserForm(request.POST,instance=user)
        else:form = CreateUserForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            newuser = User.objects.create_user(display_name=user_form.display_name,useremail=user_form.useremail, password=user_form.password)
            newuser.display_name=user_form.display_name
            newuser.profile_slug = getUniqueValue(User,slugify(newuser.useremail.split("@")[0]),field_name="profile_slug") 
            newuser.save()
            privacy= ProfilePrivacy(profile=newuser)
            privacy.save()
            data = {'form':form}
            append_data={'profile':newuser,'edit_url':reverse('admin_ajax_create_user')}
            append_template='admin/usermgmt/append_user_list.html'
            return success_response_create_user(append_data,append_template,data,template,ADMIN_MSG['UCS'],request)
        else:
            data = {'form':form,'user_obj':user}
            return error_response_create_user(data,template,ADMIN_MSG['OOPS'],request)    
        
    data={'form':form}    
    return render_to_response (template, data, context_instance=RequestContext(request))        

@admin_required
def ajax_update_user(request,template='admin/usermgmt/ajax-update-users.html'):
    ''' ajax method for updating user account '''   
    try:
        user = User.objects.get(id=request.REQUEST['uid']) 
    except:user=False
    if not request.POST:
        form = EditUserForm(instance=user)    
    else:
        form = EditUserForm(request.POST,instance=user)
        if form.is_valid():
            user_form = form.save(commit=False)
            user.display_name = user_form.display_name
            user.useremail = user_form.useremail
            user.save()
            
            data = {'form':form,'user_obj':user}
            append_data={'profile':user}
            append_template='admin/usermgmt/append_user_list.html'
            return success_response_create_user(append_data,append_template,data,template,ADMIN_MSG['UUS'],request)
        else:
            data = {'form':form,'user_obj':user}
            return error_response_create_user(data,template,ADMIN_MSG['OOPS'],request)    
        
    data = {'form':form,'user_obj':user}  
    return render_to_response (template, data, context_instance=RequestContext(request))  

@admin_required
def ajax_delete_type(request,id,template='admin/usermgmt/ajax-delete-deactivate-user.html'):
    try:
        user = User.objects.get(id=id)
    except:
        user=False
    data={} 
    data['user']=user
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def ajax_delete_user(request,template='admin/usermgmt/ajax-delete-users.html'):
    ''' ajax method for deleting user account '''
    try:
        user = User.objects.get(id=request.GET['uid']) 
        uid = request.GET['uid']
        try:all_ids = request.GET['all_ids'].split(',')
        except:all_ids = request.GET['all_ids']
        new_id=[]
        Event.objects.filter(created_by=user).delete()
        Article.objects.filter(created_by=user).delete()
        Bookmark.objects.filter(created_by=user).delete()
        PhotoAlbum.objects.filter(created_by=user).delete()
        Videos.objects.filter(created_by=user).delete()
        Classifieds.objects.filter(created_by=user).delete()
        Entry.objects.filter(created_by=user).delete()
        Business.objects.filter(created_by=user).delete()
        BannerAdvertisements.objects.filter(created_by=user).delete()
        user.delete()
        msg=str(ADMIN_MSG['UDS'])
        mtype=get_msg_class_name('s')
        data=filter_users(request)
        for profile in data['profiles']:new_id.append(int(profile.user().id))
        all_ids.remove(uid)
        
        for ri in all_ids:
            for ni in new_id:
                if int(ni)==int(ri):
                    new_id.remove(int(ri))
                    
        data['new_id']=new_id
        send_data={}
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        if data['search']:send_data['search']=True
        if data['has_next']:send_data['next']=True
        if data['has_previous']:send_data['previous']=True
        if data['count']:send_data['count']=data['count']
        '''if data['from_range'] and data['to_range']:
            send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])'''
        send_data['msg']=msg
        send_data['mtype']=mtype  
        return HttpResponse(simplejson.dumps(send_data)) 
    except:
        import sys
        return HttpResponse(str(sys.exc_info()))

@admin_required
def ajax_promote_user(request,id,template='admin/usermgmt/ajax-promote-user.html'):  
    ''' ajax method for promoting user account '''
    groups = Group.objects.all().order_by('name')
    try:user = User.objects.get(id=id) 
    except:user=False
    if not request.POST:
        if user:form = PromoteUserForm(instance=user)
        else:form = PromoteUserForm()
    else:
        user.is_staff=True
        user.save()
        try:
            group_obj = Group.objects.get(id=request.POST['groups'])
            user.groups.clear()
            user.groups.add(group_obj)
        except:
            pass
        profiles = User.objects.filter(is_staff=False).order_by('-date_joined')
        page = 1 
        
        data=filter_users(request) 
        
        '''
        all_ids = [str(p.user.id) for p in profiles]
        new_id=[]
        for profile in data['profiles']:new_id.append(int(profile.user().id))
        all_ids.remove(id)
        for ri in all_ids:
            for ni in new_id:
                if int(ni)==int(ri):
                    new_id.remove(int(ri))
        data['new_id']=new_id
        '''

        send_data={}
        send_data['html'] = render_to_string('admin/usermgmt/ajax-display-users.html',data,context_instance=RequestContext(request))
        send_data['pagination']=render_to_string('admin/usermgmt/ajax-pagination.html',data,context_instance=RequestContext(request))
        if data['search']: send_data['search']=True
        if data['has_next']: send_data['next']=True
        if data['has_previous']: send_data['previous']=True
        if data['count']: send_data['count']=data['count']
        send_data['sort'] = '-date_joined'
        send_data['total_count'] = len(profiles)
        send_data['msg'] = 'succesfully promoted'
        send_data['mtype'] = get_msg_class_name('s')
        try:
            return HttpResponse(simplejson.dumps(send_data))
        except:
            pass

        
    data={'form':form,'uid':id}    
    return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def get_user_stats(request):
    data = {
        'acive_user_count': User.objects.filter(is_staff=False,status='A',is_superuser=False).count(),
        'inactive_user_count': User.objects.filter(is_staff=False,status='B',is_superuser=False).count(),
        'total_user_count': User.objects.filter(is_staff=False,is_superuser=False).count()
        }
    return HttpResponse(simplejson.dumps(data),mimetype='application/json')

@admin_required
def ajax_users_action(request,template='admin/usermgmt/ajax-delete-users.html'):
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    action_user = User.objects.filter(id__in=id,is_staff=False)
    status=0
    if action=='DEL':
        action_user.delete()
        status=1
        msg=str(ADMIN_MSG['UDS'])
        mtype=get_msg_class_name('s')
    else:
        if action == 'UACTS':action_user.update(status = 'A')
        else:action_user.update(status = 'B')
        status=1
        msg=str(ADMIN_MSG[action])
        mtype=get_msg_class_name('s')
        
    data=filter_users(request)
    
    new_id=[]
    for cs in data['profiles']:new_id.append(int(cs.id))
    for ai in id:all_ids.remove(ai)
    
    for ri in all_ids:
        for ni in new_id:
            if int(ni)==int(ri):
                new_id.remove(int(ri))
    data['new_id']=new_id
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagination']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    send_data['msg']=msg
    send_data['mtype']=mtype    
    send_data['status']=status
    return HttpResponse(simplejson.dumps(send_data))


@admin_required
def ajax_user_profile(request,template='admin/usermgmt/ajax-user-profile.html'):
    try:
        profile = User.objects.get(id=request.GET['uid'])
    except:
        profile = False
    data={'profile':profile}        
    return render_to_response (template, data, context_instance=RequestContext(request))


def get_user_contribution(request):
    ''' get profile contribution count'''
    from business.models import Business
    from article.models import Article
    from events.models import Event
    from community.models import Entry
    from classifieds.models import Classifieds
    from gallery.models import PhotoAlbum
    from videos.models import Videos
    
    try:
        user = User.objects.get(id=request.GET['uid'])
        data = {
            'article': Article.objects.filter(created_by=user,status='P').count(),
            'business': Business.objects.filter(created_by=user,status='P').count(),
            'events': Event.objects.filter(created_by=user,status='P').count(),
            'photos': PhotoAlbum.objects.filter(created_by=user,status='P').count(),
            'videos': Videos.objects.filter(created_by=user,status='P').count(),
            'questions': Entry.objects.filter(created_by=user,entry_type='Q').count(),
            'classifieds': Classifieds.objects.filter(created_by=user,status='P').count(),
            }
        return HttpResponse(simplejson.dumps(data),mimetype='application/json')
    
    except:
        pass

@admin_required
def import_users_csv(request,template='admin/usermgmt/import-users-csv.html'):
    ''' method for importing bulk users via csv file'''
    data = {}
    import csv,itertools, operator
    if request.method == 'POST':
        try:
            total=0
            added=0
            exist = False
            rows = csv.DictReader( request.FILES['userscsv'] )
            CSV_LIST = ['FIRST_NAME','EMAIL','PASSWORD']
            msg = ''
            alertmsg = ''
            val = []
            business_name = ''
            for r in rows:
                total = total+1
                row = {}
                for key in CSV_LIST:
                    try:row[key]=r[key]
                    except:row[key]=None
                       
                #validate the Data
                #############validating First Name,Email,Password compulsary######################
                if not row['FIRST_NAME'] or not row['EMAIL'] or not row['PASSWORD']:
                    if not row['FIRST_NAME']:
                        if 'FIRST_NAME' not in val:
                            val.append('FIRST_NAME')
                        msg=msg+'FIRST_NAME '
                    if not row['EMAIL']:
                        if 'EMAIL' not in val:
                            val.append('EMAIL')
                        msg=msg+'EMAIL'
                    if not row['PASSWORD']:
                        if 'PASSWORD' not in val:
                            val.append('PASSWORD')
                        msg=msg+'PASSWORD '
                        
                    msg=msg+'not found in the row %d\n'%(total)
                    continue
                ################### Checking User is Already or not##########################
                
                try:
                    User.objects.get(useremail=row['EMAIL'])
                    msg = msg+' error found while saving users, %s e-mail is already exists.'%(row['EMAIL'])
                    exist = True
                except:
                    if row['FIRST_NAME'] and row['EMAIL'] and row['PASSWORD']:
                        first_name = row['FIRST_NAME']
                        useremail = row['EMAIL']
                        #profile_slug = useremail.split('@')[0] 
                        #profile_slug = get_unique_username(profile_slug)
                        profile_slug = getUniqueValue(User,slugify(useremail.split("@")[0]),field_name="profile_slug")
                        password = row['PASSWORD']
                        newuser = User.objects.create_user(display_name=first_name, useremail=useremail, password=password)
                        newuser.save()
                        added=added+1
                    else:continue
            
            if val:
                val = ', '.join(val)
                alertmsg = alertmsg+' not found or improper.'
            else:
                val = ""
                
            if total==added:
                messages.success(request, str(ADMIN_MSG['UCS']))
                return HttpResponseRedirect(reverse('admin_display_users'))
            elif exist:
                msg = _('Some of the users cannot be added,it is already exist')
                messages.error(request,msg)
                return HttpResponseRedirect(reverse('admin_display_users'))
            else:
                #msg = _('Out of %(totaluser)s users %(usercount)s user has been added successfully')%{'totaluser':total,'usercount':added}
                alertmsg=alertmsg+'\n%s user(s) added out of %s users successfully'%(added,total)
                messages.info(request,val+alertmsg)
                return HttpResponseRedirect(reverse('admin_display_users'))
        except:
            messages.error(request, str(ADMIN_MSG['OOPS']))
            return HttpResponseRedirect(reverse('admin_display_users'))
    else:
        return render_to_response (template, data, context_instance=RequestContext(request))

@admin_required
def export_users_to_csv(request,template='admin/usermgmt/export-user-csv.html'):
    data = {}
    ''' export users records into csv format '''
    if request.method == "POST":
        
        try:start_date = datetime.datetime.strptime(request.POST['start_date'], "%d/%m/%Y")
        except:start_date = False
        try:end_date = datetime.datetime.strptime(request.POST['end_date'], "%d/%m/%Y")
        except:end_date = False
        
        order = request.POST.get('order','-id')
        data['start_date'] = start_date
        data['end_date'] = end_date
        data['order'] = order
            
        if start_date and end_date:
            users = User.objects.filter(date_joined__range=[start_date,end_date],is_staff=False,is_superuser=False).order_by(order) 
        else:
            users = User.objects.filter(is_staff=False,is_superuser=False).order_by(order)
        
        if users.count()==0:
            data['error_msg'] = _('No records were found for your search. Please try again!')
            return render_to_response (template, data, context_instance=RequestContext(request))
            
        response = HttpResponse(mimetype='text/csv')
        if start_date and end_date:
            sdate=request.POST['start_date'].replace('/','-')
            edate=request.POST['end_date'].replace('/','-')
            file_name='users'+sdate+'_to_'+edate
        else:file_name='users'
        response['Content-Disposition'] = 'attachment;filename="users.csv"'
        headers = ['FIRST_NAME','USERNAME','EMAIL']    
        writer = csv.writer(response)
        writer.writerow(headers) 
         
        for user in users:
                writer.writerow([user.first_name(), user.username(), user.useremail])
        return response
    
    else:
        return render_to_response (template, data, context_instance=RequestContext(request))
        
############################################################################### Staff Management #################################################################################################                

@admin_required
def display_staff(request,template='admin/usermgmt/display-staffs.html'): 
    ''' displays all staff account users '''  
    profiles = User.objects.filter(is_staff=True).order_by('-date_joined')
    page = int(request.GET.get('page',1))  
    
    data=ds_pagination(profiles,page,'profiles',ITEM_PER_PAGE)
    data['view_by']='staff'
    data['search'] =False
    data['groups'] = Group.objects.all().order_by('name')
    try:data['msg'] =ADMIN_MSG[request.GET['msg']]
    except:data['msg'] =False
    try:data['mtype'] =get_msg_class_name(request.GET['mtype'])
    except:data['mtype']=False
    return render_to_response(template,data, context_instance=RequestContext(request))
    
def filter_staffs(request):
    ''' global method for managing staffs (sort,filter,search etc..) '''
    data=key={}
    q=()
    sort='-date_joined'
    view_by = request.GET.get('view_by','staff')
    search = request.GET.get('search',False)
    page = int(request.GET.get('page',1))  
    key['is_staff']=True
    if view_by !='staff':key['groups__id']=view_by
    if search:
        search_keyword = request.GET.get('kwd',"").strip()
        if search_keyword:
            q =(Q(profile_slug__icontains=search_keyword)|Q(useremail__icontains=search_keyword)|Q(display_name__icontains=search_keyword)|Q(about__icontains=search_keyword)|Q(city__icontains=search_keyword)|Q(groups__name__icontains=search_keyword))                                              
            profiles=User.objects.filter(q,**key).order_by(sort)
        else:
            profiles=User.objects.filter(**key).order_by(sort)
    else:
        profiles=User.objects.filter(**key).order_by(sort)
    
    data = ds_pagination(profiles,page,'profiles',ITEM_PER_PAGE)
    data['sort']= sort
    data['search']= search
    data['view_by']= view_by
    data['groups'] = Group.objects.all().order_by('name')
    return data 

@admin_required
def ajax_display_staff(request,template='admin/usermgmt/ajax-display-staffs.html'):
    ''' ajax method for managing staffs ''' 
    data=filter_staffs(request)
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    '''if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])'''
    return HttpResponse(simplejson.dumps(send_data))

@admin_required
def ajax_update_staff_roll(request):
    ''' ajax method for assigning new role to staff or updating existing role ''' 
    data={}
    try:
        user = User.objects.get(id=request.GET['uid'],is_staff=True) 
        try:
            group = Group.objects.get(id=request.GET['roll_id'])
            user.groups.clear()
            user.groups.add(group)
            msg=str(ADMIN_MSG['SRUS'])
            mtype=get_msg_class_name('s')
            data['msg']=msg
            data['mtype']=mtype  
            data['success']=True
        except:data['success']=False
    except:data['success']=False
    return HttpResponse(simplejson.dumps(data))                   

@admin_required
def ajax_create_staff(request,template='admin/usermgmt/ajax-create-staffs.html'):  
    ''' ajax method for creating staff account '''
    groups = Group.objects.all().order_by('name')
    try:user = User.objects.get(id=request.REQUEST['uid']) 
    except:user=False
    if not request.POST:
        if user:form = CreateStaffForm(instance=user)
        else:form = CreateStaffForm()
    else:
        if user:form = CreateStaffForm(request.POST,instance=user)
        else:form = CreateStaffForm(request.POST)
        if form.is_valid():
            user_form = form.save(commit=False)
            newuser = User.objects.create_user(display_name=user_form.display_name,useremail=user_form.useremail, password=user_form.password)
            newuser.profile_slug=getUniqueValue(User,slugify(newuser.useremail.split("@")[0]),field_name="profile_slug")
            newuser.is_staff=True
            newuser.save()
          
            #form.save_m2m()
            try:
                group_obj = Group.objects.get(id=request.POST['groups'])
                newuser.groups.clear()
                newuser.groups.add(group_obj)
            except:
                pass    
                
            data = {'form':form,'user_obj':newuser}
            append_data={'profile':newuser,'groups':groups}
            append_template='admin/usermgmt/append-staff-list.html'
            return success_response_create_user(append_data,append_template,data,template,ADMIN_MSG['SCS'],request)
        else:
            data = {'form':form,'user_obj':user}
            return error_response_create_user(data,template,ADMIN_MSG['OOPS'],request)    
        
    data={'form':form}    
    return render_to_response (template, data, context_instance=RequestContext(request))
    
@admin_required
def ajax_update_staff(request,template='admin/usermgmt/ajax-update-staff.html'):  
    ''' ajax method for updating staff account '''
    groups = Group.objects.all().order_by('name')
    try:
        user = User.objects.get(id=request.REQUEST['uid'],is_staff=True) 
    except:user=False
    if not request.POST:
        form = UpdateStaffForm(instance=user)    
    else:
        form = UpdateStaffForm(request.POST,instance=user)
        if form.is_valid():
            user_form = form.save(commit=False)
            user_form.save()
            try:
                group_obj = Group.objects.get(id=request.POST['groups'])
                user_form.groups.clear()
                user_form.groups.add(group_obj)
            except:pass
            
            data = {'form':form,'user_obj':user}
            append_data={'profile':user,'groups':groups}
            append_template='admin/usermgmt/append-staff-list.html'
            return success_response_create_user(append_data,append_template,data,template,ADMIN_MSG['SUS'],request)
        else:
            data = {'form':form,'user_obj':user}
            return error_response_create_user(data,template,ADMIN_MSG['OOPS'],request)    
        
    data = {'form':form,'user_obj':user,'groups':groups}  
    return render_to_response (template, data, context_instance=RequestContext(request)) 

@admin_required
def ajax_update_staff_rolls_count(request,template='admin/usermgmt/admin-roles-side-nav.html'):
    ''' ajax method displaying/updating number of staffs under a particular group(role)'''
    data={'groups':Group.objects.all().order_by('name')} 
    append_html=render_to_string(template,data,context_instance=RequestContext(request))     
    send_data={'append_html':append_html,'success':True}
    return HttpResponse(simplejson.dumps(send_data))

@admin_required
def ajax_delete_staff(request,template='admin/usermgmt/ajax-delete-staffs.html'):
    ''' ajax method for deleting staff account '''
    try:
        user = User.objects.get(id=request.GET['uid'],is_staff=True) 
        uid = request.GET['uid']
        try:all_ids = request.GET['all_ids'].split(',')
        except:all_ids = request.GET['all_ids']
        new_id=[]
        
        user.delete()
        msg=str(ADMIN_MSG['SDS'])
        mtype=get_msg_class_name('s')
        
        data=filter_staffs(request)
        for profile in data['profiles']:new_id.append(int(profile.id))
        all_ids.remove(uid)
        
        for ri in all_ids:
            for ni in new_id:
                if int(ni)==int(ri):
                    new_id.remove(int(ri))
                    
        data['new_id']=new_id
        send_data={}
        send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
        if data['search']:send_data['search']=True
        if data['has_next']:send_data['next']=True
        if data['has_previous']:send_data['previous']=True
        if data['count']:send_data['count']=data['count']
        '''if data['from_range'] and data['to_range']:
            send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])'''
        send_data['msg']=msg
        send_data['mtype']=mtype  
        return HttpResponse(simplejson.dumps(send_data)) 
    except:
        return HttpResponseRedirect(reverse('admin_display_staff'))
    

######################################################################################### Role Management #################################################################################

modulename = ['Community','Article','Attraction','Business','Bookmarks','Classifieds','Deals','Events','Movies','Photos','Polls','Videos','Channels']
model = [['entry'],['article'],['attraction'],['business'],['bookmark'],['classifieds'],['deal'],['event'],['movies'],['photoalbum'],['poll'],['videos'],['channel']]

def _get_all_roles(request):
    ''' method used for getting all roles and permissions '''
    allmod = []
    i=0
    for x in model:
        perms = Permission.objects.filter(content_type__model__in=x).order_by('id')
        a={'id':i,'mname':modulename[i],'p':perms}
        i = i + 1
        allmod.append(a)
    return allmod


@admin_required
def add_role(request,template='admin/usermgmt/admin-add-roles.html'):
    ''' method for adding/eding group,permissions '''
    data={}
    
    try:
        group_obj = Group.objects.get(id=request.REQUEST['gid'])
        permissions = Permission.objects.filter(group=group_obj)
    except:
        group_obj=False
        permissions=False
    
    data['allmod'] = _get_all_roles(request)
    
    if not request.POST:
        if group_obj:form = AddRoleForm(instance=group_obj)
        else:form=AddRoleForm()
    else:
        if group_obj:form = AddRoleForm(request.POST,instance=group_obj)
        else:form=AddRoleForm(request.POST)
        
        if form.is_valid():
            try:selected_roles = request.POST.getlist('selected_roles')
            except:selected_roles = False
            group = form.save()
            group.permissions.clear()
            if selected_roles:
                for role in selected_roles:
                    p=Permission.objects.get(id=role)
                    group.permissions.add(p)
            if group_obj:msg='RUS'
            else:msg='RAS'   
            messages.success(request, str(ADMIN_MSG[msg]))     
            return HttpResponseRedirect(reverse('admin_display_staff'))
        else:
            data['form'] = form
    data['form'] = form
    data['permissions']=permissions
    data['group_obj'] = group_obj
    return render_to_response (template, data, context_instance=RequestContext(request)) 

@admin_required
def delete_role(request):
    ''' method for deleting group '''
    try:
        group_obj = Group.objects.get(id=request.GET['gid'])
        group_obj.delete()
        messages.success(request, str(ADMIN_MSG['RDS']))  
        return HttpResponseRedirect(reverse('admin_display_staff'))
    except:
        messages.error(request, str(ADMIN_MSG['OOPS']))  
        return HttpResponseRedirect(reverse('admin_display_staff'))
    
@admin_required
def ajax_staff_action(request,template='admin/usermgmt/ajax-delete-staffs.html'):
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    try:all_ids=request.GET['all_ids'].split(',')
    except:all_ids=request.GET['all_ids']
    action=request.GET['action']
    action_user = User.objects.filter(id__in=id,is_staff=True)
    status=0
    
    if action=='DEL':
        action_user.delete()
        status=1
        msg=str(ADMIN_MSG['SDS'])
        mtype=get_msg_class_name('s')
    else:
        if action == 'SACTS':action_user.update(is_active = True)
        else:action_user.update(is_active = False)
        status=1
        msg=str(ADMIN_MSG[action])
        mtype=get_msg_class_name('s')
        
    data = filter_staffs(request)
    
    new_id=[]
    for cs in data['profiles']:new_id.append(int(cs.id))
    for ai in id:all_ids.remove(ai)

    for ri in all_ids:
        for ni in new_id:
            if int(ni)==int(ri):
                new_id.remove(int(ri))
                
    data['new_id']=new_id
    send_data={}
    send_data['html']=render_to_string(template,data,context_instance=RequestContext(request))
    send_data['pagination']=render_to_string('common/pagination_ajax_delete.html',data,context_instance=RequestContext(request))
    if data['search']:send_data['search']=True
    if data['has_next']:send_data['next']=True
    if data['has_previous']:send_data['previous']=True
    if data['count']:send_data['count']=data['count']
    if data['from_range'] and data['to_range']:
        send_data['pagerange']=str(data['from_range'])+' - '+str(data['to_range'])
    send_data['msg']=msg
    send_data['mtype']=mtype    
    send_data['status']=status
    return HttpResponse(simplejson.dumps(send_data))     
    
#############################################################################################      Shaan Code Ends
