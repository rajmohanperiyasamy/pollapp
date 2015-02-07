# Python Libs and methods
from datetime import date

# Django Libs 
from django.http import HttpResponse, HttpResponseRedirect,Http404
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.core.cache import cache
from django.views.decorators.cache import cache_control
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
#Application Libs and Common Methods
from django.conf import settings as my_settings
from django.template.response import TemplateResponse
#Module Files(models,forms etc...)
from common.utils import get_global_settings
from common.user_messages import CONTACT_MSG
from common.models import Contacts
from common.templatetags.ds_utils import get_msg_class_name
from common.staff_messages import ENQUIRY_MSG
import datetime
import urllib
import common
from django.db.models import Count
from common.utils import ds_pagination
import string
ITEM_PER_PAGE = 10

@staff_member_required
def advertisement_listing(request,template_name = "enquiry/staff/advertisement_listing.html"):
    advertisements = Contacts.objects.filter(type = 'A').order_by('-created_on')
    page = int(request.REQUEST.get('page',1))
    data = {}
    data = ds_pagination(advertisements,page,'advertisements',ITEM_PER_PAGE)
    data['filter'] = filter
    data['keyword'] = "Search Advertisement"
    return render_to_response(template_name,data,context_instance=RequestContext(request))

@staff_member_required    
def advertise_sort(request,template_name = "enquiry/staff/advertisement_listing.html"):
    try:
       sorting = request.POST.get("sorting", request.session["filter"])
    except:
       sorting = request.POST.get("sorting","")
       
    if 'all' in sorting:
        advertisements = Contacts.objects.filter(type = 'A')
    else:
        advertisements = Contacts.objects.filter(type = 'A').order_by(sorting)
    page = int(request.REQUEST.get('page',1))
    data = {}
    data = ds_pagination(advertisements,page,'advertisements',ITEM_PER_PAGE)
    data['filter'] = sorting
    data['keyword'] = "Search feedback"
    request.session["filter"] = sorting
    
    return render_to_response(template_name,data,context_instance=RequestContext(request))

@staff_member_required
def advertise_delete(request):
    id = request.GET.get('id',False)
    advertisements = Contacts.objects.get(id = id)
    advertisements.delete()
    status = 0
    messages.success(request, str(ENQUIRY_MSG['EDS']))
    return HttpResponse(status)

@staff_member_required
def searching(request,template_name = "enquiry/staff/advertisement_listing.html" ):
    keyword = request.POST.get('search_keyword','')
    advertisements = Contacts.objects.filter(type = 'A')
    result = []
    if keyword:
        for row in advertisements:
            if keyword in row.name or keyword in row.company:
                result.append(row)
    else:
        result = []
    page = int(request.REQUEST.get('page',1))
    data = {}
    data = ds_pagination(result,page,'advertisements',ITEM_PER_PAGE)
    data['filter'] = 'all'    
    data['keyword'] = keyword
    data['search'] = True
    return render_to_response(template_name,data,context_instance=RequestContext(request))
    
@staff_member_required
def advertisment_details(request,id,template_name = "enquiry/staff/contact_details.html"):
    advertisements = Contacts.objects.get(id = id)
    data = {}
    data['contact'] = advertisements
    return render_to_response(template_name,data,context_instance=RequestContext(request))
           


@staff_member_required
def contacts_listing(request,template_name = "enquiry/staff/contacts_listing.html"):
    try:contacts = Contacts.objects.filter(type = 'C').order_by('-created_on')
    except:contacts = False
    page = int(request.REQUEST.get('page',1))
    data = {}
    data = ds_pagination(contacts,page,'contacts',ITEM_PER_PAGE)
    data['keyword'] = "Search contacts"
    data['filter'] = 'all'
    return render_to_response(template_name,data,context_instance=RequestContext(request))       
        
@staff_member_required
def contacts_sort(request,template_name = "enquiry/staff/contacts_listing.html"):
    try:
        try:
           sorting = request.POST.get("sorting", request.session["filter"])
        except:
           sorting = request.POST.get("sorting","")
        if 'all' in sorting:
            contacts = Contacts.objects.filter(type = 'C')
        else:
            contacts = Contacts.objects.filter(type = 'C').order_by(sorting)
    except:
        contacts = False
    page = int(request.REQUEST.get('page',1))
    data = {}
    data = ds_pagination(contacts,page,'contacts',ITEM_PER_PAGE)
    data['filter'] = sorting
    data['keyword'] = "Search feedback"
    request.session["filter"] = sorting
    return render_to_response(template_name,data,context_instance=RequestContext(request))       
        
@staff_member_required
def contacts_delete(request):
    id = request.GET.get('id',False)
    contacts = Contacts.objects.get(id = id)
    status = contacts.type == "Contact"
    contacts.delete()
    messages.success(request, str(ENQUIRY_MSG['EDS']))
    return HttpResponse(status)

@staff_member_required
def contacts_searching(request,template_name = "enquiry/staff/contacts_listing.html" ):
    keyword = request.POST.get('search_keyword','')
    try:contacts = Contacts.objects.filter(type = 'C')
    except:contacts = False
    result = []
    if contacts:
        if keyword:
            for row in contacts:
                if keyword in row.name or keyword in row.email or keyword in row.subject:
                    result.append(row)
        else:
            result = []
    else:result = []
    page = int(request.REQUEST.get('page',1))
    data = {}
    data = ds_pagination(result,page,'contacts',ITEM_PER_PAGE)
    data['filter'] = 'all'    
    data['keyword'] = keyword
    data['search'] = True
    return render_to_response(template_name,data,context_instance=RequestContext(request))        
    
@staff_member_required
def contacts_details(request,id,template_name = "enquiry/staff/contact_details.html"):
    contacts = Contacts.objects.get(id = id)
    data = {}
    data['contact'] = contacts
    return render_to_response(template_name,data,context_instance=RequestContext(request))       
        
@staff_member_required
def ajax_advertise_action(request):
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    action=request.GET['action']
    action_advertise = advertisements = Contacts.objects.filter(type = 'A', id__in=id)
    status=0
    send_data={}
    if action=='DEL':
        action_advertise.delete()
        status=1
        send_data['status']=1
        send_data['msg']="Advertisements deleted successfully"
        send_data['mtype']=get_msg_class_name('s')
    else:
        send_data['status']=0
        send_data['err']="Oops! Cannot process your request. please try again later"
    return HttpResponse(simplejson.dumps(send_data))

@staff_member_required
def ajax_contacts_action(request):
    try:id=request.GET['ids'].split(',')
    except:id=request.GET['ids']
    action=request.GET['action']
    action_advertise = advertisements = Contacts.objects.filter(type = 'C', id__in=id)
    status=0
    send_data={}
    if action=='DEL':
        action_advertise.delete()
        status=1
        send_data['status']=1
        send_data['msg']="Enquiries deleted successfully"
        send_data['mtype']=get_msg_class_name('s')
    else:
        send_data['status']=0
        send_data['err']="Oops! Cannot process your request. please try again later"
    return HttpResponse(simplejson.dumps(send_data))
