from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from common.utils import ds_pagination
from bmshop.order.models import Order


NO_OF_ITEMS_PER_PAGE = 15

@login_required
def my_orders(request,template='bmshop/user/my_orders.html'):
    filter_data = filter(request)
    orders=filter_data['orders']
    try:page = int(request.GET['page'])
    except:page=1
    data = ds_pagination(orders,page,'orders',NO_OF_ITEMS_PER_PAGE)
    data['filter']=filter_data['filter']
    data['search']=filter_data['search']
    return render_to_response (template, data, context_instance=RequestContext(request))

@login_required
def ajax_view_my_orders(request,template='bmshop/user/include_my_orders.html'):
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
        key={'user':request.user}
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
        orders = Order.objects.filter(user=request.user).order_by('-id')
    return {'orders':orders,'search':search,'filter':filter}
