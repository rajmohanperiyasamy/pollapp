import datetime

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect  
from django.template.loader import render_to_string

from common.utils import ds_pagination
from bmshop.order.models import Order
from bmshop.mail_utils import send_mail_shippment,send_mail_delivery

NO_OF_ITEMS_PER_PAGE = 15

def payment_orders(request,template='bmshop/staff/order_listing.html'):
    filter_data = filter(request)
    orders=filter_data['orders']
    try:page = int(request.GET['page'])
    except:page=1
    data = ds_pagination(orders,page,'orders',NO_OF_ITEMS_PER_PAGE)
    data['filter']=filter_data['filter']
    data['search']=filter_data['search']
    return render_to_response (template, data, context_instance=RequestContext(request))

@staff_member_required
def ajax_view_payment_orders(request,template='bmshop/staff/ajax_order_listing.html'):
    filter_data = filter(request)
    orders=filter_data['orders']
    try:page = int(request.GET['page'])
    except:page=1
    data = ds_pagination(orders,page,'orders',NO_OF_ITEMS_PER_PAGE)
    data['filter']=filter_data['filter']
    data['search']=filter_data['search']
    return render_to_response(template,data, context_instance=RequestContext(request))

def filter(request):
    try:
        try:filter=request.GET['filter']
        except:filter=False
        try:search=request.GET['search'].strip()
        except:search=False
        key={}
        args=()
        if filter:
            if filter=='PP' or filter=='GC' or filter=='CD':
                key['payment_method']=filter
            elif filter=='0' or filter=='1' or filter=='4':
                key['status']=filter
            
        if search:
            args=(Q(order_number__icontains = search))
        if key:
            if search:orders = Order.objects.filter(args,**key).order_by('-id')
            else:orders = Order.objects.filter(**key).order_by('-id')
        else:
            if search:orders = Order.objects.filter(args).order_by('-id')
            else:orders = Order.objects.all().order_by('-id')
    except:
        import sys
        print sys.exc_info()
        orders = Order.objects.all().order_by('-id')
    return {'orders':orders,'search':search,'filter':filter}

def chane_delivery_status(request,template='bmshop/staff/append_delivery_status.html'):
    try:
        order = Order.objects.get(id=request.GET['id'])
        print order.delivery_status
        if order.delivery_status == 'N':
            order.delivery_status = 'S'
            send_mail_shippment(order)
            order.delivery_date = datetime.datetime.today()
        elif order.delivery_status == 'S':
            order.delivery_status = 'D'
            send_mail_delivery(order)
            order.delivery_date = datetime.datetime.today()
        order.save()   
        
        html=render_to_string(template,{'order':order})
        data={'html':html,'status':1}    
    except:
        data={'status':0}    
    return HttpResponse(simplejson.dumps(data))    
    
    
    

