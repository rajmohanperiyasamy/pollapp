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

#Application Libs and Common Methods
from django.conf import settings as my_settings
from django.template.response import TemplateResponse
#Module Files(models,forms etc...)
from common.utils import get_global_settings
from common.user_messages import CONTACT_MSG
from common.models import Feedback
import datetime
import urllib
import common
from django.db.models import Count
from common.utils import ds_pagination
import string
ITEM_PER_PAGE = 10


def feedback_listing(request,template_name = "enquiry/staff/feedback_listing.html"):
    try:feedbacks = Feedback.objects.all()
    except:feedbacks = False
    page = int(request.REQUEST.get('page',1))
    data = {}
    data = ds_pagination(feedbacks,page,'feedbacks',ITEM_PER_PAGE)
    data['keyword'] = "Search feedback"
    data['filter'] = 'all'
    return render_to_response(template_name,data,context_instance=RequestContext(request))

    
def feedback_sort(request,template_name = "enquiry/staff/feedback_listing.html"):
    sorting = request.POST.get("sorting", "")
    type = request.POST.get("type", "")
    try:
	    if 'all' in sorting and 'all' in type:
	        feedbacks = Feedback.objects.all()
	    elif 'all' in sorting and 'all' not in type:
	        feedbacks = Feedback.objects.filter(type = type)
	    elif 'all' not in sorting and 'all' in type:
	        feedbacks = Feedback.objects.all().order_by(sorting)
	    else:
	        feedbacks = Feedback.objects.filter(type = type).order_by(sorting)
    except:
        feedbacks = Feedback.objects.all()
        sorting = "all"
        type = 'all'
    page = int(request.REQUEST.get('page',1))
    data = {}
    data = ds_pagination(feedbacks,page,'feedbacks',ITEM_PER_PAGE)
    data['filter'] = sorting
    data['type_filter'] = type
    data['keyword'] = "Search feedback"
    request.session["filter"] = sorting
    return render_to_response(template_name,data,context_instance=RequestContext(request))
    
    
    
def feedback_delete(request):
    id = request.GET.get('id',False)
    feedback = Feedback.objects.get(id = id)
    feedback.delete()
    status = 0
    return HttpResponse(status)


    
def searching(request,template_name = "enquiry/staff/feedback_listing.html" ):
    keyword = request.POST.get('search_keyword','')
    previous_url = request.META.get('HTTP_REFERER', None)
    previous_url = previous_url.split('feedback/')
    feedbacks = Feedback.objects.all()
    result = []
    try:filter = request.session["filter"]
    except:filter = 'all'
    try:
	    if 'all' in filter:
	        feedbacks = Feedback.objects.all()
	    else:
	        feedbacks = Feedback.objects.all().order_by(filter)
    except:feedbacks = False
    if feedbacks:
	    if keyword:
	        for row in feedbacks:
	            if keyword in row.name or keyword in row.email or keyword in row.message or keyword in row.module:
	                result.append(row)
	    else:
	        result = []
    else:
	    result = []
    page = int(request.REQUEST.get('page',1))
    data = {}
    data = ds_pagination(result,page,'feedbacks',ITEM_PER_PAGE)
    data['filter'] = filter    
    data['keyword'] = keyword
    data['search'] = True
    return render_to_response(template_name,data,context_instance=RequestContext(request))

    

       
def feedback_details(request,id,template_name = "enquiry/staff/feedback_detail.html"):
    feedback = Feedback.objects.get(id = id)
    data = {}
    data['feedback'] = feedback
    return render_to_response(template_name,data,context_instance=RequestContext(request))
           
        
        
        
        
        
        
        
        
            